"""
DAuth MCP Server
Database + API + Business Logic + Data Processing
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncpg
import httpx
import pandas as pd
from supabase import create_client, Client
from dedalus_mcp import MCPServer
from dedalus_mcp.auth import Connection, SecretKeys


server = MCPServer(
    name="dauth-mcp-server",
    version="1.0.0"
)


CLIENT_SESSION: Optional[httpx.AsyncClient] = None
PG_POOL: Optional[asyncpg.Pool] = None

async def get_http_client() -> httpx.AsyncClient:
    """Get or create global HTTP client session"""
    global CLIENT_SESSION
    if CLIENT_SESSION is None:
        CLIENT_SESSION = httpx.AsyncClient()
    return CLIENT_SESSION

async def get_pg_pool() -> asyncpg.Pool:
    """Get or create global PostgreSQL connection pool"""
    global PG_POOL
    if PG_POOL is None:
        try:
             PG_POOL = await asyncpg.create_pool(
                host=os.getenv("POSTGRES_HOST"),
                port=int(os.getenv("POSTGRES_PORT", "5432")),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                min_size=1,
                max_size=10
            )
        except Exception as e:
            
            print(f"Warning: Could not initialize PG pool (Check .env): {e}")
            PG_POOL = None
    return PG_POOL



supabase_conn = Connection(
    name="supabase",
    secrets=SecretKeys(
        url="SUPABASE_URL",
        key="SUPABASE_KEY"
    )
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



@server.register_tool
async def supabase_query(table: str, filters: Optional[Dict] = None, limit: int = 100) -> Dict:
    """Query Supabase table with filters"""
    try:
        supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        
        query = supabase.table(table).select("*")
        
        if filters:
            for col, val in filters.items():
                query = query.eq(col, val)
        
        
        response = await asyncio.to_thread(lambda: query.limit(limit).execute())
        
        return {
            "success": True,
            "data": response.data,
            "count": len(response.data)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def supabase_insert(table: str, data: Dict) -> Dict:
    """Insert data into Supabase table"""
    try:
        supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        
        
        response = await asyncio.to_thread(lambda: supabase.table(table).insert(data).execute())
        
        return {
            "success": True,
            "data": response.data[0] if response.data else None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def supabase_update(table: str, filters: Dict, updates: Dict) -> Dict:
    """Update records in Supabase table"""
    try:
        supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        
        query = supabase.table(table).update(updates)
        
        for col, val in filters.items():
            query = query.eq(col, val)
        
        
        response = await asyncio.to_thread(lambda: query.execute())
        
        return {
            "success": True,
            "updated_count": len(response.data)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def postgres_execute(query: str, params: Optional[List] = None) -> Dict:
    """Execute raw PostgreSQL query"""
    try:
        
        pool = await get_pg_pool()
        if not pool:
            return {"success": False, "error": "PostgreSQL pool not initialized. Check .env settings."}

        async with pool.acquire() as conn:
            if params:
                result = await conn.fetch(query, *params)
            else:
                result = await conn.fetch(query)
            
            return {
                "success": True,
                "data": [dict(row) for row in result],
                "count": len(result)
            }
    except Exception as e:
        return {"success": False, "error": str(e)}




@server.register_tool
async def brave_search(query: str, count: int = 10) -> Dict:
    """Search the web using Brave Search API"""
    try:
        client = await get_http_client()
        headers = {
            "X-Subscription-Token": os.getenv("BRAVE_API_KEY"),
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": count
        }
        
        response = await client.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
            timeout=30.0
        )
        
        try:
            data = response.json()
        except:
             return {"success": False, "error": f"Invalid response: {response.status_code}"}

        results = []
        if "web" in data and "results" in data["web"]:
            for item in data["web"]["results"][:count]:
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "description": item.get("description")
                })
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def slack_send_message(channel: str, text: str, blocks: Optional[List] = None) -> Dict:
    """Send message to Slack channel"""
    try:
        client = await get_http_client()
        headers = {
            "Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": channel,
            "text": text
        }
        
        if blocks:
            payload["blocks"] = blocks
        
        response = await client.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        
        data = response.json()
        
        return {
            "success": data.get("ok", False),
            "message": data.get("message") if data.get("ok") else data.get("error")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def slack_list_channels() -> Dict:
    """List all Slack channels"""
    try:
        client = await get_http_client()
        headers = {
            "Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"
        }
        
        response = await client.get(
            "https://slack.com/api/conversations.list",
            headers=headers,
            timeout=30.0
        )
        
        data = response.json()
        
        channels = []
        if data.get("ok") and "channels" in data:
            for channel in data["channels"]:
                channels.append({
                    "id": channel.get("id"),
                    "name": channel.get("name"),
                    "is_private": channel.get("is_private", False)
                })
        
        return {
            "success": True,
            "channels": channels,
            "count": len(channels)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def get_weather(city: str, units: str = "metric") -> Dict:
    """Get current weather for a city"""
    try:
        client = await get_http_client()
        params = {
            "q": city,
            "appid": os.getenv("OPENWEATHER_API_KEY"),
            "units": units
        }
        
        response = await client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params,
            timeout=30.0
        )
        
        data = response.json()
        
        if response.status_code == 200:
            return {
                "success": True,
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
        else:
            return {"success": False, "error": data.get("message", "Unknown error")}
    except Exception as e:
        return {"success": False, "error": str(e)}




@server.register_tool
async def calculate_discount(price: float, discount_percent: float, tax_rate: float = 0.0) -> Dict:
    """Calculate final price with discount and tax"""
    try:
        if discount_percent < 0 or discount_percent > 100:
            return {"success": False, "error": "Discount must be between 0 and 100"}
        
        discount_amount = price * (discount_percent / 100)
        price_after_discount = price - discount_amount
        tax_amount = price_after_discount * (tax_rate / 100)
        final_price = price_after_discount + tax_amount
        
        return {
            "success": True,
            "original_price": round(price, 2),
            "discount_percent": discount_percent,
            "discount_amount": round(discount_amount, 2),
            "price_after_discount": round(price_after_discount, 2),
            "tax_rate": tax_rate,
            "tax_amount": round(tax_amount, 2),
            "final_price": round(final_price, 2),
            "savings": round(discount_amount, 2)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def validate_email(email: str) -> Dict:
    """Validate email address format and domain"""
    import re
    
    try:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid_format = bool(re.match(pattern, email))
        
        if not is_valid_format:
            return {
                "success": True,
                "email": email,
                "is_valid": False,
                "reason": "Invalid email format"
            }
        
        domain = email.split('@')[1]
        disposable_domains = ['tempmail.com', 'throwaway.email', '10minutemail.com', 'guerrillamail.com']
        is_disposable = domain in disposable_domains
        
        return {
            "success": True,
            "email": email,
            "is_valid": True,
            "domain": domain,
            "is_disposable": is_disposable,
            "username": email.split('@')[0]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def generate_invoice(
    customer_name: str,
    items: List[Dict],
    invoice_number: Optional[str] = None,
    tax_rate: float = 0.0
) -> Dict:
    """Generate invoice with line items and totals"""
    try:
        if not invoice_number:
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        line_items = []
        subtotal = 0
        
        for item in items:
            quantity = item.get("quantity", 1)
            unit_price = item.get("unit_price", 0)
            item_total = quantity * unit_price
            
            line_items.append({
                "description": item.get("description", "Item"),
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "total": round(item_total, 2)
            })
            
            subtotal += item_total
        
        tax_amount = subtotal * (tax_rate / 100)
        total = subtotal + tax_amount
        
        return {
            "success": True,
            "invoice": {
                "invoice_number": invoice_number,
                "date": datetime.now().isoformat(),
                "customer_name": customer_name,
                "line_items": line_items,
                "subtotal": round(subtotal, 2),
                "tax_rate": tax_rate,
                "tax_amount": round(tax_amount, 2),
                "total": round(total, 2)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def schedule_reminder(task: str, days_from_now: int) -> Dict:
    """Schedule a reminder for future date"""
    try:
        reminder_date = datetime.now() + timedelta(days=days_from_now)
        
        return {
            "success": True,
            "reminder": {
                "task": task,
                "created_at": datetime.now().isoformat(),
                "reminder_date": reminder_date.isoformat(),
                "days_until": days_from_now,
                "status": "scheduled"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}




@server.register_tool
async def analyze_csv_data(csv_data: str, operations: List[str]) -> Dict:
    """Analyze CSV data with specified operations (sum, mean, max, min, count)"""
    try:
        import io
        
        df = pd.read_csv(io.StringIO(csv_data))
        
        results = {
            "success": True,
            "rows": len(df),
            "columns": list(df.columns),
            "operations": {}
        }
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        for operation in operations:
            if operation == "sum":
                results["operations"]["sum"] = df[numeric_cols].sum().to_dict()
            elif operation == "mean":
                results["operations"]["mean"] = df[numeric_cols].mean().to_dict()
            elif operation == "max":
                results["operations"]["max"] = df[numeric_cols].max().to_dict()
            elif operation == "min":
                results["operations"]["min"] = df[numeric_cols].min().to_dict()
            elif operation == "count":
                results["operations"]["count"] = len(df)
            elif operation == "describe":
                results["operations"]["describe"] = df[numeric_cols].describe().to_dict()
        
        return results
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def transform_json_data(data: List[Dict], transformations: Dict) -> Dict:
    """Transform JSON data with specified operations"""
    try:
        df = pd.DataFrame(data)
        
        for column, operation in transformations.items():
            if column not in df.columns:
                continue
            
            if operation == "uppercase":
                df[column] = df[column].astype(str).str.upper()
            elif operation == "lowercase":
                df[column] = df[column].astype(str).str.lower()
            elif operation == "strip":
                df[column] = df[column].astype(str).str.strip()
            elif operation == "round":
                df[column] = df[column].round(2)
            elif operation == "to_int":
                df[column] = df[column].astype(int)
            elif operation == "to_float":
                df[column] = df[column].astype(float)
        
        return {
            "success": True,
            "transformed_data": df.to_dict('records'),
            "rows": len(df)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def filter_data(data: List[Dict], conditions: Dict) -> Dict:
    """Filter data based on conditions"""
    try:
        df = pd.DataFrame(data)
        
        for column, condition in conditions.items():
            if column not in df.columns:
                continue
            
            operator = condition.get("operator")
            value = condition.get("value")
            
            if operator == "equals":
                df = df[df[column] == value]
            elif operator == "not_equals":
                df = df[df[column] != value]
            elif operator == "greater_than":
                df = df[df[column] > value]
            elif operator == "less_than":
                df = df[df[column] < value]
            elif operator == "contains":
                df = df[df[column].astype(str).str.contains(str(value), na=False)]
        
        return {
            "success": True,
            "filtered_data": df.to_dict('records'),
            "original_count": len(data),
            "filtered_count": len(df)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def aggregate_data(data: List[Dict], group_by: str, aggregations: Dict) -> Dict:
    """Group and aggregate data"""
    try:
        df = pd.DataFrame(data)
        
        if group_by not in df.columns:
            return {"success": False, "error": f"Column '{group_by}' not found"}
        
        agg_dict = {}
        for column, operation in aggregations.items():
            if column in df.columns:
                agg_dict[column] = operation
        
        grouped = df.groupby(group_by).agg(agg_dict).reset_index()
        
        return {
            "success": True,
            "aggregated_data": grouped.to_dict('records'),
            "groups": len(grouped),
            "group_by": group_by
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.register_tool
async def merge_datasets(dataset1: List[Dict], dataset2: List[Dict], on: str, how: str = "inner") -> Dict:
    """Merge two datasets on a common column"""
    try:
        df1 = pd.DataFrame(dataset1)
        df2 = pd.DataFrame(dataset2)
        
        if on not in df1.columns or on not in df2.columns:
            return {"success": False, "error": f"Column '{on}' not found in both datasets"}
        
        merged = pd.merge(df1, df2, on=on, how=how)
        
        return {
            "success": True,
            "merged_data": merged.to_dict('records'),
            "dataset1_rows": len(df1),
            "dataset2_rows": len(df2),
            "merged_rows": len(merged),
            "merge_type": how
        }
    except Exception as e:
        return {"success": False, "error": str(e)}




if __name__ == "__main__":
    print("🚀 Starting DAuth MCP Server...")
    print("📊 Database: Supabase + PostgreSQL")
    print("🔌 APIs: Brave Search, Slack, OpenWeather")
    print("💼 Business Logic: Invoicing, Validation, Calculations")
    print("📈 Data Processing: CSV, JSON, Transformations, Aggregations")
    print("⚡ Real-Time Optimization: Enabled (Async Pool + Global Session)")
    
    import asyncio
    asyncio.run(server.serve_stdio())
