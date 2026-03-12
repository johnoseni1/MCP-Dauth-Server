"""
DAuth MCP Server — Test Client
Tests the DEPLOYED server using the Dedalus SDK.

How it works:
- DedalusRunner sends your prompt to an AI model via the Dedalus API
- The AI discovers and calls tools from your deployed MCP server
- mcp_servers=["johnoseni1/MCP-Dauth-Server"] routes to your specific server

Requires in .env:
    DEDALUS_API_KEY=your-key
"""

import asyncio
import os
from dotenv import load_dotenv
from dedalus_labs import AsyncDedalus, DedalusRunner

load_dotenv()

# Your deployed MCP server identifier: "dedalus-org/repo-name"
# From: https://www.dedaluslabs.ai/marketplace/littlbird/MCP-Dauth-Server
MCP_SERVER = "littlbird/MCP-Dauth-Server"

# Using OpenAI GPT-4.1 — works cleanly with Dedalus runner (no forced streaming)
MODEL = "openai/gpt-4.1"


def make_runner() -> DedalusRunner:
    api_key = os.getenv("DEDALUS_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: DEDALUS_API_KEY not set in .env")
    client = AsyncDedalus(api_key=api_key)
    return DedalusRunner(client)


async def run_test(label: str, prompt: str) -> None:
    """Run a single prompt against the deployed MCP server."""
    print(f"\n--- {label} ---")
    print(f"User: {prompt}")

    runner = make_runner()
    result = await runner.run(
        input=prompt,
        model=MODEL,
        mcp_servers=[MCP_SERVER],
    )

    # result.output is the final text response
    print(f"Agent: {result.output}")

    # Show which MCP tools the AI called
    if hasattr(result, "mcp_results") and result.mcp_results:
        print("MCP tools called:")
        for r in result.mcp_results:
            duration = getattr(r, "duration_ms", "?")
            print(f"  {r.tool_name} ({duration}ms): {str(r.result)[:200]}")


async def main():
    print("=" * 55)
    print("  DAuth MCP Server — Deployed Server Test")
    print(f"  Server : {MCP_SERVER}")
    print(f"  Model  : {MODEL}")
    print("=" * 55)

    try:
        await run_test(
            "Business Logic — calculate_discount",
            "Calculate the final price for an item that costs $100 "
            "with a 20% discount and 7.5% tax. Use the calculate_discount tool.",
        )

        await run_test(
            "Business Logic — validate_email",
            "Validate this email address: john@dedaluslabs.ai",
        )

        await run_test(
            "Data Processing — analyze_csv_data",
            "Analyze this CSV data and give me the mean, max, and sum "
            "for age and salary:\nname,age,salary\n"
            "John,30,50000\nJane,25,60000\nBob,35,75000",
        )

        await run_test(
            "External API — get_weather",
            "What is the current weather in Lagos, Nigeria?",
        )

        print("\nAll tests completed.")

    except SystemExit as e:
        print(f"\nSetup error: {e}")
    except (KeyboardInterrupt, SystemExit):
        print("\nStopped.")
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
