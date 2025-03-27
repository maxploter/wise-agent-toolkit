# Wise Agent Toolkit

The Wise Agent Toolkit enables the integration of LangChain with Wise APIs to create and manage transfers programmatically. This library simplifies working with the Wise API and empowers developers to embed financial operations into AI-driven workflows using Python.

Included below are basic instructions, but refer to the Python package documentation for more information.

## Python

### Installation
You don't need this source code unless you want to modify the package. If you just want to use the package, run:

```bash
pip install wise-agent-toolkit
```

### Requirements
- Python 3.11+

### Usage
The library needs to be configured with your Wise API key, which is available in your Wise account dashboard.

```python
from wise_agent_toolkit.langchain.toolkit import WiseAgentToolkit

wise_agent_toolkit = WiseAgentToolkit(
    api_key="YOUR_WISE_API_KEY",
    configuration={
        "actions": {
            "transfers": {
                "create": True,
            },
        }
    },
)
```

The toolkit works with LangChain and can be passed as a list of tools. For example:

```python
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
wise_tools = wise_agent_toolkit.get_tools()

agent = initialize_agent(
    tools=wise_tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
)

# Example usage of the agent
response = agent.run("Create a transfer of 100 EUR to John Doe's account.")
print(response)
```

### Examples
For detailed examples, refer to the `/examples` directory in the source repository.

### Context
In some cases, you will want to provide default values for specific API requests. The context parameter allows you to specify these defaults. For example:

```python
wise_agent_toolkit = WiseAgentToolkit(
    api_key="YOUR_WISE_API_KEY",
    configuration={
        "context": {
            "currency": "EUR"
        }
    },
)
```

## Supported API Methods
- Create a transfer
- List all transfers
- Retrieve transfer details
- Cancel a transfer
