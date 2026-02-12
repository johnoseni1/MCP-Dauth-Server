"""
Test Client for Comprehensive DAuth MCP Server
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from dedalus_labs import AsyncDedalus, DedalusRunner


from server import server

load_dotenv()

def get_server_tools():
    """Extract tool callables from the server instance"""
    tools = []
    if hasattr(server, 'tools') and hasattr(server.tools, '_tool_specs'):
        for name, spec in server.tools._tool_specs.items():
            if hasattr(spec, 'fn'):
                tools.append(spec.fn)
    return tools

async def test_business_logic():
    """Test business logic tools"""
    print("\n💼 Testing Business Logic...")
    
    client = AsyncDedalus(api_key=os.getenv("DEDALUS_API_KEY"))
    
    
    server_tools = get_server_tools()
    print(f"Loaded {len(server_tools)} tools from server.")
    
    
    runner = DedalusRunner(client)
    
    input_text = "Calculate the final price for an item that costs $100 with a 20% discount and 7.5% tax"
    
    print(f"🤖 User: {input_text}")
    
    response = runner.run(
        input=input_text,
        tools=server_tools,
        model="claude-sonnet-4-5",
        stream=True
    )
    
    final_text = ""
    print("🤖 Agent: ", end="", flush=True)
    
    async for chunk in response:
        if isinstance(chunk, str):
            final_text += chunk
            print(chunk, end="", flush=True)
        elif hasattr(chunk, 'choices') and len(chunk.choices) > 0:
             delta = chunk.choices[0].delta
             if hasattr(delta, 'content') and delta.content:
                 content = delta.content
                 final_text += content
                 print(content, end="", flush=True)
        elif hasattr(chunk, 'content'):
             content = str(chunk.content)
             final_text += content
             print(content, end="", flush=True)
            
    print("\n")

async def test_data_processing():
    """Test data processing tools"""
    print("\n📊 Testing Data Processing...")
    
    client = AsyncDedalus(api_key=os.getenv("DEDALUS_API_KEY"))
    server_tools = get_server_tools()
    runner = DedalusRunner(client)
    
    csv_data = """name,age,salary
John,30,50000
Jane,25,60000
Bob,35,75000"""
    
    print(f"🤖 User: Analyze this CSV data...")
    
    response = runner.run(
        input=f"Analyze this CSV data and calculate the mean, max, and sum: {csv_data}",
        tools=server_tools,
        model="claude-sonnet-4-5",
        stream=True
    )
    
    print("🤖 Agent: ", end="", flush=True)
    async for chunk in response:
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)
        elif hasattr(chunk, 'choices') and len(chunk.choices) > 0:
             delta = chunk.choices[0].delta
             if hasattr(delta, 'content') and delta.content:
                 print(delta.content, end="", flush=True)
        elif hasattr(chunk, 'content'):
             print(str(chunk.content), end="", flush=True)
            
    print("\n")

async def test_database_interaction():
    """Test database interaction tools (Supabase)"""
    print("\n🗄️ Testing Database Interaction...")
    
    
    insert_prompt = "Add a new product 'Gaming Headset' with price 89.99 and stock 15 to the products table."
    print(f"🤖 User: {insert_prompt}")
    
    client = AsyncDedalus(api_key=os.getenv("DEDALUS_API_KEY"))
    server_tools = get_server_tools()
    runner = DedalusRunner(client)
    
    response = runner.run(
        input=insert_prompt,
        tools=server_tools,
        model="claude-sonnet-4-5",
        stream=True
    )
    
    print("🤖 Agent (Insert): ", end="", flush=True)
    async for chunk in response:
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)
        elif hasattr(chunk, 'choices') and len(chunk.choices) > 0:
             delta = chunk.choices[0].delta
             if hasattr(delta, 'content') and delta.content:
                 print(delta.content, end="", flush=True)
        elif hasattr(chunk, 'content'):
             print(str(chunk.content), end="", flush=True)
    print("\n")
    
    
    query_prompt = "Find products in the products table that cost less than 100."
    print(f"🤖 User: {query_prompt}")
    
    response_query = runner.run(
        input=query_prompt,
        tools=server_tools,
        model="claude-sonnet-4-5",
        stream=True
    )
    
    print("🤖 Agent (Query): ", end="", flush=True)
    async for chunk in response_query:
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)
        elif hasattr(chunk, 'choices') and len(chunk.choices) > 0:
             delta = chunk.choices[0].delta
             if hasattr(delta, 'content') and delta.content:
                 print(delta.content, end="", flush=True)
        elif hasattr(chunk, 'content'):
             print(str(chunk.content), end="", flush=True)
    print("\n")

async def main():
    print("🚀 Starting Tests...\n")
    
    if not os.getenv("DEDALUS_API_KEY"):
        print("❌ Error: DEDALUS_API_KEY not found in .env file")
        return
    
    try:
        await test_business_logic()
        await test_data_processing()
        await test_database_interaction()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
