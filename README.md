# DAuth MCP Server

A comprehensive Model Context Protocol (MCP) server designed for **Business Logic**, **Data Processing**, and **Database Interactions**. Built with Python, it leverages `dedalus-mcp` and `dedalus-labs` for robust agentic capabilities.

## Features

### 1.  Business Logic
- **`calculate_discount`**: Compute final prices with discounts and tax.
- **`validate_email`**: Validate email formats and domains.
- **`generate_invoice`**: Create structured invoice dictionaries.
- **`schedule_reminder`**: Mock scheduling for task reminders.

### 2.  Data Processing
- **`analyze_csv_data`**: Calculate statistics (mean, max, sum) from CSV strings.
- **`transform_json_data`**: Apply transformations (uppercase, scaling) to JSON lists.
- **`filter_data`**: Filter datasets based on specific criteria.
- **`aggregate_data`**: Group and aggregate data by fields.
- **`merge_datasets`**: Join two datasets on common keys.

### 3.  Database (Supabase / PostgreSQL)
- **`supabase_query`**: Execute safe `SELECT` queries with filters.
- **`supabase_insert`**: Insert records into tables.
- **`supabase_update`**: Update existing records.
- **`postgres_execute`**: Execute raw SQL queries (for complex operations).

##  Deployment

### Prerequisites
- Python 3.13+
- PostgreSQL Database (e.g., Supabase, Railway)
- Dedalus API Key

### Environment Variables
Configure the following in your deployment environment or `.env` file:

```bash

DEDALUS_API_KEY=your_dedalus_api_key


POSTGRES_HOST=your.database.host
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password


SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key
```

### Database Setup
To initialize the database tables (`products`, `customers`, `invoices`), run the setup script from an environment with database access:

```bash
python db_setup.py
```
*Note: If deploying to Railway/cloud, this script usually runs as a build step or one-off command.*

### Running the Server
python main.py
```

- **Local Development**: Runs via **Stdio** by default.
- **Cloud Deployment**: Automatically switches to **HTTP/SSE** if the `PORT` environment variable is detected (e.g., in Railway/Render).

##  Testing Locally
Use the included `test_client.py` to verify functionality. It extracts the tools directly from the server instance for testing.

```bash
python test_client.py
```

### Interactive Manual Testing
For manual testing and exploration without writing code, use the **Interactive Client**. This tool provides a menu-driven interface to execute any available tool with custom inputs.

#### How to Use
1. **Launch the Client**:
   ```bash
   python interactive_client.py
   ```

2. **Select a Tool**:
   - You will see a numbered list of all available tools (e.g., `1. calculate_discount`, `5. supabase_insert`).
   - Enter the number corresponding to the tool you want to run.

3. **Input Parameters**:
   - The client will prompt you for each required argument.
   - **Simple Values**: Enter strings, numbers, or booleans directly (e.g., `100`, `Gaming Headset`, `true`).
   - **JSON / Complex Data**: For arguments requiring a list or dictionary (like `filters` or `data`), enter valid JSON.
     - *Example for `supabase_insert` data*: `{"name": "New Item", "price": 19.99, "stock_quantity": 50}`
     - *Example for `supabase_query` filters*: `{"price": {"lt": 50}}`

4. **View Results**:
   - The tool output will be displayed in formatted JSON.
   - Press **Enter** to return to the main menu.

