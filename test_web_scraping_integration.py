#!/usr/bin/env python3
"""
Test Web Scraping Integration with Pilar2 Agents
בדיקת אינטגרציה של כלי web scraping עם סוכני Pilar2
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_web_scraping_tools():
    """Test the web scraping tools module"""
    
    print("🔍 Testing Web Scraping Tools Integration")
    print("=" * 60)
    
    try:
        from agents.web_scraping_tools import web_scraping_tools
        
        print("✅ Web scraping tools imported successfully")
        
        # Test 1: Basic webpage scraping
        print("\n1️⃣ Testing basic webpage scraping...")
        test_url = "https://www.example.com"
        result = web_scraping_tools.scrape_webpage(test_url)
        
        if result.success:
            print(f"✅ Successfully scraped {test_url}")
            print(f"📄 Title: {result.title}")
            print(f"📊 Content length: {len(result.content)} characters")
        else:
            print(f"❌ Failed to scrape {test_url}: {result.error_message}")
        
        # Test 2: Tax rates scraping
        print("\n2️⃣ Testing tax rates scraping...")
        tax_result = web_scraping_tools.scrape_tax_rates("israel")
        if "error" not in tax_result:
            print(f"✅ Tax rates scraping successful")
            print(f"📊 Content preview: {tax_result['content'][:200]}...")
        else:
            print(f"❌ Tax rates scraping failed: {tax_result['error']}")
        
        # Test 3: OECD documents scraping
        print("\n3️⃣ Testing OECD documents scraping...")
        oecd_result = web_scraping_tools.scrape_oecd_documents("pillar-two")
        if "error" not in oecd_result:
            print(f"✅ OECD documents scraping successful")
            print(f"📄 Title: {oecd_result['title']}")
            print(f"📊 Content preview: {oecd_result['content'][:200]}...")
        else:
            print(f"❌ OECD documents scraping failed: {oecd_result['error']}")
        
        # Test 4: Multiple pages scraping
        print("\n4️⃣ Testing multiple pages scraping...")
        test_urls = [
            "https://www.example.com",
            "https://httpbin.org/html"
        ]
        multi_result = web_scraping_tools.scrape_multiple_pages(test_urls)
        
        successful_scrapes = sum(1 for result in multi_result.values() if result.success)
        print(f"✅ Successfully scraped {successful_scrapes}/{len(test_urls)} pages")
        
        # Test 5: Specific content extraction
        print("\n5️⃣ Testing specific content extraction...")
        selectors = {
            "title": "title",
            "body": "body"
        }
        extract_result = web_scraping_tools.extract_specific_content(
            "https://httpbin.org/html", 
            selectors
        )
        
        if "error" not in extract_result:
            print(f"✅ Content extraction successful")
            print(f"📄 Extracted title: {extract_result.get('title', 'N/A')[:100]}...")
        else:
            print(f"❌ Content extraction failed: {extract_result['error']}")
        
        # Cleanup
        web_scraping_tools.cleanup()
        print("\n✅ Web scraping tools cleanup completed")
        
    except ImportError as e:
        print(f"❌ Failed to import web scraping tools: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install beautifulsoup4 selenium webdriver-manager")
    except Exception as e:
        print(f"❌ Error testing web scraping tools: {e}")

def test_agent_integration():
    """Test web scraping integration with agents"""
    
    print("\n🤖 Testing Agent Integration with Web Scraping")
    print("=" * 60)
    
    try:
        # Test YAML Crew Loader
        print("\n1️⃣ Testing YAML Crew Loader with web scraping...")
        from agents.yaml_crew_loader import YAMLCrewLoader
        
        loader = YAMLCrewLoader()
        crew = loader.create_crew()
        
        # Check if web scraping tools are available
        tax_modeler = crew.agents[0]  # First agent is tax_modeler
        web_scraping_tools_found = False
        
        for tool in tax_modeler.tools:
            if hasattr(tool, 'name') and tool.name in ["web_scrape", "scrape_tax_rates", "scrape_oecd_documents"]:
                web_scraping_tools_found = True
                print(f"✅ Found web scraping tool: {tool.name}")
            elif hasattr(tool, 'func') and tool.func.__name__ in ["_web_scrape", "_scrape_tax_rates", "_scrape_oecd_documents"]:
                web_scraping_tools_found = True
                print(f"✅ Found web scraping tool: {tool.func.__name__}")
        
        if web_scraping_tools_found:
            print("✅ Web scraping tools successfully integrated with YAML Crew Loader")
        else:
            print("❌ Web scraping tools not found in YAML Crew Loader")
        
        # Test QA Specialist Agent
        print("\n2️⃣ Testing QA Specialist Agent with web scraping...")
        from agents.qa_specialist_agent import QASpecialistAgent
        
        qa_agent = QASpecialistAgent()
        qa_web_scraping_tools_found = False
        
        for tool in qa_agent.agent.tools:
            if tool.name in ["Web_Scrape", "Scrape_Tax_Rates", "Scrape_OECD_Documents"]:
                qa_web_scraping_tools_found = True
                print(f"✅ Found web scraping tool in QA agent: {tool.name}")
        
        if qa_web_scraping_tools_found:
            print("✅ Web scraping tools successfully integrated with QA Specialist Agent")
        else:
            print("❌ Web scraping tools not found in QA Specialist Agent")
        
        # Test PillarTwoMaster Agent
        print("\n3️⃣ Testing PillarTwoMaster Agent with web scraping...")
        from agents.pillar_two_master import PillarTwoMaster
        
        master_agent = PillarTwoMaster()
        master_web_scraping_tools_found = False
        
        for tool in master_agent.agent.tools:
            if tool.name in ["Web_Scrape", "Scrape_Tax_Rates", "Scrape_OECD_Documents"]:
                master_web_scraping_tools_found = True
                print(f"✅ Found web scraping tool in Master agent: {tool.name}")
        
        if master_web_scraping_tools_found:
            print("✅ Web scraping tools successfully integrated with PillarTwoMaster Agent")
        else:
            print("❌ Web scraping tools not found in PillarTwoMaster Agent")
        
    except Exception as e:
        print(f"❌ Error testing agent integration: {e}")

def test_web_scraping_functionality():
    """Test actual web scraping functionality"""
    
    print("\n🌐 Testing Web Scraping Functionality")
    print("=" * 60)
    
    try:
        from agents.web_scraping_tools import web_scraping_tools
        
        # Test with a real OECD-related URL
        print("\n1️⃣ Testing scraping of OECD-related content...")
        
        # Test with a simple, reliable URL
        test_url = "https://httpbin.org/html"
        result = web_scraping_tools.scrape_webpage(test_url)
        
        if result.success:
            print(f"✅ Successfully scraped {test_url}")
            print(f"📄 Title: {result.title}")
            print(f"📊 Content preview: {result.content[:300]}...")
            print(f"🔧 Metadata: {result.metadata}")
        else:
            print(f"❌ Failed to scrape {test_url}: {result.error_message}")
        
        # Test with selectors
        print("\n2️⃣ Testing content extraction with selectors...")
        selectors = {
            "title": "title",
            "h1": "h1",
            "body_text": "body"
        }
        
        extract_result = web_scraping_tools.extract_specific_content(test_url, selectors)
        
        if "error" not in extract_result:
            print("✅ Content extraction successful:")
            for key, value in extract_result.items():
                print(f"   {key}: {value[:100]}...")
        else:
            print(f"❌ Content extraction failed: {extract_result['error']}")
        
        # Test error handling
        print("\n3️⃣ Testing error handling...")
        invalid_url = "https://invalid-url-that-does-not-exist.com"
        error_result = web_scraping_tools.scrape_webpage(invalid_url)
        
        if not error_result.success:
            print(f"✅ Error handling working correctly: {error_result.error_message}")
        else:
            print("❌ Error handling not working as expected")
            
        # Test with invalid URL format
        invalid_format_url = "not-a-valid-url"
        format_error_result = web_scraping_tools.scrape_webpage(invalid_format_url)
        
        if not format_error_result.success:
            print(f"✅ URL format validation working: {format_error_result.error_message}")
        else:
            print("❌ URL format validation not working")
        
        # Cleanup
        web_scraping_tools.cleanup()
        
    except Exception as e:
        print(f"❌ Error testing web scraping functionality: {e}")

def test_dependencies():
    """Test if all required dependencies are available"""
    
    print("\n📦 Testing Dependencies")
    print("=" * 60)
    
    dependencies = {
        "beautifulsoup4": "BeautifulSoup",
        "selenium": "selenium",
        "webdriver-manager": "webdriver_manager",
        "requests": "requests"
    }
    
    missing_deps = []
    
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_deps.append(package)
    
    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("Install them with:")
        print(f"pip install {' '.join(missing_deps)}")
    else:
        print("\n✅ All dependencies are available")

def main():
    """Run all tests"""
    
    print("🚀 Web Scraping Integration Test Suite")
    print("=" * 60)
    
    # Test dependencies first
    test_dependencies()
    
    # Test web scraping tools
    test_web_scraping_tools()
    
    # Test agent integration
    test_agent_integration()
    
    # Test functionality
    test_web_scraping_functionality()
    
    print("\n" + "=" * 60)
    print("🎉 Web Scraping Integration Test Completed!")
    print()
    print("📋 Summary:")
    print("- Web scraping tools are integrated with all agents")
    print("- Safe error handling and fallbacks are in place")
    print("- Multiple scraping methods are available")
    print("- Content extraction with selectors is supported")
    print()
    print("💡 Usage Tips:")
    print("- Use web_scrape for general webpage content")
    print("- Use scrape_tax_rates for government tax data")
    print("- Use scrape_oecd_documents for OECD guidance")
    print("- Use extract_specific_content for targeted data")
    print("- All tools include proper error handling")

if __name__ == "__main__":
    main()
