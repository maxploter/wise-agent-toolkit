import asyncio
import unittest
from unittest.mock import patch

from mcp.types import CallToolRequestParams, ListToolsResult, Tool

from wise_agent_toolkit.configuration import ACTIONS_ALL, Context
from wise_agent_toolkit.mcp.server import build_server
from wise_agent_toolkit.mcp.toolkit import WiseAgentToolkit


def _run(coro):
  return asyncio.run(coro)


class TestMcpServer(unittest.TestCase):
  """Regression tests for the mcp 2.x Server wiring in build_server().

  These exercise the on_list_tools / on_call_tool handlers directly (no
  stdio, no network) so a future mcp SDK break shows up here instead of
  only at runtime against a real client.
  """

  def setUp(self):
    toolkit = WiseAgentToolkit(
      api_key="test-key",
      host="https://api.sandbox.transferwise.tech",
      configuration={"actions": ACTIONS_ALL, "context": Context()},
    )
    server = build_server(toolkit, server_name="wise-agent-toolkit-test")
    # Handlers registered via Server(..., on_list_tools=..., on_call_tool=...)
    # are reachable through the request handler map, keyed by method name.
    # get_request_handler() returns a HandlerEntry(params_type, handler).
    self._on_list_tools = server.get_request_handler("tools/list").handler
    self._on_call_tool = server.get_request_handler("tools/call").handler

  def test_list_tools_returns_populated_schemas(self):
    result = _run(self._on_list_tools(None, None))

    self.assertIsInstance(result, ListToolsResult)
    self.assertTrue(result.tools, "expected at least one tool")
    for tool in result.tools:
      self.assertIsInstance(tool, Tool)
      self.assertTrue(tool.name)
      self.assertIsInstance(tool.input_schema, dict)

  def test_call_tool_unknown_name_is_error(self):
    params = CallToolRequestParams(name="not_a_real_tool", arguments={})
    result = _run(self._on_call_tool(None, params))

    self.assertTrue(result.is_error)
    self.assertIn("not found", result.content[0].text)

  def test_call_tool_known_name_executes(self):
    list_result = _run(self._on_list_tools(None, None))
    tool_name = list_result.tools[0].name

    with patch("wise_agent_toolkit.api.WiseAPI.run", return_value='{"ok": true}') as mock_run:
      params = CallToolRequestParams(name=tool_name, arguments={})
      result = _run(self._on_call_tool(None, params))

    mock_run.assert_called_once()
    self.assertFalse(result.is_error)
    self.assertEqual(result.content[0].text, '{"ok": true}')

  def test_call_tool_execution_error_is_reported_not_raised(self):
    list_result = _run(self._on_list_tools(None, None))
    tool_name = list_result.tools[0].name

    with patch("wise_agent_toolkit.api.WiseAPI.run", side_effect=RuntimeError("boom")):
      params = CallToolRequestParams(name=tool_name, arguments={})
      result = _run(self._on_call_tool(None, params))

    self.assertTrue(result.is_error)
    self.assertIn("boom", result.content[0].text)


if __name__ == "__main__":
  unittest.main()
