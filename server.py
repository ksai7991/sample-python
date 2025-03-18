import os
import aiohttp
from aiohttp import web
import asyncio
import socket
import asyncpg

# Database connection pool
db_pool = None

async def init_db():
    """Initialize database connection pool."""
    global db_pool
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
    db_pool = await asyncpg.create_pool(dsn=db_url)

async def close_db(app):
    """Close database connection pool on shutdown."""
    await db_pool.close()

async def fetch_data(request):
    """Fetch data from the database."""
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM users LIMIT 10")
        data = [{"id": row["id"], "name": row["name"]} for row in rows]
        return web.json_response(data)

async def insert_data(request):
    """Insert data into the database."""
    name = request.match_info.get("name", "default_name")
    async with db_pool.acquire() as conn:
        await conn.execute("INSERT INTO users (name) VALUES ($1)", name)
    return web.Response(text=f"Inserted {name} into database.")

async def external_request(request):
    """Make an external API request and return the response."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://faas-blr1-8177d592.doserverless.co/api/v1/web/fn-100bea51-4ace-4d4f-bd57-ec37b1664387/default/python",
            headers={"Content-Type": "application/json", "X-Require-Whisk-Auth": "Ne7r8kmzYl0wswE"},
        ) as response:
            response_content = await response.text() if response.status == 200 else "Failed to fetch response"

    hostname = socket.gethostname()
    return web.Response(text=f"Response from API: {response_content}. Hostname: {hostname}")

async def delayed_startup(app):
    await asyncio.sleep(2)
    print("Server startup delayed by 2 seconds")

app = web.Application()
app.on_startup.append(init_db)
app.on_startup.append(delayed_startup)
app.on_cleanup.append(close_db)

app.router.add_get("/", external_request)
app.router.add_get("/fetch", fetch_data)
app.router.add_get("/insert/{name}", insert_data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    web.run_app(app, port=port)
