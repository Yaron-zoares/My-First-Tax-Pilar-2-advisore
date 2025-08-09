"""
QA Specialist Agent
Specialized agent for advanced Q&A capabilities with integration to existing agents
"""

from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import json
import logging
import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.enhanced_qa_engine import EnhancedQAEngine
from config.settings import settings
from .web_scraping_tools import web_scraping_tools

logger = logging.getLogger(__name__)

class QASpecialistAgent:
    """
    QA Specialist Agent - Advanced Q&A capabilities with agent integration
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.enhanced_qa_engine = EnhancedQAEngine(openai_api_key=self.openai_api_key)
        self.agent = self._create_agent()
        self.knowledge_base = self._load_comprehensive_knowledge()
        
        # Initialize Serper API key
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
    def _create_agent(self) -> Agent:
        """Create the QA Specialist agent"""
        agent = Agent(
            role="Advanced Q&A Specialist for OECD Pillar Two",
            goal="Provide comprehensive, accurate, and actionable answers to complex questions about OECD Pillar Two, tax calculations, compliance, and strategic planning",
            backstory="""You are a world-renowned expert in international taxation and OECD Pillar Two regulations with over 15 years of experience. 
            You have advised Fortune 500 companies, governments, and international organizations on implementing the global minimum tax framework.
            
            Your expertise includes:
            - Deep understanding of OECD Pillar Two Model Rules and Commentary
            - Advanced ETR calculations and adjustments
            - Comprehensive risk assessment and mitigation strategies
            - Strategic tax planning and optimization
            - Regulatory compliance and reporting requirements
            - Integration with other specialized agents for comprehensive analysis
            
            You provide practical, actionable advice while ensuring full regulatory compliance.""",
            verbose=True,
            allow_delegation=True,
            tools=self._get_tools()
        )
        
        return agent
    
    def _get_tools(self) -> List[Tool]:
        """Define tools available to the QA Specialist agent"""
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
                name="Enhanced_QA_Engine",
                func=self._enhanced_qa_analysis,
                description="Analyze questions using enhanced QA engine with ChatGPT 3.5 integration"
            ),
            Tool(
                name="Knowledge_Base_Search",
                func=self._search_knowledge_base,
                description="Search comprehensive knowledge base for relevant information"
            ),
            Tool(
                name="Question_Classification",
                func=self._classify_question,
                description="Classify question type and determine appropriate analysis approach"
            ),
            Tool(
                name="Risk_Assessment",
                func=self._assess_risks,
                description="Assess compliance and tax risks based on question context"
            ),
            Tool(
                name="Strategic_Recommendations",
                func=self._generate_recommendations,
                description="Generate strategic recommendations and next steps"
            ),
            Tool(
                name="Agent_Integration",
                func=self._integrate_with_agents,
                description="Integrate with other specialized agents for comprehensive analysis"
            ),
            Tool(
                name="Compliance_Check",
                func=self._check_compliance,
                description="Check regulatory compliance with OECD Pillar Two requirements"
            ),
            Tool(
                name="Data_Analysis",
                func=self._analyze_financial_data,
                description="Analyze financial data for tax implications and compliance"
            )
        ]
    
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
    
    def _load_comprehensive_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive knowledge base"""
        return {
            'pillar_two_rules': {
                'description': 'OECD Pillar Two Global Minimum Tax Rules',
                'sources': [
                    'OECD Pillar Two Model Rules',
                    'OECD Commentary on Pillar Two',
                    'Administrative Guidance',
                    'Safe Harbour Provisions',
                    'GloBE Information Return (GIR) Requirements'
                ],
                'key_concepts': [
                    'Effective Tax Rate (ETR)',
                    'Top-Up Tax',
                    'Income Inclusion Rule (IIR)',
                    'Undertaxed Profits Rule (UTPR)',
                    'Qualified Domestic Minimum Top-up Tax (QDMTT)',
                    'Substance-based Income Exclusion (SBIE)'
                ]
            },
            'tax_calculations': {
                'description': 'Advanced Tax Calculations and Adjustments',
                'sources': [
                    'IFRS Standards',
                    'Local GAAP',
                    'Tax Accounting Standards',
                    'Deferred Tax Accounting',
                    'Timing Differences'
                ],
                'key_concepts': [
                    'ETR Calculation Methods',
                    'Covered Taxes',
                    'GloBE Income',
                    'Tax Adjustments',
                    'Deferred Tax Assets/Liabilities'
                ]
            },
            'compliance_requirements': {
                'description': 'Regulatory Compliance and Reporting',
                'sources': [
                    'OECD Transfer Pricing Guidelines',
                    'BEPS Action Plan',
                    'Country-by-Country Reporting',
                    'Local Tax Authority Requirements'
                ],
                'key_concepts': [
                    'Compliance Deadlines',
                    'Reporting Requirements',
                    'Documentation Standards',
                    'Penalty Provisions'
                ]
            },
            'risk_management': {
                'description': 'Risk Assessment and Mitigation Strategies',
                'sources': [
                    'Enterprise Risk Management',
                    'Tax Risk Assessment',
                    'Compliance Risk Management'
                ],
                'key_concepts': [
                    'Risk Identification',
                    'Risk Assessment',
                    'Mitigation Strategies',
                    'Monitoring and Review'
                ]
            },
            'strategic_planning': {
                'description': 'Strategic Tax Planning and Optimization',
                'sources': [
                    'International Tax Planning',
                    'Business Restructuring',
                    'Tax Optimization Strategies'
                ],
                'key_concepts': [
                    'Tax Planning Strategies',
                    'Business Restructuring',
                    'Optimization Opportunities',
                    'Implementation Planning'
                ]
            }
        }
    
    def _enhanced_qa_analysis(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze question using enhanced QA engine"""
        try:
            # Prepare context
            if context is None:
                context = {}
            
            # Get enhanced answer
            response = self.enhanced_qa_engine.ask_enhanced_question(
                question=question,
                language=context.get('language', 'en')
            )
            
            # Add analysis metadata
            response['analysis_timestamp'] = datetime.now().isoformat()
            response['question_complexity'] = self._assess_question_complexity(question)
            response['knowledge_sources_used'] = self._identify_used_sources(question)
            
            return response
            
        except Exception as e:
            logger.error(f"Enhanced QA analysis error: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _search_knowledge_base(self, query: str, category: str = None) -> Dict[str, Any]:
        """Search knowledge base for relevant information"""
        try:
            results = {}
            
            if category and category in self.knowledge_base:
                # Search specific category
                category_data = self.knowledge_base[category]
                results[category] = {
                    'description': category_data['description'],
                    'sources': category_data['sources'],
                    'key_concepts': category_data['key_concepts'],
                    'relevance_score': self._calculate_relevance(query, category_data)
                }
            else:
                # Search all categories
                for cat_name, cat_data in self.knowledge_base.items():
                    relevance_score = self._calculate_relevance(query, cat_data)
                    if relevance_score > 0.3:  # Only include relevant results
                        results[cat_name] = {
                            'description': cat_data['description'],
                            'sources': cat_data['sources'],
                            'key_concepts': cat_data['key_concepts'],
                            'relevance_score': relevance_score
                        }
            
            # Sort by relevance
            results = dict(sorted(results.items(), key=lambda x: x[1]['relevance_score'], reverse=True))
            
            return {
                'search_results': results,
                'total_results': len(results),
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Knowledge base search error: {str(e)}")
            return {'error': str(e)}
    
    def _classify_question(self, question: str) -> Dict[str, Any]:
        """Classify question type and determine analysis approach"""
        try:
            # Use enhanced QA engine classification
            question_type = self.enhanced_qa_engine._classify_enhanced_question(question.lower())
            
            # Determine complexity
            complexity = self._assess_question_complexity(question)
            
            # Identify required analysis components
            analysis_components = self._identify_analysis_components(question, question_type)
            
            return {
                'question_type': question_type,
                'complexity_level': complexity,
                'analysis_components': analysis_components,
                'requires_agent_integration': complexity in ['high', 'very_high'],
                'estimated_analysis_time': self._estimate_analysis_time(complexity)
            }
            
        except Exception as e:
            logger.error(f"Question classification error: {str(e)}")
            return {'error': str(e)}
    
    def _assess_risks(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Assess compliance and tax risks"""
        try:
            risks = {
                'compliance_risks': [],
                'tax_risks': [],
                'operational_risks': [],
                'reputational_risks': [],
                'overall_risk_level': 'low'
            }
            
            # Analyze question for risk indicators
            risk_indicators = self._identify_risk_indicators(question)
            
            # Assess compliance risks
            if any(indicator in question.lower() for indicator in ['compliance', 'regulatory', 'violation']):
                risks['compliance_risks'].append({
                    'risk_type': 'Regulatory Non-Compliance',
                    'description': 'Potential violation of OECD Pillar Two regulations',
                    'severity': 'medium',
                    'mitigation': 'Implement compliance monitoring and reporting systems'
                })
            
            # Assess tax risks
            if any(indicator in question.lower() for indicator in ['tax', 'etr', 'top-up']):
                risks['tax_risks'].append({
                    'risk_type': 'Tax Calculation Errors',
                    'description': 'Risk of incorrect ETR calculations or Top-Up Tax assessments',
                    'severity': 'high',
                    'mitigation': 'Implement robust tax calculation and review processes'
                })
            
            # Determine overall risk level
            risk_levels = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
            max_severity = max([risk_levels[risk['severity']] for risk_list in risks.values() 
                              for risk in risk_list if isinstance(risk, dict)], default=1)
            
            risks['overall_risk_level'] = [k for k, v in risk_levels.items() if v == max_severity][0]
            
            return risks
            
        except Exception as e:
            logger.error(f"Risk assessment error: {str(e)}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, question: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic recommendations and next steps"""
        try:
            recommendations = {
                'immediate_actions': [],
                'short_term_actions': [],
                'long_term_actions': [],
                'priority_level': 'medium'
            }
            
            # Generate recommendations based on question type and analysis
            question_type = analysis_results.get('question_type', 'general')
            
            if question_type == 'pillar_two_compliance':
                recommendations['immediate_actions'].extend([
                    'Conduct comprehensive compliance assessment',
                    'Review current ETR calculations',
                    'Identify potential Top-Up Tax exposure'
                ])
                recommendations['short_term_actions'].extend([
                    'Implement compliance monitoring systems',
                    'Develop reporting procedures',
                    'Train staff on Pillar Two requirements'
                ])
                recommendations['long_term_actions'].extend([
                    'Establish ongoing compliance framework',
                    'Develop risk management strategies',
                    'Create contingency plans'
                ])
            
            elif question_type == 'tax_calculations':
                recommendations['immediate_actions'].extend([
                    'Review current tax calculation methodologies',
                    'Validate ETR calculations',
                    'Identify calculation errors or inconsistencies'
                ])
                recommendations['short_term_actions'].extend([
                    'Implement calculation review processes',
                    'Develop calculation documentation',
                    'Establish quality control procedures'
                ])
            
            elif question_type == 'strategic_planning':
                recommendations['immediate_actions'].extend([
                    'Conduct strategic tax planning assessment',
                    'Identify optimization opportunities',
                    'Evaluate current tax structure'
                ])
                recommendations['short_term_actions'].extend([
                    'Develop strategic tax planning roadmap',
                    'Implement optimization strategies',
                    'Monitor effectiveness of changes'
                ])
            
            # Set priority level
            if len(recommendations['immediate_actions']) > 3:
                recommendations['priority_level'] = 'high'
            elif len(recommendations['immediate_actions']) == 0:
                recommendations['priority_level'] = 'low'
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendations generation error: {str(e)}")
            return {'error': str(e)}
    
    def _integrate_with_agents(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Integrate with other specialized agents for comprehensive analysis"""
        try:
            integration_results = {
                'agents_consulted': [],
                'integrated_analysis': {},
                'consolidated_recommendations': []
            }
            
            # Determine which agents to consult based on question
            agents_to_consult = self._identify_relevant_agents(question)
            
            for agent_type in agents_to_consult:
                agent_analysis = self._consult_agent(agent_type, question, context)
                if agent_analysis:
                    integration_results['agents_consulted'].append(agent_type)
                    integration_results['integrated_analysis'][agent_type] = agent_analysis
            
            # Consolidate recommendations from all agents
            integration_results['consolidated_recommendations'] = self._consolidate_agent_recommendations(
                integration_results['integrated_analysis']
            )
            
            return integration_results
            
        except Exception as e:
            logger.error(f"Agent integration error: {str(e)}")
            return {'error': str(e)}
    
    def _check_compliance(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Check regulatory compliance with OECD Pillar Two requirements"""
        try:
            compliance_check = {
                'compliance_status': 'unknown',
                'compliance_issues': [],
                'compliance_score': 0.0,
                'required_actions': []
            }
            
            # Analyze question for compliance indicators
            compliance_indicators = self._identify_compliance_indicators(question)
            
            # Check specific compliance areas
            if 'etr' in question.lower() or 'effective tax rate' in question.lower():
                compliance_check['compliance_issues'].append({
                    'area': 'ETR Calculation',
                    'issue': 'Ensure ETR calculations follow OECD guidelines',
                    'severity': 'medium',
                    'action': 'Review ETR calculation methodology'
                })
            
            if 'top-up' in question.lower() or 'topup' in question.lower():
                compliance_check['compliance_issues'].append({
                    'area': 'Top-Up Tax',
                    'issue': 'Verify Top-Up Tax calculation and payment requirements',
                    'severity': 'high',
                    'action': 'Assess Top-Up Tax exposure and payment obligations'
                })
            
            if 'gir' in question.lower() or 'report' in question.lower():
                compliance_check['compliance_issues'].append({
                    'area': 'GIR Reporting',
                    'issue': 'Ensure GIR reporting compliance',
                    'severity': 'high',
                    'action': 'Review GIR reporting requirements and deadlines'
                })
            
            # Calculate compliance score
            if not compliance_check['compliance_issues']:
                compliance_check['compliance_score'] = 1.0
                compliance_check['compliance_status'] = 'compliant'
            else:
                severity_weights = {'low': 0.1, 'medium': 0.3, 'high': 0.6, 'critical': 0.9}
                total_weight = sum(severity_weights[issue['severity']] for issue in compliance_check['compliance_issues'])
                compliance_check['compliance_score'] = max(0.0, 1.0 - total_weight)
                
                if compliance_check['compliance_score'] >= 0.8:
                    compliance_check['compliance_status'] = 'compliant'
                elif compliance_check['compliance_score'] >= 0.6:
                    compliance_check['compliance_status'] = 'mostly_compliant'
                else:
                    compliance_check['compliance_status'] = 'non_compliant'
            
            # Generate required actions
            compliance_check['required_actions'] = [
                issue['action'] for issue in compliance_check['compliance_issues']
            ]
            
            return compliance_check
            
        except Exception as e:
            logger.error(f"Compliance check error: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_financial_data(self, question: str, data_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze financial data for tax implications and compliance"""
        try:
            analysis = {
                'data_insights': [],
                'tax_implications': [],
                'compliance_indicators': [],
                'risk_factors': []
            }
            
            # Analyze question for data requirements
            data_requirements = self._identify_data_requirements(question)
            
            # If we have data context, analyze it
            if data_context and 'data_summary' in data_context:
                data_summary = data_context['data_summary']
                
                if data_summary.get('status') == 'available':
                    # Analyze financial columns
                    financial_columns = data_summary.get('financial_columns', [])
                    if financial_columns:
                        analysis['data_insights'].append({
                            'insight': f"Found {len(financial_columns)} financial columns for analysis",
                            'columns': financial_columns
                        })
                    
                    # Analyze data quality
                    missing_values = data_summary.get('missing_values', {})
                    if missing_values:
                        high_missing = {k: v for k, v in missing_values.items() if v > 0}
                        if high_missing:
                            analysis['risk_factors'].append({
                                'factor': 'Data Quality Issues',
                                'description': f"Missing values in {len(high_missing)} columns",
                                'impact': 'May affect accuracy of tax calculations'
                            })
            
            # Add tax implications based on question
            if 'etr' in question.lower():
                analysis['tax_implications'].append({
                    'implication': 'ETR Calculation Required',
                    'description': 'Question requires effective tax rate calculation',
                    'data_needs': ['revenue', 'tax_expense', 'profit_before_tax']
                })
            
            if 'top-up' in question.lower():
                analysis['tax_implications'].append({
                    'implication': 'Top-Up Tax Assessment',
                    'description': 'Question requires Top-Up Tax calculation',
                    'data_needs': ['etr', 'globe_income', 'covered_taxes']
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Financial data analysis error: {str(e)}")
            return {'error': str(e)}
    
    # Helper methods
    def _assess_question_complexity(self, question: str) -> str:
        """Assess question complexity level"""
        word_count = len(question.split())
        
        if word_count > 20:
            return 'very_high'
        elif word_count > 15:
            return 'high'
        elif word_count > 10:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_relevance(self, query: str, category_data: Dict[str, Any]) -> float:
        """Calculate relevance score for knowledge base search"""
        query_lower = query.lower()
        relevance_score = 0.0
        
        # Check description
        if any(word in category_data['description'].lower() for word in query_lower.split()):
            relevance_score += 0.3
        
        # Check key concepts
        for concept in category_data['key_concepts']:
            if any(word in concept.lower() for word in query_lower.split()):
                relevance_score += 0.2
        
        # Check sources
        for source in category_data['sources']:
            if any(word in source.lower() for word in query_lower.split()):
                relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    def _identify_analysis_components(self, question: str, question_type: str) -> List[str]:
        """Identify required analysis components"""
        components = ['basic_qa']
        
        if question_type in ['pillar_two_compliance', 'regulatory_analysis']:
            components.extend(['compliance_check', 'risk_assessment'])
        
        if question_type in ['tax_calculations', 'strategic_planning']:
            components.extend(['data_analysis', 'strategic_recommendations'])
        
        if 'risk' in question.lower() or 'exposure' in question.lower():
            components.append('risk_assessment')
        
        if 'recommend' in question.lower() or 'strategy' in question.lower():
            components.append('strategic_recommendations')
        
        return components
    
    def _estimate_analysis_time(self, complexity: str) -> str:
        """Estimate analysis time based on complexity"""
        time_estimates = {
            'low': '1-2 minutes',
            'medium': '3-5 minutes',
            'high': '5-10 minutes',
            'very_high': '10-15 minutes'
        }
        return time_estimates.get(complexity, 'unknown')
    
    def _identify_risk_indicators(self, question: str) -> List[str]:
        """Identify risk indicators in question"""
        risk_keywords = [
            'risk', 'exposure', 'violation', 'penalty', 'non-compliance',
            'error', 'mistake', 'failure', 'breach', 'sanction'
        ]
        return [keyword for keyword in risk_keywords if keyword in question.lower()]
    
    def _identify_relevant_agents(self, question: str) -> List[str]:
        """Identify relevant agents to consult"""
        agents = []
        
        if 'tax' in question.lower() or 'etr' in question.lower():
            agents.append('tax_modeler')
        
        if 'legal' in question.lower() or 'compliance' in question.lower():
            agents.append('legal_interpreter')
        
        if 'risk' in question.lower() or 'assessment' in question.lower():
            agents.append('risk_analyst')
        
        if 'xml' in question.lower() or 'report' in question.lower():
            agents.append('xml_reporter')
        
        return agents
    
    def _consult_agent(self, agent_type: str, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Consult with specific agent type"""
        # This would integrate with the actual agent system
        # For now, return placeholder analysis
        return {
            'agent_type': agent_type,
            'analysis_provided': True,
            'recommendations': [f"Recommendation from {agent_type} agent"],
            'confidence': 0.8
        }
    
    def _consolidate_agent_recommendations(self, integrated_analysis: Dict[str, Any]) -> List[str]:
        """Consolidate recommendations from multiple agents"""
        consolidated = []
        
        for agent_type, analysis in integrated_analysis.items():
            if 'recommendations' in analysis:
                consolidated.extend(analysis['recommendations'])
        
        return consolidated
    
    def _identify_compliance_indicators(self, question: str) -> List[str]:
        """Identify compliance indicators in question"""
        compliance_keywords = [
            'compliance', 'regulatory', 'requirement', 'obligation',
            'deadline', 'filing', 'report', 'documentation'
        ]
        return [keyword for keyword in compliance_keywords if keyword in question.lower()]
    
    def _identify_data_requirements(self, question: str) -> List[str]:
        """Identify data requirements for question"""
        data_keywords = [
            'revenue', 'income', 'tax', 'profit', 'expense',
            'etr', 'globe', 'covered', 'financial'
        ]
        return [keyword for keyword in data_keywords if keyword in question.lower()]
    
    def _identify_used_sources(self, question: str) -> List[str]:
        """Identify knowledge sources used for question"""
        used_sources = []
        
        for category, data in self.knowledge_base.items():
            if self._calculate_relevance(question, data) > 0.3:
                used_sources.extend(data['sources'])
        
        return list(set(used_sources))  # Remove duplicates
    
    def answer_comprehensive_question(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Answer comprehensive question with full agent capabilities"""
        try:
            # Start comprehensive analysis
            analysis_results = {
                'question': question,
                'timestamp': datetime.now().isoformat(),
                'analysis_steps': []
            }
            
            # Step 1: Classify question
            classification = self._classify_question(question)
            analysis_results['classification'] = classification
            analysis_results['analysis_steps'].append('question_classification')
            
            # Step 2: Enhanced QA analysis
            qa_analysis = self._enhanced_qa_analysis(question, context)
            analysis_results['qa_analysis'] = qa_analysis
            analysis_results['analysis_steps'].append('enhanced_qa_analysis')
            
            # Step 3: Knowledge base search
            knowledge_search = self._search_knowledge_base(question, classification.get('question_type'))
            analysis_results['knowledge_search'] = knowledge_search
            analysis_results['analysis_steps'].append('knowledge_base_search')
            
            # Step 4: Risk assessment
            risk_assessment = self._assess_risks(question, context)
            analysis_results['risk_assessment'] = risk_assessment
            analysis_results['analysis_steps'].append('risk_assessment')
            
            # Step 5: Compliance check
            compliance_check = self._check_compliance(question, context)
            analysis_results['compliance_check'] = compliance_check
            analysis_results['analysis_steps'].append('compliance_check')
            
            # Step 6: Generate recommendations
            recommendations = self._generate_recommendations(question, analysis_results)
            analysis_results['recommendations'] = recommendations
            analysis_results['analysis_steps'].append('recommendations_generation')
            
            # Step 7: Agent integration (if complex question)
            if classification.get('requires_agent_integration', False):
                agent_integration = self._integrate_with_agents(question, context)
                analysis_results['agent_integration'] = agent_integration
                analysis_results['analysis_steps'].append('agent_integration')
            
            # Step 8: Financial data analysis
            if context and 'data_summary' in context:
                data_analysis = self._analyze_financial_data(question, context)
                analysis_results['data_analysis'] = data_analysis
                analysis_results['analysis_steps'].append('financial_data_analysis')
            
            # Calculate overall confidence
            confidence_scores = []
            if 'qa_analysis' in analysis_results and 'confidence' in analysis_results['qa_analysis']:
                confidence_scores.append(analysis_results['qa_analysis']['confidence'])
            
            analysis_results['overall_confidence'] = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.7
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Comprehensive question answering error: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed',
                'question': question
            }
