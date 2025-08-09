#!/usr/bin/env python3
"""
Test Serper Integration with Pilar2 Agents
דוגמה לשימוש בכלי Serper עם הסוכנים
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.yaml_crew_loader import YAMLCrewLoader
from agents.qa_specialist_agent import QASpecialistAgent
from agents.pillar_two_master import PillarTwoMaster

def test_serper_integration():
    """Test Serper web search integration with all agents"""
    
    print("🔍 Testing Serper Integration with Pilar2 Agents")
    print("=" * 60)
    
    # Check if SERPER_API_KEY is configured
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        print("❌ SERPER_API_KEY not configured!")
        print("Please create a .env file in the project root with:")
        print("SERPER_API_KEY=your-serper-api-key-here")
        print("Get your API key from: https://serper.dev")
        print()
        print("Example .env file content:")
        print("OPENAI_API_KEY=your-openai-api-key-here")
        print("SERPER_API_KEY=your-serper-api-key-here")
        print("SECRET_KEY=your-super-secret-key-change-this-in-production")
        print("DEBUG=True")
        return
    
    print("✅ SERPER_API_KEY configured")
    print()
    
    # Test 1: YAML Crew Loader
    print("1️⃣ Testing YAML Crew Loader with Serper...")
    try:
        loader = YAMLCrewLoader()
        crew = loader.create_crew()
        print("✅ YAML Crew Loader created successfully")
        
        # Test web search with tax modeler agent
        tax_modeler = crew.agents[0]  # First agent is tax_modeler
        web_search_tool = None
        for tool in tax_modeler.tools:
            if tool.name == "serper_web_search":
                web_search_tool = tool
                break
        
        if web_search_tool:
            print("🔍 Testing web search with tax modeler...")
            result = web_search_tool.func("ETR calculation methods 2024")
            print(f"📊 Search result preview: {result[:200]}...")
        else:
            print("❌ Web search tool not found in tax modeler")
            
    except Exception as e:
        print(f"❌ YAML Crew Loader test failed: {str(e)}")
    
    print()
    
    # Test 2: QA Specialist Agent
    print("2️⃣ Testing QA Specialist Agent with Serper...")
    try:
        qa_agent = QASpecialistAgent()
        print("✅ QA Specialist Agent created successfully")
        
        # Test web search
        web_search_tool = None
        for tool in qa_agent.agent.tools:
            if tool.name == "Web_Search":
                web_search_tool = tool
                break
        
        if web_search_tool:
            print("🔍 Testing web search with QA specialist...")
            result = web_search_tool.func("OECD Pillar Two implementation timeline")
            print(f"📊 Search result preview: {result[:200]}...")
        else:
            print("❌ Web search tool not found in QA specialist")
            
    except Exception as e:
        print(f"❌ QA Specialist Agent test failed: {str(e)}")
    
    print()
    
    # Test 3: PillarTwoMaster Agent
    print("3️⃣ Testing PillarTwoMaster Agent with Serper...")
    try:
        master_agent = PillarTwoMaster()
        print("✅ PillarTwoMaster Agent created successfully")
        
        # Test web search
        web_search_tool = None
        for tool in master_agent.agent.tools:
            if tool.name == "Web_Search":
                web_search_tool = tool
                break
        
        if web_search_tool:
            print("🔍 Testing web search with PillarTwoMaster...")
            result = web_search_tool.func("global implementation status")
            print(f"📊 Search result preview: {result[:200]}...")
        else:
            print("❌ Web search tool not found in PillarTwoMaster")
            
    except Exception as e:
        print(f"❌ PillarTwoMaster Agent test failed: {str(e)}")
    
    print()
    
    # Test 4: Direct web search function
    print("4️⃣ Testing direct web search function...")
    try:
        from agents.yaml_crew_loader import YAMLCrewLoader
        loader = YAMLCrewLoader()
        
        # Test different search queries
        test_queries = [
            "corporate tax rates 2024",
            "OECD administrative guidance",
            "GIR XML schema updates",
            "transfer pricing guidelines",
            "Pillar Two compliance risks"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"🔍 Test {i}: Searching for '{query}'...")
            result = loader._web_search(query)
            print(f"📊 Result preview: {result[:150]}...")
            print()
            
    except Exception as e:
        print(f"❌ Direct web search test failed: {str(e)}")
    
    print("=" * 60)
    print("🎉 Serper Integration Test Completed!")
    print()
    print("📋 Summary:")
    print("- All agents now have web search capabilities")
    print("- Search queries are automatically enhanced with OECD Pillar Two context")
    print("- Results include title, snippet, and link for each result")
    print("- Top 5 most relevant results are returned")
    print()
    print("💡 Usage Tips:")
    print("- Use specific queries for better results")
    print("- Combine web search with internal knowledge base")
    print("- Monitor API usage limits")
    print("- Keep API key secure")

def test_hebrew_queries():
    """Test Hebrew search queries"""
    print("\n🇮🇱 Testing Hebrew Search Queries")
    print("=" * 40)
    
    try:
        from agents.yaml_crew_loader import YAMLCrewLoader
        loader = YAMLCrewLoader()
        
        hebrew_queries = [
            "חישובי מס תאגידים 2024",
            "תקנות OECD Pillar Two",
            "דיווחי GIR XML",
            "הערכת סיכונים",
            "תכנון מס בינלאומי"
        ]
        
        for i, query in enumerate(hebrew_queries, 1):
            print(f"🔍 בדיקה {i}: חיפוש '{query}'...")
            result = loader._web_search(query)
            print(f"📊 תצוגה מקדימה: {result[:150]}...")
            print()
            
    except Exception as e:
        print(f"❌ Hebrew search test failed: {str(e)}")

if __name__ == "__main__":
    test_serper_integration()
    test_hebrew_queries()
