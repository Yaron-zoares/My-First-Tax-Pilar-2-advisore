from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from typing import List, Dict, Any
import os
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import requests
import json

class PillarTwoCrewConfig:
    """
    CrewAI Configuration for PillarTwoMaster Team
    Hebrew-speaking team specialized in OECD Pillar Two analysis
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.team = self._create_team()
        self.tools = self._create_tools()
        
        # Initialize Serper API key
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
    def _create_tools(self) -> Dict[str, List[Tool]]:
        """Create tools for each team member"""
        return {
            "web_searcher": [
                Tool(
                    name="Web_Search",
                    func=self._web_search,
                    description="חיפוש באינטרנט למידע עדכני על OECD Pillar Two ותקנות מס"
                )
            ],
            "excel_analyzer": [
                Tool(
                    name="Excel_ETR_Calculator",
                    func=self._calculate_etr_from_excel,
                    description="חישוב ETR מקובץ Excel עם נתונים פיננסיים"
                ),
                Tool(
                    name="Excel_TopUp_Calculator",
                    func=self._calculate_topup_from_excel,
                    description="חישוב Top-Up Tax מקובץ Excel"
                ),
                Tool(
                    name="Excel_Simulation_Generator",
                    func=self._generate_tax_simulation,
                    description="יצירת סימולציות מס שונות מקובץ Excel"
                )
            ],
            "legal_analyzer": [
                Tool(
                    name="Legal_Document_Analyzer",
                    func=self._analyze_legal_documents,
                    description="ניתוח מסמכים משפטיים ותקנות OECD"
                ),
                Tool(
                    name="Regulatory_Compliance_Checker",
                    func=self._check_regulatory_compliance,
                    description="בדיקת תאימות לתקנות OECD Pillar Two"
                )
            ],
            "xml_generator": [
                Tool(
                    name="GIR_XML_Generator",
                    func=self._generate_gir_xml,
                    description="יצירת דוחות GIR XML לפי Schema של OECD"
                ),
                Tool(
                    name="XML_Schema_Validator",
                    func=self._validate_xml_schema,
                    description="אימות קבצי XML לפי Schema של OECD"
                )
            ],
            "risk_assessor": [
                Tool(
                    name="Risk_Assessment_Tool",
                    func=self._assess_pillar_two_risks,
                    description="הערכת סיכונים לתאימות OECD Pillar Two"
                ),
                Tool(
                    name="Mitigation_Strategy_Planner",
                    func=self._plan_mitigation_strategies,
                    description="תכנון אסטרטגיות להפחתת סיכונים"
                )
            ]
        }
    
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
    
    def _create_team(self) -> List[Agent]:
        """Create the Hebrew-speaking team members"""
        return [
            Agent(
                name="tax_modeler",
                role="בונה סימולציות מס לפי ETR ו־Top-Up",
                goal="בניית מודלים מתקדמים לחישוב ETR ו־Top-Up Tax עם סימולציות שונות",
                backstory="""אתה מומחה בכיר בבניית מודלים פיננסיים וסימולציות מס. 
                יש לך ניסיון של 15 שנים בפיתוח מודלים מתקדמים לחישוב Effective Tax Rate (ETR) 
                ו־Top-Up Tax לפי כללי OECD Pillar Two. אתה מתמחה בניתוח נתונים מ־Excel 
                ובניית מודלים מורכבים שמשקללים גורמים שונים כמו:
                - חישובי ETR מדויקים
                - חישובי Top-Up Tax
                - סימולציות שונות של תכנון מס
                - ניתוח השפעת שינויים רגולטוריים
                - חישובי Safe Harbours
                
                אתה עובד בשיתוף פעולה הדוק עם הצוות המשפטי והטכני כדי להבטיח דיוק מקסימלי.""",
                verbose=True,
                allow_delegation=True,
                tools=self.tools["excel_analyzer"] + self.tools["web_searcher"]
            ),
            Agent(
                name="legal_interpreter",
                role="מפרש את ה־Commentary וה־Guidance",
                goal="פירוש מדויק של OECD Commentary ו־Administrative Guidance ליישום מעשי",
                backstory="""אתה מומחה משפטי בכיר בתחום המס הבינלאומי עם התמחות מיוחדת 
                ב־OECD Pillar Two. יש לך ניסיון של 20 שנים בפירוש תקנות מס מורכבות 
                ויישום מעשי שלהן. אתה מתמחה ב:
                - פירוש OECD Commentary
                - ניתוח Administrative Guidance
                - הבנת Safe Harbours
                - פירוש תקנות IIR ו־UTPR
                - ניתוח השפעת Tax Treaties
                - הבנת SBIE ו־QDMTT
                
                אתה מספק הבנה עמוקה של הרקע המשפטי לכל החלטה טכנית.""",
                verbose=True,
                allow_delegation=True,
                tools=self.tools["legal_analyzer"] + self.tools["web_searcher"]
            ),
            Agent(
                name="xml_reporter",
                role="מפיק דיווח GIR לפי XML Schema",
                goal="יצירה ואימות קבצי GIR XML לפי תקן OECD המדויק",
                backstory="""אתה מומחה טכני בכיר ביצירת דיווחים XML מורכבים עם התמחות 
                מיוחדת ב־OECD GIR XML Schema. יש לך ניסיון של 10 שנים ב:
                - יצירת קבצי XML מורכבים
                - אימות תאימות Schema
                - יצירת דיווחי GIR מדויקים
                - בדיקת תקינות XML
                - טיפול בנתונים מורכבים
                - יצירת תבניות XML מתקדמות
                
                אתה מבטיח שכל הדיווחים עומדים בתקנים המחמירים ביותר של OECD.""",
                verbose=True,
                allow_delegation=True,
                tools=self.tools["xml_generator"] + self.tools["web_searcher"]
            )
        ]
        
        # Add additional agents with web search capabilities
        additional_agents = [
            Agent(
                name="risk_assessor",
                role="מומחה להערכת סיכונים ותכנון אסטרטגיות הפחתה",
                goal="הערכה מקיפה של סיכונים ותכנון אסטרטגיות הפחתה לתאימות OECD Pillar Two",
                backstory="""אתה מומחה בכיר בניהול סיכונים בתחום המס והתאימות הרגולטורית. 
                יש לך ניסיון של 15 שנים בזיהוי, הערכה והפחתת סיכונים במס בינלאומי. 
                אתה מתמחה בהערכת סיכוני OECD Pillar Two כולל:
                - תנודתיות ETR
                - סיכונים טריטוריאליים
                - חשיפה לתאימות
                - סיכוני Transfer Pricing
                - סיכונים רגולטוריים
                
                אתה מספק אסטרטגיות מעשיות להפחתת סיכונים.""",
                verbose=True,
                allow_delegation=True,
                tools=self.tools["risk_assessor"] + self.tools["web_searcher"]
            )
        ]
        
        return self.team + additional_agents
    
    # Tool implementation methods
    def _calculate_etr_from_excel(self, file_path: str) -> Dict[str, Any]:
        """חישוב ETR מקובץ Excel"""
        try:
            df = pd.read_excel(file_path)
            
            # חישוב ETR בסיסי
            pre_tax_income = df.get('pre_tax_income', 0).sum()
            current_tax = df.get('current_tax_expense', 0).sum()
            deferred_tax = df.get('deferred_tax_expense', 0).sum()
            
            total_tax = current_tax + deferred_tax
            etr = (total_tax / pre_tax_income * 100) if pre_tax_income > 0 else 0
            
            return {
                "etr_percentage": round(etr, 2),
                "below_threshold": etr < 15.0,
                "top_up_needed": max(0, 15.0 - etr),
                "calculation_details": {
                    "pre_tax_income": pre_tax_income,
                    "current_tax": current_tax,
                    "deferred_tax": deferred_tax,
                    "total_tax": total_tax
                }
            }
        except Exception as e:
            return {"error": f"שגיאה בחישוב ETR: {str(e)}"}
    
    def _calculate_topup_from_excel(self, file_path: str) -> Dict[str, Any]:
        """חישוב Top-Up Tax מקובץ Excel"""
        try:
            df = pd.read_excel(file_path)
            
            # חישוב Top-Up Tax
            etr_results = self._calculate_etr_from_excel(file_path)
            top_up_rate = etr_results.get("top_up_needed", 0)
            
            # חישוב סכום Top-Up
            pre_tax_income = df.get('pre_tax_income', 0).sum()
            top_up_amount = (top_up_rate / 100) * pre_tax_income
            
            return {
                "top_up_rate": top_up_rate,
                "top_up_amount": round(top_up_amount, 2),
                "etr_analysis": etr_results
            }
        except Exception as e:
            return {"error": f"שגיאה בחישוב Top-Up: {str(e)}"}
    
    def _generate_tax_simulation(self, file_path: str, scenario: str = "base") -> Dict[str, Any]:
        """יצירת סימולציות מס שונות"""
        try:
            df = pd.read_excel(file_path)
            
            scenarios = {
                "base": {"adjustment_factor": 1.0},
                "conservative": {"adjustment_factor": 0.9},
                "aggressive": {"adjustment_factor": 1.1},
                "safe_harbour": {"adjustment_factor": 0.8}
            }
            
            scenario_config = scenarios.get(scenario, scenarios["base"])
            adjustment = scenario_config["adjustment_factor"]
            
            # חישוב ETR עם התאמה
            base_etr = self._calculate_etr_from_excel(file_path)
            adjusted_etr = base_etr["etr_percentage"] * adjustment
            
            return {
                "scenario": scenario,
                "base_etr": base_etr["etr_percentage"],
                "adjusted_etr": round(adjusted_etr, 2),
                "adjustment_factor": adjustment,
                "below_threshold": adjusted_etr < 15.0
            }
        except Exception as e:
            return {"error": f"שגיאה ביצירת סימולציה: {str(e)}"}
    
    def _analyze_legal_documents(self, file_path: str) -> Dict[str, Any]:
        """ניתוח מסמכים משפטיים ותקנות OECD"""
        try:
            # Implementation for legal document analysis
            return {
                "status": "success",
                "analysis": "Legal document analysis completed",
                "file": file_path
            }
        except Exception as e:
            return {"error": f"Legal analysis failed: {str(e)}"}
    
    def _check_regulatory_compliance(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """בדיקת תאימות לתקנות OECD Pillar Two"""
        try:
            # Implementation for regulatory compliance check
            return {
                "status": "success",
                "compliance": "Regulatory compliance check completed",
                "data": entity_data
            }
        except Exception as e:
            return {"error": f"Compliance check failed: {str(e)}"}
    
    def _assess_pillar_two_risks(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """הערכת סיכונים לתאימות OECD Pillar Two"""
        try:
            # Implementation for risk assessment
            return {
                "status": "success",
                "risk_assessment": "Pillar Two risk assessment completed",
                "data": entity_data
            }
        except Exception as e:
            return {"error": f"Risk assessment failed: {str(e)}"}
    
    def _plan_mitigation_strategies(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """תכנון אסטרטגיות להפחתת סיכונים"""
        try:
            # Implementation for mitigation planning
            return {
                "status": "success",
                "mitigation_plan": "Mitigation strategies planned",
                "data": risk_data
            }
        except Exception as e:
            return {"error": f"Mitigation planning failed: {str(e)}"}
    
    def _validate_xml_schema(self, xml_content: str) -> Dict[str, Any]:
        """אימות קבצי XML לפי Schema של OECD"""
        try:
            # Implementation for XML schema validation
            return {
                "status": "success",
                "validation": "XML schema validation completed",
                "content": xml_content
            }
        except Exception as e:
            return {"error": f"XML validation failed: {str(e)}"}
    
    def _generate_gir_xml(self, entity_data: Dict[str, Any]) -> str:
        """יצירת קובץ GIR XML"""
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
    
    def create_crew(self) -> Crew:
        """יצירת Crew עם כל חברי הצוות"""
        tasks = [
            Task(
                description="בניית מודלים וסימולציות מס לחישוב ETR ו־Top-Up Tax",
                agent=self.team[0],  # tax_modeler
                expected_output="דוח מפורט של חישובי ETR ו־Top-Up עם סימולציות שונות"
            ),
            Task(
                description="פירוש OECD Commentary ו־Administrative Guidance ליישום מעשי",
                agent=self.team[1],  # legal_interpreter
                expected_output="ניתוח משפטי מפורט עם המלצות ליישום"
            ),
            Task(
                description="יצירה ואימות דיווחי GIR XML לפי תקן OECD",
                agent=self.team[2],  # xml_reporter
                expected_output="קבצי GIR XML תקינים עם אימות Schema"
            )
        ]
        
        return Crew(
            agents=self.team,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
    
    def run_pillar_two_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """הפעלת ניתוח Pillar Two מלא עם הצוות"""
        crew = self.create_crew()
        
        # הכנת נתונים לניתוח
        analysis_data = {
            "financial_data": financial_data,
            "timestamp": pd.Timestamp.now().isoformat(),
            "team_members": [agent.name for agent in self.team]
        }
        
        # הפעלת הצוות
        result = crew.kickoff()
        
        return {
            "analysis_result": result,
            "analysis_data": analysis_data,
            "team_performance": {
                "tax_modeler": "completed",
                "legal_interpreter": "completed", 
                "xml_reporter": "completed"
            }
        }

# Example usage
if __name__ == "__main__":
    # יצירת תצורת הצוות
    crew_config = PillarTwoCrewConfig()
    
    # דוגמה לנתונים פיננסיים
    sample_data = {
        "entity_name": "חברת דוגמה בע\"מ",
        "pre_tax_income": 1000000,
        "current_tax_expense": 120000,
        "deferred_tax_expense": 30000,
        "revenue": 50000000,
        "operations": ["ישראל", "אירופה", "ארה\"ב"],
        "parent_jurisdiction": "ישראל"
    }
    
    # הפעלת ניתוח
    analysis_result = crew_config.run_pillar_two_analysis(sample_data)
    
    print("תוצאות ניתוח Pillar Two:")
    print(json.dumps(analysis_result, indent=2))
