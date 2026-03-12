# DAuth MCP Server — Demo Script
John's personal notes for the live demo.

---

## What This Server Is

My name is John. I built and deployed an MCP server called the **DAuth MCP Server**, hosted on Dedalus Labs infrastructure.

The live server URL is:
https://mcp.dedaluslabs.ai/0953950c17f204c4

MCP stands for Model Context Protocol. It is an open standard — think of it like a USB port for AI. Instead of building custom integrations for every AI tool out there, you build one MCP server, deploy it once, and any AI that supports MCP can connect to it and immediately use all the tools inside, with no extra work.

This server has 17 tools split across four categories:

- Business Logic — calculate_discount, validate_email, generate_invoice, schedule_reminder
- Data Processing — analyze_csv_data, transform_json_data, filter_data, aggregate_data, merge_datasets
- Database — supabase_query, supabase_insert, supabase_update, postgres_execute
- External APIs — brave_search, slack_send_message, slack_list_channels, get_weather

The server is production-ready and live right now. Any AI agent can call these tools using plain English.

Dedalus docs: https://docs.dedaluslabs.ai/dmcp

---

## Opening 

Good morning everyone. My name is John and today I will show you a live demo of the DAuth MCP Server — a fully deployed AI tool server I built using the Model Context Protocol, hosted on Dedalus Labs.

MCP is an open standard that works like a USB port for AI. Instead of building different plugins for every AI platform, I build one server, deploy it once, and any MCP-compatible AI — Claude, GPT, Cursor, or a custom agent — can connect to it and immediately use all its tools.

The server I built is live right now at this URL: https://mcp.dedaluslabs.ai/0953950c17f204c4

It has 17 tools covering business logic, data processing, database operations, and external API calls. I will demonstrate each category right now.

---

## Step 1 — Open Terminal and Set Up

Run these commands:

```
cd "/Users/johnoseni/Downloads/Dedalus-Labs MCP Servers"
source venv/bin/activate
```

 The server is already running live in the cloud. I am just loading the local demo client that connects to it.

---

## Step 2 — Start the Demo Client

```
python interactive_client.py
```

This client loaded all 17 tools directly from the deployed server. You can see them all listed. I will now call some of them live.

---

## Step 3 — Live Demos

---

### Demo 1 — Calculate Discount (select 5)

Let me start with business logic. Imagine an AI handling an e-commerce checkout — it can work out the final price automatically.

Select 5 from the menu.

Enter these values:
- price: 100
- discount_percent: 20
- tax_rate: 7.5

The server returns the original price, how much was saved, the tax amount, and the exact final price — all as structured data. Any AI or app can use this result immediately.

---

### Demo 2 — Generate Invoice (select 7)

Now let me generate a real invoice. This is the kind of task a finance AI agent would handle end-to-end.

Select 7 from the menu.

Enter these values:
- customer: {"name": "Acme Corp", "email": "billing@acme.com"}
- items: [{"name": "Server License", "price": 299.99, "qty": 2}]

    The server created a full invoice — unique ID, timestamp, customer details, line items, and calculated total. An AI agent can call this, email the invoice, and log it to the database, all on its own.

---

### Demo 3 — Validate Email (select 6)

: Simple but very practical — real-time email validation.

Select 6 from the menu.

Enter this value:
- email: john@dedaluslabs.ai

: It validated the format and extracted the domain. Any AI handling user signups can call this in real time to prevent bad data getting into the system.

---

### Demo 4 — Analyze CSV Data (select 9)

 Now data processing. A user uploads a CSV — the AI can analyze it instantly, no spreadsheet needed.

Select 9 from the menu.

Enter this value (type it line by line, press Enter at the end):
- csv_string:
  name,age,salary
  John,30,50000
  Jane,25,60000
  Bob,35,75000

 The server calculated mean, max, sum, and count across every numeric column — returned instantly. That is three rows of data analyzed in milliseconds.

---

### Demo 5 — Get Live Weather (select 17)

 Now let me call a real external API. This shows how the server wraps third-party services and makes them available to any AI.

Select 17 from the menu.

Enter this value:
- city: Lagos

 That just hit the OpenWeatherMap API and returned live weather for Lagos right now — temperature, humidity, wind speed. Any AI agent can answer "what is the weather today?" without anyone writing a custom integration.

---

### Demo 6 — Query the Live Database (select 1)

 Finally, let me query the live production database.

Select 1 from the menu.

Enter these values:
- table: products
- filters: (just press Enter, leave empty — this returns all records)

 That ran a SELECT query against a live Supabase PostgreSQL database and returned real records. An AI agent can read, insert, and update this database using plain English. No SQL knowledge needed.

---

## Step 4 — Full AI Agent Demo (only if time allows)

Now I want to show the full end-to-end. A real AI agent using these tools autonomously — no manual selection from my side, just a natural language prompt.

This test client talks to the DEPLOYED server on Dedalus Labs using the SDK. It passes the server identifier `littlbird/MCP-Dauth-Server` and the AI automatically discovers and calls all 17 tools.

```
python test_client.py
```

I sent plain English prompts to Claude. It read them, decided which tools to call on the deployed server, called them, and returned a natural language response — the AI did all the tool selection by itself.

The test runs four scenarios:
- Business logic: calculate a discount price
- Data processing: analyze CSV statistics
- Database: insert a product, then query products
- External API: get live weather for Lagos

Each response shows what the AI said AND which MCP tools it called behind the scenes.

---

## Step 5 — Show the Live Server in the Browser

Open a browser and go to:
https://mcp.dedaluslabs.ai/0953950c17f204c4

 This is the server running live in the cloud right now. Any MCP-compatible AI can point to this URL and immediately discover and use all 17 tools. No setup, no integration code — just the URL.

---

## Testing the Deployed Server Without the Local Machine

The correct way to test the deployed server remotely is using the Dedalus SDK with `mcp_servers`. This is what `test_client.py` does.

Do NOT try to curl the MCP URL directly — Dedalus manages the routing internally through the SDK.

---

### Option 1 — Test using an External Script (Two Methods)

I've set up two examples in the project folder to show exactly how people can consume this server now that it's live on the Dedalus Marketplace under the `littlbird` organization.

#### Method A: Using the Dedalus AI SDK (`test_client.py`)
This is the "magic" method for Python developers. You give an AI model a prompt, and the Dedalus platform automatically routes the required tools to your deployed server.

```bash
# Make sure your .env has DEDALUS_API_KEY
python test_client.py
```
**What happens here:** The script uses `mcp_servers=["littlbird/MCP-Dauth-Server"]`. The AI (GPT-4.1) realizes it needs a tool (e.g., `calculate_discount`), sends the request via Dedalus to your live server, your server executes the math, and returns the result to the AI to answer the user.

#### Method B: Direct REST API / cURL (`curl_test.sh`)
This shows that **anyone** can use your server in any language (JavaScript, Go, Bash, Postman) without using the Dedalus Python SDK. They just hit the standard Dedalus API endpoint.

```bash
./curl_test.sh
```
**What happens here:** It sends a standard HTTP POST request to `https://api.dedaluslabs.ai/v1/chat/completions` with your API Key as the Bearer token. By including `"mcp_servers": ["littlbird/MCP-Dauth-Server"]` in the JSON payload, the Dedalus gateway automatically connects the AI model to your live tools!

---

### Option 2 — Connect Claude Desktop to the server

Add this to: ~/Library/Application Support/Claude/claude_desktop_config.json

```json
{
  "mcpServers": {
    "dauth-server": {
      "url": "https://mcp.dedaluslabs.ai/0953950c17f204c4"
    }
  }
}
```

Restart Claude Desktop. All 17 tools will appear and Claude can call them from any conversation.

---

### Option 3 — Connect from Cursor

In Cursor go to Settings → MCP Servers and add:
https://mcp.dedaluslabs.ai/0953950c17f204c4

The tools are discovered automatically.

---

### Option 4 — Use the Dedalus Labs Dashboard

Go to: https://www.dedaluslabs.ai/dashboard/overview

The deployed server appears in the dashboard. You can test tool calls directly from the UI with no code needed.

---

## Closing 

So to wrap up what you have just seen:

- A live deployed MCP server accessible to any compatible AI from a single URL
- Business logic tools for pricing, invoicing, and validation
- Data processing tools for CSV analysis and JSON transformations
- Live database tools reading and writing to Supabase in real time
- External API tools pulling live weather, web search, and Slack

No custom integrations. No rebuilding for each AI platform. One URL, 17 tools, any AI.

I am happy to take questions.

---

## Quick Reference

| What | Value |
|------|-------|
| Project folder | /Users/johnoseni/Downloads/Dedalus-Labs MCP Servers |
| Activate environment | source venv/bin/activate |
| Interactive demo | python interactive_client.py |
| AI agent demo | python test_client.py |
| Start locally | python main.py |
| Live server | https://mcp.dedaluslabs.ai/0953950c17f204c4 |
| Dedalus docs | https://docs.dedaluslabs.ai/dmcp |
| Dashboard | https://www.dedaluslabs.ai/dashboard/overview |

---

## If Something Breaks

| Problem | Fix |
|---------|-----|
| ModuleNotFoundError | Run: source venv/bin/activate |
| Missing DEDALUS_API_KEY | Check the .env file |
| test_client.py: model error | Check the model name is "anthropic/claude-opus-4-6" |
| test_client.py: server not found | Check MCP_SERVER = "littlbird/MCP-Dauth-Server" matches your Dedalus deployment |
| Weather or search tool fails | Check OPENWEATHER_API_KEY and BRAVE_API_KEY in .env |
| Supabase error | Check SUPABASE_URL and SUPABASE_KEY in .env |
| 0 tools loaded in interactive client | Make sure you are running from the project root folder |
