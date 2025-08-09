#!/usr/bin/env python3
"""
Simple Agents Report Display Script
Generates and displays comprehensive reports about all agents in the Pillar Two system
Without CrewAI dependencies to avoid import issues
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class SimpleAgentsReportDisplay:
    """Display comprehensive reports about all agents in the system without CrewAI dependencies"""
    
    def __init__(self):
        self.report_data = {}
        self.timestamp = datetime.now().isoformat()
        
    def generate_agents_overview(self) -> Dict[str, Any]:
        """Generate overview of all agents in the system"""
        overview = {
            "timestamp": self.timestamp,
            "total_agents": 0,
            "agents_by_category": {},
            "system_status": "operational",
            "available_workflows": []
        }
        
        # Main Pillar Two Master Agent (static info)
        overview["agents_by_category"]["main_agent"] = {
            "name": "PillarTwoMaster",
            "role": "OECD Pillar Two Tax Expert",
            "status": "configured",
            "tools_count": 16,
            "team_members": 5,
            "capabilities": [
                "ETR calculations",
                "Tax adjustments analysis",
                "GIR XML generation",
                "Safe Harbour checking",
                "Country-by-country analysis",
                "Regulatory compliance checking",
                "Tax treaty analysis",
                "SBIE calculations",
                "QDMTT analysis",
                "IIR/UTPR analysis",
                "Risk assessment",
                "Compliance monitoring",
                "Mitigation planning",
                "Transfer pricing analysis",
                "OECD guidelines parsing",
                "Jurisdiction risk scanning"
            ]
        }
        overview["total_agents"] += 1
        
        # Team Members
        team_members = [
            {
                "name": "Financial Data Analyst",
                "role": "Analyze financial statements and extract relevant data",
                "specialization": "Financial statement analysis and accounting standards"
            },
            {
                "name": "Legal Compliance Specialist", 
                "role": "Ensure legal compliance across jurisdictions",
                "specialization": "International tax law and regulatory compliance"
            },
            {
                "name": "Technical Implementation Expert",
                "role": "Provide practical implementation guidance",
                "specialization": "Tax systems and processes implementation"
            },
            {
                "name": "Risk Assessment Specialist",
                "role": "Identify and assess implementation risks",
                "specialization": "Tax risk assessment and mitigation strategies"
            },
            {
                "name": "Transfer Pricing Specialist",
                "role": "Analyze transfer pricing implications",
                "specialization": "Transfer pricing and international taxation"
            }
        ]
        
        overview["agents_by_category"]["team_members"] = {
            "count": len(team_members),
            "members": team_members
        }
        overview["total_agents"] += len(team_members)
        
        # YAML-based Agents
        yaml_agents = [
            {
                "name": "tax_modeler",
                "role": "Tax simulation builder based on ETR and Top-Up",
                "goal": "Building advanced models for calculating ETR and Top-Up Tax",
                "tools": ["excel_analyzer", "etr_calculator", "topup_simulator"]
            },
            {
                "name": "legal_interpreter", 
                "role": "Interpreter of Commentary and Guidance",
                "goal": "Legal interpretation of OECD Pillar Two rules",
                "tools": ["pdf_extractor", "file_reader", "legal_analyzer"]
            },
            {
                "name": "xml_reporter",
                "role": "GIR report generator according to XML Schema",
                "goal": "Creating valid GIR reports according to OECD XML Schema",
                "tools": ["xml_validator", "gir_generator", "schema_checker"]
            },
            {
                "name": "risk_analyst",
                "role": "Risk Assessment and Mitigation Specialist",
                "goal": "Comprehensive risk analysis and mitigation strategies",
                "tools": ["risk_assessor", "compliance_monitor", "mitigation_planner"]
            },
            {
                "name": "transfer_pricing_specialist",
                "role": "Transfer Pricing Analysis Specialist",
                "goal": "Comprehensive transfer pricing analysis for Pillar Two compliance",
                "tools": ["transfer_pricing_analyzer", "oecd_guidelines_parser", "jurisdiction_risk_scanner"]
            }
        ]
        
        overview["agents_by_category"]["yaml_agents"] = {
            "count": len(yaml_agents),
            "agents": yaml_agents
        }
        overview["total_agents"] += len(yaml_agents)
        
        # Available Workflows
        overview["available_workflows"] = [
            "financial_analysis",
            "legal_review", 
            "xml_generation",
            "risk_assessment",
            "transfer_pricing_analysis"
        ]
        
        return overview
    
    def generate_tools_report(self) -> Dict[str, Any]:
        """Generate detailed report of all available tools"""
        tools_report = {
            "timestamp": self.timestamp,
            "total_tools": 0,
            "tools_by_category": {},
            "tool_details": {}
        }
        
        # Financial Analysis Tools
        financial_tools = [
            {
                "name": "ETR_Calculator",
                "description": "Calculate Effective Tax Rate (ETR) based on financial data",
                "category": "financial_analysis",
                "status": "active"
            },
            {
                "name": "Tax_Adjustment_Analyzer", 
                "description": "Analyze and categorize tax adjustments for Pillar Two compliance",
                "category": "financial_analysis",
                "status": "active"
            },
            {
                "name": "SBIE_Calculator",
                "description": "Calculate Substance-based income exclusion (SBIE) for qualifying activities",
                "category": "financial_analysis", 
                "status": "active"
            },
            {
                "name": "QDMTT_Analyzer",
                "description": "Analyze Qualified Domestic Minimum Top-up Tax (QDMTT) implications",
                "category": "financial_analysis",
                "status": "active"
            }
        ]
        
        # Compliance Tools
        compliance_tools = [
            {
                "name": "Safe_Harbour_Checker",
                "description": "Check if company qualifies for Safe Harbours under Pillar Two rules",
                "category": "compliance",
                "status": "active"
            },
            {
                "name": "Regulatory_Compliance_Checker",
                "description": "Check regulatory compliance with Pillar Two requirements across jurisdictions",
                "category": "compliance",
                "status": "active"
            },
            {
                "name": "Compliance_Monitor",
                "description": "Monitor and track compliance status across jurisdictions",
                "category": "compliance",
                "status": "active"
            }
        ]
        
        # Reporting Tools
        reporting_tools = [
            {
                "name": "GIR_XML_Generator",
                "description": "Generate Global Information Return (GIR) XML files according to OECD schema",
                "category": "reporting",
                "status": "active"
            },
            {
                "name": "Country_By_Country_Analyzer",
                "description": "Analyze country-by-country reporting data for Pillar Two implications",
                "category": "reporting",
                "status": "active"
            }
        ]
        
        # Risk Assessment Tools
        risk_tools = [
            {
                "name": "Risk_Assessor",
                "description": "Assess comprehensive Pillar Two compliance risks and exposure",
                "category": "risk_assessment",
                "status": "active"
            },
            {
                "name": "Mitigation_Planner",
                "description": "Plan and recommend risk mitigation strategies",
                "category": "risk_assessment",
                "status": "active"
            }
        ]
        
        # Transfer Pricing Tools
        tp_tools = [
            {
                "name": "Transfer_Pricing_Analyzer",
                "description": "Analyze transfer pricing structures and arm's length compliance",
                "category": "transfer_pricing",
                "status": "active"
            },
            {
                "name": "OECD_Guidelines_Parser",
                "description": "Parse and interpret OECD Transfer Pricing Guidelines",
                "category": "transfer_pricing",
                "status": "active"
            },
            {
                "name": "Jurisdiction_Risk_Scanner",
                "description": "Scan jurisdictions for transfer pricing and compliance risks",
                "category": "transfer_pricing",
                "status": "active"
            }
        ]
        
        # Legal Analysis Tools
        legal_tools = [
            {
                "name": "Tax_Treaty_Analyzer",
                "description": "Analyze impact of tax treaties on Pillar Two calculations",
                "category": "legal_analysis",
                "status": "active"
            },
            {
                "name": "IIR_UTPR_Analyzer",
                "description": "Analyze Income Inclusion Rule (IIR) and Undertaxed Profits Rule (UTPR)",
                "category": "legal_analysis",
                "status": "active"
            }
        ]
        
        # Organize tools by category
        tools_report["tools_by_category"] = {
            "financial_analysis": {
                "count": len(financial_tools),
                "tools": financial_tools
            },
            "compliance": {
                "count": len(compliance_tools),
                "tools": compliance_tools
            },
            "reporting": {
                "count": len(reporting_tools),
                "tools": reporting_tools
            },
            "risk_assessment": {
                "count": len(risk_tools),
                "tools": risk_tools
            },
            "transfer_pricing": {
                "count": len(tp_tools),
                "tools": tp_tools
            },
            "legal_analysis": {
                "count": len(legal_tools),
                "tools": legal_tools
            }
        }
        
        # Calculate total tools
        for category in tools_report["tools_by_category"].values():
            tools_report["total_tools"] += category["count"]
        
        return tools_report
    
    def generate_system_status_report(self) -> Dict[str, Any]:
        """Generate system status and performance report"""
        status_report = {
            "timestamp": self.timestamp,
            "system_health": "operational",
            "components": {},
            "performance_metrics": {},
            "recent_activities": []
        }
        
        # Check report directories
        report_dirs = ["reports/pdf", "reports/xml", "reports/word"]
        for dir_path in report_dirs:
            try:
                dir_exists = os.path.exists(dir_path)
                files_count = len(os.listdir(dir_path)) if dir_exists else 0
                status_report["components"][f"report_directory_{dir_path.split('/')[-1]}"] = {
                    "status": "operational" if dir_exists else "missing",
                    "exists": dir_exists,
                    "files_count": files_count
                }
            except Exception as e:
                status_report["components"][f"report_directory_{dir_path.split('/')[-1]}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Check agent files
        agent_files = [
            "agents/pillar_two_master.py",
            "agents/report_generator.py",
            "agents/crew_config.yaml",
            "agents/tasks_config.yaml"
        ]
        
        for file_path in agent_files:
            try:
                file_exists = os.path.exists(file_path)
                status_report["components"][f"agent_file_{file_path.split('/')[-1]}"] = {
                    "status": "operational" if file_exists else "missing",
                    "exists": file_exists
                }
            except Exception as e:
                status_report["components"][f"agent_file_{file_path.split('/')[-1]}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return status_report
    
    def display_report(self, report_type: str = "all"):
        """Display the agents report in a formatted way"""
        print("=" * 80)
        print("🤖 PILLAR TWO AGENTS SYSTEM REPORT")
        print("=" * 80)
        print(f"Generated: {self.timestamp}")
        print()
        
        if report_type in ["all", "overview"]:
            self._display_overview()
        
        if report_type in ["all", "tools"]:
            self._display_tools_report()
        
        if report_type in ["all", "status"]:
            self._display_status_report()
        
        print("=" * 80)
        print("📊 Report generation completed")
        print("=" * 80)
    
    def _display_overview(self):
        """Display agents overview"""
        print("📋 AGENTS OVERVIEW")
        print("-" * 40)
        
        overview = self.generate_agents_overview()
        
        print(f"Total Agents: {overview['total_agents']}")
        print(f"System Status: {overview['system_status'].upper()}")
        print()
        
        # Main Agent
        main_agent = overview["agents_by_category"].get("main_agent", {})
        print("🎯 MAIN AGENT:")
        print(f"  Name: {main_agent['name']}")
        print(f"  Role: {main_agent['role']}")
        print(f"  Tools: {main_agent['tools_count']}")
        print(f"  Team Members: {main_agent['team_members']}")
        print(f"  Capabilities: {len(main_agent['capabilities'])} functions")
        print()
        
        # Team Members
        team = overview["agents_by_category"].get("team_members", {})
        print("👥 TEAM MEMBERS:")
        for member in team["members"]:
            print(f"  • {member['name']} - {member['role']}")
        print()
        
        # YAML Agents
        yaml_agents = overview["agents_by_category"].get("yaml_agents", {})
        print("⚙️ YAML-CONFIGURED AGENTS:")
        for agent in yaml_agents["agents"]:
            print(f"  • {agent['name']} - {agent['role']}")
            print(f"    Tools: {', '.join(agent['tools'])}")
        print()
        
        # Available Workflows
        if overview["available_workflows"]:
            print("🔄 AVAILABLE WORKFLOWS:")
            for workflow in overview["available_workflows"]:
                print(f"  • {workflow}")
        
        print()
    
    def _display_tools_report(self):
        """Display tools report"""
        print("🛠️ TOOLS INVENTORY")
        print("-" * 40)
        
        tools_report = self.generate_tools_report()
        
        print(f"Total Tools: {tools_report['total_tools']}")
        print()
        
        for category, data in tools_report["tools_by_category"].items():
            print(f"📁 {category.upper().replace('_', ' ')} ({data['count']} tools):")
            for tool in data["tools"]:
                status_icon = "✅" if tool["status"] == "active" else "❌"
                print(f"  {status_icon} {tool['name']}")
                print(f"     {tool['description']}")
            print()
    
    def _display_status_report(self):
        """Display system status report"""
        print("🔍 SYSTEM STATUS")
        print("-" * 40)
        
        status_report = self.generate_system_status_report()
        
        print(f"Overall Health: {status_report['system_health'].upper()}")
        print()
        
        for component, info in status_report["components"].items():
            if info["status"] == "operational":
                print(f"✅ {component.replace('_', ' ').title()}")
                for key, value in info.items():
                    if key != "status":
                        print(f"    {key}: {value}")
            else:
                print(f"❌ {component.replace('_', ' ').title()}")
                print(f"    Error: {info.get('error', 'Unknown error')}")
            print()
    
    def save_report_to_file(self, filename: str = None) -> str:
        """Save comprehensive report to JSON file"""
        if filename is None:
            filename = f"agents_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "overview": self.generate_agents_overview(),
            "tools": self.generate_tools_report(),
            "status": self.generate_system_status_report()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            print(f"Error saving report: {e}")
            return ""

def main():
    """Main function to run the agents report display"""
    display = SimpleAgentsReportDisplay()
    
    # Display the report
    display.display_report("all")
    
    # Save to file
    saved_file = display.save_report_to_file()
    if saved_file:
        print(f"📄 Report saved to: {saved_file}")
    
    return display

if __name__ == "__main__":
    main()
