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

## 🧪 Testing

### Local API Verification
```bash
python test_client.py
```

### Interactive Console
Use the **Interactive Client** to test any tool manually without writing code:
```bash
python interactive_client.py
```

### Dedalus Labs Integration (Demo curl)
To test your deployed server via the Dedalus API:
```bash
export DEDALUS_API_KEY=your_key && curl -s -X POST https://api.dedaluslabs.ai/v1/chat/completions \
  -H "Authorization: Bearer ${DEDALUS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4.1",
    "messages": [
      {
        "role": "user",
        "content": "List all our Slack channels. Use the slack_list_channels tool."
      }
    ],
    "mcp_servers": ["YOUR_SERVER_HANDLE"]
  }'
```

