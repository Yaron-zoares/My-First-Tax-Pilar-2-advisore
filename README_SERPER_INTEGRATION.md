# 🔍 Serper Integration - Web Search for OECD Pillar Two Agents

## Overview
All agents in the Pilar2 system now include **Serper web search capabilities** to access current information about OECD Pillar Two regulations, tax updates, and legal developments.

## 🚀 New Capabilities

### Web Search Tool
- **Real-time Information**: Access current OECD Pillar Two updates and regulations
- **Multi-language Support**: Search in Hebrew and English
- **Contextual Results**: Automatically enhance queries with OECD Pillar Two context
- **Top 5 Results**: Get the most relevant search results for each query

## 📋 Setup Instructions

### 1. Get Serper API Key
1. Visit [Serper.dev](https://serper.dev)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Configure Environment
Create a `.env` file in the project root with your API keys:

```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
echo "SERPER_API_KEY=your-serper-api-key-here" >> .env
echo "SECRET_KEY=your-super-secret-key-change-this-in-production" >> .env
echo "DEBUG=True" >> .env
```

Or manually create `.env` file with:
```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Web Search API Configuration
SERPER_API_KEY=your-serper-api-key-here

# Application Settings
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🤖 Agents with Web Search

### 1. Tax Modeler Agent
- **Tool**: `serper_web_search`
- **Use Case**: Search for current ETR calculation methods and tax rate updates
- **Example Query**: "ETR calculation methods 2024"

### 2. Legal Interpreter Agent
- **Tool**: `serper_web_search`
- **Use Case**: Search for latest OECD guidance and legal interpretations
- **Example Query**: "OECD Pillar Two administrative guidance"

### 3. XML Reporter Agent
- **Tool**: `serper_web_search`
- **Use Case**: Search for latest XML schema updates and reporting requirements
- **Example Query**: "GIR XML schema updates 2024"

### 4. Risk Analyst Agent
- **Tool**: `serper_web_search`
- **Use Case**: Search for current risk factors and compliance issues
- **Example Query**: "Pillar Two compliance risks 2024"

### 5. Transfer Pricing Specialist Agent
- **Tool**: `serper_web_search`
- **Use Case**: Search for transfer pricing developments and OECD guidelines
- **Example Query**: "Transfer pricing OECD guidelines 2024"

### 6. QA Specialist Agent
- **Tool**: `Web_Search`
- **Use Case**: Comprehensive search for answering complex questions
- **Example Query**: "Pillar Two implementation timeline"

### 7. PillarTwoMaster Agent
- **Tool**: `Web_Search`
- **Use Case**: Master-level search for comprehensive analysis
- **Example Query**: "OECD Pillar Two global implementation status"

## 🔧 Technical Implementation

### Search Function
```python
def _web_search(self, query: str) -> str:
    """
    Search the web using Serper API for current information about OECD Pillar Two
    """
    # Automatically enhances query with OECD Pillar Two context
    enhanced_query = f"OECD Pillar Two {query} tax regulations 2024"
    
    # Returns formatted results with title, snippet, and link
    return formatted_search_results
```

### Query Enhancement
The system automatically enhances search queries by:
- Adding "OECD Pillar Two" context
- Including "tax regulations 2024" for current information
- Focusing on relevant regulatory content

### Result Format
Search results include:
- **Title**: Page title
- **Snippet**: Relevant text excerpt
- **Link**: Source URL
- **Top 5 Results**: Most relevant results

## 📊 Usage Examples

### Example 1: Tax Rate Updates
```python
# Agent will search for current tax rate information
result = agent.tools[0].func("corporate tax rates 2024")
```

### Example 2: Regulatory Updates
```python
# Agent will search for latest OECD guidance
result = agent.tools[0].func("administrative guidance updates")
```

### Example 3: Implementation Status
```python
# Agent will search for global implementation status
result = agent.tools[0].func("country implementation status")
```

## 🛡️ Error Handling

### Missing API Key
If `SERPER_API_KEY` is not configured:
```
Error: SERPER_API_KEY not configured. Please set the environment variable.
```

### API Errors
If the search fails:
```
Error: Failed to search web. Status code: [status_code]
```

### No Results
If no relevant results are found:
```
No relevant web results found for '[query]'
```

## 🔄 Integration with Existing Tools

The web search tool works alongside existing tools:

1. **Knowledge Base Search**: Internal knowledge + web search
2. **Enhanced QA Engine**: AI analysis + current web information
3. **Risk Assessment**: Historical data + current regulatory updates
4. **Compliance Monitoring**: Internal rules + latest requirements

## 📈 Benefits

### 1. Current Information
- Access to latest OECD updates
- Real-time regulatory changes
- Current implementation status

### 2. Comprehensive Analysis
- Combine internal knowledge with web data
- Enhanced accuracy and relevance
- Up-to-date recommendations

### 3. Multi-Source Validation
- Cross-reference internal data with web sources
- Verify regulatory requirements
- Confirm implementation timelines

## 🔧 Configuration Options

### Search Parameters
- **Number of Results**: Default 5 (configurable)
- **Query Enhancement**: Automatic OECD Pillar Two context
- **Language Support**: Hebrew and English queries

### API Limits
- **Free Tier**: 100 searches per month
- **Paid Plans**: Higher limits available
- **Rate Limiting**: Automatic handling

## 🚨 Important Notes

1. **API Key Security**: Keep your Serper API key secure
2. **Usage Limits**: Monitor your API usage
3. **Data Privacy**: Search results are processed but not stored
4. **Fallback**: System works without web search if API is unavailable

## 📞 Support

For issues with Serper integration:
1. Check API key configuration
2. Verify internet connectivity
3. Monitor API usage limits
4. Review error messages in logs

---

**Note**: The web search tool enhances all agents' capabilities by providing access to current, real-time information about OECD Pillar Two regulations and developments.
