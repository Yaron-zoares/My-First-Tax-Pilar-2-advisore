from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import json
import logging
from .web_scraping_tools import web_scraping_tools

logger = logging.getLogger(__name__)

# Import new data processing components with error handling
try:
    from data_validator import DataValidator
except ImportError:
    class DataValidator:
        def validate_financial_data(self, data):
            return {"is_valid": True, "errors": []}

try:
    from data_format_adapter import DataFormatAdapter
except ImportError:
    class DataFormatAdapter:
        def detect_format(self, data):
            return "unknown"
        def adapt_data(self, data, format_type):
            return data

try:
    from enhanced_error_handler import EnhancedErrorHandler
except ImportError:
    class EnhancedErrorHandler:
        def validate_data_structure(self, data, structure):
            return {"is_valid": True, "errors": []}
        def handle_validation_errors(self, validation):
            return "Validation errors occurred"
        def handle_error(self, error, context):
            return str(error)

try:
    from flexible_data_processor import FlexibleDataProcessor
except ImportError:
    class FlexibleDataProcessor:
        def process_data(self, data, format_type=None):
            return {"success": True, "data": data}

class PillarTwoMaster:
    """
    PillarTwoMaster - Comprehensive OECD Pillar Two analysis agent
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.agent = self._create_agent()
        self.memory = self._initialize_memory()
        
        # Initialize Serper API key
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
    def _create_agent(self) -> Agent:
        """Create the PillarTwoMaster agent"""
        agent = Agent(
            role="PillarTwoMaster - OECD Pillar Two Expert",
            goal="Provide comprehensive analysis, guidance, and solutions for OECD Pillar Two compliance and implementation",
            backstory="""You are PillarTwoMaster, a world-renowned expert in international tax law with over 20 years of experience specializing in OECD Pillar Two regulations. 
            You have advised Fortune 500 companies, governments, and international organizations on implementing the global minimum tax framework. 
            Your expertise spans from technical ETR calculations to strategic tax planning and regulatory compliance across multiple jurisdictions.
            
            You have deep knowledge of:
            - Effective Tax Rate (ETR) calculations and adjustments
            - Deferred tax accounting and timing differences
            - BEPS (Base Erosion and Profit Shifting) principles
            - International tax treaties and their impact on Pillar Two
            - GIR (Global Information Return) XML Schema requirements
            - Safe Harbours and Administrative Guidance
            - Country-by-country reporting requirements
            - Substance-based income exclusion (SBIE) calculations
            - Qualified domestic minimum top-up tax (QDMTT)
            - Income inclusion rule (IIR) and undertaxed profits rule (UTPR)
            
            You provide practical, actionable advice while ensuring full regulatory compliance.""",
            verbose=True,
            allow_delegation=True,
            memory=self._initialize_memory()
        )
        
        # Add tools after creation
        agent.tools = self._get_tools()
        
        return agent
    
    def _get_tools(self) -> List[Tool]:
        """Define the tools available to the agent"""
        return [
            Tool(
                name="Web_Search",
                func=self._web_search,
                description="Search the web for current information about OECD Pillar Two, tax regulations, and legal updates"
            ),
            Tool(
                name="Web_Scrape",
                func=self._web_scrape,
                description="Scrape content from specific webpages for detailed analysis"
            ),
            Tool(
                name="Scrape_Tax_Rates",
                func=self._scrape_tax_rates,
                description="Scrape tax rates from government websites and OECD databases"
            ),
            Tool(
                name="Scrape_OECD_Documents",
                func=self._scrape_oecd_documents,
                description="Scrape OECD documents and guidance for Pillar Two analysis"
            ),
            Tool(
                name="Extract_Specific_Content",
                func=self._extract_specific_content,
                description="Extract specific content from webpages using CSS selectors"
            ),
            Tool(
                name="ETR_Calculator",
                func=self._calculate_etr,
                description="Calculate Effective Tax Rate (ETR) based on financial data and tax adjustments"
            ),
            Tool(
                name="Tax_Adjustment_Analyzer",
                func=self._analyze_tax_adjustments,
                description="Analyze and categorize tax adjustments for Pillar Two compliance"
            ),
            Tool(
                name="GIR_XML_Generator",
                func=self._generate_gir_xml,
                description="Generate Global Information Return (GIR) XML files according to OECD schema"
            ),
            Tool(
                name="Safe_Harbour_Checker",
                func=self._check_safe_harbours,
                description="Check if company qualifies for Safe Harbours under Pillar Two rules"
            ),
            Tool(
                name="Country_By_Country_Analyzer",
                func=self._analyze_cbcr,
                description="Analyze country-by-country reporting data for Pillar Two implications"
            ),
            Tool(
                name="Regulatory_Compliance_Checker",
                func=self._check_compliance,
                description="Check regulatory compliance with Pillar Two requirements across jurisdictions"
            ),
            Tool(
                name="Tax_Treaty_Analyzer",
                func=self._analyze_tax_treaties,
                description="Analyze impact of tax treaties on Pillar Two calculations"
            ),
            Tool(
                name="SBIE_Calculator",
                func=self._calculate_sbie,
                description="Calculate Substance-based income exclusion (SBIE) for qualifying activities"
            ),
            Tool(
                name="Top_Up_Tax_Calculator",
                func=self._calculate_top_up_tax,
                description="Calculate Top-Up Tax based on ETR and jurisdictional requirements"
            ),
            Tool(
                name="Jurisdiction_Risk_Analyzer",
                func=self._analyze_jurisdiction_risks,
                description="Analyze jurisdictional risks and compliance requirements"
            ),
            Tool(
                name="Implementation_Planner",
                func=self._plan_implementation,
                description="Create comprehensive implementation plans for Pillar Two compliance"
            )
        ]
    
    def _initialize_memory(self) -> Dict[str, Any]:
        """Initialize the agent's memory with key Pillar Two concepts"""
        return {
            "pillar_two_knowledge": {
                "etr_threshold": 15.0,  # 15% minimum ETR
                "safe_harbours": {
                    "transitional_safe_harbour": "Available until 2026",
                    "simplified_etr_safe_harbour": "Available until 2026",
                    "de_minimis_safe_harbour": "Available until 2026"
                },
                "key_dates": {
                    "implementation_start": "2024",
                    "full_implementation": "2025",
                    "safe_harbour_expiry": "2026"
                },
                "jurisdictions": {
                    "implementing": ["EU", "UK", "Switzerland", "Norway", "Australia", "Canada", "Japan", "South Korea"],
                    "considering": ["United States", "China", "India", "Brazil"],
                    "not_implementing": ["Russia", "Saudi Arabia"]
                }
            },
            "recent_analysis": [],
            "client_preferences": {},
            "regulatory_updates": []
        }
    
    def _load_sources(self) -> Dict[str, Any]:
        """Load authoritative sources for Pillar Two analysis"""
        return {
            "primary_sources": {
                "oecd_model_rules": "OECD Model Rules on Pillar Two",
                "commentary": "OECD Commentary on Pillar Two Model Rules",
                "administrative_guidance": "OECD Administrative Guidance on Pillar Two",
                "safe_harbour_guidance": "OECD Safe Harbour and Penalty Relief Guidance",
                "gir_schema": "OECD GIR XML Schema Documentation"
            },
            "secondary_sources": {
                "country_implementations": "Country-specific Pillar Two implementations",
                "academic_papers": "Academic research on Pillar Two",
                "practitioner_guides": "Professional practice guides",
                "case_studies": "Real-world implementation case studies"
            },
            "regulatory_bodies": {
                "oecd": "Organisation for Economic Co-operation and Development",
                "eu": "European Union",
                "un": "United Nations",
                "g20": "Group of 20"
            }
        }
    
    def _create_team(self) -> List[Agent]:
        """Create supporting team members for comprehensive analysis"""
        return [
            Agent(
                role="Financial Data Analyst",
                goal="Analyze financial statements and extract relevant data for Pillar Two calculations",
                backstory="Expert in financial statement analysis with deep understanding of accounting standards and their impact on tax calculations",
                verbose=True,
                allow_delegation=False
            ),
            Agent(
                role="Legal Compliance Specialist",
                goal="Ensure all recommendations comply with applicable laws and regulations across jurisdictions",
                backstory="Legal expert specializing in international tax law and regulatory compliance with experience in multiple jurisdictions",
                verbose=True,
                allow_delegation=False
            ),
            Agent(
                role="Technical Implementation Expert",
                goal="Provide practical implementation guidance for Pillar Two requirements",
                backstory="Technical expert in implementing tax systems and processes, with experience in large-scale tax transformation projects",
                verbose=True,
                allow_delegation=False
            ),
            Agent(
                role="Risk Assessment Specialist",
                goal="Identify and assess risks associated with Pillar Two implementation and compliance",
                backstory="Risk management expert with specialization in tax risk assessment and mitigation strategies",
                verbose=True,
                allow_delegation=False
            ),
            Agent(
                role="Transfer Pricing Specialist",
                goal="Analyze transfer pricing implications for Pillar Two compliance",
                backstory="PhD in Law and Economics with 15+ years experience in transfer pricing and international taxation",
                verbose=True,
                allow_delegation=False
            )
        ]
    
    # Tool implementation methods
    def _calculate_etr(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Effective Tax Rate (ETR) for Pillar Two purposes with enhanced validation"""
        try:
            # Initialize data processing components
            validator = DataValidator()
            error_handler = EnhancedErrorHandler()
            
            # Validate input data
            validation_result = validator.validate_financial_data(financial_data)
            
            if not validation_result["is_valid"]:
                error_info = error_handler.handle_validation_errors(validation_result)
                return {
                    "error": "ETR calculation failed due to validation errors",
                    "validation_errors": error_info,
                    "suggestions": error_info.get("suggestions", [])
                }
            
            # Extract key financial metrics
            pre_tax_income = financial_data.get("pre_tax_income", 0)
            current_tax_expense = financial_data.get("current_tax_expense", 0)
            deferred_tax_expense = financial_data.get("deferred_tax_expense", 0)
            
            # Additional validation
            if pre_tax_income <= 0:
                return {
                    "error": "ETR calculation failed: Pre-tax income must be positive",
                    "suggestions": ["Check financial data accuracy", "Verify income calculations"]
                }
            
            # Calculate ETR
            total_tax_expense = current_tax_expense + deferred_tax_expense
            etr = (total_tax_expense / pre_tax_income * 100) if pre_tax_income > 0 else 0
            
            # Determine if below 15% threshold
            below_threshold = etr < 15.0
            top_up_tax_rate = max(0, 15.0 - etr) if below_threshold else 0
            
            # Enhanced result with warnings
            result = {
                "etr_percentage": round(etr, 2),
                "below_threshold": below_threshold,
                "top_up_tax_rate": round(top_up_tax_rate, 2),
                "calculation_components": {
                    "pre_tax_income": pre_tax_income,
                    "current_tax_expense": current_tax_expense,
                    "deferred_tax_expense": deferred_tax_expense,
                    "total_tax_expense": total_tax_expense
                },
                "validation_warnings": validation_result.get("warnings", []),
                "validation_suggestions": validation_result.get("suggestions", [])
            }
            
            # Add risk assessment
            if below_threshold:
                result["risk_level"] = "high"
                result["risk_description"] = "ETR below 15% threshold - potential Top-Up Tax exposure"
            elif etr < 18:
                result["risk_level"] = "medium"
                result["risk_description"] = "ETR close to 15% threshold - monitor closely"
            else:
                result["risk_level"] = "low"
                result["risk_description"] = "ETR above 18% - low risk of Top-Up Tax"
            
            return result
            
        except Exception as e:
            error_info = error_handler.handle_error(e, "etr_calculation")
            return {
                "error": f"ETR calculation failed: {error_info['error_message']}",
                "suggestions": error_info.get("suggestions", []),
                "error_category": error_info.get("error_category", "unknown")
            }
    
    def _analyze_tax_adjustments(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tax adjustments for Pillar Two compliance"""
        adjustments = {
            "permanent_differences": [],
            "temporary_differences": [],
            "excluded_items": [],
            "included_items": []
        }
        
        # Analyze common adjustment categories
        for item, amount in financial_data.get("adjustments", {}).items():
            if "depreciation" in item.lower():
                adjustments["temporary_differences"].append({
                    "item": item,
                    "amount": amount,
                    "type": "timing_difference"
                })
            elif "provision" in item.lower():
                adjustments["permanent_differences"].append({
                    "item": item,
                    "amount": amount,
                    "type": "permanent_difference"
                })
            elif "foreign_income" in item.lower():
                adjustments["excluded_items"].append({
                    "item": item,
                    "amount": amount,
                    "type": "excluded_income"
                })
        
        return adjustments
    
    def _generate_gir_xml(self, entity_data: Dict[str, Any]) -> str:
        """Generate Global Information Return (GIR) XML file"""
        # This would generate XML according to OECD GIR schema
        xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<GIR xmlns="urn:oecd:ties:gir:v1">
    <Entity>
        <Name>{entity_data.get('name', 'Unknown')}</Name>
        <TaxResidence>{entity_data.get('tax_residence', 'Unknown')}</TaxResidence>
        <ConstituentEntity>
            <Name>{entity_data.get('constituent_name', 'Unknown')}</Name>
            <TaxResidence>{entity_data.get('constituent_tax_residence', 'Unknown')}</TaxResidence>
            <ETR>{entity_data.get('etr', 0)}</ETR>
        </ConstituentEntity>
    </Entity>
</GIR>"""
        return xml_template
    
    def _check_safe_harbours(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if entity qualifies for Safe Harbours"""
        safe_harbours = {
            "transitional_safe_harbour": {
                "qualified": False,
                "conditions": ["Simplified ETR calculation", "Available until 2026"],
                "requirements": []
            },
            "simplified_etr_safe_harbour": {
                "qualified": False,
                "conditions": ["Simplified ETR calculation", "Available until 2026"],
                "requirements": []
            },
            "de_minimis_safe_harbour": {
                "qualified": False,
                "conditions": ["De minimis thresholds", "Available until 2026"],
                "requirements": []
            }
        }
        
        # Check qualification criteria
        revenue = entity_data.get("revenue", 0)
        if revenue < 75000000:  # 75 million threshold
            safe_harbours["de_minimis_safe_harbour"]["qualified"] = True
        
        return safe_harbours
    
    def _analyze_cbcr(self, cbcr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze country-by-country reporting data"""
        analysis = {
            "jurisdictions": [],
            "high_risk_countries": [],
            "low_tax_jurisdictions": [],
            "recommendations": []
        }
        
        for jurisdiction, data in cbcr_data.get("jurisdictions", {}).items():
            etr = data.get("etr", 0)
            if etr < 15.0:
                analysis["low_tax_jurisdictions"].append({
                    "jurisdiction": jurisdiction,
                    "etr": etr,
                    "risk_level": "high" if etr < 10.0 else "medium"
                })
        
        return analysis
    
    def _check_compliance(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check regulatory compliance with Pillar Two requirements"""
        compliance_status = {
            "overall_compliance": "pending",
            "jurisdictions": {},
            "missing_requirements": [],
            "recommendations": []
        }
        
        # Check implementation status by jurisdiction
        for jurisdiction in entity_data.get("operations", []):
            if jurisdiction in self.memory["pillar_two_knowledge"]["jurisdictions"]["implementing"]:
                compliance_status["jurisdictions"][jurisdiction] = "implementing"
            elif jurisdiction in self.memory["pillar_two_knowledge"]["jurisdictions"]["considering"]:
                compliance_status["jurisdictions"][jurisdiction] = "considering"
            else:
                compliance_status["jurisdictions"][jurisdiction] = "not_implementing"
        
        return compliance_status
    
    def _analyze_tax_treaties(self, treaty_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of tax treaties on Pillar Two calculations"""
        analysis = {
            "treaty_impact": {},
            "withholding_tax_implications": [],
            "permanent_establishment_issues": [],
            "recommendations": []
        }
        
        for treaty in treaty_data.get("treaties", []):
            if treaty.get("type") == "tax_treaty":
                analysis["treaty_impact"][treaty.get("country")] = {
                    "withholding_tax_rate": treaty.get("withholding_tax_rate"),
                    "permanent_establishment_threshold": treaty.get("pe_threshold")
                }
        
        return analysis
    
    def _calculate_sbie(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Substance-based income exclusion (SBIE)"""
        sbie_calculation = {
            "eligible_activities": [],
            "exclusion_amount": 0,
            "calculation_method": "5% of eligible payroll + 5% of eligible tangible assets"
        }
        
        # Calculate SBIE based on eligible activities
        eligible_payroll = entity_data.get("eligible_payroll", 0)
        eligible_assets = entity_data.get("eligible_tangible_assets", 0)
        
        sbie_calculation["exclusion_amount"] = (eligible_payroll * 0.05) + (eligible_assets * 0.05)
        
        return sbie_calculation
    
    def _analyze_qdmtt(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Qualified Domestic Minimum Top-up Tax (QDMTT) implications"""
        qdmtt_analysis = {
            "qdmtt_applicable": False,
            "qdmtt_rate": 0,
            "credit_available": False,
            "implications": []
        }
        
        # Check if QDMTT applies
        if entity_data.get("domestic_tax_rate", 0) < 15.0:
            qdmtt_analysis["qdmtt_applicable"] = True
            qdmtt_analysis["qdmtt_rate"] = 15.0 - entity_data.get("domestic_tax_rate", 0)
        
        return qdmtt_analysis
    
    def _analyze_iir_utpr(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Income Inclusion Rule (IIR) and Undertaxed Profits Rule (UTPR) applicability"""
        iir_utpr_analysis = {
            "iir_applicable": False,
            "utpr_applicable": False,
            "parent_entity_analysis": {},
            "constituent_entity_analysis": {},
            "recommendations": []
        }
        
        # Check if parent entity is in implementing jurisdiction
        parent_jurisdiction = entity_data.get("parent_jurisdiction", "")
        if parent_jurisdiction in self.memory["pillar_two_knowledge"]["jurisdictions"]["implementing"]:
            iir_utpr_analysis["iir_applicable"] = True
        
        # Check constituent entities
        for entity in entity_data.get("constituent_entities", []):
            if entity.get("etr", 0) < 15.0:
                iir_utpr_analysis["utpr_applicable"] = True
                break
        
        return iir_utpr_analysis
    
    def _assess_pillar_two_risks(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive risk assessment for Pillar Two compliance"""
        try:
            risks = {
                "high_risk": [],
                "medium_risk": [],
                "low_risk": [],
                "mitigation_strategies": []
            }
            
            # ETR volatility risk
            etr = entity_data.get("etr", 0)
            if etr < 12:
                risks["high_risk"].append("Low ETR - High exposure to Top-Up Tax")
                risks["mitigation_strategies"].append("Review tax planning strategies and consider Safe Harbour elections")
            
            # Jurisdictional risk
            jurisdiction = entity_data.get("jurisdiction", "")
            if jurisdiction in ["Brazil", "Mexico"]:
                risks["medium_risk"].append("Jurisdiction not yet implementing Pillar Two")
                risks["mitigation_strategies"].append("Monitor regulatory developments and prepare for implementation")
            
            # Compliance risk
            if not entity_data.get("qualified_status", False):
                risks["high_risk"].append("Entity not qualified for Safe Harbour")
                risks["mitigation_strategies"].append("Review qualification criteria and improve compliance")
            
            return risks
        except Exception as e:
            return {"error": f"Risk assessment failed: {str(e)}"}
    
    def _monitor_compliance_status(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor ongoing compliance status and regulatory changes"""
        try:
            compliance_status = {
                "current_status": "Compliant",
                "pending_actions": [],
                "regulatory_changes": [],
                "next_review_date": "2024-12-31"
            }
            
            # Check compliance indicators
            if entity_data.get("etr", 0) < 15:
                compliance_status["current_status"] = "At Risk"
                compliance_status["pending_actions"].append("Calculate and prepare Top-Up Tax payment")
            
            if not entity_data.get("safe_harbour", False):
                compliance_status["pending_actions"].append("Review Safe Harbour eligibility")
            
            return compliance_status
        except Exception as e:
            return {"error": f"Compliance monitoring failed: {str(e)}"}
    
    def _plan_mitigation_strategies(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop risk mitigation strategies and contingency plans"""
        try:
            strategies = {
                "immediate_actions": [],
                "short_term_plans": [],
                "long_term_plans": [],
                "contingency_plans": []
            }
            
            # Immediate actions for high risks
            if risk_data.get("high_risk"):
                strategies["immediate_actions"].append("Engage tax advisors for urgent review")
                strategies["immediate_actions"].append("Prepare Top-Up Tax calculations")
            
            # Short-term plans
            strategies["short_term_plans"].append("Implement enhanced compliance monitoring")
            strategies["short_term_plans"].append("Review and update tax planning strategies")
            
            # Long-term plans
            strategies["long_term_plans"].append("Develop comprehensive Pillar Two compliance framework")
            strategies["long_term_plans"].append("Establish regular risk assessment procedures")
            
            # Contingency plans
            strategies["contingency_plans"].append("Prepare for regulatory changes and new requirements")
            strategies["contingency_plans"].append("Establish backup compliance procedures")
            
            return strategies
        except Exception as e:
            return {"error": f"Mitigation planning failed: {str(e)}"}
    
    def _analyze_transfer_pricing(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze transfer pricing implications for Pillar Two compliance"""
        try:
            tp_analysis = {
                "arm_length_compliance": {},
                "high_risk_jurisdictions": [],
                "globe_income_adjustments": [],
                "oecd_guidelines_compliance": {},
                "documentation_mismatches": [],
                "recommendations": []
            }
            
            # Analyze intercompany transactions
            for transaction in entity_data.get("intercompany_transactions", []):
                jurisdiction = transaction.get("jurisdiction", "")
                transaction_type = transaction.get("type", "")
                arm_length_range = transaction.get("arm_length_range", [])
                actual_price = transaction.get("actual_price", 0)
                
                # Check if within arm's length range
                if arm_length_range and actual_price:
                    min_price, max_price = arm_length_range[0], arm_length_range[1]
                    if actual_price < min_price or actual_price > max_price:
                        tp_analysis["arm_length_compliance"][jurisdiction] = {
                            "status": "non_compliant",
                            "deviation": actual_price - ((min_price + max_price) / 2),
                            "transaction_type": transaction_type
                        }
                        
                        # Recommend GloBE Income adjustment
                        adjustment = {
                            "jurisdiction": jurisdiction,
                            "adjustment_type": "transfer_pricing",
                            "amount": actual_price - ((min_price + max_price) / 2),
                            "reason": f"Arm's length deviation in {transaction_type}"
                        }
                        tp_analysis["globe_income_adjustments"].append(adjustment)
            
            # Identify high-risk jurisdictions
            high_risk_jurisdictions = ["Brazil", "Mexico", "India", "China"]
            for jurisdiction in entity_data.get("operations", []):
                if jurisdiction in high_risk_jurisdictions:
                    tp_analysis["high_risk_jurisdictions"].append({
                        "jurisdiction": jurisdiction,
                        "risk_factors": ["Complex transfer pricing rules", "Aggressive enforcement"],
                        "recommendations": ["Enhanced documentation", "Local expert review"]
                    })
            
            return tp_analysis
        except Exception as e:
            return {"error": f"Transfer pricing analysis failed: {str(e)}"}
    
    def _parse_oecd_guidelines(self, guidelines_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and analyze OECD Transfer Pricing Guidelines"""
        try:
            guidelines_analysis = {
                "chapter_compliance": {},
                "methodology_application": {},
                "documentation_requirements": [],
                "risk_assessment": {}
            }
            
            # Analyze compliance with key chapters
            chapters = ["I", "II", "III", "IV", "V", "VI", "VII"]
            for chapter in chapters:
                guidelines_analysis["chapter_compliance"][chapter] = {
                    "status": "compliant",
                    "key_requirements": [],
                    "gaps": []
                }
            
            # Check methodology application
            methodologies = ["CUP", "Resale Minus", "Cost Plus", "TNMM", "Profit Split"]
            for method in methodologies:
                if method in guidelines_data.get("applied_methods", []):
                    guidelines_analysis["methodology_application"][method] = {
                        "appropriateness": "appropriate",
                        "documentation": "complete",
                        "risk_level": "low"
                    }
            
            return guidelines_analysis
        except Exception as e:
            return {"error": f"OECD guidelines parsing failed: {str(e)}"}
    
    def _scan_jurisdiction_risks(self, jurisdiction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scan jurisdictions for transfer pricing risk factors"""
        try:
            risk_scan = {
                "high_risk_jurisdictions": [],
                "medium_risk_jurisdictions": [],
                "low_risk_jurisdictions": [],
                "risk_factors": {},
                "mitigation_strategies": {}
            }
            
            # Define risk factors by jurisdiction
            jurisdiction_risks = {
                "Brazil": ["Complex TP rules", "Aggressive enforcement", "Documentation requirements"],
                "Mexico": ["TP audits", "Penalty regime", "Local file requirements"],
                "India": ["Detailed TP rules", "Safe harbor provisions", "Audit focus"],
                "China": ["TP documentation", "Local file requirements", "Audit intensity"],
                "Germany": ["Standard TP rules", "Moderate enforcement", "OECD compliance"],
                "Netherlands": ["Standard TP rules", "Moderate enforcement", "OECD compliance"]
            }
            
            for jurisdiction in jurisdiction_data.get("jurisdictions", []):
                if jurisdiction in jurisdiction_risks:
                    risk_level = "high" if jurisdiction in ["Brazil", "Mexico", "India", "China"] else "medium"
                    risk_scan["risk_factors"][jurisdiction] = jurisdiction_risks.get(jurisdiction, [])
                    
                    if risk_level == "high":
                        risk_scan["high_risk_jurisdictions"].append(jurisdiction)
                    elif risk_level == "medium":
                        risk_scan["medium_risk_jurisdictions"].append(jurisdiction)
                    else:
                        risk_scan["low_risk_jurisdictions"].append(jurisdiction)
            
            return risk_scan
        except Exception as e:
            return {"error": f"Jurisdiction risk scanning failed: {str(e)}"}
    
    def _web_search(self, query: str) -> str:
        """
        Search the web using Serper API for current information about OECD Pillar Two
        """
        try:
            if not self.serper_api_key:
                return "Error: SERPER_API_KEY not configured. Please set the environment variable."
            
            # Prepare the search query with OECD Pillar Two context
            enhanced_query = f"OECD Pillar Two {query} tax regulations 2024"
            
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': enhanced_query,
                'num': 5  # Get top 5 results
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract and format search results
                results = []
                if 'organic' in data:
                    for result in data['organic'][:5]:
                        title = result.get('title', '')
                        snippet = result.get('snippet', '')
                        link = result.get('link', '')
                        results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
                
                if results:
                    return f"Web search results for '{query}':\n\n" + "\n".join(results)
                else:
                    return f"No relevant web results found for '{query}'"
            else:
                return f"Error: Failed to search web. Status code: {response.status_code}"
                
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def _web_scrape(self, url: str) -> str:
        """
        Scrape content from a specific webpage
        """
        try:
            result = web_scraping_tools.scrape_webpage(url)
            if result.success:
                return f"Successfully scraped {url}\n\nTitle: {result.title}\n\nContent Preview: {result.content[:500]}..."
            else:
                return f"Failed to scrape {url}: {result.error_message}"
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"
    
    def _scrape_tax_rates(self, country: str = "israel") -> str:
        """
        Scrape tax rates from government websites
        """
        try:
            result = web_scraping_tools.scrape_tax_rates(country)
            if "error" not in result:
                return f"Tax rates for {country}:\n{result['content']}"
            else:
                return f"Failed to scrape tax rates for {country}: {result['error']}"
        except Exception as e:
            return f"Error scraping tax rates: {str(e)}"
    
    def _scrape_oecd_documents(self, document_type: str = "pillar-two") -> str:
        """
        Scrape OECD documents
        """
        try:
            result = web_scraping_tools.scrape_oecd_documents(document_type)
            if "error" not in result:
                return f"OECD {document_type} document:\n\nTitle: {result['title']}\n\nContent Preview: {result['content']}"
            else:
                return f"Failed to scrape OECD {document_type} document: {result['error']}"
        except Exception as e:
            return f"Error scraping OECD documents: {str(e)}"
    
    def _extract_specific_content(self, url: str, selectors: str) -> str:
        """
        Extract specific content using CSS selectors
        """
        try:
            # Parse selectors from string format
            import json
            selectors_dict = json.loads(selectors)
            
            result = web_scraping_tools.extract_specific_content(url, selectors_dict)
            if "error" not in result:
                return f"Extracted content from {url}:\n{json.dumps(result, indent=2)}"
            else:
                return f"Failed to extract content from {url}: {result['error']}"
        except Exception as e:
            return f"Error extracting specific content: {str(e)}"
    
    def _plan_implementation(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive implementation plans for Pillar Two compliance"""
        try:
            implementation_plan = {
                "immediate_actions": [],
                "short_term_plans": [],
                "long_term_plans": [],
                "contingency_plans": []
            }
            
            # Immediate actions for high risks
            if risk_data.get("high_risk"):
                implementation_plan["immediate_actions"].append("Engage tax advisors for urgent review")
                implementation_plan["immediate_actions"].append("Prepare Top-Up Tax calculations")
            
            # Short-term plans
            implementation_plan["short_term_plans"].append("Implement enhanced compliance monitoring")
            implementation_plan["short_term_plans"].append("Review and update tax planning strategies")
            
            # Long-term plans
            implementation_plan["long_term_plans"].append("Develop comprehensive Pillar Two compliance framework")
            implementation_plan["long_term_plans"].append("Establish regular risk assessment procedures")
            
            # Contingency plans
            implementation_plan["contingency_plans"].append("Prepare for regulatory changes and new requirements")
            implementation_plan["contingency_plans"].append("Establish backup compliance procedures")
            
            return implementation_plan
        except Exception as e:
            return {"error": f"Implementation planning failed: {str(e)}"}
    
    def analyze_pillar_two_compliance(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to analyze Pillar Two compliance with enhanced data processing"""
        try:
            # Initialize data processing components
            data_processor = FlexibleDataProcessor()
            validator = DataValidator()
            error_handler = EnhancedErrorHandler()
            
            # Process and validate input data
            if isinstance(financial_data, str):
                # Try to process as file path or JSON string
                try:
                    import json
                    parsed_data = json.loads(financial_data)
                    processing_result = data_processor.process_data(parsed_data)
                except json.JSONDecodeError:
                    # Treat as file path
                    processing_result = data_processor.process_file(financial_data)
            else:
                # Process as dictionary
                processing_result = data_processor.process_data(financial_data)
            
            # Check if data processing was successful
            if not processing_result["success"]:
                return {
                    "error": "Data processing failed",
                    "processing_error": processing_result["error"],
                    "suggestions": processing_result["error"].get("suggestions", [])
                }
            
            # Use processed data for analysis
            processed_data = processing_result["data"]
            validation_details = processing_result["validation_details"]
            
            # Perform comprehensive analysis
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "entity_name": processed_data.get("entity_name", "Unknown"),
                "data_processing_info": processing_result["processing_info"],
                "validation_details": validation_details,
                "etr_analysis": self._calculate_etr(processed_data),
                "tax_adjustments": self._analyze_tax_adjustments(processed_data),
                "safe_harbours": self._check_safe_harbours(processed_data),
                "compliance_status": self._check_compliance(processed_data),
                "sbie_calculation": self._calculate_sbie(processed_data),
                "qdmtt_analysis": self._analyze_qdmtt(processed_data),
                "iir_utpr_analysis": self._analyze_iir_utpr(processed_data),
                "risk_assessment": self._assess_pillar_two_risks(processed_data),
                "compliance_monitoring": self._monitor_compliance_status(processed_data),
                "mitigation_strategies": self._plan_mitigation_strategies(processed_data),
                "transfer_pricing_analysis": self._analyze_transfer_pricing(processed_data),
                "oecd_guidelines_compliance": self._parse_oecd_guidelines(processed_data),
                "jurisdiction_risk_scan": self._scan_jurisdiction_risks(processed_data),
                "recommendations": [],
                "data_quality_assessment": {
                    "source_format": processed_data.get("source_format", "unknown"),
                    "validation_passed": validation_details.get("is_valid", False),
                    "warnings": validation_details.get("warnings", []),
                    "suggestions": validation_details.get("suggestions", [])
                }
            }
            
            # Generate recommendations based on analysis
            etr_analysis = analysis["etr_analysis"]
            if "error" not in etr_analysis and etr_analysis.get("below_threshold"):
                analysis["recommendations"].append({
                    "priority": "high",
                    "category": "ETR_improvement",
                    "description": "Entity has ETR below 15% threshold. Consider tax planning strategies to improve ETR.",
                    "action_items": [
                        "Review tax structure and planning opportunities",
                        "Consider substance-based income exclusion",
                        "Evaluate safe harbour availability"
                    ]
                })
            
            # Add data quality recommendations
            if validation_details.get("warnings"):
                analysis["recommendations"].append({
                    "priority": "medium",
                    "category": "data_quality",
                    "description": "Data quality issues detected. Review and improve data accuracy.",
                    "action_items": [
                        "Verify financial data accuracy",
                        "Check for missing required fields",
                        "Validate data types and formats"
                    ]
                })
            
            return analysis
            
        except Exception as e:
            error_info = error_handler.handle_error(e, "pillar_two_analysis")
            return {
                "error": f"Pillar Two analysis failed: {error_info['error_message']}",
                "suggestions": error_info.get("suggestions", []),
                "error_category": error_info.get("error_category", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
    
    def create_crew(self) -> Crew:
        """Create a crew with the main agent and supporting team"""
        tasks = [
            Task(
                description="Analyze financial data for Pillar Two compliance",
                agent=self.agent,
                expected_output="Comprehensive Pillar Two compliance analysis report"
            ),
            Task(
                description="Review legal compliance across jurisdictions",
                agent=self.team[1],  # Legal Compliance Specialist
                expected_output="Legal compliance assessment and recommendations"
            ),
            Task(
                description="Assess implementation risks and provide mitigation strategies",
                agent=self.team[3],  # Risk Assessment Specialist
                expected_output="Risk assessment report with mitigation strategies"
            ),
            Task(
                description="Perform comprehensive risk assessment and develop mitigation plans",
                agent=self.agent,  # Using main agent with new risk tools
                expected_output="Detailed risk assessment with immediate actions and long-term strategies"
            ),
            Task(
                description="Analyze transfer pricing implications for Pillar Two compliance",
                agent=self.team[4],  # Transfer Pricing Specialist
                expected_output="Transfer pricing analysis with GloBE Income adjustments"
            )
        ]
        
        return Crew(
            agents=[self.agent] + self.team,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    pillar_two_master = PillarTwoMaster()
    
    # Example financial data
    sample_data = {
        "entity_name": "Sample Corp",
        "pre_tax_income": 1000000,
        "current_tax_expense": 120000,
        "deferred_tax_expense": 30000,
        "revenue": 50000000,
        "operations": ["EU", "UK", "Switzerland"],
        "parent_jurisdiction": "EU",
        "eligible_payroll": 2000000,
        "eligible_tangible_assets": 5000000,
        "domestic_tax_rate": 12.0,
        "adjustments": {
            "depreciation_difference": 50000,
            "provision_adjustment": 25000,
            "foreign_income_exclusion": 100000
        },
        "constituent_entities": [
            {"name": "Subsidiary A", "etr": 10.0},
            {"name": "Subsidiary B", "etr": 18.0}
        ]
    }
    
    # Perform analysis
    analysis_result = pillar_two_master.analyze_pillar_two_compliance(sample_data)
    
    # Print results
    print("Pillar Two Compliance Analysis Results:")
    print(json.dumps(analysis_result, indent=2))
