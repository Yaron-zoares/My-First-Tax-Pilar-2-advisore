#!/usr/bin/env python3
"""
Comprehensive Test Script for Enhanced Q&A System
Tests all components: EnhancedQAEngine, API routes, and UI functions
"""

import sys
import os
import asyncio
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Test backend imports
        from backend.services.enhanced_qa_engine import EnhancedQAEngine
        from backend.services.qa_engine import QAEngine
        print("✅ EnhancedQAEngine imported successfully")
        
        # Test frontend imports
        from frontend.app import (
            qa_page, basic_qa_section, enhanced_qa_section, 
            advanced_analysis_section, settings_page,
            general_settings_section, ai_settings_section,
            api_settings_section, analysis_preferences_section
        )
        print("✅ Frontend functions imported successfully")
        
        # Test agents imports
        from agents.qa_specialist_agent import QASpecialistAgent
        print("✅ QASpecialistAgent imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"   Python path: {sys.path}")
        print(f"   Current directory: {os.getcwd()}")
        return False

def test_enhanced_qa_engine():
    """Test EnhancedQAEngine functionality"""
    print("\n🔍 Testing EnhancedQAEngine...")
    
    try:
        # Import the class first
        from backend.services.enhanced_qa_engine import EnhancedQAEngine
        
        # Create sample data
        sample_data = pd.DataFrame({
            'revenue': [1000000, 1200000, 1100000],
            'expenses': [800000, 900000, 850000],
            'tax_rate': [0.25, 0.25, 0.25],
            'year': [2021, 2022, 2023]
        })
        
        # Initialize engine
        engine = EnhancedQAEngine(data=sample_data)
        print("✅ EnhancedQAEngine initialized successfully")
        
        # Test basic question
        basic_response = engine.ask_question("מה הרווח ב-2022?", "he")
        print(f"✅ Basic question answered: {basic_response['confidence']:.2f} confidence")
        
        # Test enhanced question
        enhanced_response = engine.ask_enhanced_question("הסבר על חישובי מס לפי עמוד שני", "he")
        print(f"✅ Enhanced question answered: {enhanced_response.get('ai_enhanced', False)}")
        
        # Test suggestions
        suggestions = engine.get_enhanced_suggestions("pillar_two_compliance", "he")
        print(f"✅ Got {len(suggestions)} suggestions")
        
        # Test categories
        categories = engine.get_enhanced_categories("he")
        print(f"✅ Got {len(categories)} categories")
        
        return True
        
    except Exception as e:
        print(f"❌ EnhancedQAEngine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qa_specialist_agent():
    """Test QASpecialistAgent functionality"""
    print("\n🔍 Testing QASpecialistAgent...")
    
    try:
        # Import the class first
        from agents.qa_specialist_agent import QASpecialistAgent
        
        # Initialize agent
        agent = QASpecialistAgent()
        print("✅ QASpecialistAgent initialized successfully")
        
        # Test comprehensive question
        result = agent.answer_comprehensive_question(
            "מה הסיכונים בהתחייבויות מס לפי עמוד שני?",
            {"context": "חברה בינלאומית עם הכנסות מעל 750 מיליון יורו"}
        )
        print(f"✅ Comprehensive analysis completed: {len(result)} components")
        
        return True
        
    except Exception as e:
        print(f"❌ QASpecialistAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_functions():
    """Test frontend function imports and basic structure"""
    print("\n🔍 Testing frontend functions...")
    
    try:
        # Test that all functions are callable
        from frontend.app import (
            qa_page, basic_qa_section, enhanced_qa_section, 
            advanced_analysis_section, settings_page,
            general_settings_section, ai_settings_section,
            api_settings_section, analysis_preferences_section
        )
        
        functions = [
            qa_page, basic_qa_section, enhanced_qa_section, 
            advanced_analysis_section, settings_page,
            general_settings_section, ai_settings_section,
            api_settings_section, analysis_preferences_section
        ]
        
        for func in functions:
            if callable(func):
                print(f"✅ {func.__name__} is callable")
            else:
                print(f"❌ {func.__name__} is not callable")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_files():
    """Test configuration files exist and are valid"""
    print("\n🔍 Testing configuration files...")
    
    try:
        # Test YAML config
        yaml_path = Path("agents/crew_config.yaml")
        if yaml_path.exists():
            print("✅ crew_config.yaml exists")
        else:
            print("❌ crew_config.yaml missing")
            return False
        
        # Test requirements
        req_path = Path("requirements.txt")
        if req_path.exists():
            with open(req_path, 'r') as f:
                content = f.read()
                if 'openai' in content:
                    print("✅ OpenAI dependency in requirements.txt")
                else:
                    print("❌ OpenAI dependency missing from requirements.txt")
                    return False
        else:
            print("❌ requirements.txt missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config files test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality without complex imports"""
    print("\n🔍 Testing basic functionality...")
    
    try:
        # Test that we can create a simple DataFrame
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        print("✅ Pandas DataFrame creation works")
        
        # Test that we can import basic modules
        import logging
        logger = logging.getLogger(__name__)
        print("✅ Logging works")
        
        # Test that we can read files
        with open("requirements.txt", "r") as f:
            content = f.read()
            print(f"✅ File reading works (requirements.txt: {len(content)} chars)")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Enhanced Q&A System Tests\n")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Imports", test_imports),
        ("EnhancedQAEngine", test_enhanced_qa_engine),
        ("QASpecialistAgent", test_qa_specialist_agent),
        ("Frontend Functions", test_frontend_functions),
        ("Configuration Files", test_config_files)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced Q&A system is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
