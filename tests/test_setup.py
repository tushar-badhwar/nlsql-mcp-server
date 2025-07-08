#!/usr/bin/env python3
"""
Test script for NLSQL MCP Server
"""

import sys
import os

def test_imports():
    """Test all imports work correctly"""
    print("🧪 Testing NLSQL MCP Server Setup\n")
    
    # Test 1: Basic Python modules
    print("1. Testing basic imports...")
    try:
        import json
        import logging
        from pathlib import Path
        print("   ✅ Basic Python modules imported")
    except ImportError as e:
        print(f"   ❌ Basic import error: {e}")
        return False
    
    # Test 2: MCP modules
    print("2. Testing MCP modules...")
    try:
        import mcp
        from mcp.server import Server
        from mcp.types import Tool
        print("   ✅ MCP modules imported")
    except ImportError as e:
        print(f"   ❌ MCP import error: {e}")
        return False
    
    # Test 3: Check nl2sql/nlsql directory exists
    print("3. Checking nl2sql application directory...")
    nlsql_dir = Path(__file__).parent.parent / "nlsql"
    if not nlsql_dir.exists():
        nlsql_dir = Path(__file__).parent.parent / "nl2sql"
    
    if nlsql_dir.exists():
        print(f"   ✅ Found nl2sql application at: {nlsql_dir}")
        
        # Check key files
        key_files = ["database_manager.py", "crew_setup.py", "agents.py", "tasks.py"]
        for file in key_files:
            if (nlsql_dir / file).exists():
                print(f"      ✅ Found {file}")
            else:
                print(f"      ❌ Missing {file}")
                return False
    else:
        print(f"   ❌ nl2sql application not found. Please install from:")
        print(f"      https://github.com/tushar-badhwar/nl2sql")
        return False
    
    # Test 4: NLSQL modules import
    print("4. Testing nlsql module imports...")
    sys.path.insert(0, str(nlsql_dir))
    try:
        from database_manager import DatabaseManager
        from crew_setup import NL2SQLCrew
        from agents import NL2SQLAgents
        from tasks import NL2SQLTasks
        print("   ✅ NLSQL modules imported successfully")
    except ImportError as e:
        print(f"   ❌ NLSQL import error: {e}")
        return False
    
    # Test 5: MCP Server modules
    print("5. Testing MCP server modules...")
    try:
        from nlsql_mcp_server.nlsql_client import NLSQLClient
        from nlsql_mcp_server.tools import NLSQLTools
        print("   ✅ MCP server modules imported")
    except ImportError as e:
        print(f"   ❌ MCP server import error: {e}")
        return False
    
    # Test 6: Create client instance
    print("6. Testing client instantiation...")
    try:
        client = NLSQLClient()
        tools = NLSQLTools(client)
        print("   ✅ Client and tools created successfully")
        print(f"   📊 Available tools: {len(tools.get_tools())}")
    except Exception as e:
        print(f"   ❌ Client creation error: {e}")
        return False
    
    # Test 7: Check environment
    print("7. Checking environment...")
    if os.getenv("OPENAI_API_KEY"):
        print("   ✅ OpenAI API key found")
    else:
        print("   ⚠️  OpenAI API key not set (required for NL→SQL conversion)")
    
    return True

def test_sample_database():
    """Test connection to sample database"""
    print("\n🏀 Testing Sample Database Connection\n")
    
    try:
        from nlsql_mcp_server.nlsql_client import NLSQLClient
        
        client = NLSQLClient()
        result = client.connect_sample_database()
        
        if result["success"]:
            print("   ✅ Sample database connected successfully")
            print(f"   📊 Database type: {result.get('database_type', 'Unknown')}")
            print(f"   📋 Tables found: {result.get('table_count', 0)}")
            if result.get('tables'):
                print(f"   📝 Table names: {', '.join(result['tables'][:5])}")
            
            # Test basic info
            info = client.get_database_info()
            if info["success"]:
                print("   ✅ Database info retrieved successfully")
            
            # Disconnect
            client.disconnect()
            print("   ✅ Disconnected successfully")
            
            return True
        else:
            print(f"   ❌ Sample database connection failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Sample database test error: {e}")
        return False

def test_tools():
    """Test MCP tools"""
    print("\n🔧 Testing MCP Tools\n")
    
    try:
        from nlsql_mcp_server.nlsql_client import NLSQLClient
        from nlsql_mcp_server.tools import NLSQLTools
        
        client = NLSQLClient()
        tools = NLSQLTools(client)
        
        # List tools
        tool_list = tools.get_tools()
        print(f"   📋 Found {len(tool_list)} tools:")
        for tool in tool_list:
            print(f"      - {tool.name}: {tool.description}")
        
        # Test a simple tool call (status check)
        print("\n   🧪 Testing get_connection_status tool...")
        import asyncio
        result = asyncio.run(tools.call_tool("get_connection_status", {}))
        print(f"   ✅ Tool call successful: {result[0].text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Tools test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("NLSQL MCP SERVER - SETUP TEST")
    print("=" * 60)
    
    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_sample_database()
    success &= test_tools()
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Your NLSQL MCP Server is ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Run: python -m nlsql_mcp_server.server")
        print("3. Configure your MCP client to use this server")
    else:
        print("❌ SOME TESTS FAILED. Please check the errors above.")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)