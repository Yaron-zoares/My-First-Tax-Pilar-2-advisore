# Pilar2 Streamlit Cloud Deployment Guide

## 🚀 Overview

This guide explains how to deploy the Pilar2 Financial Report Analysis System to Streamlit Cloud, resolving dependency conflicts and ensuring smooth deployment.

## ⚠️ Known Issues & Solutions

### 1. Dependency Conflicts

**Problem**: `crewai` and `guardrails-ai` have incompatible regex requirements:
- `crewai>=0.150.0` requires `regex>=2024.9.11`
- `guardrails-ai>=0.3.0` requires `regex>=2023.10.3,<2024.0.0`

**Solution**: Use `requirements-streamlit.txt` which excludes conflicting packages for initial deployment.

### 2. Build Dependencies

**Problem**: Some packages like `lxml` require system-level dependencies that aren't available on Streamlit Cloud.

**Solution**: Use pre-compiled wheels or alternative packages.

## 📋 Deployment Steps

### Step 1: Prepare Repository

1. **Use Streamlit-Compatible Requirements**:
   ```bash
   # Use requirements-streamlit.txt instead of requirements.txt
   cp requirements-streamlit.txt requirements.txt
   ```

2. **Update .streamlit/config.toml**:
   ```toml
   [global]
   developmentMode = false
   
   [server]
   headless = true
   enableCORS = false
   enableXsrfProtection = false
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Connect Repository**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file path: `frontend/app.py`

2. **Environment Variables** (Optional):
   ```
   STREAMLIT_CLOUD=true
   API_BASE_URL=your-api-url
   ```

3. **Deploy**:
   - Click "Deploy"
   - Wait for build completion

## 🔧 Configuration Files

### requirements-streamlit.txt
Minimal dependencies for Streamlit Cloud:
```txt
streamlit==1.36.0
pandas==2.2.3
numpy==1.26.4
plotly==5.17.0
openai==1.58.0
langchain==0.3.27
langchain-openai==0.3.29
```

### .streamlit/config.toml
Streamlit configuration for production:
```toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
```

## 🚧 Limitations in Streamlit Cloud

### What Won't Work:
1. **Backend API**: FastAPI backend won't be available
2. **CrewAI Agents**: Advanced AI agents require backend
3. **Guardrails**: AI safety features need backend
4. **File Uploads**: Limited file processing capabilities

### What Will Work:
1. **Basic UI**: Streamlit interface loads successfully
2. **Data Display**: View existing data and reports
3. **Basic Q&A**: Simple question answering (if OpenAI key provided)
4. **Visualizations**: Plotly charts and data displays

## 🔄 Future Improvements

### Phase 1: Basic Deployment ✅
- [x] Resolve dependency conflicts
- [x] Create minimal requirements file
- [x] Configure Streamlit settings

### Phase 2: Enhanced Features
- [ ] Implement backend-less file processing
- [ ] Add client-side AI capabilities
- [ ] Integrate with external APIs

### Phase 3: Full Functionality
- [ ] Deploy backend to cloud service
- [ ] Enable full AI agent system
- [ ] Restore all features

## 🐛 Troubleshooting

### Build Failures
```bash
# Check requirements compatibility
pip check

# Test locally first
streamlit run frontend/app.py
```

### Runtime Errors
```bash
# Check Streamlit logs
# Verify environment variables
# Test API connectivity
```

### Dependency Issues
```bash
# Use minimal requirements
pip install -r requirements-streamlit.txt

# Check for conflicts
pip list | grep -E "(crewai|guardrails)"
```

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Dependency Management](https://pip.pypa.io/en/stable/user_guide/)
- [Python Package Conflicts](https://pip.pypa.io/en/stable/topics/dependency-resolution/)

## 🎯 Success Metrics

- ✅ App deploys without build errors
- ✅ UI loads successfully
- ✅ Basic functionality works
- ✅ No dependency conflicts
- ✅ Stable performance

---

**Note**: This deployment guide focuses on getting a working Streamlit app deployed. Full functionality requires backend deployment and resolution of AI package conflicts.
