import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
import json
from pathlib import Path
import os

class PillarTwoReportGenerator:
    """
    PillarTwoReportGenerator - Generates comprehensive regulatory analysis reports
    Processes GIR XML data and creates detailed English reports
    """
    
    def __init__(self):
        self.report_templates = self._load_report_templates()
        self.analysis_engine = None  # Will be connected to CrewAI team
        
    def _load_report_templates(self) -> Dict[str, str]:
        """Load report templates in English"""
        return {
            "executive_summary": """
# Regulatory Analysis Report according to Pillar Two – OECD

## Client Details
- Company Name: {company_name}
- Active Countries: {active_countries}
- Business Sector: {business_sector}
- Reporting Year: {reporting_year}

---

## Effective Tax Rate (ETR) Analysis
- Reported Profits: €{total_profit:,.0f}
- Taxes Paid: €{total_taxes:,.0f}
- Effective Tax Rate: {average_etr:.1f}%
- Minimum Tax Required by Pillar Two: 15%
- Exposure to Additional Tax (Top-Up Tax): €{total_topup:,.0f}

---

## Legal Analysis – Tax Treaty
{legal_analysis}

---

## Regulatory Recommendations
{regulatory_recommendations}

---

## Appendices
- Tax Simulation (attached Excel file)
- Executive Summary (attached PDF file)
- Links to relevant OECD publications
""",
            
            "detailed_analysis": """
# Detailed Analysis – Pillar Two Compliance

## 1. ETR Analysis by Entity
{entity_analysis}

## 2. Top-Up Tax Analysis
{topup_analysis}

## 3. Legal Analysis
{legal_detailed_analysis}

## 4. Implementation Recommendations
{implementation_recommendations}

## 5. Risk Summary
{risk_summary}
""",
            
            "xml_validation_report": """
# GIR XML Validation Report

## Validation Status
- XML Validity: {xml_valid}
- Schema Compliance: {schema_compliant}
- Errors: {validation_errors}

## Entity Details
{entity_details}

## Financial Summary
{financial_summary}
"""
        }
    
    def parse_gir_xml(self, xml_content: str) -> Dict[str, Any]:
        """Parse GIR XML content and extract structured data"""
        try:
            root = ET.fromstring(xml_content)
            
            # Extract filing entity information
            filing_entity = root.find('.//FilingEntity')
            company_name = filing_entity.find('EntityName').text if filing_entity.find('EntityName') is not None else "Unknown"
            entity_id = filing_entity.find('EntityID').text if filing_entity.find('EntityID') is not None else "Unknown"
            jurisdiction = filing_entity.find('Jurisdiction').text if filing_entity.find('Jurisdiction') is not None else "Unknown"
            
            # Extract reporting period
            reporting_period = root.find('.//ReportingPeriod')
            start_date = reporting_period.find('StartDate').text if reporting_period.find('StartDate') is not None else "Unknown"
            end_date = reporting_period.find('EndDate').text if reporting_period.find('EndDate') is not None else "Unknown"
            
            # Extract constituent entities
            entities = []
            total_profit = 0
            total_taxes = 0
            total_topup = 0
            
            for entity in root.findall('.//ConstituentEntities/Entity'):
                entity_data = {
                    'name': entity.find('EntityName').text if entity.find('EntityName') is not None else "Unknown",
                    'jurisdiction': entity.find('Jurisdiction').text if entity.find('Jurisdiction') is not None else "Unknown",
                    'etr': float(entity.find('ETR').text) if entity.find('ETR') is not None else 0.0,
                    'topup_tax': float(entity.find('TopUpTax').text) if entity.find('TopUpTax') is not None else 0.0,
                    'qualified': entity.find('QualifiedStatus').text == 'Yes' if entity.find('QualifiedStatus') is not None else False
                }
                
                # Extract financial data
                financial_data = entity.find('FinancialData')
                if financial_data is not None:
                    entity_data['revenue'] = float(financial_data.find('Revenue').text) if financial_data.find('Revenue') is not None else 0.0
                    entity_data['profit_before_tax'] = float(financial_data.find('ProfitBeforeTax').text) if financial_data.find('ProfitBeforeTax') is not None else 0.0
                    entity_data['covered_taxes'] = float(financial_data.find('CoveredTaxes').text) if financial_data.find('CoveredTaxes') is not None else 0.0
                
                entities.append(entity_data)
                total_profit += entity_data.get('profit_before_tax', 0)
                total_taxes += entity_data.get('covered_taxes', 0)
                total_topup += entity_data.get('topup_tax', 0)
            
            # Extract summary
            summary = root.find('.//Summary')
            if summary is not None:
                summary_data = {
                    'total_topup_tax': float(summary.find('TotalTopUpTax').text) if summary.find('TotalTopUpTax') is not None else total_topup,
                    'total_covered_taxes': float(summary.find('TotalCoveredTaxes').text) if summary.find('TotalCoveredTaxes') is not None else total_taxes,
                    'total_profit': float(summary.find('TotalProfit').text) if summary.find('TotalProfit') is not None else total_profit
                }
            else:
                summary_data = {
                    'total_topup_tax': total_topup,
                    'total_covered_taxes': total_taxes,
                    'total_profit': total_profit
                }
            
            return {
                'company_name': company_name,
                'entity_id': entity_id,
                'jurisdiction': jurisdiction,
                'reporting_period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'entities': entities,
                'summary': summary_data,
                'parsing_success': True
            }
            
        except Exception as e:
            return {
                'parsing_success': False,
                'error': str(e),
                'entities': [],
                'summary': {}
            }
    
    def analyze_etr_data(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ETR data and generate insights"""
        entities = parsed_data.get('entities', [])
        
        if not entities:
            return {'error': 'No entities found for analysis'}
        
        # Calculate average ETR
        total_profit = sum(entity.get('profit_before_tax', 0) for entity in entities)
        total_taxes = sum(entity.get('covered_taxes', 0) for entity in entities)
        average_etr = (total_taxes / total_profit * 100) if total_profit > 0 else 0
        
        # Analyze entities below threshold
        below_threshold_entities = [e for e in entities if e.get('etr', 0) < 15.0]
        above_threshold_entities = [e for e in entities if e.get('etr', 0) >= 15.0]
        
        # Calculate total top-up tax
        total_topup = sum(entity.get('topup_tax', 0) for entity in entities)
        
        return {
            'average_etr': round(average_etr, 2),
            'total_profit': total_profit,
            'total_taxes': total_taxes,
            'total_topup': total_topup,
            'below_threshold_count': len(below_threshold_entities),
            'above_threshold_count': len(above_threshold_entities),
            'below_threshold_entities': below_threshold_entities,
            'above_threshold_entities': above_threshold_entities,
            'risk_level': 'high' if len(below_threshold_entities) > len(above_threshold_entities) else 'medium'
        }
    
    def generate_legal_analysis(self, parsed_data: Dict[str, Any]) -> str:
        """Generate legal analysis based on jurisdiction and tax treaties"""
        entities = parsed_data.get('entities', [])
        jurisdictions = list(set(entity.get('jurisdiction') for entity in entities))
        
        legal_analysis = []
        
        for jurisdiction in jurisdictions:
            jurisdiction_entities = [e for e in entities if e.get('jurisdiction') == jurisdiction]
            
            # Analyze jurisdiction-specific legal considerations
            if jurisdiction == 'IE':  # Ireland
                legal_analysis.append(f"""
### Ireland (IE)
- Tax treaty between Ireland and Israel signed in 1995
- Article 23: Credit mechanism to prevent double taxation
- Article 24: Non-discrimination between domestic and foreign companies
- Assessment: Potential conflict between Top-Up Tax collection and treaty provisions
- Entities in Ireland: {len(jurisdiction_entities)}
- Top-Up Tax required: €{sum(e.get('topup_tax', 0) for e in jurisdiction_entities):,.0f}
""")
            
            elif jurisdiction == 'NL':  # Netherlands
                legal_analysis.append(f"""
### Netherlands (NL)
- Tax treaty between Netherlands and Israel signed in 1973
- Article 23: Credit mechanism to prevent double taxation
- Article 24: Non-discrimination between domestic and foreign companies
- Assessment: ETR above 15% - no Top-Up Tax required
- Entities in Netherlands: {len(jurisdiction_entities)}
- Top-Up Tax required: €{sum(e.get('topup_tax', 0) for e in jurisdiction_entities):,.0f}
""")
        
        return '\n'.join(legal_analysis)
    
    def generate_regulatory_recommendations(self, analysis_data: Dict[str, Any]) -> str:
        """Generate regulatory recommendations based on analysis"""
        recommendations = []
        
        if analysis_data.get('risk_level') == 'high':
            recommendations.append("""
### Urgent Recommendations:
1. **Check Temporary Recognition under Central Record**
   - Check possibility for temporary recognition in countries with low ETR
   - Consider applying for Safe Harbour

2. **Restructure Operations**
   - Consider moving operations to QDMTT Qualified countries
   - Check options for Substance-based Income Exclusion (SBIE)

3. **Activate Treaty Provisions**
   - Activate credit provisions in treaty to prevent double taxation
   - Check possibility of Mutual Agreement Procedure (MAP)
""")
        
        recommendations.append("""
### General Recommendations:
1. **File Reports**
   - Submit GIR according to new XML Schema
   - Ensure accuracy of financial data

2. **Future Tax Planning**
   - Develop strategy to improve ETR
   - Consider investments in countries with higher tax rates

3. **Regulatory Monitoring**
   - Monitor regulatory changes
   - Stay updated on new OECD guidelines
""")
        
        return '\n'.join(recommendations)
    
    def generate_entity_analysis(self, entities: List[Dict[str, Any]]) -> str:
        """Generate detailed entity analysis"""
        analysis_lines = []
        
        for entity in entities:
            name = entity.get('name', 'Unknown')
            jurisdiction = entity.get('jurisdiction', 'Unknown')
            etr = entity.get('etr', 0)
            topup = entity.get('topup_tax', 0)
            profit = entity.get('profit_before_tax', 0)
            taxes = entity.get('covered_taxes', 0)
            
            status = "✅ Above 15% threshold" if etr >= 15.0 else "⚠️ Below 15% threshold"
            
            analysis_lines.append(f"""
#### {name} ({jurisdiction})
- Profit before tax: €{profit:,.0f}
- Taxes paid: €{taxes:,.0f}
- ETR: {etr:.2f}% {status}
- Top-Up Tax required: €{topup:,.0f}
""")
        
        return '\n'.join(analysis_lines)
    
    def generate_executive_report(self, xml_content: str) -> str:
        """Generate executive summary report"""
        # Parse XML data
        parsed_data = self.parse_gir_xml(xml_content)
        
        if not parsed_data.get('parsing_success'):
            return f"XML parsing error: {parsed_data.get('error', 'Unknown error')}"
        
        # Analyze ETR data
        analysis_data = self.analyze_etr_data(parsed_data)
        
        # Generate legal analysis
        legal_analysis = self.generate_legal_analysis(parsed_data)
        
        # Generate recommendations
        regulatory_recommendations = self.generate_regulatory_recommendations(analysis_data)
        
        # Extract company information
        company_name = parsed_data.get('company_name', 'Unknown')
        jurisdictions = list(set(entity.get('jurisdiction') for entity in parsed_data.get('entities', [])))
        active_countries = ', '.join(jurisdictions)
        reporting_year = parsed_data.get('reporting_period', {}).get('start_date', '2025')[:4]
        
        # Fill template
        report = self.report_templates['executive_summary'].format(
            company_name=company_name,
            active_countries=active_countries,
            business_sector="Technology",  # Default, could be extracted from data
            reporting_year=reporting_year,
            total_profit=analysis_data.get('total_profit', 0),
            total_taxes=analysis_data.get('total_taxes', 0),
            average_etr=analysis_data.get('average_etr', 0),
            total_topup=analysis_data.get('total_topup', 0),
            legal_analysis=legal_analysis,
            regulatory_recommendations=regulatory_recommendations
        )
        
        return report
    
    def generate_detailed_report(self, xml_content: str) -> str:
        """Generate detailed analysis report"""
        # Parse XML data
        parsed_data = self.parse_gir_xml(xml_content)
        
        if not parsed_data.get('parsing_success'):
            return f"XML parsing error: {parsed_data.get('error', 'Unknown error')}"
        
        # Analyze ETR data
        analysis_data = self.analyze_etr_data(parsed_data)
        
        # Generate detailed analyses
        entity_analysis = self.generate_entity_analysis(parsed_data.get('entities', []))
        legal_detailed_analysis = self.generate_legal_analysis(parsed_data)
        implementation_recommendations = self.generate_regulatory_recommendations(analysis_data)
        
        # Generate risk summary
        risk_summary = f"""
### Risk Summary
- **Overall Risk Level**: {analysis_data.get('risk_level', 'medium')}
- **Entities below threshold**: {analysis_data.get('below_threshold_count', 0)}
- **Entities above threshold**: {analysis_data.get('above_threshold_count', 0)}
- **Total Top-Up Tax**: €{analysis_data.get('total_topup', 0):,.0f}
- **Average ETR**: {analysis_data.get('average_etr', 0):.2f}%
"""
        
        # Fill detailed template
        report = self.report_templates['detailed_analysis'].format(
            entity_analysis=entity_analysis,
            topup_analysis=f"Total Top-Up Tax required: €{analysis_data.get('total_topup', 0):,.0f}",
            legal_detailed_analysis=legal_detailed_analysis,
            implementation_recommendations=implementation_recommendations,
            risk_summary=risk_summary
        )
        
        return report
    
    def validate_xml_schema(self, xml_content: str) -> Dict[str, Any]:
        """Validate XML against OECD GIR schema"""
        try:
            root = ET.fromstring(xml_content)
            
            # Basic validation
            validation_errors = []
            
            # Check required elements
            required_elements = [
                'FilingEntity',
                'ReportingPeriod', 
                'ConstituentEntities'
            ]
            
            for element in required_elements:
                if root.find(f'.//{element}') is None:
                    validation_errors.append(f"Missing required element: {element}")
            
            # Check entity structure
            entities = root.findall('.//ConstituentEntities/Entity')
            for i, entity in enumerate(entities):
                required_entity_elements = ['EntityName', 'Jurisdiction', 'ETR']
                for elem in required_entity_elements:
                    if entity.find(elem) is None:
                        validation_errors.append(f"Entity {i+1}: Missing {elem}")
            
            return {
                'xml_valid': len(validation_errors) == 0,
                'schema_compliant': len(validation_errors) == 0,
                'validation_errors': validation_errors,
                'entity_count': len(entities)
            }
            
        except ET.ParseError as e:
            return {
                'xml_valid': False,
                'schema_compliant': False,
                'validation_errors': [f"XML Parse Error: {str(e)}"],
                'entity_count': 0
            }
    
    def generate_validation_report(self, xml_content: str) -> str:
        """Generate XML validation report"""
        validation_result = self.validate_xml_schema(xml_content)
        parsed_data = self.parse_gir_xml(xml_content)
        
        # Generate entity details
        entity_details = []
        for entity in parsed_data.get('entities', []):
            entity_details.append(f"""
- {entity.get('name', 'Unknown')} ({entity.get('jurisdiction', 'Unknown')})
  - ETR: {entity.get('etr', 0):.2f}%
  - Top-Up Tax: €{entity.get('topup_tax', 0):,.0f}
""")
        
        # Generate financial summary
        summary = parsed_data.get('summary', {})
        financial_summary = f"""
- Total Profit: €{summary.get('total_profit', 0):,.0f}
- Total Taxes: €{summary.get('total_covered_taxes', 0):,.0f}
- Total Top-Up Tax: €{summary.get('total_topup_tax', 0):,.0f}
"""
        
        # Fill validation template
        report = self.report_templates['xml_validation_report'].format(
            xml_valid="✅ Valid" if validation_result.get('xml_valid') else "❌ Invalid",
            schema_compliant="✅ Compliant" if validation_result.get('schema_compliant') else "❌ Non-compliant",
            validation_errors='\n'.join(validation_result.get('validation_errors', [])) or "No errors",
            entity_details='\n'.join(entity_details),
            financial_summary=financial_summary
        )
        
        return report
    
    def save_report(self, report_content: str, filename: str, output_dir: str = "reports") -> str:
        """Save report to file"""
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Save report
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            return filepath
            
        except Exception as e:
            return f"Error saving report: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Initialize report generator
    generator = PillarTwoReportGenerator()
    
    # Example XML content (from user's input)
    xml_content = """<GIRSubmission xmlns="http://oecd.org/pillar2/gir">
  <FilingEntity>
    <EntityName>Company Name</EntityName>
    <EntityID>123456789</EntityID>
    <Jurisdiction>IE</Jurisdiction>
  </FilingEntity>

  <ReportingPeriod>
    <StartDate>2025-01-01</StartDate>
    <EndDate>2025-12-31</EndDate>
  </ReportingPeriod>

  <ConstituentEntities>
    <Entity>
      <EntityName>Subsidiary Ireland</EntityName>
      <Jurisdiction>IE</Jurisdiction>
      <FinancialData>
        <Revenue>100000000</Revenue>
        <ProfitBeforeTax>95000000</ProfitBeforeTax>
        <CoveredTaxes>12500000</CoveredTaxes>
      </FinancialData>
      <ETR>12.5</ETR>
      <TopUpTax>2500000</TopUpTax>
      <QualifiedStatus>No</QualifiedStatus>
    </Entity>
    <Entity>
      <EntityName>Subsidiary Netherlands</EntityName>
      <Jurisdiction>NL</Jurisdiction>
      <FinancialData>
        <Revenue>100000000</Revenue>
        <ProfitBeforeTax>97000000</ProfitBeforeTax>
        <CoveredTaxes>15000000</CoveredTaxes>
      </FinancialData>
      <ETR>15.46</ETR>
      <TopUpTax>0</TopUpTax>
      <QualifiedStatus>Yes</QualifiedStatus>
    </Entity>
  </ConstituentEntities>

  <Summary>
    <TotalTopUpTax>2500000</TotalTopUpTax>
    <TotalCoveredTaxes>27500000</TotalCoveredTaxes>
    <TotalProfit>192000000</TotalProfit>
  </Summary>
</GIRSubmission>"""
    
    # Generate reports
    executive_report = generator.generate_executive_report(xml_content)
    detailed_report = generator.generate_detailed_report(xml_content)
    validation_report = generator.generate_validation_report(xml_content)
    
    # Save reports
    generator.save_report(executive_report, "executive_report.md")
    generator.save_report(detailed_report, "detailed_report.md")
    generator.save_report(validation_report, "validation_report.md")
    
    print("Reports generated successfully!")
    print("Executive Report Preview:")
    print(executive_report[:500] + "...")
