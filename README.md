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
The server is configured to run via **Standard I/O (stdio)**, which is the standard mode for MCP servers running within an agent host/runner.

```bash
python main.py
```

##  Testing Locally
Use the included `test_client.py` to verify functionality. It extracts the tools directly from the server instance for testing.

```bash
python test_client.py
```

### Interactive Verification
To manually test individual tools (e.g., inserting specific data into the database):

```bash
python interactive_client.py
```
This launches a menu-driven interface where you can select tools and input your own parameters.
