import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import search_gmail, send_gmail_reply

# Load Key from file
with open("key.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read().strip()


def run_agent():
    """
        Initializes and runs an interactive AI Gmail Assistant.

        Workflow:
        1. Setup: Configures GPT-4 and Gmail tools (search/reply).
        2. Prompting: Enforces a 4-step logic (Search -> Suggest -> Wait -> Send).
        3. Execution: Enters a continuous loop to process user input, maintaining
           chat history to preserve context and Thread IDs.

        Raises:
           Exception: Handles API connectivity issues or missing local credentials.
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    tools = [search_gmail, send_gmail_reply]

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a professional Gmail Assistant.\n"
            "STEP 1: Use search_gmail to find the email. Extract the 'threadId' and 'recipient'.\n"
            "STEP 2: Show the email snippet to the user and suggest a reply.\n"
            "STEP 3: WAIT for the user to say 'yes' or 'confirm'.\n"
            "STEP 4: Use the EXACT threadId from Step 1. NEVER make up an ID like '1a2b3c4d'.\n"
            "If the user says 'yes' but you lost the threadId, use search_gmail again to find it."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    chat_history = []
    print("\n" + "=" * 50)
    print("AI Email Response Agent is live.")
    print("Capabilities: Searching Gmail, Generating Responses, Sending Replies.")
    print("Type 'exit' to quit.")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            response = executor.invoke({"input": user_input, "chat_history": chat_history})
            print(f"Agent: {response['output']}\n")

            chat_history.append(("human", user_input))
            chat_history.append(("ai", response['output']))

        except Exception as e:
            print(f"Agent: I encountered an error: {e}")
            print("Please ensure your Gmail 'credentials.json' is valid and your API key is correct.\n")

if __name__ == "__main__":
    run_agent()