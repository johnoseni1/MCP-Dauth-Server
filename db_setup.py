import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def setup_database():
    print("🚀 Connecting to database...")
    try:
        conn = await asyncpg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB")
        )
        print("✅ Connected to database!")
        
        with open("schema.sql", "r") as f:
            schema = f.read()
            
        print("📜 Executing schema.sql...")
        await conn.execute(schema)
        print("✅ Schema executed successfully!")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")

if __name__ == "__main__":
    asyncio.run(setup_database())
