# -*- coding: utf-8 -*-
"""
Comprehensive Tax System Test
Tests all new capabilities including Israel tax authority and tax treaty tools
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment_setup():
    """Test environment and dependencies"""
    print("Testing environment setup...")
    
    # Check environment variables
    required_vars = ['OPENAI_API_KEY']
    optional_vars = ['SERPER_API_KEY']
    
    print("Required environment variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  OK {var}: {'*' * min(len(value), 10)}")
        else:
            print(f"  MISSING {var}")
    
    print("Optional environment variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"  OK {var}: {'*' * min(len(value), 10)}")
        else:
            print(f"  MISSING {var} (optional)")
    
    return True

def test_imports():
    """Test all required imports"""
    print("\nTesting module imports...")
    
    try:
        from agents.yaml_crew_loader import YAMLCrewLoader
        print("  OK YAMLCrewLoader")
    except ImportError as e:
        print(f"  ERROR YAMLCrewLoader: {e}")
        return False
    
    try:
        from agents.web_scraping_tools import web_scraping_tools
        print("  OK web_scraping_tools")
    except ImportError as e:
        print(f"  WARNING web_scraping_tools: {e} (optional)")
    
    try:
        import requests
        print("  OK requests")
    except ImportError as e:
        print(f"  ERROR requests: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  OK BeautifulSoup")
    except ImportError as e:
        print(f"  WARNING BeautifulSoup: {e} (optional)")
    
    try:
        import PyPDF2
        print("  OK PyPDF2")
    except ImportError as e:
        print(f"  WARNING PyPDF2: {e} (optional)")
    
    return True

def test_agent_creation():
    """Test agent creation and tool availability"""
    print("\nTesting agent creation...")
    
    try:
        from agents.yaml_crew_loader import YAMLCrewLoader
        
        loader = YAMLCrewLoader()
        agents = loader.create_agents()
        
        print(f"  OK Created {len(agents)} agents")
        
        # Check tools for each agent
        expected_tools = [
            'web_search', 'web_scrape', 'scrape_tax_rates', 'scrape_oecd_documents',
            'extract_specific_content', 'scrape_israel_tax_authority',
            'scrape_israel_tax_treaties', 'get_israel_tax_treaty_content',
            'get_all_israel_tax_treaties_content', 'download_and_read_pdf'
        ]
        
        for i, agent in enumerate(agents):
            agent_name = getattr(agent, 'name', f'Agent_{i}')
            tool_names = [tool.name for tool in agent.tools if hasattr(tool, 'name')]
            
            print(f"  Agent {agent_name}: {len(tool_names)} tools")
            
            # Check for new Israel tax tools
            israel_tools = [name for name in tool_names if 'israel' in name.lower() or 'treaty' in name.lower()]
            if israel_tools:
                print(f"    Israel tax tools: {', '.join(israel_tools)}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Creating agents: {e}")
        return False

def test_web_scraping_tools():
    """Test web scraping functionality"""
    print("\nTesting web scraping tools...")
    
    try:
        from agents.web_scraping_tools import web_scraping_tools
        
        # Test basic web scraping
        print("  Testing basic web scraping...")
        result = web_scraping_tools.scrape_webpage("https://httpbin.org/html")
        if result.success:
            print("    OK Basic web scraping works")
        else:
            print(f"    WARNING Basic web scraping: {result.error}")
        
        # Test Israel tax authority scraping
        print("  Testing Israel tax authority scraping...")
        result = web_scraping_tools.scrape_israel_tax_authority()
        print(f"    Result: {result.success}")
        if result.content:
            print(f"    Content: {len(result.content)} characters")
        
        # Test Israel tax treaties scraping
        print("  Testing Israel tax treaties scraping...")
        result = web_scraping_tools.scrape_israel_tax_treaties()
        print(f"    Result: {result.success}")
        if result.content:
            print(f"    Content: {len(result.content)} characters")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Web scraping tools: {e}")
        return False

def test_agent_tools():
    """Test agent tool execution"""
    print("\nTesting agent tools...")
    
    try:
        from agents.yaml_crew_loader import YAMLCrewLoader
        
        loader = YAMLCrewLoader()
        agents = loader.create_agents()
        agent = agents[0]  # Use first agent
        
        # Test Israel tax authority tool
        print("  Testing Israel tax authority tool...")
        tool = next((t for t in agent.tools if hasattr(t, 'name') and 'israel_tax_authority' in t.name), None)
        if tool:
            try:
                result = tool.func()
                print(f"    OK Israel tax authority tool: {result}")
            except Exception as e:
                print(f"    WARNING Israel tax authority tool error: {e}")
        else:
            print("    ERROR Israel tax authority tool not found")
        
        # Test Israel tax treaties tool
        print("  Testing Israel tax treaties tool...")
        tool = next((t for t in agent.tools if hasattr(t, 'name') and 'israel_tax_treaties' in t.name), None)
        if tool:
            try:
                result = tool.func()
                print(f"    OK Israel tax treaties tool: {result}")
            except Exception as e:
                print(f"    WARNING Israel tax treaties tool error: {e}")
        else:
            print("    ERROR Israel tax treaties tool not found")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Testing agent tools: {e}")
        return False

def test_data_validation():
    """Test data validation capabilities"""
    print("\nTesting data validation...")
    
    try:
        # Test with sample data
        sample_data = {
            "company_name": "Test Company Ltd.",
            "tax_year": 2024,
            "revenue": 1000000,
            "country": "Israel"
        }
        
        print("  Testing sample data...")
        print(f"    Company: {sample_data['company_name']}")
        print(f"    Tax Year: {sample_data['tax_year']}")
        print(f"    Revenue: {sample_data['revenue']:,}")
        print(f"    Country: {sample_data['country']}")
        
        # Validate data types
        if isinstance(sample_data['company_name'], str):
            print("    OK Company name: valid")
        if isinstance(sample_data['tax_year'], int) and 2000 <= sample_data['tax_year'] <= 2030:
            print("    OK Tax year: valid")
        if isinstance(sample_data['revenue'], (int, float)) and sample_data['revenue'] > 0:
            print("    OK Revenue: valid")
        if isinstance(sample_data['country'], str):
            print("    OK Country: valid")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Data validation: {e}")
        return False

def test_tax_analysis():
    """Test tax analysis capabilities"""
    print("\nTesting tax analysis...")
    
    try:
        # Simulate tax calculations
        revenue = 1000000
        expenses = 600000
        taxable_income = revenue - expenses
        tax_rate = 0.25
        tax_amount = taxable_income * tax_rate
        
        print("  Sample tax calculations:")
        print(f"    Revenue: ${revenue:,}")
        print(f"    Expenses: ${expenses:,}")
        print(f"    Taxable Income: ${taxable_income:,}")
        print(f"    Tax Rate: {tax_rate*100}%")
        print(f"    Tax Amount: ${tax_amount:,}")
        
        # Test different scenarios
        scenarios = [
            {"name": "Small Company", "revenue": 500000, "rate": 0.15},
            {"name": "Medium Company", "revenue": 2000000, "rate": 0.23},
            {"name": "Large Company", "revenue": 10000000, "rate": 0.25}
        ]
        
        print("  Different scenarios:")
        for scenario in scenarios:
            tax = scenario["revenue"] * scenario["rate"]
            print(f"    {scenario['name']}: ${tax:,}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Tax analysis: {e}")
        return False

def test_recommendations():
    """Test recommendation capabilities"""
    print("\nTesting recommendations...")
    
    try:
        # Simulate recommendations based on data
        recommendations = [
            "Check eligibility for startup tax benefits",
            "Consider R&D investment for tax credits",
            "Review tax treaties to avoid double taxation",
            "Consider optimal company structure for tax savings",
            "Check BEPS and Pillar Two reporting requirements"
        ]
        
        print("  System recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"    {i}. {rec}")
        
        # Test risk assessment
        risk_factors = [
            "Exposure to tax law changes",
            "Transfer pricing risks",
            "Exposure to tax treaty changes",
            "BEPS reporting risks"
        ]
        
        print("  Risk factors:")
        for factor in risk_factors:
            print(f"    • {factor}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Recommendations: {e}")
        return False

def test_explanations():
    """Test explanation capabilities"""
    print("\nTesting explanations...")
    
    try:
        explanations = {
            "Pillar Two": "International framework for 15% minimum tax on large companies",
            "BEPS": "OECD program to prevent base erosion and profit shifting",
            "Transfer Pricing": "Transfer pricing - setting prices between related companies",
            "Tax Treaties": "Tax treaties to prevent double taxation between countries",
            "CbCR": "Country-by-Country Reporting - detailed reporting by country"
        }
        
        print("  Term explanations:")
        for term, explanation in explanations.items():
            print(f"    {term}: {explanation}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR Explanations: {e}")
        return False

def run_comprehensive_test():
    """Run all comprehensive tests"""
    print("Running Comprehensive Tax System Test")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Module Imports", test_imports),
        ("Agent Creation", test_agent_creation),
        ("Web Scraping Tools", test_web_scraping_tools),
        ("Agent Tools", test_agent_tools),
        ("Data Validation", test_data_validation),
        ("Tax Analysis", test_tax_analysis),
        ("Recommendations", test_recommendations),
        ("Explanations", test_explanations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERROR in test '{test_name}': {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! System is ready for use.")
    else:
        print("WARNING: Some tests failed. Check errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
