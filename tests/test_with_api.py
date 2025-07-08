#!/usr/bin/env python3
"""
Test MCP server with OpenAI API key
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from nlsql_mcp_server.nlsql_client import NLSQLClient
from nlsql_mcp_server.tools import NLSQLTools

async def test_with_api_key():
    """Test full functionality with API key"""
    print("🤖 Testing NLSQL MCP Server with OpenAI API\n")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API key loaded: {api_key[:10]}...")
    
    # Create client and tools
    client = NLSQLClient()
    tools = NLSQLTools(client)
    
    try:
        # Test 1: Connect to sample database
        print("1. Connecting to sample database...")
        result = await tools.call_tool("connect_sample_database", {})
        print(f"   ✅ Connection result: {result[0].text[:100]}...")
        
        # Test 2: Get database info
        print("2. Getting database information...")
        result = await tools.call_tool("get_database_info", {})
        print(f"   ✅ Database info: {result[0].text[:150]}...")
        
        # Test 3: Analyze schema (AI-powered)
        print("3. Analyzing schema with AI...")
        result = await tools.call_tool("analyze_schema", {})
        print(f"   ✅ Schema analysis: {result[0].text[:200]}...")
        
        # Test 4: Natural language to SQL (AI-powered)
        print("4. Converting natural language to SQL...")
        result = await tools.call_tool("natural_language_to_sql", {
            "question": "How many teams are in the NBA?",
            "skip_schema": True  # Use cached schema for faster processing
        })
        print(f"   ✅ NL to SQL result: {result[0].text[:300]}...")
        
        # Test 5: Execute a simple query
        print("5. Executing SQL query...")
        result = await tools.call_tool("execute_sql_query", {
            "sql_query": "SELECT COUNT(*) as team_count FROM team LIMIT 10"
        })
        print(f"   ✅ Query result: {result[0].text[:200]}...")
        
        print("\n🎉 All tests with API key passed!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_api_key())