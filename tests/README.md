# NLSQL MCP Server Tests

This directory contains test scripts to verify your NLSQL MCP server setup and functionality.

## Test Files

### `test_basic.py`
**Purpose**: Basic functionality test without API key requirements
**What it tests**:
- Module imports and dependencies
- MCP tool framework
- Database connection (SQLite)
- Basic operations

**Usage**:
```bash
cd /path/to/nlsql-mcp-server
python3 tests/test_basic.py
```

### `test_setup.py` 
**Purpose**: Comprehensive setup validation
**What it tests**:
- All module imports
- Environment configuration
- Sample database connection
- Tool instantiation and calling
- Directory structure validation

**Usage**:
```bash
cd /path/to/nlsql-mcp-server
python3 tests/test_setup.py
```

### `test_with_api.py`
**Purpose**: Full AI functionality test with OpenAI API
**What it tests**:
- Natural language to SQL conversion
- AI-powered schema analysis
- CrewAI agent workflows
- End-to-end MCP tool operations

**Prerequisites**: 
- OpenAI API key set in environment or .env file

**Usage**:
```bash
cd /path/to/nlsql-mcp-server
export OPENAI_API_KEY="your_key_here"  # or use .env file
python3 tests/test_with_api.py
```

## Quick Start Testing

1. **First time setup**:
   ```bash
   python3 tests/test_basic.py
   ```

2. **Verify everything works**:
   ```bash
   python3 tests/test_setup.py
   ```

3. **Test AI features** (requires API key):
   ```bash
   python3 tests/test_with_api.py
   ```

## Expected Results

### ✅ All tests passing means:
- MCP server is properly installed
- Dependencies are correctly configured
- Database operations work
- AI features are functional (with API key)
- Ready for production use

### ❌ If tests fail:
- Check error messages for specific issues
- Verify nlsql directory exists and contains required files
- Ensure all dependencies are installed (`pip install -r requirements.txt`)
- For AI tests, verify OpenAI API key is set correctly

## Integration with CI/CD

These tests can be integrated into automated testing pipelines:

```yaml
# Example GitHub Actions workflow
- name: Test Basic Functionality
  run: python3 tests/test_basic.py

- name: Test Setup
  run: python3 tests/test_setup.py

- name: Test AI Features
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: python3 tests/test_with_api.py
```