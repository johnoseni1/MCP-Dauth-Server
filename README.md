# DAuth MCP Server

A comprehensive, production-ready **Model Context Protocol (MCP)** server designed for **Business Logic**, **Data Processing**, and **Database Interactions**. Built with Python and the `dedalus-mcp` framework, it empowers AI agents with secure, real-time tool access.

---

##  Architecture & Security
This server follows the **MCP Security Model** to ensure your credentials remain private:
*   **Zero-Trust Credentials**: Your Slack tokens, Database passwords, and API keys stay on **your server** (in `.env`). They are never passed to the AI model or the Dedalus platform via `curl` or prompts.
*   **Encapsulated Execution**: The AI only requests a *tool action* (e.g., `slack_send_message`). The server then executes that action locally using its own secret store.

---

##  Key Features

### 1.  Business & Logic
*   **`calculate_discount`**: Compute final prices with discounts and tax.
*   **`validate_email`**: Validate email formats and domains.
*   **`generate_invoice`**: Create structured invoice dictionaries.
*   **`schedule_reminder`**: Mock scheduling for task reminders.

### 2.  Data Modeling & Transformations
*   **`analyze_csv_data`**: Calculate statistics (mean, max, sum) from CSV strings.
*   **`transform_json_data`**: Apply transformations (uppercase, scaling) to JSON lists.
*   **`filter_data`**: Filter datasets based on specific criteria.
*   **`aggregate_data`**: Group and aggregate data by fields.
*   **`merge_datasets`**: Join two datasets on common keys.

### 3.  Database (Supabase / PostgreSQL)
*   **`supabase_query`**: Execute safe `SELECT` queries with filters.
*   **`supabase_insert`**: Insert records into tables.
*   **`supabase_update`**: Update existing records.
*   **`postgres_execute`**: Execute raw SQL queries (for complex operations).

### 4.  External Integrations
*   **`slack`**: Send messages and list channels efficiently.
*   **`search`**: Web search via Brave API.
*   **`weather`**: Real-time weather data from OpenWeather.

---

##  Deployment

### Environment Configuration
Create a `.env` file with the following variables:

```bash
# Core API Key
DEDALUS_API_KEY=your_dedalus_api_key

# Database (PostgreSQL)
POSTGRES_HOST=your.database.host
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

# Database (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key

# External Services (Required for Integration Tools)
BRAVE_API_KEY=your_brave_search_api_key
SLACK_BOT_TOKEN=your_slack_bot_token
OPENWEATHER_API_KEY=your_openweather_api_key
```

> [!IMPORTANT]
> **Slack Setup**: Ensure your bot has `chat:write`, `channels:read`, and `groups:read` scopes. You **must** invite the bot to a channel (e.g., `/invite @MyBot`) before it can post messages.

### Running the Server
```bash
python main.py
```

*   **Local**: Typically runs via **Stdio**.
*   **Cloud (Railway/Render)**: Automatically switches to **HTTP/SSE** if a `PORT` is detected.

---

##  Testing

### Local API Verification
```bash
python test_client.py
```

### Interactive Console
Use the **Interactive Client** to test any tool manually without writing code:
```bash
python interactive_client.py
```

###  Dedalus Labs Live Demo (Full Command Suite)

To test any tool through the Dedalus API, use the templates below. Replace `YOUR_DEDALUS_KEY` with your API key and `YOUR_SERVER_HANDLE` with your server's registered handle.

####  Business & Logic
<details>
<summary>View Commands</summary>

**Calculate Discount**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Calculate the price for a $200 item with 15% discount and 5% tax. Use calculate_discount."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```

**Validate Email**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Validate if test@example.com is a valid email. Use validate_email."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```
</details>

####  Data Processing
<details>
<summary>View Commands</summary>

**Analyze CSV**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Analyze these sales: 10,20,30,40. Use analyze_csv_data."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```

**JSON Transformation**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Uppercase these names: [\"alice\", \"bob\"]. Use transform_json_data."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```
</details>

####  Database Management
<details>
<summary>View Commands</summary>

**Supabase Search**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Find all products in our supabase database. Use supabase_query."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```

**Postgres Raw SQL**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Get the current database time using postgres_execute with SELECT NOW()."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```
</details>

####  External Connectivity
<details>
<summary>View Commands</summary>

**Slack Channel List**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "List all our Slack channels. Use slack_list_channels."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```

**Brave Web Search**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "Search for the latest tech news. Use brave_search."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```

**Weather Check**
```bash
curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_DEDALUS_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4.1", "messages": [{"role": "user", "content": "What is the weather in London? Use get_weather."}], "mcp_servers": ["YOUR_SERVER_HANDLE"]}'
```
</details>

