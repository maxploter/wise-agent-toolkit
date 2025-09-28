# Wise (TransferWise) Agent Toolkit

The Wise Agent Toolkit enables the integration of various AI frameworks and libraries with Wise APIs to create and manage transfers programmatically. This library simplifies working with the Wise API and empowers developers to embed financial operations into AI-driven workflows using Python.

The toolkit supports multiple AI libraries through optional dependencies, allowing you to install only what you need.

Included below are basic instructions, but refer to the Python package documentation for more information.

## Python

### Installation

#### Core Installation
For the basic toolkit without any AI library integrations:
```bash
pip install wise-agent-toolkit
```

#### Integration-Specific Installation
Choose your AI library and install the corresponding extra:

**LangChain Integration:**
```bash
pip install wise-agent-toolkit[langchain]
```

**All Integrations (if you want everything):**
```bash
pip install wise-agent-toolkit[all]
```

**Development Installation:**
```bash
pip install wise-agent-toolkit[dev]
```

### Supported Integrations
- ✅ **LangChain** - Full support with `wise-agent-toolkit[langchain]`
- 🚧 **CrewAI** - Coming soon with `wise-agent-toolkit[crewai]`
- 🚧 **AutoGen** - Coming soon with `wise-agent-toolkit[autogen]`

### Requirements
- Python 3.11+

### Usage

#### LangChain Integration
The library needs to be configured with your Wise API key, which is available in your Wise account dashboard.

```python
from wise_agent_toolkit.langchain.toolkit import WiseAgentToolkit

wise_agent_toolkit = WiseAgentToolkit(
    api_key="YOUR_WISE_API_KEY",
    host="https://api.transferwise.com",
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

#### Checking Available Integrations
You can check which integrations are available in your installation:

```python
from wise_agent_toolkit import get_available_integrations

print("Available integrations:", get_available_integrations())
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
            "profile_id": 42,
        }
    },
)
```

### Adding New Integration Support
The library is designed to be extensible. To add support for a new AI library:

1. Create a new directory under `wise_agent_toolkit/` for your integration
2. Implement the integration-specific toolkit and tool classes inheriting from the base classes
3. Add the optional dependency to `pyproject.toml`
4. Update the main `__init__.py` to conditionally import your integration

## Supported API Methods
- Create a quote
- List recipient accounts
- Create recipient account
- Create a transfer (WIP)