import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import altair as alt
from datetime import datetime
import json
import sys
import os

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

# Import our custom modules
try:
    from report_generator import PillarTwoReportGenerator
    from yaml_crew_loader import (
        load_crew_from_yaml, 
        run_pillar_two_analysis, 
        load_tasks_from_yaml,
        get_available_workflows,
        run_workflow
    )
except ImportError:
    st.error("Could not import required modules. Please ensure all agent files are in the correct location.")
    st.stop()

# Configure page
st.set_page_config(
    page_title="GIR Report Generator - Pillar Two",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for English support
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'entities' not in st.session_state:
    st.session_state.entities = []
if 'adjustments' not in st.session_state:
    st.session_state.adjustments = []
if 'generated_xml' not in st.session_state:
    st.session_state.generated_xml = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Tax account types dictionary
account_types = {
    "Representation Expenses": {"classification": "Non-deductible expense", "section": "32(1)"},
    "Penalties": {"classification": "Non-deductible expense", "section": "32(8)"},
    "Vehicle Expenses": {"classification": "Limited expense", "section": "31(a)"},
    "Salary Expenses": {"classification": "Deductible expense", "section": "17"},
    "Interest Income": {"classification": "Additional income", "section": "2(4)"},
    "Depreciation Expenses": {"classification": "Deductible expense", "section": "21"},
    "Private Expenses": {"classification": "Non-deductible expense", "section": "32(11)"}
}

def main():
    st.markdown('<h1 class="main-header">🧾 GIR Report Generator according to Pillar Two</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Select page:",
        ["🏢 Company Details", "📊 Financial Analysis", "🔧 Tax Adjustments", "📈 Charts and Analysis", "📤 XML Generation", "🤖 AI Analysis", "📄 Reports"]
    )
    
    if page == "🏢 Company Details":
        company_details_page()
    elif page == "📊 Financial Analysis":
        financial_analysis_page()
    elif page == "🔧 Tax Adjustments":
        tax_adjustments_page()
    elif page == "📈 Charts and Analysis":
        charts_analysis_page()
    elif page == "📤 XML Generation":
        xml_generation_page()
    elif page == "🤖 AI Analysis":
        ai_analysis_page()
    elif page == "📄 Reports":
        reports_page()

def company_details_page():
    st.markdown('<h2 class="section-header">🏢 Reporting Company Details</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", key="company_name")
        entity_id = st.text_input("Entity ID / Tax ID", key="entity_id")
        jurisdiction = st.selectbox("Country", ["IE", "NL", "US", "IL", "CH"], key="jurisdiction")
    
    with col2:
        business_sector = st.selectbox("Business Sector", ["Technology", "Finance", "Insurance", "Industry", "Services"], key="business_sector")
        reporting_year = st.number_input("Reporting Year", min_value=2024, max_value=2030, value=2025, key="reporting_year")
    
    st.markdown('<h3 class="section-header">📅 Reporting Period</h3>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        start_date = st.date_input("Start Date", key="start_date")
    with col4:
        end_date = st.date_input("End Date", key="end_date")
    
    # Store in session state
    st.session_state.company_info = {
        "name": company_name,
        "entity_id": entity_id,
        "jurisdiction": jurisdiction,
        "business_sector": business_sector,
        "reporting_year": reporting_year,
        "start_date": start_date,
        "end_date": end_date
    }

def financial_analysis_page():
    st.markdown('<h2 class="section-header">📊 Financial Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">🏢 Subsidiary Entities</h3>', unsafe_allow_html=True)
    
    num_entities = st.number_input("How many subsidiaries?", min_value=1, max_value=10, step=1, key="num_entities")
    
    entities = []
    
    for i in range(num_entities):
        st.subheader(f"Company {i+1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(f"Company Name {i+1}", key=f"name_{i}")
            country = st.selectbox(f"Country {i+1}", ["IE", "NL", "US", "IL", "CH"], key=f"country_{i}")
            revenue = st.number_input(f"Revenue (€) {i+1}", min_value=0, key=f"rev_{i}")
        
        with col2:
            profit = st.number_input(f"Profit before tax (€) {i+1}", min_value=0, key=f"profit_{i}")
            tax = st.number_input(f"Tax paid (€) {i+1}", min_value=0, key=f"tax_{i}")
            qualified = st.selectbox(f"Qualified Status {i+1}", ["Yes", "No"], key=f"qual_{i}")
        
        # Calculate ETR and Top-Up Tax
        etr = round((tax / profit) * 100, 2) if profit and profit > 0 else 0
        topup = round(max(0, (0.15 * profit) - tax), 2) if profit else 0
        
        # Display metrics
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric("ETR", f"{etr}%")
        
        with col4:
            st.metric("Top-Up Tax", f"€{topup:,.0f}")
        
        with col5:
            status_color = "🟢" if etr >= 15.0 else "🔴"
            st.metric("Status", f"{status_color} {'Above threshold' if etr >= 15.0 else 'Below threshold'}")
        
        entities.append({
            "name": name,
            "country": country,
            "revenue": revenue,
            "profit": profit,
            "tax": tax,
            "etr": etr,
            "topup": topup,
            "qualified": qualified
        })
    
    st.session_state.entities = entities
    
    # Summary metrics
    if entities:
        total_profit = sum(e["profit"] for e in entities)
        total_tax = sum(e["tax"] for e in entities)
        total_topup = sum(e["topup"] for e in entities)
        avg_etr = (total_tax / total_profit * 100) if total_profit > 0 else 0
        
        st.markdown('<h3 class="section-header">📊 General Summary</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Profit", f"€{total_profit:,.0f}")
        
        with col2:
            st.metric("Total Tax", f"€{total_tax:,.0f}")
        
        with col3:
            st.metric("Average ETR", f"{avg_etr:.2f}%")
        
        with col4:
            st.metric("Total Top-Up", f"€{total_topup:,.0f}")

def tax_adjustments_page():
    st.markdown('<h2 class="section-header">🔧 Tax Adjustments to Accounting Profit</h2>', unsafe_allow_html=True)
    
    st.info("Tax adjustments are differences between accounting profit and profit for tax purposes")
    
    # Initialize adjustments list in session state if not exists
    if 'adjustments_list' not in st.session_state:
        st.session_state.adjustments_list = []
    
    # Method 1: Manual entry
    st.markdown('<h3 class="section-header">📝 Manual Entry</h3>', unsafe_allow_html=True)
    
    num_adj = st.number_input("How many adjustments?", min_value=0, max_value=20, step=1, key="num_adjustments")
    
    adjustments = []
    
    for j in range(num_adj):
        st.subheader(f"Adjustment {j+1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            desc = st.text_input(f"Adjustment description {j+1}", key=f"desc_{j}")
            amount = st.number_input(f"Amount (€) {j+1}", key=f"amt_{j}")
        
        with col2:
            adj_type = st.selectbox(
                f"Adjustment type {j+1}", 
                list(account_types.keys()),
                key=f"type_{j}"
            )
            
            # Show classification info
            if adj_type in account_types:
                info = account_types[adj_type]
                st.info(f"Classification: {info['classification']}, Section: {info['section']}")
        
        adjustments.append({
            "desc": desc, 
            "amount": amount, 
            "type": adj_type,
            "classification": account_types.get(adj_type, {}).get("classification", "Not defined")
        })
    
    # Method 2: Account type selection
    st.markdown('<h3 class="section-header">🧮 Adjustments by Account Type</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_account = st.selectbox("Select account type", list(account_types.keys()), key="selected_account")
        amount = st.number_input("Adjustment amount (€)", key="selected_amount")
    
    with col2:
        classification = account_types[selected_account]["classification"]
        section = account_types[selected_account]["section"]
        
        st.write(f"📌 Tax classification: {classification}")
        st.write(f"📘 Section in ordinance: {section}")
    
    if st.button("➕ Add adjustment", key="add_adjustment"):
        st.session_state.adjustments_list.append({
            "desc": selected_account,
            "amount": amount if classification != "Non-deductible expense" else -amount,
            "type": classification,
            "section": section
        })
        st.success(f"✅ Added adjustment: {selected_account} - €{amount:,.0f}")
    
    # Display current adjustments
    if st.session_state.adjustments_list:
        st.markdown('<h4>Adjustments you added:</h4>', unsafe_allow_html=True)
        
        for i, adj in enumerate(st.session_state.adjustments_list):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{adj['desc']}**")
            with col2:
                st.write(f"€{adj['amount']:,.0f}")
            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.adjustments_list.pop(i)
                    st.rerun()
    
    # Combine both methods
    all_adjustments = adjustments + st.session_state.adjustments_list
    st.session_state.adjustments = all_adjustments
    
    # Calculate adjusted profit
    if adjustments and st.session_state.entities:
        total_profit = sum(e["profit"] for e in st.session_state.entities)
        
        # Calculate adjustments impact
        total_adjustments = 0
        for adj in adjustments:
            if adj["classification"] == "Non-deductible expense":
                total_adjustments -= adj["amount"]  # Add back to profit
            elif adj["classification"] == "Additional income":
                total_adjustments += adj["amount"]  # Add to profit
            # Deductible expense and Limited expense don't affect profit for tax purposes
        
        taxable_income = total_profit + total_adjustments
        
        st.markdown('<h3 class="section-header">📌 Adjustment Summary</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Accounting Profit", f"€{total_profit:,.0f}")
        
        with col2:
            st.metric("Total Adjustments", f"€{total_adjustments:,.0f}")
        
        with col3:
            st.metric("Profit for Tax Purposes", f"€{taxable_income:,.0f}")

def charts_analysis_page():
    st.markdown('<h2 class="section-header">📈 Charts and Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.entities:
        st.warning("Please enter financial data in the 'Financial Analysis' page")
        return
    
    df = pd.DataFrame(st.session_state.entities)
    
    # ETR Chart
    st.markdown('<h3 class="section-header">📊 Effective Tax Rate (ETR) Chart by Company</h3>', unsafe_allow_html=True)
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("name", title="Company Name"),
        y=alt.Y("etr", title="Effective Tax Rate (%)"),
        color=alt.Color("qualified", title="Qualified Status")
    ).properties(
        width=600,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Top-Up Tax Chart
    st.markdown('<h3 class="section-header">💰 Top-Up Tax Chart by Company</h3>', unsafe_allow_html=True)
    
    topup_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("name", title="Company Name"),
        y=alt.Y("topup", title="Top-Up Tax (€)"),
        color=alt.condition(
            alt.datum.topup > 0,
            alt.value("red"),
            alt.value("green")
        )
    ).properties(
        width=600,
        height=400
    )
    
    st.altair_chart(topup_chart, use_container_width=True)
    
    # Tax Adjustments Chart
    if st.session_state.adjustments:
        st.markdown('<h3 class="section-header">🔧 Impact of Tax Adjustments</h3>', unsafe_allow_html=True)
        
        adj_df = pd.DataFrame(st.session_state.adjustments)
        
        # Create adjustment impact chart
        adj_chart = alt.Chart(adj_df).mark_bar().encode(
            x="desc",
            y="amount",
            color="type"
        ).properties(
            title="Impact of Tax Adjustments on Profit",
            width=600,
            height=400
        )
        
        st.altair_chart(adj_chart, use_container_width=True)
        
        # Section-based chart
        if any('section' in adj for adj in st.session_state.adjustments):
            st.markdown('<h4>📊 Adjustments by Income Tax Ordinance Sections</h4>', unsafe_allow_html=True)
            
            section_chart = alt.Chart(adj_df).mark_bar().encode(
                x="section",
                y="amount",
                color="type"
            ).properties(
                title="Adjustments by Income Tax Ordinance Sections",
                width=600,
                height=400
            )
            
            st.altair_chart(section_chart, use_container_width=True)
        
        # Summary table
        st.markdown('<h4>Adjustment Summary</h4>', unsafe_allow_html=True)
        
        summary_data = []
        for adj in st.session_state.adjustments:
            impact = "Add to profit" if adj.get("classification") == "Additional income" else "Subtract from profit"
            summary_data.append({
                "Description": adj["desc"],
                "Amount": f"€{adj['amount']:,.0f}",
                "Classification": adj.get("classification", adj.get("type", "Not defined")),
                "Impact": impact
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)

def xml_generation_page():
    st.markdown('<h2 class="section-header">📤 Generate GIR XML File</h2>', unsafe_allow_html=True)
    
    if not st.session_state.entities:
        st.warning("Please enter financial data in the 'Financial Analysis' page")
        return
    
    if st.button("📤 Generate XML File", type="primary"):
        try:
            # Create XML structure
            root = ET.Element("GIRSubmission")
            root.set("xmlns", "http://oecd.org/pillar2/gir")
            
            # Filing Entity
            filing = ET.SubElement(root, "FilingEntity")
            ET.SubElement(filing, "EntityName").text = st.session_state.get('company_info', {}).get('name', 'Unknown')
            ET.SubElement(filing, "EntityID").text = st.session_state.get('company_info', {}).get('entity_id', 'Unknown')
            ET.SubElement(filing, "Jurisdiction").text = st.session_state.get('company_info', {}).get('jurisdiction', 'Unknown')
            
            # Reporting Period
            period = ET.SubElement(root, "ReportingPeriod")
            ET.SubElement(period, "StartDate").text = str(st.session_state.get('company_info', {}).get('start_date', '2025-01-01'))
            ET.SubElement(period, "EndDate").text = str(st.session_state.get('company_info', {}).get('end_date', '2025-12-31'))
            
            # Constituent Entities
            ce = ET.SubElement(root, "ConstituentEntities")
            
            total_profit = 0
            total_taxes = 0
            total_topup = 0
            
            for e in st.session_state.entities:
                ent = ET.SubElement(ce, "Entity")
                ET.SubElement(ent, "EntityName").text = e["name"]
                ET.SubElement(ent, "Jurisdiction").text = e["country"]
                
                fd = ET.SubElement(ent, "FinancialData")
                ET.SubElement(fd, "Revenue").text = str(e["revenue"])
                ET.SubElement(fd, "ProfitBeforeTax").text = str(e["profit"])
                ET.SubElement(fd, "CoveredTaxes").text = str(e["tax"])
                
                ET.SubElement(ent, "ETR").text = str(e["etr"])
                ET.SubElement(ent, "TopUpTax").text = str(e["topup"])
                ET.SubElement(ent, "QualifiedStatus").text = e["qualified"]
                
                total_profit += e["profit"]
                total_taxes += e["tax"]
                total_topup += e["topup"]
            
            # Summary
            summary = ET.SubElement(root, "Summary")
            ET.SubElement(summary, "TotalTopUpTax").text = str(total_topup)
            ET.SubElement(summary, "TotalCoveredTaxes").text = str(total_taxes)
            ET.SubElement(summary, "TotalProfit").text = str(total_profit)
            
            xml_str = ET.tostring(root, encoding="unicode")
            st.session_state.generated_xml = xml_str
            
            st.success("✅ XML file generated successfully!")
            
            # Display XML preview
            with st.expander("👀 XML Preview"):
                st.code(xml_str, language="xml")
            
            # Download button
            st.download_button(
                "📥 Download XML File",
                xml_str,
                file_name="gir_report.xml",
                mime="application/xml"
            )
            
        except Exception as e:
            st.error(f"Error generating XML: {str(e)}")

def ai_analysis_page():
    st.markdown('<h2 class="section-header">🤖 AI Analysis with CrewAI</h2>', unsafe_allow_html=True)
    
    # YAML Configuration Section
    st.markdown('<h3 class="section-header">⚙️ YAML Settings</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        use_yaml = st.checkbox("Use YAML file", value=True, key="use_yaml")
        yaml_path = st.text_input("YAML file path", value="agents/crew_config.yaml", key="yaml_path")
        tasks_path = st.text_input("Tasks file path", value="agents/tasks_config.yaml", key="tasks_path")
    
    with col2:
        if st.button("📋 Show YAML Settings", key="show_yaml"):
            try:
                with open(yaml_path, 'r', encoding='utf-8') as file:
                    yaml_content = file.read()
                st.code(yaml_content, language="yaml")
            except Exception as e:
                st.error(f"Error reading YAML file: {str(e)}")
        
        if st.button("📋 Show Tasks Settings", key="show_tasks"):
            try:
                with open(tasks_path, 'r', encoding='utf-8') as file:
                    tasks_content = file.read()
                st.code(tasks_content, language="yaml")
            except Exception as e:
                st.error(f"Error reading tasks file: {str(e)}")
    
    # Workflow Selection
    st.markdown('<h4>🔄 Workflow Selection</h4>', unsafe_allow_html=True)
    
    try:
        available_workflows = get_available_workflows(tasks_path)
        selected_workflow = st.selectbox(
            "Select Workflow:",
            available_workflows,
            key="selected_workflow"
        )
        
        if selected_workflow:
            tasks_config = load_tasks_from_yaml(tasks_path)
            workflow_info = tasks_config.get('workflows', {}).get(selected_workflow, {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Name:** {workflow_info.get('name', selected_workflow)}")
            with col2:
                st.write(f"**Estimated Duration:** {workflow_info.get('estimated_duration', 'Unknown')}")
            with col3:
                st.write(f"**Tasks:** {len(workflow_info.get('tasks', []))}")
            
            st.write(f"**Description:** {workflow_info.get('description', '')}")
            
    except Exception as e:
        st.warning(f"Cannot load workflows: {str(e)}")
        selected_workflow = None
    
    # AI Analysis Section
    st.markdown('<h3 class="section-header">🚀 AI Analysis</h3>', unsafe_allow_html=True)
    
    if not st.session_state.generated_xml:
        st.warning("Please generate an XML file in the 'XML Generation' page before running AI analysis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Run Report Analysis", type="primary", key="run_reports"):
            with st.spinner("Running report analysis..."):
                try:
                    # Initialize report generator
                    generator = PillarTwoReportGenerator()
                    
                    # Generate reports
                    executive_report = generator.generate_executive_report(st.session_state.generated_xml)
                    detailed_report = generator.generate_detailed_report(st.session_state.generated_xml)
                    validation_report = generator.generate_validation_report(st.session_state.generated_xml)
                    
                    st.session_state.analysis_results = {
                        "executive": executive_report,
                        "detailed": detailed_report,
                        "validation": validation_report
                    }
                    
                    st.success("✅ Report analysis completed successfully!")
                    
                except Exception as e:
                    st.error(f"Error in report analysis: {str(e)}")
    
    with col2:
        if st.button("🤖 Run CrewAI", type="primary", key="run_crewai"):
            with st.spinner("Running CrewAI..."):
                try:
                    if use_yaml:
                        # Use YAML configuration
                        result = run_pillar_two_analysis(st.session_state.generated_xml, yaml_path)
                    else:
                        # Use default configuration
                        result = run_pillar_two_analysis(st.session_state.generated_xml)
                    
                    if result["success"]:
                        st.session_state.crewai_result = result
                        st.success("✅ CrewAI analysis completed successfully!")
                    else:
                        st.error(f"Error in CrewAI analysis: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"Error in CrewAI analysis: {str(e)}")
    
    # Workflow Execution
    if selected_workflow:
        st.markdown('<h4>🚀 Workflow Execution</h4>', unsafe_allow_html=True)
        
        if st.button(f"▶️ Run {selected_workflow}", type="primary", key="run_workflow"):
            with st.spinner(f"Running {selected_workflow}..."):
                try:
                    result = run_workflow(
                        selected_workflow,
                        st.session_state.generated_xml,
                        yaml_path,
                        tasks_path
                    )
                    
                    if result["success"]:
                        st.session_state.workflow_result = result
                        st.success(f"✅ {selected_workflow} completed successfully!")
                    else:
                        st.error(f"Error in {selected_workflow}: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"Error running workflow: {str(e)}")
    
    # Q&A Section
    st.markdown('<h3 class="section-header">❓ Ask the Agent</h3>', unsafe_allow_html=True)
    
    user_question = st.text_input("Ask a question about the data:", key="user_question")
    
    if user_question:
        if st.button("🔍 Search for answer", key="search_answer"):
            # Simple Q&A logic - can be enhanced with actual AI
            if "vehicle" in user_question:
                st.write("🚗 Vehicle expenses are deductible in a limited manner according to section 31(a) of the Income Tax Ordinance.")
            elif "15%" in user_question:
                st.write("📉 If your tax rate is below 15%, you may be exposed to supplementary tax according to Pillar Two rules.")
            elif "ETR" in user_question:
                st.write("📊 ETR (Effective Tax Rate) is the effective tax rate calculated by dividing tax paid by profit before tax.")
            else:
                st.write("🤔 Interesting question! The agent will check the data and get back to you.")
    
    # Display results if available
    if st.session_state.analysis_results:
        st.markdown('<h3 class="section-header">📊 Analysis Results</h3>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📋 Executive Summary", "📊 Detailed Analysis", "✅ XML Validation"])
        
        with tab1:
            st.markdown(st.session_state.analysis_results["executive"])
        
        with tab2:
            st.markdown(st.session_state.analysis_results["detailed"])
        
        with tab3:
            st.markdown(st.session_state.analysis_results["validation"])
    
    # Display CrewAI results if available
    if hasattr(st.session_state, 'crewai_result') and st.session_state.crewai_result:
        st.markdown('<h3 class="section-header">🤖 CrewAI Results</h3>', unsafe_allow_html=True)
        
        result = st.session_state.crewai_result
        if result["success"]:
            st.success("✅ CrewAI analysis completed successfully!")
            st.write(f"**Result:** {result['result']}")
            if result.get('crew_info'):
                st.write(f"**Crew:** {result['crew_info']['name']}")
                st.write(f"**Number of agents:** {result['crew_info']['agents_count']}")
                st.write(f"**Number of tasks:** {result['crew_info']['tasks_count']}")
        else:
            st.error(f"❌ Error in CrewAI analysis: {result.get('error', 'Unknown error')}")
    
    # Display Workflow results if available
    if hasattr(st.session_state, 'workflow_result') and st.session_state.workflow_result:
        st.markdown('<h3 class="section-header">🔄 Workflow Results</h3>', unsafe_allow_html=True)
        
        result = st.session_state.workflow_result
        if result["success"]:
            st.success("✅ Workflow completed successfully!")
            st.write(f"**Result:** {result['result']}")
            if result.get('workflow_info'):
                workflow_info = result['workflow_info']
                st.write(f"**Workflow Name:** {workflow_info.get('name', 'Unknown')}")
                st.write(f"**Description:** {workflow_info.get('description', '')}")
                st.write(f"**Estimated Duration:** {workflow_info.get('estimated_duration', '')}")
                st.write(f"**Tasks:** {', '.join(workflow_info.get('tasks', []))}")
        else:
            st.error(f"❌ Error in Workflow: {result.get('error', 'Unknown error')}")

def reports_page():
    st.markdown('<h2 class="section-header">📄 Reports</h2>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.warning("Please run AI analysis in the 'AI Analysis' page")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Executive Report"):
            st.download_button(
                "📄 Download PDF",
                st.session_state.analysis_results["executive"],
                file_name="executive_report.md",
                mime="text/markdown"
            )
    
    with col2:
        if st.button("📥 Download Detailed Report"):
            st.download_button(
                "📄 Download PDF",
                st.session_state.analysis_results["detailed"],
                file_name="detailed_report.md",
                mime="text/markdown"
            )
    
    with col3:
        if st.button("📥 Download Validation Report"):
            st.download_button(
                "📄 Download PDF",
                st.session_state.analysis_results["validation"],
                file_name="validation_report.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
