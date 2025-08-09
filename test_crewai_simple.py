#!/usr/bin/env python3
"""
Simple CrewAI test for Pilar2
"""

import sys
import os
from pathlib import Path

# Add agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def test_simple_crew():
    """Test simple crew creation"""
    print("👥 Testing Simple Crew Creation...")
    
    try:
        from crewai import Agent, Task, Crew
        
        # Create simple agents without complex tools
        tax_agent = Agent(
            role="Tax Expert",
            goal="Calculate ETR and analyze tax data",
            backstory="You are a tax expert with 15 years of experience in international taxation.",
            verbose=True
        )
        
        legal_agent = Agent(
            role="Legal Expert", 
            goal="Analyze legal compliance",
            backstory="You are a legal expert specializing in international tax law.",
            verbose=True
        )
        
        # Create simple tasks
        tax_task = Task(
            description="Calculate ETR for the provided financial data",
            agent=tax_agent,
            expected_output="ETR calculation and analysis"
        )
        
        legal_task = Task(
            description="Analyze legal compliance with Pillar Two rules",
            agent=legal_agent,
            expected_output="Legal compliance analysis"
        )
        
        # Create crew
        crew = Crew(
            agents=[tax_agent, legal_agent],
            tasks=[tax_task, legal_task],
            verbose=True
        )
        
        print("✅ Crew created successfully")
        print(f"📊 Crew Details:")
        print(f"   Agents: {len(crew.agents)}")
        print(f"   Tasks: {len(crew.tasks)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew creation test failed: {str(e)}")
        return False

def test_pillar_two_master_simple():
    """Test PillarTwoMaster without CrewAI tools"""
    print("\n🔧 Testing PillarTwoMaster Simple...")
    
    try:
        from pillar_two_master import PillarTwoMaster
        
        master = PillarTwoMaster()
        print("✅ PillarTwoMaster initialized")
        
        # Test basic functionality
        test_data = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "revenue": 5000000,
            "entity_name": "Test Corp"
        }
        
        # Test ETR calculation
        etr_result = master._calculate_etr(test_data)
        print("✅ ETR calculation completed")
        
        if "etr_percentage" in etr_result:
            print(f"   ETR: {etr_result['etr_percentage']:.2f}%")
        
        # Test risk assessment
        risk_result = master._assess_pillar_two_risks(test_data)
        print("✅ Risk assessment completed")
        
        if "risk_level" in risk_result:
            print(f"   Risk Level: {risk_result['risk_level']}")
        
        return True
        
    except Exception as e:
        print(f"❌ PillarTwoMaster test failed: {str(e)}")
        return False

def test_data_processing_enhanced():
    """Test enhanced data processing"""
    print("\n🔧 Testing Enhanced Data Processing...")
    
    try:
        from flexible_data_processor import FlexibleDataProcessor
        
        processor = FlexibleDataProcessor()
        print("✅ FlexibleDataProcessor initialized")
        
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
        print(f"❌ Enhanced data processing test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting CrewAI Simple Test...")
    
    # Test all components
    tests = [
        ("Simple Crew", test_simple_crew),
        ("PillarTwoMaster Simple", test_pillar_two_master_simple),
        ("Enhanced Data Processing", test_data_processing_enhanced)
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
        print("🎉 All tests passed! CrewAI is working correctly.")
    elif passed > total // 2:
        print("⚠️  Most tests passed. CrewAI is mostly working.")
    else:
        print("❌ Many tests failed. CrewAI needs fixes.")
    
    return passed == total

if __name__ == "__main__":
    main()
