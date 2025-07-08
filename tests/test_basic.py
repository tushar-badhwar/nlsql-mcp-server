#!/usr/bin/env python3
"""
Basic test without API key requirements
"""

import asyncio
import os
from nlsql_mcp_server.nlsql_client import NLSQLClient
from nlsql_mcp_server.tools import NLSQLTools

async def test_basic_functionality():
    """Test basic functionality without API key"""
    print("🧪 Testing basic MCP server functionality (no API key required)\n")
    
    # Test 1: Client creation
    print("1. Creating client...")
    client = NLSQLClient()
    tools = NLSQLTools(client)
    print(f"   ✅ Client created with {len(tools.get_tools())} tools")
    
    # Test 2: Status check
    print("2. Testing connection status...")
    result = await tools.call_tool("get_connection_status", {})
    print(f"   ✅ Status check: {result[0].text[:100]}...")
    
    # Test 3: List available tools
    print("3. Listing available tools...")
    tool_list = tools.get_tools()
    for tool in tool_list:
        print(f"   📋 {tool.name}")
    
    # Test 4: Try connecting to sample database (without creating crew)
    print("4. Testing sample database connection (basic)...")
    nba_db_path = "/home/tbadhwar/nlsql/nba.sqlite"
    if os.path.exists(nba_db_path):
        print(f"   ✅ NBA database file found at: {nba_db_path}")
        
        # Test basic database connection without crew
        from nlsql_mcp_server.nlsql_client import DatabaseManager
        db_manager = DatabaseManager()
        try:
            success = db_manager.connect(db_type='sqlite', file_path=nba_db_path)
            if success:
                print("   ✅ Database connection successful")
                
                # Get table names
                tables = db_manager.get_table_names()
                print(f"   📊 Found {len(tables)} tables: {', '.join(tables)}")
                
                # Get sample data from first table
                if tables:
                    sample = db_manager.get_sample_data(tables[0], limit=1)
                    if sample['success']:
                        print(f"   📝 Sample data from {tables[0]}: {len(sample['data'])} rows")
                
                db_manager.disconnect()
                print("   ✅ Disconnected successfully")
            else:
                print("   ❌ Database connection failed")
        except Exception as e:
            print(f"   ❌ Database test error: {e}")
    else:
        print(f"   ❌ NBA database file not found at: {nba_db_path}")
    
    print("\n✅ Basic functionality test completed!")

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())