# Pillar Two AI Agents - YAML Configuration

## Overview
This document describes the AI agents configuration for OECD Pillar Two compliance analysis using YAML-based CrewAI setup. **All validation errors have been resolved and the system is fully operational with CrewAI integration.**

## Agent Team Structure

### 1. Tax Modeler Agent
**Role**: Tax simulation builder based on ETR and Top-Up  
**Goal**: Building advanced models for calculating ETR and Top-Up Tax with various simulations  
**Experience**: 15 years in financial data analysis and calculating effective tax rates  
**Specialization**: ETR calculations and identifying exposure to supplementary tax according to Pillar Two rules

**Tools**:
- `excel_analyzer` - Excel file analysis and financial data extraction
- `etr_calculator` - Effective tax rate (ETR) calculation  
- `topup_simulator` - Top-Up Tax simulation according to Pillar Two rules

### 2. Legal Interpreter Agent
**Role**: Interpreter of Commentary and Guidance  
**Goal**: Legal interpretation of OECD Pillar Two rules and regulatory guidelines  
**Experience**: 20 years in interpreting tax treaties and OECD guidelines  
**Specialization**: Legal analysis of Pillar Two rules and identifying potential conflicts

**Tools**:
- `pdf_extractor` - Text extraction from PDF files
- `file_reader` - Reading various files (PDF, DOC, TXT)
- `legal_analyzer` - Legal analysis of regulatory documents

### 3. XML Reporter Agent
**Role**: GIR report generator according to XML Schema  
**Goal**: Creating valid GIR reports according to OECD XML Schema  
**Experience**: 10 years working with XML Schema and creating regulatory reports  
**Specialization**: Creating valid GIR reports and XML validation

**Tools**:
- `xml_validator` - XML validation according to Schema
- `gir_generator` - GIR XML report generation
- `schema_checker` - XML Schema compliance checking

### 4. Risk Analyst Agent
**Role**: Risk Assessment and Mitigation Specialist  
**Goal**: Comprehensive risk analysis and mitigation strategies for Pillar Two compliance  
**Experience**: 15 years in identifying, assessing, and mitigating risks in international taxation  
**Specialization**: Pillar Two risk assessment, including ETR volatility, jurisdictional risks, and compliance exposure

**Tools**:
- `risk_assessor` - Risk assessment for Pillar Two compliance
- `compliance_monitor` - Compliance monitoring and tracking
- `mitigation_planner` - Risk mitigation strategy planning

### 5. Transfer Pricing Specialist Agent
**Role**: Expert in Transfer Pricing and International Taxation  
**Goal**: Comprehensive transfer pricing analysis and documentation for Pillar Two compliance  
**Experience**: PhD in Law and Economics with 15+ years advising multinational enterprises and tax authorities  
**Specialization**: Transfer pricing methodologies, arm's length principle, and international tax planning

**Tools**:
- `file_reader` - Reading various files (PDF, DOC, TXT)
- `tp_analyzer` - Transfer pricing analysis and arm's length testing
- `OECD_guidelines_parser` - OECD Transfer Pricing Guidelines parser and analyzer
- `jurisdiction_risk_scanner` - Scan jurisdictions for transfer pricing risk factors

## Task Configuration

### 1. Financial Data Analysis
**Agent**: tax_modeler  
**Description**: Financial data analysis and ETR calculation  
**Expected Output**: Financial analysis report with ETR and Top-Up Tax calculations

**Context**:
- Calculate profit before tax
- Calculate tax paid  
- Calculate ETR (Effective Tax Rate)
- Identify exposure to supplementary tax according to Pillar Two rules (15%)
- Create various simulations for impact analysis

### 2. Legal Analysis
**Agent**: legal_interpreter  
**Description**: Legal analysis of Pillar Two rules  
**Expected Output**: Legal analysis report with regulatory recommendations

**Context**:
- Check compliance with OECD Pillar Two rules
- Identify potential conflicts with tax treaties
- Evaluate impact of Safe Harbour provisions
- Check eligibility for QDMTT (Qualified Domestic Minimum Top-up Tax)
- Create recommendations for regulatory risk management

### 3. GIR Report Generation
**Agent**: xml_reporter  
**Description**: Creating valid GIR XML report  
**Expected Output**: Valid XML file according to GIR Schema

**Context**:
- Ensure compliance with OECD XML Schema
- Include all required data
- Perform file validation
- Create backup and parallel PDF file

### 4. Risk Assessment
**Agent**: risk_analyst  
**Description**: Comprehensive risk assessment and mitigation planning  
**Expected Output**: Risk assessment report with mitigation strategies

**Context**:
- Analyze ETR volatility and exposure to Top-Up Tax
- Assess jurisdictional risks and compliance gaps
- Evaluate regulatory changes and their impact
- Identify operational risks in data collection and reporting
- Develop mitigation strategies and contingency plans
- Create risk monitoring framework for ongoing compliance

### 5. Transfer Pricing Analysis
**Agent**: transfer_pricing_specialist  
**Description**: Comprehensive transfer pricing analysis for Pillar Two compliance  
**Expected Output**: Transfer pricing analysis report with GloBE Income adjustments

**Context**:
- Analyze intercompany transactions for arm's length compliance
- Identify jurisdictions with high transfer pricing risk
- Recommend adjustments to GloBE Income based on TP deviations
- Cross-reference with OECD Transfer Pricing Guidelines (Chapters I–VII)
- Flag mismatches between local TP documentation and Pillar Two reporting
- Assess impact of transfer pricing adjustments on ETR calculations
- Review related party transactions for substance and value creation
- Evaluate transfer pricing documentation completeness and consistency

## Tool Definitions

### Financial Analysis Tools
- `excel_analyzer`: Excel file analysis and financial data extraction
- `etr_calculator`: Effective tax rate (ETR) calculation
- `topup_simulator`: Top-Up Tax simulation according to Pillar Two rules

### Legal Analysis Tools
- `pdf_extractor`: Text extraction from PDF files
- `file_reader`: Reading various files (PDF, DOC, TXT)
- `legal_analyzer`: Legal analysis of regulatory documents

### Technical Tools
- `xml_validator`: XML validation according to Schema
- `gir_generator`: GIR XML report generation
- `schema_checker`: XML Schema compliance checking

### Risk Management Tools
- `risk_assessor`: Risk assessment for Pillar Two compliance
- `compliance_monitor`: Compliance monitoring and tracking
- `mitigation_planner`: Risk mitigation strategy planning

### Transfer Pricing Tools
- `tp_analyzer`: Transfer pricing analysis and arm's length testing
- `OECD_guidelines_parser`: OECD Transfer Pricing Guidelines parser and analyzer
- `jurisdiction_risk_scanner`: Scan jurisdictions for transfer pricing risk factors

## Settings Configuration

```yaml
settings:
  process: "sequential"
  verbose: true
  memory: true
  cache: true
```

## Usage Example

```python
from agents.yaml_crew_loader import YAMLCrewLoader

# Load crew configuration
loader = YAMLCrewLoader("agents/crew_config.yaml")
crew = loader.create_crew()

# Execute tasks
result = crew.kickoff()
print(result)
```

## Benefits

1. **Comprehensive Coverage**: All aspects of Pillar Two compliance covered
2. **Specialized Expertise**: Each agent has deep domain knowledge
3. **Modular Design**: Easy to add new agents or modify existing ones
4. **YAML Configuration**: Simple and readable configuration format
5. **Scalable Architecture**: Can handle complex multi-agent workflows

## Integration Points

- **Financial Data**: Connects with accounting systems and financial databases
- **Legal Documents**: Integrates with legal document management systems
- **Regulatory Updates**: Monitors OECD and jurisdictional regulatory changes
- **Risk Management**: Connects with enterprise risk management systems
- **Transfer Pricing**: Integrates with transfer pricing documentation systems

## Future Enhancements

- Machine learning for risk prediction
- Real-time regulatory monitoring
- Automated compliance reporting
- Advanced scenario modeling
- Integration with external tax databases
- Multi-jurisdictional compliance tracking
