# 🌐 Web Scraping Integration - Pilar2 Agents

## Overview
All Pilar2 agents now include **advanced web scraping capabilities** to extract real-time data from websites, government databases, and regulatory sources for comprehensive OECD Pillar Two analysis. **All validation errors have been resolved and the system is fully operational with CrewAI integration.**

## 🚀 New Capabilities

### Web Scraping Tools
- **Real-time Data Extraction**: Extract content from any webpage
- **Government Data Access**: Scrape tax rates and regulatory information
- **OECD Document Analysis**: Extract guidance and policy documents
- **Targeted Content Extraction**: Use CSS selectors for specific data
- **Dynamic Content Support**: Handle JavaScript-heavy websites
- **Safe Error Handling**: Graceful fallbacks and retry mechanisms

## 📋 Setup Instructions

### 1. Install Dependencies
```bash
# Install web scraping dependencies
pip install beautifulsoup4 selenium webdriver-manager

# Or install all dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
echo "SERPER_API_KEY=your-serper-api-key-here" >> .env
echo "SECRET_KEY=your-super-secret-key-change-this-in-production" >> .env
echo "DEBUG=True" >> .env
```

### 3. Test Integration
```bash
# Run web scraping test suite
python test_web_scraping_integration.py
```

## 🤖 Agents with Web Scraping

### 1. Tax Modeler Agent
- **Tools**: `web_scrape`, `scrape_tax_rates`, `scrape_oecd_documents`
- **Use Case**: Extract current tax rates and OECD guidance
- **Example**: Scrape government tax databases for rate updates

### 2. Legal Interpreter Agent
- **Tools**: `web_scrape`, `scrape_oecd_documents`, `extract_specific_content`
- **Use Case**: Extract legal documents and regulatory updates
- **Example**: Scrape OECD guidance documents for legal analysis

### 3. XML Reporter Agent
- **Tools**: `web_scrape`, `scrape_oecd_documents`, `extract_specific_content`
- **Use Case**: Extract XML schemas and reporting requirements
- **Example**: Scrape latest OECD XML schema updates

### 4. Risk Analyst Agent
- **Tools**: `web_scrape`, `scrape_oecd_documents`, `extract_specific_content`
- **Use Case**: Monitor regulatory changes and compliance updates
- **Example**: Scrape enforcement actions and risk indicators

### 5. Transfer Pricing Specialist Agent
- **Tools**: `web_scrape`, `scrape_oecd_documents`, `extract_specific_content`
- **Use Case**: Extract transfer pricing guidelines and updates
- **Example**: Scrape OECD transfer pricing documentation

### 6. QA Specialist Agent
- **Tools**: `Web_Scrape`, `Scrape_Tax_Rates`, `Scrape_OECD_Documents`
- **Use Case**: Comprehensive data extraction for Q&A
- **Example**: Extract current information for answering complex questions

### 7. PillarTwoMaster Agent
- **Tools**: `Web_Scrape`, `Scrape_Tax_Rates`, `Scrape_OECD_Documents`
- **Use Case**: Master-level data extraction and analysis
- **Example**: Comprehensive scraping for strategic analysis

## 🔧 Technical Implementation

### Core Web Scraping Module
```python
from agents.web_scraping_tools import web_scraping_tools

# Basic webpage scraping
result = web_scraping_tools.scrape_webpage("https://example.com")

# Extract specific content
selectors = {"title": "h1", "content": ".main-content"}
extracted = web_scraping_tools.extract_specific_content(url, selectors)

# Scrape tax rates
tax_data = web_scraping_tools.scrape_tax_rates("israel")

# Scrape OECD documents
oecd_data = web_scraping_tools.scrape_oecd_documents("pillar-two")
```

### Safe Error Handling
```python
# All scraping operations include error handling
result = web_scraping_tools.scrape_webpage(url)
if result.success:
    print(f"Content: {result.content}")
else:
    print(f"Error: {result.error_message}")
```

### Multiple Scraping Methods
```python
# Requests + BeautifulSoup (default)
result = web_scraping_tools.scrape_webpage(url)

# Selenium for dynamic content
result = web_scraping_tools.scrape_webpage(url, use_selenium=True)

# Multiple pages
results = web_scraping_tools.scrape_multiple_pages(urls)
```

## 📊 Usage Examples

### Example 1: Extract Tax Rates
```python
# Agent will scrape current tax rates
result = agent.tools[0].func("israel")  # scrape_tax_rates
```

### Example 2: Extract OECD Documents
```python
# Agent will scrape OECD guidance
result = agent.tools[0].func("pillar-two")  # scrape_oecd_documents
```

### Example 3: Extract Specific Content
```python
# Agent will extract specific content using selectors
selectors = '{"title": "h1", "content": ".main-content"}'
result = agent.tools[0].func("https://example.com", selectors)
```

### Example 4: Scrape Multiple Pages
```python
# Agent will scrape multiple pages
urls = ["https://site1.com", "https://site2.com"]
results = web_scraping_tools.scrape_multiple_pages(urls)
```

## 🛡️ Safety Features

### 1. Error Handling
- **Network Errors**: Automatic retry with exponential backoff
- **Invalid URLs**: Validation and error reporting
- **Missing Dependencies**: Graceful fallbacks
- **Timeouts**: Configurable timeout handling

### 2. Rate Limiting
- **Respectful Scraping**: Delays between requests
- **User-Agent Headers**: Proper browser identification
- **Session Management**: Efficient connection reuse

### 3. Resource Management
- **Automatic Cleanup**: Driver and session cleanup
- **Memory Management**: Efficient resource usage
- **Connection Pooling**: Optimized HTTP connections

### 4. Content Validation
- **URL Validation**: Ensure valid URLs before scraping
- **Content Type Checking**: Validate response types
- **Encoding Handling**: Proper text encoding

## 🔄 Integration with Existing Tools

### 1. Web Search + Web Scraping
```python
# Search for relevant pages
search_results = web_search("OECD Pillar Two guidance")

# Scrape specific pages from search results
for result in search_results:
    scraped_content = web_scrape(result.url)
```

### 2. Enhanced QA with Web Data
```python
# Extract current information for Q&A
current_data = scrape_oecd_documents("pillar-two")
qa_result = enhanced_qa_analysis(question, {"web_data": current_data})
```

### 3. Risk Assessment with Live Data
```python
# Monitor regulatory changes
regulatory_updates = scrape_oecd_documents("guidance")
risk_assessment = assess_risks(context, {"updates": regulatory_updates})
```

## 📈 Benefits

### 1. Real-time Information
- **Current Data**: Access to latest regulatory updates
- **Live Monitoring**: Real-time compliance tracking
- **Dynamic Content**: Handle JavaScript-heavy websites

### 2. Comprehensive Coverage
- **Multiple Sources**: Extract from various websites
- **Structured Data**: Extract specific content with selectors
- **Bulk Operations**: Scrape multiple pages efficiently

### 3. Enhanced Analysis
- **Data Validation**: Cross-reference multiple sources
- **Trend Analysis**: Track changes over time
- **Compliance Monitoring**: Monitor regulatory updates

### 4. Operational Efficiency
- **Automation**: Reduce manual data collection
- **Accuracy**: Eliminate human error in data extraction
- **Speed**: Fast extraction of large datasets

## 🔧 Configuration Options

### Scraping Parameters
- **Timeout**: Configurable request timeouts
- **Retries**: Automatic retry with backoff
- **User-Agent**: Customizable browser identification
- **Delays**: Respectful scraping delays

### Content Extraction
- **Selectors**: CSS selectors for targeted extraction
- **Content Types**: HTML, text, structured data
- **Encoding**: Automatic encoding detection
- **Cleaning**: Automatic content cleaning

### Error Handling
- **Fallbacks**: Multiple scraping methods
- **Logging**: Comprehensive error logging
- **Recovery**: Automatic error recovery
- **Reporting**: Detailed error reporting

## 🚨 Important Notes

### 1. Legal Compliance
- **Terms of Service**: Respect website terms of service
- **Rate Limiting**: Implement appropriate delays
- **Robots.txt**: Respect robots.txt files
- **Data Privacy**: Handle personal data appropriately

### 2. Technical Considerations
- **Dependencies**: Ensure all dependencies are installed
- **Browser Requirements**: Chrome for Selenium functionality
- **Network Access**: Ensure internet connectivity
- **Resource Usage**: Monitor memory and CPU usage

### 3. Best Practices
- **Respectful Scraping**: Use appropriate delays
- **Error Handling**: Always handle errors gracefully
- **Resource Cleanup**: Clean up resources after use
- **Monitoring**: Monitor scraping performance

## 📞 Support

### Troubleshooting
1. **Import Errors**: Install missing dependencies
2. **Network Issues**: Check internet connectivity
3. **Browser Issues**: Update Chrome and ChromeDriver
4. **Memory Issues**: Monitor resource usage

### Getting Help
1. Check the logs for error messages
2. Run the test suite: `python test_web_scraping_integration.py`
3. Verify dependencies are installed
4. Check network connectivity

---

**Note**: Web scraping tools enhance all agents' capabilities by providing access to current, real-time data from websites and regulatory sources, significantly improving the accuracy and relevance of OECD Pillar Two analysis.
