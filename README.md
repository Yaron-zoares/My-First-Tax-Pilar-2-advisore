# Pilar2 - Enhanced Financial Report Analysis System

A comprehensive AI-powered system for financial report analysis, tax calculations, and regulatory compliance reporting with advanced Q&A capabilities.

## 🚀 Features

- **Multi-Agent AI System**: 6 specialized agents for different aspects of financial analysis
- **Enhanced Q&A System**: Advanced AI-powered question answering with confidence scoring
- **Web Search Integration**: Real-time internet search capabilities via Serper API
- **Web Scraping**: Advanced web scraping tools for tax rates and regulatory information
- **Israel Tax Authority Integration**: Direct access to Israeli tax authority data
- **Tax Treaty Analysis**: Comprehensive analysis of international tax treaties
- **PDF Processing**: Advanced PDF reading and analysis capabilities
- **Financial Analysis**: Automated financial data processing and analysis
- **Regulatory Reporting**: BEPS, Pillar Two, and other regulatory compliance reports
- **Smart Q&A**: AI-powered question answering system with CrewAI integration
- **Multi-language Support**: Hebrew and English interface
- **Real-time Analysis**: Live financial data analysis and insights
- **Data Validation**: Advanced CSV and Excel file validation and fixing
- **Guardrails Integration**: AI safety and content filtering
- **Comprehensive Testing**: Full test suite with automated validation

## 🏗️ Architecture

### Backend (FastAPI)
- **Port**: 8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Frontend (Streamlit)
- **Port**: 8501
- **URL**: http://localhost:8501

### AI Agents
1. **Tax Modeler**: Tax calculations and modeling
2. **Legal Interpreter**: Legal document analysis
3. **XML Reporter**: Regulatory report generation
4. **Risk Analyst**: Risk assessment and analysis
5. **Transfer Pricing Specialist**: Transfer pricing analysis
6. **QA Specialist**: Advanced question answering with CrewAI integration

## 📋 Prerequisites

- **Python 3.13+** (recommended) or Python 3.8+
- pip package manager
- Git
- OpenAI API key

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pilar2.git
cd pilar2
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```bash
cp config/secrets.env.example .env
```

Edit `.env` with your API keys:
```env
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional (for enhanced features)
SERPER_API_KEY=your-serper-api-key-here

# Security
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 5. Create Required Directories
The system will automatically create necessary directories on first run.

## 🚀 Quick Start

### Start the Backend Server
```bash
python run_backend.py
```

### Start the Frontend (in a new terminal)
```bash
streamlit run frontend/app.py
```

### Access the Application
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## 📊 Usage

### 1. Enhanced Q&A System
- **Basic Q&A**: Ask questions about OECD Pillar Two and tax regulations
- **Enhanced Analysis**: Get comprehensive analysis with confidence scoring
- **AI-Powered Insights**: Advanced analysis using CrewAI agents
- **Real-time Responses**: Instant answers with detailed explanations

### 2. Upload Financial Data
- Navigate to "Upload Files" in the sidebar
- Upload Excel, CSV, or PDF files
- The system will automatically process and validate your data
- Advanced data fixing for common CSV and Excel issues

### 3. Financial Analysis
- Go to "Financial Analysis" to view processed data
- Review tax calculations and adjustments
- Export analysis results

### 4. Smart Q&A
- Use "Q&A" section to ask questions about your data
- Get AI-powered explanations and insights
- Available in Hebrew and English
- Advanced analysis with multiple AI agents

### 5. Generate Reports
- Create regulatory reports (BEPS, Pillar Two)
- Export to PDF, Word, or XML formats
- Access report templates and customization options

## 🔧 Configuration

### API Keys Setup

#### OpenAI API Key (Required)
1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`: `OPENAI_API_KEY=your-key-here`

#### Serper API Key (Optional - for web search)
1. Get your API key from [Serper.dev](https://serper.dev)
2. Add to `.env`: `SERPER_API_KEY=your-key-here`

### Advanced Configuration
Edit `config/settings.py` for advanced settings:
- Tax rates
- File upload limits
- CORS origins
- Logging levels

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_enhanced_qa_system.py
```

### Test Individual Components
```bash
# Test Serper integration
python test_serper_integration.py

# Test web scraping
python test_web_scraping_integration.py

# Test enhanced Q&A system
python test_enhanced_qa_system.py

# Test guardrails integration
python test_guardrails_integration.py
```

## 📁 Project Structure

```
Pilar2/
├── agents/                 # AI agents and tools
│   ├── crew_config.yaml   # Agent configuration
│   ├── yaml_crew_loader.py
│   ├── web_scraping_tools.py
│   ├── qa_specialist_agent.py  # Enhanced Q&A agent
│   ├── data_validator.py       # Data validation tools
│   ├── enhanced_error_handler.py # Error handling
│   └── ...
├── backend/               # FastAPI backend
│   ├── main.py
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   │   ├── csv_fixer.py  # CSV file fixing
│   │   ├── excel_fixer.py # Excel file fixing
│   │   ├── guardrails_service.py # AI safety
│   │   └── ...
│   └── utils/            # Utilities
├── frontend/             # Streamlit frontend
│   ├── app.py
│   ├── components/
│   └── pages/
├── config/               # Configuration files
│   ├── guardrails_config.yaml # AI safety config
│   └── ...
├── data/                 # Data storage
├── reports/              # Generated reports
├── logs/                 # Application logs
└── tests/                # Test files
```

## 🔒 Security

- API keys are stored in environment variables
- `.env` file is excluded from version control
- CORS is configured for local development
- File upload validation and sanitization
- AI content filtering with guardrails integration

## 🐛 Troubleshooting

### Common Issues

#### Backend Server Won't Start
```bash
# Check if port 8000 is available
netstat -an | findstr :8000

# Kill existing processes
taskkill /F /IM python.exe
```

#### Frontend Connection Issues
- Ensure backend is running on port 8000
- Check CORS configuration in `config/settings.py`
- Verify API endpoints are accessible

#### Missing Dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### Enhanced Q&A System Issues
- Ensure OpenAI API key is properly configured
- Check CrewAI configuration in `agents/crew_config.yaml`
- Verify all dependencies are installed correctly

#### Web Scraping Issues
- Some external websites may be inaccessible
- Check internet connection
- Verify URLs in `agents/web_scraping_tools.py`

#### Data Validation Issues
- Check file format and encoding
- Ensure CSV files use proper delimiters
- Verify Excel files are not corrupted

## 📚 Documentation

- [Enhanced Q&A System Guide](README_ENHANCED_QA_SYSTEM.md)
- [Serper Integration Guide](README_SERPER_INTEGRATION.md)
- [Web Scraping Integration](README_WEB_SCRAPING_INTEGRATION.md)
- [Guardrails Integration](README_GUARDRAILS_INTEGRATION.md)
- [API Documentation](http://localhost:8000/docs)
- [Agent Configuration](agents/README_ENHANCED_DATA_PROCESSING.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## 🔄 Updates

### Recent Updates (Latest)
- ✅ **Guardrails Integration**: AI safety and content filtering system
- ✅ **Enhanced Data Validation**: Advanced CSV and Excel file fixing
- ✅ **Improved Error Handling**: Better logging and validation
- ✅ **Comprehensive Testing**: Full test suite with automated validation
- ✅ **Enhanced Q&A System**: Advanced AI-powered question answering with CrewAI
- ✅ **Fixed Validation Errors**: Resolved all agent creation and tool validation issues
- ✅ **Updated Dependencies**: Compatible versions for Windows Python 3.13

### Previous Updates
- ✅ Added Serper web search integration
- ✅ Added comprehensive web scraping tools
- ✅ Added Israel tax authority integration
- ✅ Added tax treaty analysis capabilities
- ✅ Added PDF processing and reading
- ✅ Enhanced multi-agent system

### Version History
- **v2.2.0**: Guardrails integration and enhanced data validation
- **v2.1.0**: Enhanced Q&A system with CrewAI integration
- **v2.0.0**: Major update with AI agents and web integration
- **v1.0.0**: Initial release with basic functionality

## 🎯 System Status

- **Enhanced Q&A System**: ✅ Fully Operational
- **AI Agents**: ✅ All 6 agents working correctly
- **Guardrails Integration**: ✅ AI safety system active
- **Data Validation**: ✅ CSV and Excel fixing operational
- **Dependencies**: ✅ All packages installed successfully
- **Testing**: ✅ Comprehensive test suite passing
- **Platform Support**: ✅ Windows, macOS, Linux
- **Python Version**: ✅ 3.13+ (recommended), 3.8+ (minimum)

## 🆕 New Features

### Guardrails Integration
- AI content filtering and safety
- Configurable content policies
- Real-time content validation

### Enhanced Data Validation
- Automatic CSV file fixing
- Excel file corruption detection
- Data format standardization

### Improved Error Handling
- Better logging and debugging
- User-friendly error messages
- Automated error recovery

---

**Pilar2** - Empowering financial analysis with AI 🚀

*Enhanced Q&A System powered by CrewAI and OpenAI with AI Safety Guardrails*
