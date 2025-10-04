# Wise Agent Toolkit - GitHub Copilot Instructions

## Project Overview

This is a Python library that provides AI framework integrations for Wise (TransferWise) APIs. It supports LangChain, MCP (Model Context Protocol), and other AI libraries through optional dependencies. The toolkit enables AI agents to perform financial operations like creating transfers, managing recipients, and handling currency quotes through the Wise platform.

## Repository Structure

```
wise_agent_toolkit/
├── __init__.py                 # Package initialization
├── api.py                      # API client configuration
├── configuration.py            # Context and configuration classes
├── functions.py                # Core business logic functions
├── prompts.py                  # Tool descriptions and prompts
├── schema.py                   # Pydantic models for validation
├── tools.py                    # Tool registration and metadata
├── integrations/               # AI framework integrations
├── langchain/                  # LangChain-specific implementations
├── mcp/                        # MCP (Model Context Protocol) server
├── autogen/                    # AutoGen integration
└── crewai/                     # CrewAI integration

tests/
├── test_functions.py           # Unit tests for core functions
└── test_configuration.py      # Configuration tests

examples/
├── main.py                     # Usage examples
└── README.md                   # Example documentation
```

## Tool Development Pattern

**CRITICAL: Every new tool requires updates to exactly 5 files in this specific order:**

1. **Function Implementation** (`wise_agent_toolkit/functions.py`)
2. **Pydantic Schema** (`wise_agent_toolkit/schema.py`)
3. **Tool Description** (`wise_agent_toolkit/prompts.py`)
4. **Tool Registration** (`wise_agent_toolkit/tools.py`)
5. **Unit Test** (`tests/test_functions.py`)

## Libraries and Frameworks

- **Core**: Python 3.8+, Pydantic for data validation
- **API Client**: `wise_api_client` package for Wise API interactions
  - **Source**: https://github.com/maxploter/wise-python
  - **Documentation**: See README.md and docs/ folder in the repository for API details
  - **Installation**: `pip install git+https://github.com/maxploter/wise-python.git`
  - **Version**: 0.2.4 (API version 0.4.6)
- **AI Integrations**: LangChain, MCP, AutoGen, CrewAI (optional dependencies)
- **Testing**: unittest with mock for API testing

## Coding Standards and Conventions

### Naming Conventions
- **Functions**: snake_case (e.g., `create_transfer`, `list_recipient_accounts`)
- **Classes**: PascalCase (e.g., `CreateTransfer`, `ListRecipientAccounts`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `CREATE_TRANSFER_PROMPT`)
- **Variables**: snake_case
- **Parameters**: Follow Wise API conventions (`profile_id`, `target_account`, `quote_uuid`)

### Function Signature Pattern
```python
def {function_name}(
    api_client,
    context: Context,
    {required_param}: {type},
    {optional_param}: Optional[{type}] = None,
):
```

### Context Handling
Always check for values in the `context` parameter for common fields:
```python
if not profile_id and context.profile_id:
    profile_id = context.profile_id
```

### API Client Usage

#### How to Research the Wise API Client

**Primary Documentation Sources:**
1. **Main README**: https://github.com/maxploter/wise-python/blob/main/README.md
   - Installation instructions
   - Basic usage examples
   - Getting started guide
   - API overview table

2. **Detailed API Documentation**: https://github.com/maxploter/wise-python/tree/main/docs
   - Individual API class documentation (e.g., `TransfersApi.md`, `QuotesApi.md`)
   - Request/response model schemas
   - Method signatures and parameters
   - Example usage for each endpoint

#### Research Pattern for New Tools

When implementing a new tool, always:

1. **Check the API Overview**: Look at the README.md table to find the relevant API class
2. **Read the Specific API Documentation**: Go to `docs/{ApiClass}.md` for detailed method information
3. **Review Request Models**: Check `docs/Create{Resource}Request.md` for required parameters
4. **Understand Response Models**: Check `docs/{Resource}.md` for return types

#### Standard Configuration Pattern
```python
import wise_api_client
from wise_api_client.rest import ApiException

# Standard configuration setup (check README for latest)
configuration = wise_api_client.Configuration(
    host="https://api.sandbox.transferwise.tech"  # or production URL
)
configuration.access_token = api_token

# API client context manager pattern
with wise_api_client.ApiClient(configuration) as api_client:
    api_instance = wise_api_client.{ApiClass}Api(api_client)
    # Make API calls
```

#### API Class Discovery

The wise_api_client follows OpenAPI patterns. Common API classes include:
- `TransfersApi` - Transfer operations
- `QuotesApi` - Currency quote operations  
- `RecipientsApi` - Recipient account management
- `ProfilesApi` - Profile management
- `ActivitiesApi` - Activity tracking

**Always verify the exact method names and signatures in the docs/ folder.**

#### Request/Response Model Patterns
- **Requests**: Use `wise_api_client.{ModelName}` classes
- **Method Discovery**: Check `docs/{ApiClass}.md` for available methods
- **Parameter Types**: Refer to individual model documentation
- **Return Types**: Documented in each method's documentation

#### Error Handling Pattern
```python
try:
    result = api_instance.some_method(parameters)
    return result
except wise_api_client.rest.ApiException as e:
    # Let the exception bubble up - toolkit handles this at higher level
    raise
```

### Error Handling
Let the Wise API client handle API errors naturally - don't wrap in additional try/catch blocks unless adding specific business logic.

### Import Organization
```python
# Standard library imports first
from typing import Optional
from datetime import datetime

# Third-party imports
import wise_api_client

# Local imports last
from .configuration import Context
```

## Tool Registration Actions
Use these standard action types in tools configuration:
- **transfers**: `create`, `read`, `update`, `cancel`
- **quotes**: `create`, `read`
- **recipients**: `create`, `read`, `update`, `delete`
- **accounts**: `read`
- **profiles**: `read`

## Testing Patterns

### Mock Structure
```python
mock_api_client = mock.Mock()
mock_{resource}_api = mock.Mock()
mock_response = {"id": "test-123", "status": "success"}

with mock.patch("wise_api_client.{ApiClass}Api") as mock_api_class:
    mock_api_class.return_value = mock_{resource}_api
    mock_{resource}_api.{method}.return_value = mock_response
```

### Test Assertions
- Verify API class instantiation
- Verify method calls with correct parameters
- Assert return values match expected responses

## Documentation Style

- Use clear, concise docstrings with Parameters and Returns sections
- Include type hints for all parameters
- Use consistent language patterns ("The ID of the..." vs "ID of the...")
- Describe what the function returns from the Wise API

## Key Business Domain Concepts

- **Transfers**: Money movements between accounts
- **Quotes**: Currency exchange rate calculations
- **Recipients**: Destination accounts for transfers
- **Profiles**: Wise user account contexts

## When Creating New Tools

1. **Research the Wise API**: Check `wise_api_client` documentation for the correct API class and method
   - **API Client Documentation**: https://github.com/maxploter/wise-python (see README.md and docs/ folder)
2. **Follow Existing Patterns**: Reference `create_transfer`, `create_quote`, `list_recipient_accounts` as canonical examples
3. **Update All 5 Files**: Never skip any of the required files
4. **Update README**: Add the new tool to the "Supported Tools" section in README.md with description and usage
5. **Test Thoroughly**: Include comprehensive unit tests with proper mocking
6. **Validate Changes**: Run tests after implementation to ensure no regressions (use unittest)

## Common Parameters

- `profile_id`: Wise profile identifier (often from context)
- `target_account`: Recipient account ID
- `source_account`: Source account ID (for refunds)
- `quote_uuid`: Unique identifier for currency quotes
- `transfer_id`: Unique identifier for transfers
- `currency`: 3-letter ISO currency codes (USD, EUR, GBP, etc.)
- `reference`: Human-readable transfer description
- `customer_transaction_id`: External transaction tracking ID

Always follow these established patterns when adding new functionality to maintain consistency and reliability across the toolkit.
