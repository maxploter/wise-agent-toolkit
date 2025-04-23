import os
from dotenv import load_dotenv

from langchain import hub
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from wise_agent_toolkit.langchain.toolkit import WiseAgentToolkit

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
)

wise_agent_toolkit = WiseAgentToolkit(
    api_key=os.getenv("WISE_API_KEY"),
    host=os.getenv("WISE_API_HOST"),
    configuration={
        "context": {
            "profile_id": os.getenv("WISE_PROFILE_ID"),
        },
        "actions": {
            "quotes": {
                "create": True,
            },
            "recipients": {
                "read": True,
            },
        }
    },
)

tools = []
tools.extend(wise_agent_toolkit.get_tools())

langgraph_agent_executor = create_react_agent(llm, tools)

input_state = {
    "messages": """
    You are a Wise agent. You can create quotes, and list recipient accounts.
    Please find John Doe PHP recipient and create a quote for 10 EUR to PHP to this recipient.
    Please list down ALL the quote's information including IDs.
    """,
}

output_state = langgraph_agent_executor.invoke(input_state)

print(output_state["messages"][-1].content)