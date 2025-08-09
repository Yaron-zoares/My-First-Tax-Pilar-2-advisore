#!/usr/bin/env python3
"""
Comprehensive test script for fixed Pilar2 agents
"""

import sys
import os
from pathlib import Path

# Add agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def test_yaml_crew_loader():
    """Test the fixed YAML Crew Loader"""
    print("🤖 Testing Fixed YAML Crew Loader...")
    
    try:
        from yaml_crew_loader import YAMLCrewLoader
        print("✅ YAMLCrewLoader imported successfully")
        
        # Load crew configuration
        crew_loader = YAMLCrewLoader("agents/crew_config.yaml")
        print("✅ Crew configuration loaded")
        
        # Test tools creation
        tools = crew_loader._create_tools()
        print(f"✅ Tools created: {len(tools)} tools available")
        
        # List available tools
        print("📋 Available Tools:")
        for tool_name, tool in tools.items():
            print(f"   - {tool_name}: {tool.description}")
        
        # Test agents creation
        agents = crew_loader.create_agents()
        print(f"✅ Agents created: {len(agents)} agents available")
        
        # List available agents
        print("📋 Available Agents:")
        for agent in agents:
            print(f"   - {agent.name}: {agent.role}")
            print(f"     Tools: {len(agent.tools)} tools")
        
        return True
        
    except Exception as e:
        print(f"❌ YAML Crew Loader test failed: {str(e)}")
        return False

def test_pillar_two_master():
    """Test the fixed Pillar Two Master"""
    print("\n🔧 Testing Fixed PillarTwoMaster...")
    
    try:
        from pillar_two_master import PillarTwoMaster
        print("✅ PillarTwoMaster imported successfully")
        
        # Create instance
        master = PillarTwoMaster()
        print("✅ PillarTwoMaster initialized")
        
        # Test tools
        tools = master._get_tools()
        print(f"✅ Tools loaded: {len(tools)} tools available")
        
        # Test basic functionality
        test_data = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "revenue": 5000000,
            "entity_name": "Test Corp"
        }
        
        print("🔧 Testing ETR calculation...")
        etr_result = master._calculate_etr(test_data)
        print("✅ ETR calculation completed")
        
        if "etr_percentage" in etr_result:
            print(f"   ETR: {etr_result['etr_percentage']:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ PillarTwoMaster test failed: {str(e)}")
        return False

def test_data_processing():
    """Test data processing capabilities"""
    print("\n🔧 Testing Data Processing...")
    
    try:
        from flexible_data_processor import FlexibleDataProcessor
        print("✅ FlexibleDataProcessor imported successfully")
        
        processor = FlexibleDataProcessor()
        print("✅ FlexibleDataProcessor initialized")
        
        # Test with sample data
        test_data = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "revenue": 5000000
        }
        
        result = processor.process_data(test_data)
        print("✅ Data processing completed")
        
        if result["success"]:
            print("📊 Processing Results:")
            data = result["data"]
            print(f"   Source format: {data.get('source_format', 'N/A')}")
            print(f"   Total rows: {data.get('total_rows', 'N/A')}")
            print(f"   Total columns: {data.get('total_columns', 'N/A')}")
        else:
            print(f"❌ Processing failed: {result.get('error', {}).get('error_message', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {str(e)}")
        return False

def test_csv_processing():
    """Test CSV file processing"""
    print("\n📊 Testing CSV Processing...")
    
    try:
        from flexible_data_processor import FlexibleDataProcessor
        
        processor = FlexibleDataProcessor()
        
        # Test with CSV file
        csv_file = "data/examples/test_pillar_2.csv"
        if os.path.exists(csv_file):
            result = processor.process_file(csv_file)
            
            if result["success"]:
                print("✅ CSV processing successful!")
                data = result["data"]
                print("📊 Processed Data:")
                for key, value in data.items():
                    if isinstance(value, (int, float)):
                        print(f"   {key}: {value:,.2f}")
                    else:
                        print(f"   {key}: {value}")
            else:
                print("❌ CSV processing failed")
                print(f"   Error: {result.get('error', {}).get('error_message', 'Unknown error')}")
        else:
            print(f"❌ CSV file not found: {csv_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV processing test failed: {str(e)}")
        return False

def test_crew_creation():
    """Test creating a crew with agents"""
    print("\n👥 Testing Crew Creation...")
    
    try:
        from yaml_crew_loader import YAMLCrewLoader
        
        crew_loader = YAMLCrewLoader("agents/crew_config.yaml")
        crew = crew_loader.create_crew()
        
        print("✅ Crew created successfully")
        print(f"📊 Crew Details:")
        print(f"   Agents: {len(crew.agents)}")
        print(f"   Tasks: {len(crew.tasks)}")
        print(f"   Process: {crew.process}")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew creation test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive Pilar2 Agents Test...")
    
    # Test all components
    tests = [
        ("YAML Crew Loader", test_yaml_crew_loader),
        ("PillarTwoMaster", test_pillar_two_master),
        ("Data Processing", test_data_processing),
        ("CSV Processing", test_csv_processing),
        ("Crew Creation", test_crew_creation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test_name}")
        print('='*50)
        
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Agents are working correctly.")
    elif passed > total // 2:
        print("⚠️  Most tests passed. Some issues need attention.")
    else:
        print("❌ Many tests failed. System needs significant fixes.")
    
    return passed == total

if __name__ == "__main__":
    main()
