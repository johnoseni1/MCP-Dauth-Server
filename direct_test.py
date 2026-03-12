"""
DAuth MCP Server — Direct Deployed Server Test
Uses MCPClient to connect DIRECTLY to the deployed server URL.
No AI model involved — raw MCP protocol calls.

This proves the server is live and its tools are accessible.

Requires in .env:
    DEDALUS_API_KEY=your-key
"""

import asyncio
import os
from dotenv import load_dotenv
from dedalus_mcp.client import MCPClient

load_dotenv()

# The deployed server URL
SERVER_URL = "https://mcp.dedaluslabs.ai/0953950c17f204c4"


async def main():
    api_key = os.getenv("DEDALUS_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: DEDALUS_API_KEY not set in .env")

    print("=" * 55)
    print("  DAuth MCP Server — Direct Connection Test")
    print(f"  URL: {SERVER_URL}")
    print("=" * 55)

    # Connect directly to the deployed server with the API key
    client = await MCPClient.connect(
        SERVER_URL,
        headers={"Authorization": f"Bearer {api_key}"},
    )

    try:
        # 1. List all tools
        print("\n--- Listing all tools ---")
        result = await client.list_tools()
        tools = result.tools
        print(f"Found {len(tools)} tools:\n")
        for t in tools:
            desc = (t.description or "")[:70]
            print(f"  {t.name}")
            if desc:
                print(f"    {desc}")

        # 2. Call calculate_discount directly
        print("\n--- Calling calculate_discount ---")
        r = await client.call_tool("calculate_discount", {
            "price": 100.0,
            "discount_percent": 20.0,
            "tax_rate": 7.5,
        })
        print(f"Result: {r.content[0].text if r.content else r}")

        # 3. Call validate_email directly
        print("\n--- Calling validate_email ---")
        r = await client.call_tool("validate_email", {
            "email": "john@dedaluslabs.ai",
        })
        print(f"Result: {r.content[0].text if r.content else r}")

        # 4. Call analyze_csv_data directly
        print("\n--- Calling analyze_csv_data ---")
        r = await client.call_tool("analyze_csv_data", {
            "csv_data": "name,age,salary\nJohn,30,50000\nJane,25,60000\nBob,35,75000",
        })
        print(f"Result: {r.content[0].text if r.content else r}")

        print("\nAll direct tests completed.")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
