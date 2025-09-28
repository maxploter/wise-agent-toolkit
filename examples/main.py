import os
from dotenv import load_dotenv

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
        "update": True,
        "read": True,
      },
      "recipients": {
        "create": True,
        "update": True,
        "read": True,
      },
      "transfers": {
        "create": True,
        "update": True,
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
    Send 5 EUR to recipient with name bla bla
    """,
}
try:
  output_state = langgraph_agent_executor.invoke(input_state)
  print(output_state)
  print(output_state["messages"][-1].content)
except Exception as er:
  print(er)
  raise er
