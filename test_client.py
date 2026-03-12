"""
DAuth MCP Server — Test Client
Uses the Dedalus SDK to call your DEPLOYED server via mcp_servers.

How it works:
- DedalusRunner sends your prompt to Claude via the Dedalus API
- Claude discovers and calls tools from your deployed MCP server
- stream=True is required by Anthropic; we collect chunks with async for

Requires in .env:
    DEDALUS_API_KEY=your-key
"""

import asyncio
import os
from dotenv import load_dotenv
from dedalus_labs import AsyncDedalus, DedalusRunner

load_dotenv()

# Your deployed MCP server on Dedalus Labs — format: "github-org/repo-name"
MCP_SERVER = "johnoseni1/MCP-Dauth-Server"

# Model — format: "provider/model-name"
MODEL = "anthropic/claude-opus-4-6"


def make_runner() -> DedalusRunner:
    api_key = os.getenv("DEDALUS_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: DEDALUS_API_KEY not set in .env")
    client = AsyncDedalus(api_key=api_key)
    return DedalusRunner(client)


async def run_test(label: str, prompt: str) -> None:
    """Run a single test against the deployed MCP server and print streamed output."""
    print(f"\n--- {label} ---")
    print(f"User: {prompt}")
    print("Agent: ", end="", flush=True)

    runner = make_runner()

    # stream=True is required by Anthropic Claude.
    # When stream=True, runner.run() returns an async generator — use async for.
    final_text = ""
    async for chunk in runner.run(
        input=prompt,
        model=MODEL,
        mcp_servers=[MCP_SERVER],
        stream=True,
    ):
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                final_text += delta.content
                print(delta.content, end="", flush=True)

    print()  # newline after streamed output


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
            "with a 20% discount and 7.5% tax.",
        )

        await run_test(
            "Data Processing — analyze_csv_data",
            "Analyze this CSV data and give me the mean, max, and sum "
            "for age and salary:\nname,age,salary\n"
            "John,30,50000\nJane,25,60000\nBob,35,75000",
        )

        await run_test(
            "Database — supabase_insert",
            "Insert a new product called 'Demo Widget' with price 49.99 "
            "and stock_quantity 10 into the products table.",
        )

        await run_test(
            "Database — supabase_query",
            "Find all products in the products table that cost less than $100.",
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
        print(f"\nTest failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
