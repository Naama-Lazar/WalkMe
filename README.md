AI Email Response Agent (Technical Assessment)
A conversational AI agent built with LangChain and OpenAI that orchestrates Gmail operations. This agent allows users to search for specific emails, automatically generates professional response drafts, and sends replies only after user confirmation.

🛠 Features
Intelligent Search: Uses NLP to find the correct email thread based on user keywords.

Draft Generation: Context-aware reply generation using GPT-4.

Human-in-the-Loop: Requires explicit user approval before sending any data.

Robust Threading: Ensures replies stay within the original Gmail thread.

Error Handling: Gracefully handles invalid IDs, API failures, and missing credentials.

🚀 Setup Instructions
Follow these steps to run the agent using your own credentials:

1. Environment Requirements
Python: 3.9 or higher.

Libraries: Install dependencies via pip:

Bash
pip install -r requirements.txt
2. Configure OpenAI API
Create a file named .env in the root directory.

Add your OpenAI API key to the file:

Plaintext
OPENAI_API_KEY=your_actual_key_here
(Note: This project also supports loading from a key.txt if preferred.)

3. Configure Gmail API (Google Cloud)
To allow the agent to interact with your Gmail, you must provide your own Google OAuth credentials:

Go to the Google Cloud Console.

Create a new project and enable the Gmail API.

Navigate to APIs & Services > Credentials.

Create an OAuth 2.0 Client ID (Application type: Desktop App).

Download the JSON file, rename it to credentials.json, and place it in the root directory of this project.

4. Running the Agent
Start the agent by running:

Bash
python main.py
Note: On the first run, a browser tab will open asking you to authorize the application. Once authorized, a token.json file will be created locally to manage your session securely.

🧠 Design Decisions & Assumptions
Agentic Workflow: Instead of a rigid script, I used a ReAct-style agent. This allows the LLM to "reason" if it needs more information (like re-searching a thread) before performing an action.

Verbose Filtering: Set verbose=False in the final AgentExecutor to provide a clean, chat-like interface for the user, hiding technical logs and tool-calling IDs.

Extraction Logic: Gmail headers often include names (e.g., John Doe <john@example.com>). I implemented a regex-based extraction tool to ensure the send function receives a clean email address, preventing API 400 errors.

Thread Safety: The agent is strictly instructed via the system prompt to wait for user confirmation. If the threadId is lost or invalid, the tool is designed to fallback to a standard send to ensure the user's reply is still delivered.

📂 Project Structure
main.py: The entry point and conversational loop.

tools.py: Custom LangChain tools for Gmail API integration.

requirements.txt: List of necessary Python packages.

.env.example: Template for your environment variables.

⚠️ Important Security Note
Do not include the following files in your submission:

.env (Contains your private OpenAI Key)

credentials.json (Contains your Google App secrets)

token.json (Contains your personal Gmail access session)
