from __future__ import annotations
import os
import httpx
from typing import Dict, List, Any, Optional

# Helper to get client from main or create new
# To keep tools simple, we will instantiate a client here or use a helper
# For production, we should pass the client session, but for now we create a new one or use a global if we can access it.
# Actually, the standard pattern for tools is to be standalone functions or access shared resources.
# We will use a local helper to get client to ensure it works.

async def get_http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

async def brave_search(query: str, count: int = 5) -> Dict:
    """Search the web using Brave Search API"""
    async with httpx.AsyncClient() as client:
        api_key = os.getenv("BRAVE_API_KEY")
        if not api_key:
            return {"success": False, "error": "Missing BRAVE_API_KEY"}
            
        try:
            resp = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
                params={"q": query, "count": count}
            )
            resp.raise_for_status()
            return {"success": True, "data": resp.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}


async def slack_send_message(channel: str, text: str) -> Dict:
    """Send a message to a Slack channel"""
    async with httpx.AsyncClient() as client:
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            return {"success": False, "error": "Missing SLACK_BOT_TOKEN"}
            
        try:
            resp = await client.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": f"Bearer {token}"},
                json={"channel": channel, "text": text}
            )
            data = resp.json()
            if not data.get("ok"):
                return {"success": False, "error": data.get("error")}
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}


async def slack_list_channels() -> Dict:
    """List public Slack channels"""
    async with httpx.AsyncClient() as client:
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            return {"success": False, "error": "Missing SLACK_BOT_TOKEN"}
            
        try:
            resp = await client.post(
                "https://slack.com/api/conversations.list",
                headers={"Authorization": f"Bearer {token}"},
                data={"types": "public_channel", "exclude_archived": "true"}
            )
            data = resp.json()
            if not data.get("ok"):
                return {"success": False, "error": data.get("error")}
                
            channels = [{"id": c["id"], "name": c["name"]} for c in data.get("channels", [])]
            return {"success": True, "count": len(channels), "channels": channels}
        except Exception as e:
            return {"success": False, "error": str(e)}


async def get_weather(city: str) -> Dict:
    """Get current weather for a city"""
    async with httpx.AsyncClient() as client:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return {"success": False, "error": "Missing OPENWEATHER_API_KEY"}
            
        try:
            resp = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": api_key, "units": "metric"}
            )
            resp.raise_for_status()
            return {"success": True, "data": resp.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
