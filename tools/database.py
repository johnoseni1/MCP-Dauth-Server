from __future__ import annotations
import os
import asyncio
from typing import Dict, List, Any, Optional
import asyncpg
from supabase import create_client, Client

async def supabase_query(table: str, filters: Optional[Dict] = None, limit: int = 100) -> Dict:
    """Query Supabase table with filters"""
    try:
        # Create client locally for the tool execution
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
            "data": response.data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def postgres_execute(query: str, parameters: Optional[List] = None) -> Dict:
    """Execute raw SQL query on PostgreSQL (Use with caution)"""
    try:
        # Connect strictly for this operation - safer for stateless tools
        conn = await asyncpg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        
        try:
            if query.strip().upper().startswith("SELECT"):
                rows = await conn.fetch(query, *parameters) if parameters else await conn.fetch(query)
                return {"success": True, "data": [dict(r) for r in rows]}
            else:
                result = await conn.execute(query, *parameters) if parameters else await conn.execute(query)
                return {"success": True, "result": result}
        finally:
            await conn.close()
    except Exception as e:
        return {"success": False, "error": str(e)}
