"""
Test MCP Connection - Direct JSON-RPC test

This script tests the MCP server by sending raw JSON-RPC requests.
It creates a new server instance since MCP uses stdio communication.
"""

import asyncio
import json
import sys
import subprocess


async def test_mcp_server():
    """Test the MCP server with a simple request."""

    # Server command with your credentials
    cmd = [
        sys.executable, "-m", "wise_agent_toolkit.mcp",
        "--api_key", "979999c9-10cf-4da2-9f58-77a7edb57d03",
        "--host", "https://api.sandbox.transferwise.tech",
        "--profile_id", "25",
    ]

    print(f"Starting MCP server: {' '.join(cmd)}")

    # Start the server process
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        # Initialize the connection
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        print("\n=== Sending Initialize Request ===")
        init_json = json.dumps(init_request) + "\n"
        print(f"Request: {init_json.strip()}")

        process.stdin.write(init_json.encode())
        await process.stdin.drain()

        # Read initialize response
        response_line = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        init_response = json.loads(response_line.decode().strip())
        print(f"Response: {json.dumps(init_response, indent=2)}")

        # Send 'initialized' notification (required by MCP protocol)
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }

        print("\n=== Sending Initialized Notification ===")
        initialized_json = json.dumps(initialized_notification) + "\n"
        print(f"Notification: {initialized_json.strip()}")

        process.stdin.write(initialized_json.encode())
        await process.stdin.drain()

        # Send tools/list request
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
        }

        print("\n=== Sending Tools List Request ===")
        tools_json = json.dumps(tools_request) + "\n"
        print(f"Request: {tools_json.strip()}")

        process.stdin.write(tools_json.encode())
        await process.stdin.drain()

        # Read tools response
        response_line = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        tools_response = json.loads(response_line.decode().strip())
        print(f"Response: {json.dumps(tools_response, indent=2)}")

        # Show available tools
        if "result" in tools_response:
            tools = tools_response["result"].get("tools", [])
            print(f"\n=== Available Tools ({len(tools)}) ===")
            for tool in tools:
                print(f"- {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")

            # ================================================================= #
            # === MODIFIED SECTION: Call the 'create_quote' tool directly === #
            # ================================================================= #
            if any(tool.get('name') == 'create_quote' for tool in tools):
                print(f"\n=== Testing Tool: create_quote ===")

                # Arguments for creating a quote to send 100 GBP to EUR
                quote_arguments = {
                    "source_currency": "GBP",
                    "target_currency": "EUR",
                    "source_amount": 100,
                }

                tool_call_request = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "create_quote",
                        "arguments": quote_arguments
                    }
                }

                tool_call_json = json.dumps(tool_call_request) + "\n"
                print(f"Request: {tool_call_json.strip()}")

                process.stdin.write(tool_call_json.encode())
                await process.stdin.drain()

                # Read tool call response
                response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
                tool_call_response = json.loads(response_line.decode().strip())
                print(f"Response: {json.dumps(tool_call_response, indent=2)}")
            else:
                print("\n'create_quote' tool not found in the list of available tools.")

        else:
            print(f"Error in tools/list: {tools_response}")

    except asyncio.TimeoutError:
        print("Timeout waiting for server response")

        # Check if there's any stderr output
        try:
            stderr_data = await asyncio.wait_for(process.stderr.read(1024), timeout=1.0)
            if stderr_data:
                print(f"Server stderr: {stderr_data.decode()}")
        except asyncio.TimeoutError:
            pass

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Clean up
        process.terminate()
        await process.wait()
        print("\nServer process terminated.")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())