import os
from dotenv import load_dotenv

from langchain import hub
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from wise_agent_toolkit.langchain.toolkit import WiseAgentToolkit

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
)

wise_agent_toolkit = WiseAgentToolkit(
    api_key=os.getenv("WISE_API_KEY"),
    configuration={
        "actions": {
            "recipients": {
                "create": True,
            },
        }
    },
)

tools = []
tools.extend(wise_agent_toolkit.get_tools())

langgraph_agent_executor = create_react_agent(llm, tools)

input_state = {
    "messages": """
        Check if i have a recipient with name ABC?
    """,
}

output_state = langgraph_agent_executor.invoke(input_state)

print(output_state["messages"][-1].content)