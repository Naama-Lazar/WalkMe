import os
import base64
import re
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from langchain.tools import tool

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_gmail_service():
    """
        Handles OAuth2 authentication and returns a Gmail API service instance.

        1. Loads existing credentials from 'token.json'.
        2. Refreshes expired tokens or initiates a new login flow via 'credentials.json'.
        3. Saves updated credentials to 'token.json' for future use.

        Returns: An authorized Gmail API service object.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


@tool
def search_gmail(query: str):
    """
       Searches for a single email based on a query.
       1. Fetches the latest message matching the query via Gmail API.
       2. Extracts critical metadata: threadId, sender/recipient, and subject.
       3. Returns a dictionary containing the email snippet and IDs for further processing.
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        messages = results.get('messages', [])

        if not messages:
            return "No emails found. Please try a different search term."

        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        headers = msg.get('payload', {}).get('headers', [])

        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown")

        # Clean the sender to get just the email address
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', sender)
        recipient = email_match.group(0) if email_match else sender

        return {
            "threadId": msg['threadId'],
            "recipient": recipient,
            "subject": subject,
            "snippet": msg.get('snippet', '')
        }
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def send_gmail_reply(thread_id: str, recipient: str, subject: str, body: str):
    """
        Sends a threaded reply to a specific email.
        1. Encodes the message body and subject (adding 'Re:' if missing) into MIME format.
        2. Attempts to send the email within the existing thread using the provided thread_id.
        3. Fallback: If the thread_id is invalid (404), sends the email as a new standalone message.
    """
    try:
        service = get_gmail_service()

        message = MIMEText(body)
        message['to'] = recipient
        # Gmail API likes 'Re:' for thread consistency
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
        message['subject'] = subject

        # Encode for Gmail API
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()


        create_message = {
            'raw': raw_message,
            'threadId': thread_id
        }

        try:
            service.users().messages().send(userId='me', body=create_message).execute()
            return "SUCCESS: Reply sent and threaded."
        except Exception as e:
            if "404" in str(e):
                service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
                return "SUCCESS: Thread ID was not found, so email was sent as a new message instead of a reply."
            raise e

    except Exception as e:
        return f"FAILED: {str(e)}"