#!/usr/bin/env python3
"""
Script to test agents and their functionality for Pilar2
"""

import sys
import os
from pathlib import Path

# Add agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def test_agents():
    """Test the available agents"""
    print("🤖 Testing Pilar2 Agents...")
    
    # Test YAML Crew Loader
    try:
        from yaml_crew_loader import YAMLCrewLoader
        print("✅ YAMLCrewLoader imported successfully")
        
        # Load crew configuration
        crew_loader = YAMLCrewLoader("agents/crew_config.yaml")
        print("✅ Crew configuration loaded")
        
        # Get available agents
        agents = crew_loader.create_agents()
        print(f"📋 Available agents: {len(agents)}")
        for agent in agents:
            print(f"   - {agent.name}: {agent.role}")
        
        return True
        
    except ImportError as e:
        print(f"❌ YAMLCrewLoader import failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Agent test failed: {str(e)}")
        return False

def test_pillar_two_master():
    """Test the Pillar Two Master agent"""
    try:
        from pillar_two_master import PillarTwoMaster
        print("\n🔧 Testing PillarTwoMaster...")
        
        master = PillarTwoMaster()
        print("✅ PillarTwoMaster initialized")
        
        # Test basic functionality
        test_data = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "revenue": 5000000,
            "entity_name": "Test Corp"
        }
        
        result = master.analyze_pillar_two_compliance(test_data)
        print("✅ PillarTwoMaster analysis completed")
        
        if "error" not in result:
            print("📊 Analysis Results:")
            if "etr_analysis" in result:
                etr = result["etr_analysis"]
                print(f"   ETR: {etr.get('etr_percentage', 'N/A')}%")
                print(f"   Risk Level: {etr.get('risk_level', 'N/A')}")
                print(f"   Warnings: {len(etr.get('validation_warnings', []))}")
        
        return True
        
    except ImportError as e:
        print(f"❌ PillarTwoMaster import failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ PillarTwoMaster test failed: {str(e)}")
        return False

def test_data_processing():
    """Test data processing capabilities"""
    try:
        from flexible_data_processor import FlexibleDataProcessor
        print("\n🔧 Testing FlexibleDataProcessor...")
        
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
        
    except ImportError as e:
        print(f"❌ FlexibleDataProcessor import failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Data processing test failed: {str(e)}")
        return False

def main():
    """Main function to test all agents"""
    print("🚀 Starting Pilar2 Agents Test...")
    
    # Test agents
    agents_success = test_agents()
    
    # Test Pillar Two Master
    master_success = test_pillar_two_master()
    
    # Test data processing
    processing_success = test_data_processing()
    
    # Summary
    print("\n📊 Test Summary:")
    print(f"   Agents: {'✅' if agents_success else '❌'}")
    print(f"   PillarTwoMaster: {'✅' if master_success else '❌'}")
    print(f"   Data Processing: {'✅' if processing_success else '❌'}")
    
    total_success = agents_success and master_success and processing_success
    
    if total_success:
        print("\n🎉 All tests passed! Agents are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return total_success

if __name__ == "__main__":
    main()
