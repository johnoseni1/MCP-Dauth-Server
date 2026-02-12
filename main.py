"""
DAuth MCP Server
Main Entry Point
"""

import asyncio
import os
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.auth import Connection, SecretKeys


from tools import database, business, data, api

load_dotenv()


server = MCPServer(
    name="dauth-mcp-server",
    version="1.0.0"
)



supabase_conn = Connection(
    name="supabase",
    secrets=SecretKeys(url="SUPABASE_URL", key="SUPABASE_KEY")
)

postgres_conn = Connection(
    name="postgres",
    secrets=SecretKeys(
        host="POSTGRES_HOST",
        port="POSTGRES_PORT",
        database="POSTGRES_DB",
        user="POSTGRES_USER",
        password="POSTGRES_PASSWORD"
    )
)

brave_search_conn = Connection(
    name="brave_search",
    secrets=SecretKeys(api_key="BRAVE_API_KEY"),
    base_url="https://api.search.brave.com/res/v1",
    auth_header_name="X-Subscription-Token",
    auth_header_format="{api_key}"
)

slack_conn = Connection(
    name="slack",
    secrets=SecretKeys(api_key="SLACK_BOT_TOKEN"),
    base_url="https://slack.com/api",
    auth_header_name="Authorization",
    auth_header_format="Bearer {api_key}"
)

openweather_conn = Connection(
    name="openweather",
    secrets=SecretKeys(api_key="OPENWEATHER_API_KEY"),
    base_url="https://api.openweathermap.org/data/2.5"
)


server.register_tool(database.supabase_query)
server.register_tool(database.supabase_insert)
server.register_tool(database.supabase_update)
server.register_tool(database.postgres_execute)


server.register_tool(business.calculate_discount)
server.register_tool(business.validate_email)
server.register_tool(business.generate_invoice)
server.register_tool(business.schedule_reminder)


server.register_tool(data.analyze_csv_data)
server.register_tool(data.transform_json_data)
server.register_tool(data.filter_data)
server.register_tool(data.aggregate_data)
server.register_tool(data.merge_datasets)


server.register_tool(api.brave_search)
server.register_tool(api.slack_send_message)
server.register_tool(api.slack_list_channels)
server.register_tool(api.get_weather)


if __name__ == "__main__":
    print("🚀 Starting DAuth MCP Server (Modular Structure)...")
    print("✅ Tools Registered from tools/ modules")
    print("⚡ Serving via Stdio...")
    asyncio.run(server.serve_stdio())
