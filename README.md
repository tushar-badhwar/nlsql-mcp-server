# NLSQL MCP Server

An MCP (Model Context Protocol) server that exposes the functionality of the [nl2sql](https://github.com/tushar-badhwar/nl2sql) Natural Language to SQL application as MCP tools. This allows any MCP-compatible client to convert natural language questions into SQL queries using AI.

## Features

- **Database Connection**: Connect to SQLite, PostgreSQL, and MySQL databases
- **Schema Analysis**: Automatically analyze database structure and relationships
- **Natural Language to SQL**: Convert plain English questions to SQL queries using AI
- **Query Execution**: Execute SQL queries safely with configurable limits
- **Query Validation**: Validate SQL syntax before execution
- **Sample Data**: Access sample data from database tables
- **Built-in Prompts**: Pre-configured prompts for common database tasks

## Prerequisites

1. **NLSQL Application**: This MCP server is a wrapper around the [nl2sql application](https://github.com/tushar-badhwar/nl2sql). You **must install nl2sql first**.
2. **OpenAI API Key**: Required for natural language to SQL conversion
3. **Python 3.8+**: Compatible with Python 3.8 and above

## Installation

### Step 1: Install the NLSQL Application (Required)

**This MCP server requires the original nl2sql application to be installed first.**

```bash
# Clone the original nl2sql application
git clone https://github.com/tushar-badhwar/nl2sql.git
cd nl2sql

# Install dependencies
pip install -r requirements.txt

# Test the installation
streamlit run main.py
```

### Step 2: Install the MCP Server

```bash
# Navigate to the same parent directory where nl2sql is located
cd ..  # Now you should be in the directory containing nl2sql/

# Clone this MCP server
git clone https://github.com/tushar-badhwar/nlsql-mcp-server.git
cd nlsql-mcp-server

# Install MCP server dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Step 3: Environment Setup

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your_api_key_here"

# Or create a .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Step 4: Verify Directory Structure

Ensure your directory structure looks like this:

```
parent_directory/
├── nl2sql/                # Original nl2sql application (required dependency)
│   ├── main.py
│   ├── database_manager.py
│   ├── crew_setup.py
│   ├── agents.py
│   ├── tasks.py
│   └── nba.sqlite
└── nlsql-mcp-server/      # This MCP server
    ├── src/
    ├── tests/
    ├── README.md
    └── requirements.txt
```

**Important**: The MCP server automatically looks for the nl2sql directory in the parent directory. If you have a different setup, you may need to adjust the path in `src/nlsql_mcp_server/nlsql_client.py`.

## Running the Server

### Standalone Mode

```bash
# Run the server directly
python -m nlsql_mcp_server.server

# Or using the console script (after pip install)
nlsql-mcp-server
```

### With MCP Client

Configure your MCP client to use this server. Example configuration:

```json
{
  "mcpServers": {
    "nlsql": {
      "command": "python",
      "args": ["-m", "nlsql_mcp_server.server"],
      "cwd": "/path/to/nlsql-mcp-server",
      "env": {
        "OPENAI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### Database Connection Tools

#### `connect_database`
Connect to SQLite, PostgreSQL, or MySQL database.

**Parameters:**
- `db_type` (required): "sqlite", "postgresql", or "mysql"
- `file_path`: Path to SQLite file (SQLite only)
- `host`, `port`, `database`, `username`, `password`: Connection details (PostgreSQL/MySQL)

#### `connect_sample_database`
Connect to the built-in NBA sample database for testing.

### Schema Analysis Tools

#### `analyze_schema`
Analyze database schema and structure using AI.

**Parameters:**
- `force_refresh` (optional): Force refresh of schema cache

#### `get_database_info`
Get detailed database information including tables, columns, and relationships.

#### `get_table_sample`
Get sample data from a specific table.

**Parameters:**
- `table_name` (required): Name of the table
- `limit` (optional): Number of rows to return (default: 5)

### Natural Language to SQL Tools

#### `natural_language_to_sql`
Convert natural language question to SQL query using AI.

**Parameters:**
- `question` (required): Natural language question
- `skip_schema` (optional): Skip schema analysis for faster processing

### SQL Execution Tools

#### `execute_sql_query`
Execute SQL query on connected database.

**Parameters:**
- `sql_query` (required): SQL query to execute
- `limit` (optional): Maximum rows to return (default: 100)

#### `validate_sql_query`
Validate SQL query syntax and structure.

**Parameters:**
- `sql_query` (required): SQL query to validate

### Utility Tools

#### `get_connection_status`
Get current database connection status.

#### `disconnect_database`
Disconnect from current database.

## Available Prompts

### `analyze_database`
Comprehensive database analysis workflow.

### `generate_sql_query`
Natural language to SQL generation workflow.

### `troubleshoot_sql`
SQL query troubleshooting workflow.

## Usage Examples

### Using with Claude Desktop

1. Configure Claude Desktop to use this MCP server
2. Connect to a database:
   ```
   Use the connect_sample_database tool to connect to the NBA sample database
   ```

3. Ask natural language questions:
   ```
   Use the natural_language_to_sql tool with the question "How many teams are in the NBA?"
   ```

4. Execute queries:
   ```
   Use the execute_sql_query tool to run the generated SQL
   ```

### Example Workflow

1. **Connect**: `connect_sample_database`
2. **Analyze**: `analyze_schema`
3. **Query**: `natural_language_to_sql` with question "List all teams from California"
4. **Execute**: `execute_sql_query` with the generated SQL
5. **Explore**: `get_table_sample` for additional data exploration

## Advanced Usage

### Custom Database Connection

```json
{
  "tool": "connect_database",
  "arguments": {
    "db_type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "username": "user",
    "password": "password"
  }
}
```

### Performance Optimization

- Use `skip_schema: true` in `natural_language_to_sql` for faster queries after initial schema analysis
- Set appropriate `limit` values for large result sets
- Use `get_table_sample` to explore data before writing complex queries

## Troubleshooting

### Common Issues

1. **"Could not find the nl2sql application" or "nlsql modules not found"**
   - **Solution**: Install the original nl2sql application first
   - **Command**: `git clone https://github.com/tushar-badhwar/nl2sql.git`
   - **Verify**: Check that `nl2sql/database_manager.py` exists
   - **Structure**: Ensure both `nl2sql/` and `nlsql-mcp-server/` are in the same parent directory

2. **"OpenAI API key not found"**
   - Set the OPENAI_API_KEY environment variable
   - Verify the API key is valid

3. **Database connection failures**
   - Check database credentials and connectivity
   - Ensure database server is running
   - Verify firewall settings for remote databases

4. **Import errors**
   - Install all required dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Debug Mode

Enable debug logging:

```bash
export PYTHONPATH=/path/to/nlsql-mcp-server/src
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from nlsql_mcp_server.server import main
import asyncio
asyncio.run(main())
"
```

## Testing

The repository includes comprehensive tests to verify your setup:

```bash
# Basic functionality test (no API key required)
python3 tests/test_basic.py

# Full setup validation
python3 tests/test_setup.py

# AI functionality test (requires OpenAI API key)
python3 tests/test_with_api.py
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Development

### Project Structure

```
src/
├── nlsql_mcp_server/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── tools.py           # MCP tool definitions
│   └── nlsql_client.py    # Interface to nlsql app
├── pyproject.toml
└── requirements.txt
```

### Adding New Tools

1. Define the tool in `tools.py`
2. Add handler method in `NLSQLTools.call_tool()`
3. Implement the functionality in `nlsql_client.py`
4. Update documentation

### Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy src/

# Format code
black src/
isort src/
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the nlsql application documentation