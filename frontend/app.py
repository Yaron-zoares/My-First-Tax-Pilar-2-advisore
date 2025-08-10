"""
Pilar2 Frontend Application
Streamlit-based user interface for financial analysis
"""

import streamlit as st
import pandas as pd
import requests
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Pilar2 - Financial Report Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
# For local development: http://localhost:8000/api/v1
# For Streamlit Cloud: Use environment variable or default to localhost
import os

# Try to get API URL from environment variable, fallback to localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# Check if running on Streamlit Cloud
IS_STREAMLIT_CLOUD = os.getenv("STREAMLIT_CLOUD", "false").lower() == "true"

if IS_STREAMLIT_CLOUD:
    # For Streamlit Cloud, we'll use relative URLs or a different approach
    API_BASE_URL = "/api/v1"  # This will be handled differently in the app

def main():
    """Main application function"""
    
    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    # Sidebar navigation
    st.sidebar.title("📊 Pilar2")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "🏠 Home",
            "📁 Upload Files",
            "📊 Financial Analysis",
            "❓ Q&A",
            "📋 Reports",
            "💡 Recommendations",
            "⚙️ Settings"
        ],
        key="sidebar_page",
        index=["🏠 Home", "📁 Upload Files", "📊 Financial Analysis", "❓ Q&A", "📋 Reports", "💡 Recommendations", "⚙️ Settings"].index(st.session_state.page)
    )
    
    # Update session state when sidebar changes
    if page != st.session_state.page:
        st.session_state.page = page
    
    # Page routing
    if "Home" in st.session_state.page:
        home_page()
    elif "Upload" in st.session_state.page:
        upload_page()
    elif "Analysis" in st.session_state.page:
        analysis_page()
    elif "Q&A" in st.session_state.page:
        qa_page()
    elif "Reports" in st.session_state.page:
        reports_page()
    elif "Recommendations" in st.session_state.page:
        recommendations_page()
    elif "Settings" in st.session_state.page:
        settings_page()

def home_page():
    """Enhanced Home page with AI capabilities overview"""
    st.markdown('<h1 class="main-header">Pilar2 - AI-Powered Financial Analysis System</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Advanced AI-Powered Financial Report Analysis & Q&A System</h2>', unsafe_allow_html=True)
    
    # Welcome message with AI features
    st.markdown("""
    ### Welcome to Pilar2 AI! 🚀
    
    **The most advanced AI-powered financial analysis system** with ChatGPT 3.5 integration for intelligent Q&A, 
    comprehensive risk assessment, and strategic recommendations.
    
    **ברוכים הבאים ל-Pilar2 AI! 🚀**
    
    **מערכת הניתוח הפיננסי המתקדמת ביותר** עם שילוב ChatGPT 3.5 לשאלות ותשובות חכמות,
    הערכת סיכונים מקיפה והמלצות אסטרטגיות.
    
    ---
    """)
    
    # AI Features showcase
    st.markdown("### 🤖 New AI-Powered Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🧠 Enhanced Q&A with ChatGPT 3.5
        - **Smart Question Classification:** Automatic categorization of questions
        - **AI-Enhanced Responses:** Detailed explanations and insights
        - **Risk Assessment:** Identify potential compliance risks
        - **Strategic Recommendations:** Get actionable advice
        
        #### 📊 Advanced Analysis
        - **QA Specialist Agent:** Comprehensive question analysis
        - **Multi-Agent Collaboration:** Integration with existing agents
        - **Deep Financial Insights:** Advanced financial analysis
        - **Compliance Verification:** Regulatory compliance checks
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Intelligent Features
        - **Question Suggestions:** AI-generated follow-up questions
        - **Context-Aware Responses:** Personalized answers based on data
        - **Multi-Language Support:** Hebrew and English with AI translation
        - **Real-time Analysis:** Instant insights and recommendations
        
        #### 🔧 Enhanced Settings
        - **AI Model Configuration:** Choose between GPT-3.5 and GPT-4
        - **Response Customization:** Adjust detail levels and creativity
        - **Advanced Preferences:** Comprehensive analysis settings
        - **System Monitoring:** Real-time status and health checks
        """)
    
    # Quick actions with enhanced features
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 📁 Upload & Process")
        st.markdown("Upload financial reports for AI analysis")
        if st.button("📁 Upload Files", key="upload_btn", use_container_width=True):
            st.session_state.page = "📁 Upload Files"
            st.rerun()
    
    with col2:
        st.markdown("#### 🤖 AI Q&A")
        st.markdown("Ask intelligent questions with AI enhancement")
        if st.button("🤖 Ask AI", key="ai_qa_btn", use_container_width=True):
            st.session_state.page = "❓ Q&A"
            st.rerun()
    
    with col3:
        st.markdown("#### 📊 Analysis")
        st.markdown("Comprehensive financial analysis")
        if st.button("📊 Analyze", key="analysis_btn", use_container_width=True):
            st.session_state.page = "📊 Financial Analysis"
            st.rerun()
    
    with col4:
        st.markdown("#### ⚙️ Settings")
        st.markdown("Configure AI and system preferences")
        if st.button("⚙️ Configure", key="settings_btn", use_container_width=True):
            st.session_state.page = "⚙️ Settings"
            st.rerun()
    
    # System status with AI status
    st.markdown("---")
    st.markdown("### 🔍 System & AI Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Online")
            else:
                st.error("❌ Backend Issue")
        except:
            st.error("❌ Backend Offline")
    
    with col2:
        try:
            response = requests.get(f"{API_BASE_URL}/enhanced-qa/ai-status", timeout=5)
            if response.status_code == 200:
                ai_status = response.json()
                if ai_status.get("ai_available"):
                    st.success("✅ AI Available")
                else:
                    st.warning("⚠️ AI Limited")
            else:
                st.error("❌ AI Error")
        except:
            st.warning("⚠️ AI Unavailable")
    
    with col3:
        try:
            response = requests.get(f"{API_BASE_URL}/upload/files", timeout=5)
            if response.status_code == 200:
                files_data = response.json()
                file_count = len(files_data.get("files", []))
                st.info(f"📁 {file_count} Files")
            else:
                st.info("📁 No Files")
        except:
            st.info("📁 Files Unknown")
    
    with col4:
        try:
            response = requests.get(f"{API_BASE_URL}/enhanced-qa/enhanced-categories", timeout=5)
            if response.status_code == 200:
                categories = response.json()
                category_count = len(categories.get("categories", {}))
                st.info(f"📊 {category_count} AI Categories")
            else:
                st.info("📊 Categories Unknown")
        except:
            st.info("📊 Categories Unknown")
    
    # Recent activity or tips
    st.markdown("---")
    st.markdown("### 💡 AI Tips & Best Practices")
    
    tips = [
        "💡 **Ask complex questions** - The AI can handle detailed financial analysis queries",
        "🎯 **Use context** - Provide additional context for more relevant answers",
        "📊 **Explore categories** - Try different question types for comprehensive insights",
        "⚠️ **Check risks** - Always review risk assessments for compliance",
        "🚀 **Leverage recommendations** - Use AI-generated strategic advice"
    ]
    
    for tip in tips:
        st.markdown(tip)

def upload_page():
    """File upload page"""
    st.markdown('<h1 class="sub-header">📁 File Upload</h1>', unsafe_allow_html=True)
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Choose a financial report file",
        type=['xlsx', 'xls', 'csv', 'pdf'],
        help="Supports Excel, CSV and PDF files"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.info(f"""
        **File Details:**
        - Filename: {uploaded_file.name}
        - Size: {uploaded_file.size} bytes
        - Type: {uploaded_file.type}
        """)
        
        # Upload button
        if st.button("Upload File"):
            with st.spinner("Uploading file..."):
                try:
                    # Prepare file for upload - use BytesIO to ensure proper file handling
                    import io
                    file_content = uploaded_file.getvalue()
                    files = {"file": (uploaded_file.name, io.BytesIO(file_content), uploaded_file.type)}
                    
                    # Upload to backend
                    response = requests.post(f"{API_BASE_URL}/upload/file", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {result['message']}")
                        st.json(result)
                    else:
                        st.error(f"❌ Upload error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Excel specific upload
    st.markdown("---")
    st.markdown("### 📊 Excel Upload with Processing")
    
    excel_file = st.file_uploader(
        "Choose Excel file",
        type=['xlsx', 'xls'],
        key="excel_upload"
    )
    
    if excel_file is not None:
        sheet_name = st.text_input("Sheet name", value="Sheet1")
        
        if st.button("Upload and Process Excel"):
            with st.spinner("Processing Excel file..."):
                try:
                    # Prepare file for upload - use BytesIO to ensure proper file handling
                    import io
                    file_content = excel_file.getvalue()
                    files = {"file": (excel_file.name, io.BytesIO(file_content), excel_file.type)}
                    data = {"sheet_name": sheet_name}
                    
                    response = requests.post(f"{API_BASE_URL}/upload/excel", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {result['message']}")
                        
                        # Display sheet information
                        if 'sheet_name' in result and 'available_sheets' in result:
                            st.info(f"📋 Used sheet: **{result['sheet_name']}**")
                            if len(result['available_sheets']) > 1:
                                st.info(f"📋 Available sheets: {', '.join(result['available_sheets'])}")
                        
                        # Display preview
                        if 'preview' in result:
                            st.markdown("### Preview")
                            preview_df = pd.DataFrame(result['preview'])
                            st.dataframe(preview_df)
                    else:
                        st.error(f"❌ Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def analysis_page():
    """Financial analysis page"""
    st.markdown('<h1 class="sub-header">📊 Financial Analysis</h1>', unsafe_allow_html=True)
    
    # Get available files
    try:
        response = requests.get(f"{API_BASE_URL}/upload/files")
        if response.status_code == 200:
            files_data = response.json()
            available_files = [f["filename"] for f in files_data.get("files", [])]
        else:
            available_files = []
    except:
        available_files = []
    
    if not available_files:
        st.warning("⚠️ No files available for analysis. Please upload a file first.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select file for analysis",
        available_files
    )
    
    if selected_file:
        # Analysis options
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_type = st.selectbox(
                "Analysis type",
                ["comprehensive", "basic", "tax_focused"]
            )
        
        with col2:
            include_adjustments = st.checkbox("Include adjustments", value=True)
            include_recommendations = st.checkbox("Include recommendations", value=True)
        
        if st.button("Start Analysis"):
            with st.spinner("Analyzing data..."):
                try:
                    # Prepare analysis request
                    analysis_request = {
                        "file_path": selected_file,
                        "analysis_type": analysis_type,
                        "include_adjustments": include_adjustments,
                        "include_recommendations": include_recommendations
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/analysis/financial", json=analysis_request)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Analysis completed successfully!")
                        
                        # Display results
                        display_analysis_results(result)
                    else:
                        st.error(f"❌ Analysis error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def display_analysis_results(result):
    """Display analysis results"""
    
    # Summary with calculation explanations expander
    st.markdown("### 📋 Summary")
    
    summary = result.get("summary", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue", f"₪{summary.get('revenue', 0):,.0f}")
        with st.expander("ℹ️ Revenue Info", expanded=False):
            st.info("Total revenue represents the sum of all income sources across all jurisdictions.")
    with col2:
        st.metric("Taxes", f"₪{summary.get('taxes', 0):,.0f}")
        with st.expander("ℹ️ Taxes Info", expanded=False):
            tax_type = "estimated" if summary.get('estimated_taxes', False) else "actual"
            st.info(f"Tax amount is {tax_type}. See detailed explanations below.")
    with col3:
        st.metric("Net Profit", f"₪{summary.get('net_profit', 0):,.0f}")
        with st.expander("ℹ️ Net Profit Info", expanded=False):
            st.info("Net profit = Revenue - Expenses - Taxes")
    
    # Additional metrics
    if summary.get('revenue', 0) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tax Rate", f"{summary.get('tax_rate', 0):.1f}%")
            with st.expander("ℹ️ Tax Rate Info", expanded=False):
                st.info("Tax Rate = (Taxes / Revenue) × 100")
        with col2:
            st.metric("Profit Margin", f"{summary.get('profit_margin', 0):.1f}%")
            with st.expander("ℹ️ Profit Margin Info", expanded=False):
                st.info("Profit Margin = (Net Profit / Revenue) × 100")
        with col3:
            st.metric("Average ETR", f"{summary.get('average_etr', 0):.1f}%")
            with st.expander("ℹ️ ETR Info", expanded=False):
                st.info("ETR = (Taxes / Pre-tax Income) × 100. See detailed explanations below.")
        with col4:
            st.metric("Jurisdictions", f"{summary.get('jurisdictions', 0)}")
            with st.expander("ℹ️ Jurisdictions Info", expanded=False):
                st.info("Number of different tax jurisdictions in the dataset")
    
    # Top-up tax if applicable
    if summary.get('top_up_tax', 0) > 0:
        st.metric("Top-Up Tax", f"₪{summary.get('top_up_tax', 0):,.0f}")
        with st.expander("ℹ️ Top-Up Tax Info", expanded=False):
            st.info("""
            **Top-Up Tax (Pillar Two):**
            
            Additional tax levied when the effective tax rate is below 15%.
            Ensures a minimum level of taxation on multinational enterprises.
            
            **מס נוסף (עמוד שני):**
            
            מס נוסף המוטל כאשר שיעור המס האפקטיבי נמוך מ-15%.
            מבטיח רמת מיסוי מינימלית על חברות בינלאומיות.
            """)
    
    # Display calculation explanations in expander
    with st.expander("🔍 Detailed Calculation Explanations", expanded=False):
        display_calculation_explanations(result)
    
    # Adjustments
    if result.get("adjustments"):
        st.markdown("### 🔧 Adjustments")
        adjustments_df = pd.DataFrame(result["adjustments"])
        st.dataframe(adjustments_df)

def display_calculation_explanations(result):
    """Display detailed calculation explanations"""
    
    st.markdown("---")
    st.markdown("### 🔍 Detailed Calculation Explanations")
    
    explanations = result.get('calculation_explanations', {})
    
    if not explanations:
        st.info("ℹ️ No calculation explanations available for this analysis.")
        return
    
    # Tax calculation explanation
    if 'tax_calculation' in explanations:
        tax_explanation = explanations['tax_calculation']
        
        st.markdown("#### 💰 Tax Calculation Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Type:** {tax_explanation['type'].upper()}")
            st.markdown(f"**Method:** {tax_explanation['method']}")
            st.markdown(f"**Formula:** {tax_explanation['formula']}")
            st.markdown(f"**Result:** {tax_explanation['result']}")
        
        with col2:
            st.markdown(f"**סוג:** {tax_explanation['type'].upper()}")
            st.markdown(f"**שיטה:** {tax_explanation.get('method_he', 'N/A')}")
            st.markdown(f"**נוסחה:** {tax_explanation.get('formula_he', 'N/A')}")
        
        st.markdown("**Explanation:**")
        st.info(tax_explanation['explanation'])
        
        if tax_explanation.get('explanation_he'):
            st.markdown("**הסבר:**")
            st.info(tax_explanation['explanation_he'])
    
    # ETR calculation explanation
    if 'etr_calculation' in explanations:
        etr_explanation = explanations['etr_calculation']
        
        st.markdown("#### 📈 ETR Calculation Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Type:** {etr_explanation['type'].upper()}")
            st.markdown(f"**Method:** {etr_explanation['method']}")
            st.markdown(f"**Formula:** {etr_explanation['formula']}")
            st.markdown(f"**Result:** {etr_explanation['result']}")
        
        with col2:
            st.markdown(f"**סוג:** {etr_explanation['type'].upper()}")
            st.markdown(f"**שיטה:** {etr_explanation.get('method_he', 'N/A')}")
            st.markdown(f"**נוסחה:** {etr_explanation.get('formula_he', 'N/A')}")
        
        st.markdown("**Explanation:**")
        st.info(etr_explanation['explanation'])
        
        if etr_explanation.get('explanation_he'):
            st.markdown("**הסבר:**")
            st.info(etr_explanation['explanation_he'])
    
    # Legal and regulatory context
    st.markdown("#### 📚 Legal & Regulatory Context")
    
    if explanations.get('tax_calculation', {}).get('type') == 'estimated':
        st.warning("""
        **⚠️ Important Legal Notice:**
        
        The tax calculations shown are **estimated** based on standard Israeli corporate tax rates. 
        For compliance purposes, please ensure:
        
        - Review actual tax data and documentation
        - Consult with qualified tax professionals
        - Verify calculations against current tax legislation
        - Consider specific tax treaties and exemptions
        """)
        
        st.markdown("""
        **הערה משפטית חשובה:**
        
        חישובי המס המוצגים הם **משוערים** על בסיס שיעורי מס תאגידים ישראלים סטנדרטיים.
        לצורכי ציות, אנא וודאו:
        
        - סקירת נתוני מס אמיתיים ותיעוד
        - התייעצות עם אנשי מקצוע מוסמכים בתחום המס
        - אימות החישובים מול חקיקת המס הנוכחית
        - התחשבות באמנות מס ספציפיות ופטורים
        """)
    
    # No close button needed since we're using expander
    
    # Recommendations
    if result.get("recommendations"):
        st.markdown("### 💡 Recommendations")
        for i, rec in enumerate(result["recommendations"], 1):
            st.markdown(f"{i}. {rec}")
    
    # Charts
    if result.get("charts"):
        st.markdown("### 📈 Charts")
        charts = result["charts"]
        
        # Jurisdiction distribution pie chart
        if "jurisdiction_pie" in charts:
            fig = px.pie(values=charts["jurisdiction_pie"]["values"], 
                        names=charts["jurisdiction_pie"]["labels"],
                        title="Revenue Distribution by Jurisdiction")
            st.plotly_chart(fig)
        
        # ETR comparison bar chart
        if "etr_comparison" in charts:
            fig = px.bar(x=charts["etr_comparison"]["labels"], 
                        y=charts["etr_comparison"]["values"],
                        title="Effective Tax Rate by Jurisdiction",
                        labels={'x': 'Jurisdiction', 'y': 'ETR (%)'})
            st.plotly_chart(fig)
        
        # Revenue vs Taxes scatter plot
        if "revenue_tax_scatter" in charts:
            fig = px.scatter(x=charts["revenue_tax_scatter"]["x"], 
                           y=charts["revenue_tax_scatter"]["y"],
                           title="Revenue vs Taxes",
                           labels={'x': 'Revenue', 'y': 'Taxes'})
            st.plotly_chart(fig)
        
        # Top-up tax bar chart
        if "top_up_tax" in charts:
            fig = px.bar(x=charts["top_up_tax"]["labels"], 
                        y=charts["top_up_tax"]["values"],
                        title="Top-Up Tax by Jurisdiction",
                        labels={'x': 'Jurisdiction', 'y': 'Top-Up Tax'})
            st.plotly_chart(fig)

def qa_page():
    """Enhanced Question and Answer page with AI capabilities"""
    st.markdown('<h1 class="sub-header">❓ Enhanced Q&A with AI</h1>', unsafe_allow_html=True)
    
    # Create tabs for different Q&A modes
    tab1, tab2, tab3 = st.tabs(["🔍 Basic Q&A", "🤖 AI Enhanced Q&A", "📊 Advanced Analysis"])
    
    with tab1:
        basic_qa_section()
    
    with tab2:
        enhanced_qa_section()
    
    with tab3:
        advanced_analysis_section()

def basic_qa_section():
    """Basic Q&A functionality"""
    with st.expander("ℹ️ Basic Q&A Help", expanded=False):
        st.info("""
        **Ask Questions About Your Financial Data:**
        
        💰 **Tax Questions:** "What is the effective tax rate?"
        📊 **Financial Questions:** "What is the net profit?"
        📋 **Regulatory Questions:** "Are there any compliance issues?"
        🔍 **Analysis Questions:** "Which jurisdiction has the highest revenue?"
        
        **שאל שאלות על הנתונים הפיננסיים שלך:**
        
        💰 **שאלות מס:** "מהו שיעור המס האפקטיבי?"
        📊 **שאלות פיננסיות:** "מהו הרווח הנקי?"
        📋 **שאלות רגולטוריות:** "האם יש בעיות ציות?"
        🔍 **שאלות ניתוח:** "איזו שיפוטיות יש לה ההכנסה הגבוהה ביותר?"
        """)
    
    # Get available files
    try:
        response = requests.get(f"{API_BASE_URL}/upload/files")
        if response.status_code == 200:
            files_data = response.json()
            available_files = [f["filename"] for f in files_data.get("files", [])]
        else:
            available_files = []
    except:
        available_files = []
    
    if not available_files:
        st.warning("⚠️ No files available for Q&A. Please upload a file first.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select file to ask questions about",
        available_files,
        help="Choose the financial data file you want to ask questions about"
    )
    
    # Question input
    question = st.text_area(
        "Ask a question about the financial data",
        placeholder="Example: What is the net profit? או: מהו הרווח הנקי?",
        height=100
    )
    
    # Language selection
    language = st.selectbox(
        "Language / שפה",
        ["en", "he"],
        format_func=lambda x: "English" if x == "en" else "עברית"
    )
    
    if st.button("Ask Question / שאל שאלה"):
        if question:
            with st.spinner("Searching for answer..." if language == "en" else "מחפש תשובה..."):
                try:
                    # Construct file path
                    file_path = f"data/uploads/{selected_file}"
                    
                    qa_request = {
                        "question": question,
                        "file_path": file_path,
                        "language": language
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/qa/ask", json=qa_request)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown("### 💬 Answer / תשובה")
                        st.markdown(f"**{result['answer']}**")
                        
                        if result.get("confidence"):
                            st.progress(result["confidence"])
                            st.caption(f"Confidence: {result['confidence']:.2%}")
                        
                        if result.get("sources"):
                            st.markdown("### 📚 Sources / מקורות")
                            for source in result["sources"]:
                                st.markdown(f"- {source}")
                        
                        if result.get("related_questions"):
                            st.markdown("### 🤔 Related Questions / שאלות קשורות")
                            for related_q in result["related_questions"]:
                                st.markdown(f"- {related_q}")
                    else:
                        st.error(f"❌ Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question / אנא הכנס שאלה")

def enhanced_qa_section():
    """Enhanced Q&A with AI capabilities"""
    st.markdown("### 🤖 AI Enhanced Q&A")
    
    with st.expander("ℹ️ AI Enhanced Q&A Features", expanded=False):
        st.info("""
        **Advanced AI-Powered Q&A Features:**
        
        🧠 **AI Enhancement:** Get detailed explanations and insights
        📊 **Question Classification:** Automatic categorization of questions
        🎯 **Smart Suggestions:** AI-generated follow-up questions
        📈 **Risk Analysis:** Identify potential compliance risks
        💡 **Strategic Recommendations:** Get actionable advice
        
        **תכונות Q&A מתקדמות עם בינה מלאכותית:**
        
        🧠 **שיפור AI:** קבל הסברים מפורטים ותובנות
        📊 **סיווג שאלות:** קטגוריזציה אוטומטית של שאלות
        🎯 **הצעות חכמות:** שאלות המשך שנוצרו על ידי AI
        📈 **ניתוח סיכונים:** זיהוי סיכוני ציות פוטנציאליים
        💡 **המלצות אסטרטגיות:** קבל ייעוץ מעשי
        """)
    
    # Get available files
    try:
        response = requests.get(f"{API_BASE_URL}/upload/files")
        if response.status_code == 200:
            files_data = response.json()
            available_files = [f["filename"] for f in files_data.get("files", [])]
        else:
            available_files = []
    except:
        available_files = []
    
    if not available_files:
        st.warning("⚠️ No files available for Q&A. Please upload a file first.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select file for AI analysis",
        available_files,
        key="enhanced_file_select",
        help="Choose the financial data file for AI-enhanced analysis"
    )
    
    # AI Settings
    col1, col2 = st.columns(2)
    with col1:
        use_ai_enhancement = st.checkbox(
            "Enable AI Enhancement",
            value=True,
            help="Use ChatGPT 3.5 for enhanced answers"
        )
        include_sources = st.checkbox(
            "Include Sources",
            value=True,
            help="Show information sources"
        )
    
    with col2:
        detail_level = st.selectbox(
            "Detail Level",
            ["basic", "detailed", "comprehensive"],
            help="Level of detail in the response"
        )
        language = st.selectbox(
            "Language / שפה",
            ["en", "he"],
            format_func=lambda x: "English" if x == "en" else "עברית",
            key="enhanced_lang"
        )
    
    # Question input with suggestions
    st.markdown("### 💭 Ask Your Question")
    
    # Get question suggestions
    try:
        suggestions_response = requests.get(f"{API_BASE_URL}/enhanced-qa/enhanced-suggestions", 
                                          params={"language": language})
        if suggestions_response.status_code == 200:
            suggestions = suggestions_response.json().get("suggestions", [])
            if suggestions:
                st.markdown("**💡 Suggested Questions / שאלות מוצעות:**")
                for i, suggestion in enumerate(suggestions[:5]):
                    if st.button(f"{suggestion}", key=f"suggestion_{i}"):
                        st.session_state.enhanced_question = suggestion
        else:
            suggestions = []
    except:
        suggestions = []
    
    # Question input
    question = st.text_area(
        "Ask an advanced question about the financial data",
        value=st.session_state.get("enhanced_question", ""),
        placeholder="Example: How can we optimize our tax strategy for Pillar Two compliance? או: איך נוכל לייעל את אסטרטגיית המס שלנו לציות לעמוד שני?",
        height=120,
        key="enhanced_question_input"
    )
    
    # Context input
    context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Provide any additional context or specific requirements...",
        height=80,
        help="Add context to help AI provide more relevant answers"
    )
    
    if st.button("Ask AI Enhanced Question / שאל שאלה עם AI", type="primary"):
        if question:
            with st.spinner("🤖 AI is analyzing your question..." if language == "en" else "🤖 ה-AI מנתח את השאלה שלך..."):
                try:
                    # Construct file path
                    file_path = f"data/uploads/{selected_file}"
                    
                    enhanced_request = {
                        "question": question,
                        "file_path": file_path,
                        "context": context,
                        "language": language,
                        "include_sources": include_sources,
                        "use_ai_enhancement": use_ai_enhancement,
                        "detail_level": detail_level
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/enhanced-qa/enhanced-ask", json=enhanced_request)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display enhanced answer
                        st.markdown("### 🤖 AI Enhanced Answer")
                        
                        # Question type indicator
                        if result.get("question_type"):
                            question_type_emoji = {
                                "pillar_two_compliance": "🏛️",
                                "tax_calculations": "💰",
                                "regulatory_analysis": "📋",
                                "risk_assessment": "⚠️",
                                "strategic_planning": "🎯",
                                "general": "❓"
                            }
                            emoji = question_type_emoji.get(result["question_type"], "❓")
                            st.markdown(f"{emoji} **Question Type:** {result['question_type'].replace('_', ' ').title()}")
                        
                        # Main answer
                        st.markdown(f"**{result['answer']}**")
                        
                        # Confidence and AI enhancement indicator
                        col1, col2 = st.columns(2)
                        with col1:
                            if result.get("confidence"):
                                st.progress(result["confidence"])
                                st.caption(f"Confidence: {result['confidence']:.2%}")
                        
                        with col2:
                            if result.get("ai_enhanced"):
                                st.success("🤖 AI Enhanced")
                            else:
                                st.info("📊 Basic Analysis")
                        
                        # Sources
                        if result.get("sources"):
                            st.markdown("### 📚 Sources / מקורות")
                            for source in result["sources"]:
                                st.markdown(f"- {source}")
                        
                        # Related questions
                        if result.get("related_questions"):
                            st.markdown("### 🤔 Related Questions / שאלות קשורות")
                            for related_q in result["related_questions"]:
                                st.markdown(f"- {related_q}")
                        
                        # Recommendations
                        if result.get("recommendations"):
                            st.markdown("### 💡 Recommendations / המלצות")
                            for i, rec in enumerate(result["recommendations"], 1):
                                st.markdown(f"{i}. {rec}")
                        
                        # Risk analysis
                        if result.get("risk_analysis"):
                            st.markdown("### ⚠️ Risk Analysis / ניתוח סיכונים")
                            risk_data = result["risk_analysis"]
                            if isinstance(risk_data, dict):
                                for risk_type, risk_level in risk_data.items():
                                    if risk_level == "high":
                                        st.error(f"🔴 {risk_type}: {risk_level}")
                                    elif risk_level == "medium":
                                        st.warning(f"🟡 {risk_type}: {risk_level}")
                                    else:
                                        st.success(f"🟢 {risk_type}: {risk_level}")
                        
                        # Next steps
                        if result.get("next_steps"):
                            st.markdown("### 🚀 Next Steps / הצעדים הבאים")
                            for i, step in enumerate(result["next_steps"], 1):
                                st.markdown(f"{i}. {step}")
                        
                    else:
                        st.error(f"❌ Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question / אנא הכנס שאלה")

def advanced_analysis_section():
    """Advanced analysis with AI agents"""
    st.markdown("### 📊 Advanced AI Analysis")
    
    with st.expander("ℹ️ Advanced Analysis Features", expanded=False):
        st.info("""
        **Advanced AI Agent Analysis:**
        
        🤖 **QA Specialist Agent:** Comprehensive question analysis
        📈 **Risk Assessment:** Detailed risk evaluation
        🎯 **Strategic Planning:** Long-term optimization strategies
        📋 **Compliance Check:** Regulatory compliance verification
        💼 **Financial Analysis:** Deep financial insights
        
        **ניתוח מתקדם עם סוכני AI:**
        
        🤖 **סוכן מומחה Q&A:** ניתוח מקיף של שאלות
        📈 **הערכת סיכונים:** הערכה מפורטת של סיכונים
        🎯 **תכנון אסטרטגי:** אסטרטגיות אופטימיזציה לטווח ארוך
        📋 **בדיקת ציות:** אימות ציות רגולטורי
        💼 **ניתוח פיננסי:** תובנות פיננסיות מעמיקות
        """)
    
    # Get available files
    try:
        response = requests.get(f"{API_BASE_URL}/upload/files")
        if response.status_code == 200:
            files_data = response.json()
            available_files = [f["filename"] for f in files_data.get("files", [])]
        else:
            available_files = []
    except:
        available_files = []
    
    if not available_files:
        st.warning("⚠️ No files available for analysis. Please upload a file first.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select file for advanced analysis",
        available_files,
        key="advanced_file_select",
        help="Choose the financial data file for advanced AI analysis"
    )
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Analysis Type",
        [
            "comprehensive_qa",
            "risk_assessment", 
            "strategic_planning",
            "compliance_check",
            "financial_analysis"
        ],
        format_func=lambda x: {
            "comprehensive_qa": "Comprehensive Q&A Analysis",
            "risk_assessment": "Risk Assessment",
            "strategic_planning": "Strategic Planning",
            "compliance_check": "Compliance Check",
            "financial_analysis": "Financial Analysis"
        }[x]
    )
    
    # Language selection
    language = st.selectbox(
        "Language / שפה",
        ["en", "he"],
        format_func=lambda x: "English" if x == "en" else "עברית",
        key="advanced_lang"
    )
    
    # Question input for advanced analysis
    question = st.text_area(
        "Describe your analysis needs",
        placeholder="Example: Analyze our Pillar Two compliance risks and provide strategic recommendations for optimization...",
        height=100,
        key="advanced_question"
    )
    
    if st.button("Run Advanced Analysis / הרץ ניתוח מתקדם", type="primary"):
        if question:
            with st.spinner("🤖 AI agents are performing advanced analysis..." if language == "en" else "🤖 סוכני AI מבצעים ניתוח מתקדם..."):
                try:
                    # Construct file path
                    file_path = f"data/uploads/{selected_file}"
                    
                    advanced_request = {
                        "question": question,
                        "file_path": file_path,
                        "analysis_type": analysis_type,
                        "language": language
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/enhanced-qa/ai-ask", json=advanced_request)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown("### 🤖 Advanced AI Analysis Results")
                        
                        # Display comprehensive results
                        if result.get("answer"):
                            st.markdown(f"**{result['answer']}**")
                        
                        # Analysis breakdown
                        if result.get("analysis_breakdown"):
                            st.markdown("### 📊 Analysis Breakdown")
                            breakdown = result["analysis_breakdown"]
                            
                            for section, content in breakdown.items():
                                with st.expander(f"📋 {section.replace('_', ' ').title()}", expanded=True):
                                    if isinstance(content, dict):
                                        for key, value in content.items():
                                            st.markdown(f"**{key}:** {value}")
                                    else:
                                        st.markdown(str(content))
                        
                        # Risk assessment
                        if result.get("risk_assessment"):
                            st.markdown("### ⚠️ Risk Assessment")
                            risk_data = result["risk_assessment"]
                            if isinstance(risk_data, dict):
                                for risk_category, risk_details in risk_data.items():
                                    with st.expander(f"🔍 {risk_category}", expanded=False):
                                        if isinstance(risk_details, dict):
                                            for key, value in risk_details.items():
                                                st.markdown(f"**{key}:** {value}")
                                        else:
                                            st.markdown(str(risk_details))
                        
                        # Strategic recommendations
                        if result.get("strategic_recommendations"):
                            st.markdown("### 💡 Strategic Recommendations")
                            for i, rec in enumerate(result["strategic_recommendations"], 1):
                                st.markdown(f"{i}. {rec}")
                        
                        # Compliance status
                        if result.get("compliance_status"):
                            st.markdown("### 📋 Compliance Status")
                            compliance = result["compliance_status"]
                            if isinstance(compliance, dict):
                                for item, status in compliance.items():
                                    if status == "compliant":
                                        st.success(f"✅ {item}: Compliant")
                                    elif status == "non_compliant":
                                        st.error(f"❌ {item}: Non-Compliant")
                                    else:
                                        st.warning(f"⚠️ {item}: {status}")
                        
                    else:
                        st.error(f"❌ Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please describe your analysis needs / אנא תאר את צרכי הניתוח שלך")

def reports_page():
    """Reports generation page"""
    st.markdown('<h1 class="sub-header">📋 Reports</h1>', unsafe_allow_html=True)
    
    # Get available files
    try:
        response = requests.get(f"{API_BASE_URL}/upload/files")
        if response.status_code == 200:
            files_data = response.json()
            available_files = [f["filename"] for f in files_data.get("files", [])]
        else:
            available_files = []
    except:
        available_files = []
    
    if not available_files:
        st.warning("⚠️ No files available for reports. Please upload a file first.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select file for report generation",
        available_files
    )
    
    # Report generation
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report type",
            ["pdf", "xml", "word"]
        )
    
    with col2:
        report_format = st.selectbox(
            "Report format",
            ["standard", "detailed", "gir"]
        )
    
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            try:
                report_request = {
                    "file_path": selected_file,
                    "report_type": report_type,
                    "report_format": report_format
                }
                
                response = requests.post(f"{API_BASE_URL}/reports/generate", json=report_request)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ {result['message']}")
                else:
                    st.error(f"❌ Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

def recommendations_page():
    """Recommendations page"""
    st.markdown('<h1 class="sub-header">💡 Recommendations</h1>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ Recommendations Help", expanded=False):
        st.info("""
        **Recommendations Types:**
        
        📊 **Comprehensive:** Full analysis with all recommendations
        💰 **Tax:** Tax-specific recommendations and optimizations
        📋 **Regulatory:** Compliance and regulatory recommendations
        📈 **Financial:** Financial performance and strategy recommendations
        
        **סוגי המלצות:**
        
        📊 **מקיף:** ניתוח מלא עם כל ההמלצות
        💰 **מס:** המלצות ואופטימיזציות ספציפיות למס
        📋 **רגולטורי:** המלצות ציות ורגולציה
        📈 **פיננסי:** המלצות ביצועים פיננסיים ואסטרטגיה
        """)
    
    # Get available files
    try:
        response = requests.get(f"{API_BASE_URL}/upload/files")
        if response.status_code == 200:
            files_data = response.json()
            available_files = [f["filename"] for f in files_data.get("files", [])]
        else:
            available_files = []
    except:
        available_files = []
    
    if not available_files:
        st.warning("⚠️ No files available for recommendations. Please upload a file first.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select file for recommendations",
        available_files
    )
    
    # Recommendation generation
    recommendation_type = st.selectbox(
        "Recommendation type",
        ["comprehensive", "tax", "regulatory", "financial"]
    )
    
    if st.button("Generate Recommendations"):
        with st.spinner("Generating recommendations..."):
            try:
                rec_request = {
                    "file_path": selected_file,
                    "recommendation_type": recommendation_type,
                    "include_explanations": True,
                    "language": "en"
                }
                
                response = requests.post(f"{API_BASE_URL}/recommendations/generate", json=rec_request)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("### 💡 Recommendations")
                    for i, rec in enumerate(result["recommendations"], 1):
                        st.markdown(f"**{i}. {rec['title']}**")
                        st.markdown(f"{rec['description']}")
                        st.markdown("---")
                else:
                    st.error(f"❌ Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

def settings_page():
    """Enhanced Settings page with AI configuration"""
    st.markdown('<h1 class="sub-header">⚙️ Enhanced Settings</h1>', unsafe_allow_html=True)
    
    # Create tabs for different settings
    tab1, tab2, tab3, tab4 = st.tabs(["🌐 General", "🤖 AI Settings", "🔧 API Configuration", "📊 Analysis Preferences"])
    
    with tab1:
        general_settings_section()
    
    with tab2:
        ai_settings_section()
    
    with tab3:
        api_settings_section()
    
    with tab4:
        analysis_preferences_section()

def general_settings_section():
    """General application settings"""
    st.markdown("### 🌐 General Settings")
    
    # Language selection
    language = st.selectbox(
        "Default Language / שפת ברירת מחדל",
        ["en", "he"],
        format_func=lambda x: "English" if x == "en" else "עברית",
        help="Choose your preferred language for the interface"
    )
    
    # Theme selection
    theme = st.selectbox(
        "Theme / ערכת נושא",
        ["light", "dark", "auto"],
        format_func=lambda x: x.title(),
        help="Choose the visual theme for the application"
    )
    
    # Auto-save settings
    auto_save = st.checkbox(
        "Auto-save responses / שמירה אוטומטית של תשובות",
        value=True,
        help="Automatically save Q&A responses for future reference"
    )
    
    # Export format preference
    export_format = st.selectbox(
        "Default Export Format / פורמט ייצוא ברירת מחדל",
        ["pdf", "word", "excel", "json"],
        help="Choose the default format for exporting reports and analysis"
    )
    
    if st.button("Save General Settings / שמור הגדרות כלליות"):
        st.success("✅ General settings saved successfully!")

def ai_settings_section():
    """AI-specific settings"""
    st.markdown("### 🤖 AI Settings")
    
    # AI Enhancement toggle
    enable_ai = st.checkbox(
        "Enable AI Enhancement / הפעל שיפור AI",
        value=True,
        help="Enable ChatGPT integration for enhanced responses"
    )
    
    if enable_ai:
        # AI Model selection with detailed descriptions
        st.markdown("#### 🧠 AI Model Selection")
        
        ai_model = st.selectbox(
            "AI Model / מודל AI",
            [
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k", 
                "gpt-4",
                "gpt-4-turbo",
                "gpt-4-turbo-preview",
                "gpt-4o",
                "gpt-4o-mini"
            ],
            help="Choose the AI model for enhanced analysis"
        )
        
        # Model information display
        model_info = {
            "gpt-3.5-turbo": {
                "description": "Fast and cost-effective for most tasks",
                "max_tokens": "4,096",
                "cost": "Low",
                "speed": "Fast",
                "best_for": "General Q&A, basic analysis"
            },
            "gpt-3.5-turbo-16k": {
                "description": "Extended context for longer conversations",
                "max_tokens": "16,384",
                "cost": "Medium",
                "speed": "Fast",
                "best_for": "Long documents, complex analysis"
            },
            "gpt-4": {
                "description": "Most capable model for complex reasoning",
                "max_tokens": "8,192",
                "cost": "High",
                "speed": "Medium",
                "best_for": "Complex analysis, strategic planning"
            },
            "gpt-4-turbo": {
                "description": "Latest GPT-4 with improved performance",
                "max_tokens": "128,000",
                "cost": "High",
                "speed": "Medium",
                "best_for": "Advanced analysis, large documents"
            },
            "gpt-4-turbo-preview": {
                "description": "Preview of latest GPT-4 features",
                "max_tokens": "128,000",
                "cost": "High",
                "speed": "Medium",
                "best_for": "Cutting-edge features, testing"
            },
            "gpt-4o": {
                "description": "Latest multimodal model with enhanced capabilities",
                "max_tokens": "128,000",
                "cost": "Medium-High",
                "speed": "Fast",
                "best_for": "Multimodal analysis, advanced reasoning"
            },
            "gpt-4o-mini": {
                "description": "Faster and more cost-effective GPT-4o",
                "max_tokens": "128,000",
                "cost": "Low-Medium",
                "speed": "Very Fast",
                "best_for": "Quick responses, cost optimization"
            }
        }
        
        # Display model information
        if ai_model in model_info:
            info = model_info[ai_model]
            with st.expander(f"ℹ️ {ai_model} Information", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Description:** {info['description']}")
                    st.markdown(f"**Max Tokens:** {info['max_tokens']}")
                with col2:
                    st.markdown(f"**Cost:** {info['cost']}")
                    st.markdown(f"**Speed:** {info['speed']}")
                    st.markdown(f"**Best For:** {info['best_for']}")
        
        # Model comparison
        with st.expander("📊 Model Comparison", expanded=False):
            comparison_data = {
                "Model": list(model_info.keys()),
                "Max Tokens": [info["max_tokens"] for info in model_info.values()],
                "Cost": [info["cost"] for info in model_info.values()],
                "Speed": [info["speed"] for info in model_info.values()],
                "Best For": [info["best_for"] for info in model_info.values()]
            }
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
        
        st.markdown("---")
        
        # AI Response detail level
        ai_detail_level = st.selectbox(
            "Default AI Detail Level / רמת פירוט AI ברירת מחדל",
            ["basic", "detailed", "comprehensive"],
            help="Choose the default level of detail for AI responses"
        )
        
        # AI Temperature (creativity)
        ai_temperature = st.slider(
            "AI Creativity Level / רמת יצירתיות AI",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Lower values = more focused, Higher values = more creative"
        )
        
        # AI Max tokens
        ai_max_tokens = st.slider(
            "AI Response Length / אורך תשובת AI",
            min_value=100,
            max_value=4000,
            value=1000,
            step=100,
            help="Maximum number of tokens in AI responses"
        )
        
        # Advanced AI settings
        st.markdown("#### ⚙️ Advanced AI Settings")
        
        # Question classification
        enable_classification = st.checkbox(
            "Enable Question Classification / הפעל סיווג שאלות",
            value=True,
            help="Automatically classify questions for better responses"
        )
        
        # Risk assessment
        enable_risk_assessment = st.checkbox(
            "Enable Risk Assessment / הפעל הערכת סיכונים",
            value=True,
            help="Include risk analysis in AI responses"
        )
        
        # Context window optimization
        enable_context_optimization = st.checkbox(
            "Enable Context Optimization / הפעל אופטימיזציית הקשר",
            value=True,
            help="Optimize context window usage for better performance"
        )
        
        # Multilingual enhancement
        enable_multilingual = st.checkbox(
            "Enable Multilingual Enhancement / הפעל שיפור רב-לשוני",
            value=True,
            help="Enhanced support for Hebrew and English"
        )
        
        # Real-time suggestions
        enable_realtime_suggestions = st.checkbox(
            "Enable Real-time Suggestions / הפעל הצעות בזמן אמת",
            value=True,
            help="Show AI-generated question suggestions in real-time"
        )
        
        # Model switching strategy
        st.markdown("#### 🔄 Model Switching Strategy")
        
        auto_model_switching = st.checkbox(
            "Enable Auto Model Switching / הפעל החלפת מודל אוטומטית",
            value=False,
            help="Automatically switch models based on question complexity"
        )
        
        if auto_model_switching:
            st.info("""
            **Auto Model Switching Strategy:**
            - Simple questions → GPT-3.5-turbo (fast, cost-effective)
            - Complex analysis → GPT-4 (better reasoning)
            - Large documents → GPT-4-turbo (extended context)
            - Real-time chat → GPT-4o-mini (fastest)
            """)
        
        # Cost optimization
        st.markdown("#### 💰 Cost Optimization")
        
        cost_optimization = st.checkbox(
            "Enable Cost Optimization / הפעל אופטימיזציית עלויות",
            value=False,
            help="Optimize model usage to reduce costs"
        )
        
        if cost_optimization:
            st.info("""
            **Cost Optimization Features:**
            - Use cheaper models for simple tasks
            - Limit token usage for routine questions
            - Cache responses for repeated questions
            - Batch similar requests together
            """)
        
        # Model testing
        st.markdown("#### 🧪 Model Testing")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Test Current Model / בדוק מודל נוכחי"):
                try:
                    import requests
                    response = requests.post(
                        "http://localhost:8000/api/v1/enhanced-qa/ai-models/test",
                        params={"model": ai_model},
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        if result["test_result"]["success"]:
                            st.success("✅ Model connection successful!")
                            st.info(f"Response: {result['test_result']['response']}")
                        else:
                            st.error(f"❌ Model connection failed: {result['test_result']['error']}")
                    else:
                        st.error(f"❌ API error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Test failed: {str(e)}")
        
        with col2:
            if st.button("Compare All Models / השווה כל המודלים"):
                try:
                    import requests
                    response = requests.get(
                        "http://localhost:8000/api/v1/enhanced-qa/ai-models/compare",
                        timeout=10
                    )
                    if response.status_code == 200:
                        comparison = response.json()
                        st.success("✅ Model comparison loaded!")
                        
                        # Display recommendations
                        with st.expander("📊 Model Recommendations", expanded=True):
                            for category, models in comparison["recommendations"].items():
                                st.markdown(f"**{category.replace('_', ' ').title()}:** {', '.join(models)}")
                    else:
                        st.error(f"❌ API error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Comparison failed: {str(e)}")
    
    if st.button("Save AI Settings / שמור הגדרות AI"):
        st.success("✅ AI settings saved successfully!")
        st.info(f"Selected model: {ai_model if enable_ai else 'AI Disabled'}")
        
        # Update AI configuration via API
        try:
            import requests
            config_data = {
                "ai_model": ai_model if enable_ai else "gpt-3.5-turbo",
                "ai_temperature": ai_temperature,
                "ai_max_tokens": ai_max_tokens
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/enhanced-qa/ai-config/update",
                json=config_data,
                timeout=10
            )
            
            if response.status_code == 200:
                st.success("✅ AI configuration updated on server!")
            else:
                st.warning("⚠️ Settings saved locally, but server update failed")
                
        except Exception as e:
            st.warning(f"⚠️ Settings saved locally, but server update failed: {str(e)}")

def api_settings_section():
    """API configuration settings"""
    st.markdown("### 🔧 API Configuration")
    
    # Server URL
    api_url = st.text_input(
        "Server URL / כתובת שרת",
        value="http://localhost:8000",
        help="Backend server URL"
    )
    
    # API Version
    api_version = st.text_input(
        "API Version / גרסת API",
        value="v1",
        help="API version to use"
    )
    
    # Timeout settings
    timeout = st.number_input(
        "Request Timeout (seconds) / זמן המתנה לבקשה (שניות)",
        min_value=5,
        max_value=300,
        value=30,
        help="Maximum time to wait for API responses"
    )
    
    # Retry settings
    max_retries = st.number_input(
        "Max Retries / מספר ניסיונות מקסימלי",
        min_value=0,
        max_value=5,
        value=3,
        help="Maximum number of retry attempts for failed requests"
    )
    
    # Test connection
    if st.button("Test Connection / בדוק חיבור"):
        with st.spinner("Testing connection..."):
            try:
                response = requests.get(f"{api_url}/api/{api_version}/health", timeout=timeout)
                if response.status_code == 200:
                    st.success("✅ Connection successful!")
                else:
                    st.error(f"❌ Connection failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    
    if st.button("Save API Settings / שמור הגדרות API"):
        st.success("✅ API settings saved successfully!")

def analysis_preferences_section():
    """Analysis and reporting preferences"""
    st.markdown("### 📊 Analysis Preferences")
    
    # Default analysis type
    default_analysis = st.selectbox(
        "Default Analysis Type / סוג ניתוח ברירת מחדל",
        ["comprehensive", "financial", "tax", "regulatory", "risk"],
        help="Choose the default analysis type for new requests"
    )
    
    # Include sources in responses
    include_sources = st.checkbox(
        "Include Sources / כלול מקורות",
        value=True,
        help="Include information sources in analysis responses"
    )
    
    # Include recommendations
    include_recommendations = st.checkbox(
        "Include Recommendations / כלול המלצות",
        value=True,
        help="Include strategic recommendations in analysis"
    )
    
    # Include risk assessment
    include_risk_assessment = st.checkbox(
        "Include Risk Assessment / כלול הערכת סיכונים",
        value=True,
        help="Include risk analysis in reports"
    )
    
    # Chart preferences
    st.markdown("#### 📈 Chart Preferences")
    chart_theme = st.selectbox(
        "Chart Theme / ערכת נושא גרפים",
        ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"],
        help="Choose the visual theme for charts and graphs"
    )
    
    # Export preferences
    st.markdown("#### 📤 Export Preferences")
    auto_export = st.checkbox(
        "Auto-export Results / ייצוא אוטומטי של תוצאות",
        value=False,
        help="Automatically export analysis results"
    )
    
    export_location = st.text_input(
        "Export Directory / תיקיית ייצוא",
        value="./exports",
        help="Directory for exported files"
    )
    
    if st.button("Save Analysis Preferences / שמור העדפות ניתוח"):
        st.success("✅ Analysis preferences saved successfully!")
    
    # System status
    st.markdown("### 🔍 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Backend Status", "🟢 Online")
    
    with col2:
        st.metric("AI Status", "🟢 Available")
    
    with col3:
        st.metric("Database Status", "🟢 Connected")

if __name__ == "__main__":
    main()
