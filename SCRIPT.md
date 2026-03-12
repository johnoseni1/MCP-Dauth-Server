# 🚀 DAuth MCP Server — DEMO SCRIPT
> **Read this out loud. Follow each step exactly. Sections marked SAY are what you speak to the audience.**

---

## 📌 WHAT IS THIS SERVER? (Know this before you go on stage)

**DAuth MCP Server** is a production-deployed AI tool server built using the **Model Context Protocol (MCP)** standard, hosted on **Dedalus Labs** infrastructure.

> **Live Server URL → https://mcp.dedaluslabs.ai/0953950c17f204c4**

It exposes **17 tools** in 4 categories so that any AI agent — Claude, GPT, Cursor, or your own custom agent — can call them automatically using plain English, without needing any custom integrations.

| Category | Tools |
|---|---|
| 💼 Business Logic | calculate_discount, validate_email, generate_invoice, schedule_reminder |
| 📊 Data Processing | analyze_csv_data, transform_json_data, filter_data, aggregate_data, merge_datasets |
| 🗄️ Database | supabase_query, supabase_insert, supabase_update, postgres_execute |
| 🌐 External APIs | brave_search, slack_send_message, slack_list_channels, get_weather |

**What problem does it solve?**
Normally, building AI tools means writing custom integrations for every AI platform. MCP changes that — it's like a USB standard for AI. You build ONE server, deploy it once, and any MCP-compatible AI immediately has access to all your tools with zero extra integration work.

**Docs:** https://docs.dedaluslabs.ai/dmcp

---

## 🎤 OPENING

> "Good [morning/afternoon] everyone. Today I'm going to show you a live demo of the **DAuth MCP Server** — a fully deployed AI tool server built on the **Model Context Protocol** standard, hosted on Dedalus Labs.
>
> Think of MCP as a USB standard for AI. Instead of every AI needing its own custom plugins, any MCP-compatible AI — Claude, GPT, Cursor — can plug into ONE server and immediately get access to all the tools inside it.
>
> I built this server, deployed it to the cloud, and right now it is live at this URL:
> **https://mcp.dedaluslabs.ai/0953950c17f204c4**
>
> It has **17 tools** across 4 categories: Business Logic, Data Processing, Database, and External APIs. I'm going to demo each one live right now."

---

## ⚙️ STEP 1 — Terminal Setup

**Open Terminal and run these:**

```bash
cd "/Users/johnoseni/Downloads/Dedalus-Labs MCP Servers"
```
```bash
source venv/bin/activate
```

**SAY:**
> "I'm loading the local Python environment. The server itself is already running live in the cloud — I'm just setting up the demo client that will call it."

---

## 🎮 STEP 2 — Launch the Interactive Client

```bash
python interactive_client.py
```

**SAY:**
> "This is the interactive demo client. It loaded all 17 tools straight from the server. You can see them listed here — I'll now run through a few live examples."

---

## 🔢 STEP 3 — Live Tool Demos

---

### 🟢 DEMO 1 — `calculate_discount` (Tool #5)

**SAY:**
> "Let's start with business logic. Imagine an e-commerce checkout — the AI calculates the final price automatically."

Select: **5**

Enter when prompted:
```
price:            100
discount_percent: 20
tax_rate:         7.5
```

**SAY:**
> "The server returns the original price, the discount saved, tax applied, and the exact final price — all as clean structured JSON. Any AI or frontend can consume this instantly."

---

### 🟢 DEMO 2 — `generate_invoice` (Tool #7)

**SAY:**
> "Now let's generate a real invoice — this is the kind of task a finance AI agent would handle end-to-end."

Select: **7**

Enter when prompted:
```
customer: {"name": "Acme Corp", "email": "billing@acme.com"}
items:    [{"name": "Server License", "price": 299.99, "qty": 2}]
```

**SAY:**
> "The server generates a unique invoice ID with a timestamp, customer details, line items, and the calculated total. An AI agent can call this, email the result, and log it to the database — all automatically."

---

### 🟢 DEMO 3 — `validate_email` (Tool #6)

**SAY:**
> "This one is simple but very useful — real-time email validation."

Select: **6**

Enter when prompted:
```
email: john@dedaluslabs.ai
```

**SAY:**
> "It validates the format and extracts the domain. An AI agent handling user signups or form submissions can call this in real time to prevent bad data."

---

### 🟢 DEMO 4 — `analyze_csv_data` (Tool #9)

**SAY:**
> "Now data processing. Imagine a user uploads a CSV — the AI can analyze it immediately, no spreadsheet software needed."

Select: **9**

Enter when prompted:
```
csv_string: name,age,salary
John,30,50000
Jane,25,60000
Bob,35,75000
```
*(type each line and press Enter, then press Enter again on an empty line to submit)*

**SAY:**
> "The server uses pandas to return full statistics — mean, max, sum, count — across every numeric column, instantly."

---

### 🟢 DEMO 5 — `get_weather` (Tool #17)

**SAY:**
> "Now let's call a live external API. This shows how the MCP server wraps third-party APIs and makes them instantly available to any AI."

Select: **17**

Enter when prompted:
```
city: Lagos
```

**SAY:**
> "That just hit the OpenWeatherMap API and returned live weather for Lagos — temperature, humidity, wind speed, all real-time. Any AI agent can now answer 'what's the weather in Lagos?' without you writing any integration code."

---

### 🟢 DEMO 6 — `supabase_query` (Tool #1)

**SAY:**
> "Finally, let's query the live production database directly."

Select: **1**

Enter when prompted:
```
table:   products
filters: (press Enter to skip — returns all records)
```

**SAY:**
> "That just ran a SELECT on our live Supabase PostgreSQL database. Real records, returned in real time. An AI agent can read, insert, and update this database using plain English — no SQL knowledge needed."

---

## 🤖 STEP 4 (OPTIONAL) — Full AI Agent Demo

**SAY:**
> "Now let me show you the full end-to-end: a Claude AI agent using these tools autonomously — no manual selection, just a natural language prompt."

```bash
python test_client.py
```

**SAY:**
> "I'm sending plain English instructions to Claude. It reads them, decides which MCP tools to call, calls them on our deployed server, and gives back a natural language response. The AI selected and called the right tool entirely on its own."

---

## 🌐 STEP 5 — Show the Live Deployed Server

**Open a browser and navigate to:**
```
https://mcp.dedaluslabs.ai/0953950c17f204c4
```

**SAY:**
> "This is the server running live in the cloud right now. Any MCP-compatible AI — Cursor, Claude Desktop, a custom agent — can point to this single URL and immediately discover and use all 17 tools, with zero extra setup. The tools are self-describing through the MCP protocol, so the AI automatically knows what each one does."

---

## 🧪 TESTING THE DEPLOYED SERVER DIRECTLY (No Local Machine Needed)

> If you want to test the live deployed server directly — without running anything locally — here are your options:

---

### Option A — Using `curl` to Hit the Server Directly

The deployed server speaks the MCP protocol over HTTP/SSE. You can call it directly from any terminal:

```bash
# Check that the server is reachable
curl -i https://mcp.dedaluslabs.ai/0953950c17f204c4
```

```bash
# Send a proper MCP JSON-RPC request to list available tools
curl -X POST https://mcp.dedaluslabs.ai/0953950c17f204c4 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

```bash
# Call the calculate_discount tool directly on the deployed server
curl -X POST https://mcp.dedaluslabs.ai/0953950c17f204c4 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "calculate_discount",
      "arguments": {
        "price": 100,
        "discount_percent": 20,
        "tax_rate": 7.5
      }
    }
  }'
```

---

### Option B — Connect Claude Desktop to Your Deployed Server

Add this to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "dauth-server": {
      "url": "https://mcp.dedaluslabs.ai/0953950c17f204c4"
    }
  }
}
```

Then restart Claude Desktop → your 17 tools will appear automatically and Claude can call them from any conversation.

---

### Option C — Connect from Cursor (AI Code Editor)

In Cursor, go to **Settings → MCP Servers** and add:
```
https://mcp.dedaluslabs.ai/0953950c17f204c4
```
Cursor will discover all 17 tools and your AI can use them directly inside your code editor.

---

### Option D — Connect from the Dedalus Labs Dashboard

1. Go to → **https://www.dedaluslabs.ai/dashboard/overview**
2. Navigate to your MCP servers
3. Your deployed server should already appear — you can test tool calls directly from the dashboard UI with no code needed

---

## 🎤 CLOSING — What to SAY

> "So to summarize what you've just seen:
>
> ✅ **A live deployed MCP server** — accessible to any AI client from a single URL
> ✅ **Business logic** — pricing, invoicing, email validation
> ✅ **Data processing** — CSV analysis, JSON transformations, filtering, aggregation
> ✅ **Live database** — Supabase read/write in real time
> ✅ **External APIs** — live weather, web search, Slack messaging
>
> No custom integrations. No re-building for each AI. One URL, every tool, any AI.
>
> I'm happy to take questions."

---

## 📋 QUICK COMMAND REFERENCE

| What | Command / URL |
|------|--------------|
| Go to project folder | `cd "/Users/johnoseni/Downloads/Dedalus-Labs MCP Servers"` |
| Activate environment | `source venv/bin/activate` |
| Run interactive demo | `python interactive_client.py` |
| Run full AI agent demo | `python test_client.py` |
| Start server locally | `python main.py` |
| **Live deployed server** | **https://mcp.dedaluslabs.ai/0953950c17f204c4** |
| Dedalus Docs | https://docs.dedaluslabs.ai/dmcp |
| Dedalus Dashboard | https://www.dedaluslabs.ai/dashboard/overview |

---

## 🛟 IF SOMETHING GOES WRONG

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `source venv/bin/activate` first |
| `Missing DEDALUS_API_KEY` | Check your `.env` file has the key |
| Weather/search tool fails | Check `OPENWEATHER_API_KEY` / `BRAVE_API_KEY` in `.env` |
| Supabase error | Check `SUPABASE_URL` and `SUPABASE_KEY` in `.env` |
| 0 tools loaded | Make sure you're running from the project root folder, not inside `tools/` |
| curl returns 401 | The server requires an auth header — use the dashboard instead |
