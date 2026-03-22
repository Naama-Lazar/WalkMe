📧 AI Email Response Agent
An intelligent, conversational agent designed to streamline Gmail management. This tool leverages LangChain and OpenAI's GPT-4 (LLM) to orchestrate Gmail operations through a reasoning-and-action loop.

🎯 Objective
This project was developed as part of a Technical Assessment for an AI Solution Engineer role. The goal was to build an "agent-with-tools" architecture capable of:

LLM-Driven Search: Using GPT-4 to interpret user intent and query Gmail.

Contextual Analysis: Presenting email metadata (From, Subject, Body) to the user.

Response Generation: Suggesting high-context replies using the LLM's generative capabilities.

Human-in-the-Loop: Explicitly waiting for user approval before execution.

Graceful Exception Handling: Managing API errors or missing threads without crashing.

🛠 Tech Stack
LLM: OpenAI GPT-4 (Generative AI & Reasoning)

Orchestration: LangChain (AgentExecutor & OpenAI Functions Agent)

APIs: Google Gmail API (OAuth 2.0)

Environment: python-dotenv for secure secret management

🚀 Setup & Installation
1. Install Dependencies
 Bash
 pip install -r requirements.txt

3. Configure Credentials
 OpenAI: Create a .env file and add OPENAI_API_KEY=your_key_here.

  Gmail: Place your credentials.json (OAuth Desktop App) in the project root.

3. Run the Agent
 Bash
 python main.py
🧠 Design Decisions & Engineering Notes
LLM Agentic Reasoning (ReAct)
Unlike a scripted chatbot, this agent uses an LLM-based reasoning loop. When a user says "Send it," the LLM evaluates the chat history to retrieve the correct threadId and recipient before calling the tool. This architecture allows the agent to recover if a search fails or if the user changes their mind mid-conversation.

Technical Robustness
Recipient Cleaning: The agent uses regex to isolate email addresses from "Friendly Name email@addr.com" formats, ensuring compatibility with the Gmail API.

Thread Integrity: The send_gmail_reply tool prioritizes maintaining thread consistency but includes a fallback to "New Message" if a 404 Not Found error occurs on a specific thread.

Clean UI: verbose=False is enabled to ensure the evaluator sees a polished conversational experience rather than internal JSON processing logs.

📂 Project Structure
main.py: The entry point and LLM agent configuration.

tools.py: Custom LangChain tools for Gmail API integration.

requirements.txt: Project dependencies.

README.md: Documentation.
