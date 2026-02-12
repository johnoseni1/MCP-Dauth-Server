from __future__ import annotations
import os
import asyncio
from typing import Dict, List, Any, Optional
import asyncpg
from supabase import create_client, Client


_PG_POOL: Optional[asyncpg.Pool] = None

async def get_pg_pool() -> asyncpg.Pool:
    """Get or create the global PostgreSQL connection pool"""
    global _PG_POOL
    if _PG_POOL is None:
        try:
            _PG_POOL = await asyncpg.create_pool(
                host=os.getenv("POSTGRES_HOST"),
                port=int(os.getenv("POSTGRES_PORT", "5432")),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                min_size=1,
                max_size=10
            )
        except Exception as e:
            print(f"Warning: Could not initialize PG pool: {e}")
            raise e
    return _PG_POOL

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
                if isinstance(val, dict):
                    for op, op_val in val.items():
                        if op == 'lt': query = query.lt(col, op_val)
                        elif op == 'lte': query = query.lte(col, op_val)
                        elif op == 'gt': query = query.gt(col, op_val)
                        elif op == 'gte': query = query.gte(col, op_val)
                        elif op == 'like': query = query.like(col, op_val)
                        elif op == 'ilike': query = query.ilike(col, op_val)
                        elif op == 'neq': query = query.neq(col, op_val)
                        else: query = query.eq(col, op_val) 
                else:
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
    """Execute raw SQL query on PostgreSQL using connection pool"""
    try:
        pool = await get_pg_pool()
        async with pool.acquire() as conn:
            if query.strip().upper().startswith("SELECT"):
                rows = await conn.fetch(query, *parameters) if parameters else await conn.fetch(query)
                return {"success": True, "data": [dict(r) for r in rows]}
            else:
                result = await conn.execute(query, *parameters) if parameters else await conn.execute(query)
                return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
