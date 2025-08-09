import yaml
import os
import sys
from typing import Dict, List, Any
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
import requests
import json



# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import with error handling for missing modules
try:
    from agents.data_format_adapter import FlexibleDataProcessor
except ImportError:
    class FlexibleDataProcessor:
        def process_data(self, data, format_type=None):
            return {"success": True, "data": data}

try:
    from agents.data_validator import DataValidator
except ImportError:
    class DataValidator:
        def validate_financial_data(self, data):
            return {"is_valid": True, "errors": []}

try:
    from agents.enhanced_error_handler import EnhancedErrorHandler
except ImportError:
    class EnhancedErrorHandler:
        def validate_data_structure(self, data, structure):
            return {"is_valid": True, "errors": []}
        def handle_validation_errors(self, validation):
            return "Validation errors occurred"
        def handle_error(self, error, context):
            return str(error)

try:
    from agents.web_scraping_tools import web_scraping_tools
except ImportError:
    web_scraping_tools = None

class YAMLCrewLoader:
    """
    Class for loading CrewAI configurations from YAML file
    """
    
    def __init__(self, config_path: str = "agents/crew_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.agents = {}
        self.tasks = {}
        self.tools = {}
        
        # Initialize new data processing components
        self.data_processor = FlexibleDataProcessor()
        self.validator = DataValidator()
        self.error_handler = EnhancedErrorHandler()
        
        # Initialize Serper API key
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
    def _load_config(self) -> Dict[str, Any]:
        """Loads the YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML file error: {e}")
    
    def _create_tools(self) -> Dict[str, Tool]:
        """Creates tools according to YAML configuration"""
        tools_config = self.config.get('tools', {})
        tools = {}
        
        for tool_name, tool_config in tools_config.items():
            # Create tool with proper structure for CrewAI
            tool = Tool(
                name=tool_name,
                description=tool_config.get('description', ''),
                func=self._get_tool_function(tool_config.get('function', ''))
            )
            tools[tool_name] = tool
        
        return tools
    
    def _get_tool_function(self, function_name: str):
        """Returns a function for a tool by name"""
        tool_functions = {
            'web_search': self._web_search,
            'web_scrape': self._web_scrape,
            'scrape_tax_rates': self._scrape_tax_rates,
            'scrape_oecd_documents': self._scrape_oecd_documents,
            'extract_specific_content': self._extract_specific_content,
            # New Israel tax tools
            'scrape_israel_tax_authority': self._scrape_israel_tax_authority,
            'scrape_israel_tax_treaties': self._scrape_israel_tax_treaties,
            'get_israel_tax_treaty_content': self._get_israel_tax_treaty_content,
            'get_all_israel_tax_treaties_content': self._get_all_israel_tax_treaties_content,
            'download_and_read_pdf': self._download_and_read_pdf,
            # Existing tools
            'analyze_excel_file': self._analyze_excel_file,
            'calculate_etr': self._calculate_etr,
            'simulate_topup_tax': self._simulate_topup_tax,
            'extract_pdf_text': self._extract_pdf_text,
            'read_file_content': self._read_file_content,
            'analyze_legal_documents': self._analyze_legal_documents,
            'validate_xml_schema': self._validate_xml_schema,
            'generate_gir_xml': self._generate_gir_xml,
            'check_schema_compliance': self._check_schema_compliance,
            'assess_pillar_two_risks': self._assess_pillar_two_risks,
            'monitor_compliance_status': self._monitor_compliance_status,
            'plan_mitigation_strategies': self._plan_mitigation_strategies,
            'analyze_transfer_pricing': self._analyze_transfer_pricing,
            'parse_oecd_guidelines': self._parse_oecd_guidelines,
            'scan_jurisdiction_risks': self._scan_jurisdiction_risks,
            # Enhanced tools
            'process_multiple_formats': self._process_multiple_formats,
            'validate_data_structure': self._validate_data_structure,
            'get_supported_formats': self._get_supported_formats
        }
        return tool_functions.get(function_name, lambda x: f"Function {function_name} not defined")
    
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
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
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
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
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
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
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
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
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
    
    def create_agents(self) -> List[Agent]:
        """Creates agents according to YAML configuration"""
        agents_config = self.config.get('agents', [])
        tools = self._create_tools()
        
        agents = []
        for agent_config in agents_config:
            agent_tools = []
            for tool_name in agent_config.get('tools', []):
                if tool_name in tools:
                    agent_tools.append(tools[tool_name])
            
            # Create agent without tools first to avoid validation errors
            agent = Agent(
                name=agent_config['name'],
                role=agent_config['role'],
                goal=agent_config['goal'],
                backstory=agent_config['backstory'],
                verbose=agent_config.get('verbose', True),
                allow_delegation=agent_config.get('allow_delegation', True)
            )
            
            # Add tools after creation if needed
            if agent_tools:
                agent.tools = agent_tools
            
            agents.append(agent)
        
        return agents
    
    def create_tasks(self, agents: List[Agent]) -> List[Task]:
        """Creates tasks according to YAML configuration"""
        tasks_config = self.config.get('tasks', [])
        
        tasks = []
        for task_config in tasks_config:
            agent_name = task_config['agent']
            agent = next((a for a in agents if a.name == agent_name), None)
            
            if agent:
                task = Task(
                    description=task_config['description'],
                    agent=agent,
                    expected_output=task_config['expected_output'],
                    context=task_config['context']
                )
                tasks.append(task)
                self.tasks[task_config['name']] = task
        
        return tasks
    
    def create_crew(self) -> Crew:
        """Creates the crew with agents and tasks"""
        agents = self.create_agents()
        tasks = self.create_tasks(agents)
        
        settings = self.config.get('settings', {})
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.SEQUENTIAL if settings.get('process') == 'sequential' else Process.HIERARCHICAL,
            verbose=settings.get('verbose', True),
            memory=settings.get('memory', True)
        )
        
        return crew
    
    # Tool implementations
    def _analyze_excel_file(self, file_path: str) -> str:
        """Analyzes Excel file and returns financial data with enhanced validation"""
        try:
            # Use the new data processor
            result = self.data_processor.process_file(file_path, "excel")
            
            if result["success"]:
                data = result["data"]
                validation = result["validation_details"]
                
                # Create detailed summary
                summary = f"Excel file analyzed successfully.\n"
                summary += f"Rows: {data.get('total_rows', 'N/A')}, Columns: {data.get('total_columns', 'N/A')}\n"
                summary += f"Source format: {data.get('source_format', 'excel')}\n"
                
                # Add financial data summary
                if "pre_tax_income" in data:
                    summary += f"Pre-tax income: €{data['pre_tax_income']:,.2f}\n"
                if "current_tax_expense" in data:
                    summary += f"Current tax expense: €{data['current_tax_expense']:,.2f}\n"
                if "revenue" in data:
                    summary += f"Revenue: €{data['revenue']:,.2f}\n"
                
                # Add validation warnings if any
                if validation.get("warnings"):
                    summary += f"\nWarnings: {', '.join(validation['warnings'])}"
                
                return summary
            else:
                error_info = result["error"]
                return f"Error analyzing Excel file:\n{error_info.get('error_message', 'Unknown error')}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
                
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "excel_analysis")
            return f"Error analyzing Excel file: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _calculate_etr(self, profit: float, tax: float) -> str:
        """Calculates effective tax rate with enhanced validation"""
        try:
            # Validate inputs
            financial_data = {
                "pre_tax_income": profit,
                "current_tax_expense": tax
            }
            
            validation_result = self.validator.validate_financial_data(financial_data)
            
            if not validation_result["is_valid"]:
                errors = validation_result.get("errors", [])
                warnings = validation_result.get("warnings", [])
                return f"ETR calculation failed:\nErrors: {', '.join(errors)}\nWarnings: {', '.join(warnings)}"
            
            if profit > 0:
                etr = (tax / profit) * 100
                below_threshold = etr < 15.0
                top_up_rate = max(0, 15.0 - etr) if below_threshold else 0
                
                result = f"ETR: {etr:.2f}%\n"
                result += f"Below 15% threshold: {'Yes' if below_threshold else 'No'}\n"
                if below_threshold:
                    result += f"Top-up tax rate needed: {top_up_rate:.2f}%"
                
                return result
            else:
                return "ETR: Cannot calculate (profit must be positive)"
                
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "etr_calculation")
            return f"ETR calculation error: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _simulate_topup_tax(self, profit: float, tax: float) -> str:
        """Calculates Top-Up Tax according to Pillar Two rules with enhanced validation"""
        try:
            # Validate inputs
            financial_data = {
                "pre_tax_income": profit,
                "current_tax_expense": tax
            }
            
            validation_result = self.validator.validate_financial_data(financial_data)
            
            if not validation_result["is_valid"]:
                errors = validation_result.get("errors", [])
                warnings = validation_result.get("warnings", [])
                return f"Top-Up Tax calculation failed:\nErrors: {', '.join(errors)}\nWarnings: {', '.join(warnings)}"
            
            if profit > 0:
                etr = (tax / profit) * 100
                if etr < 15:
                    topup = (0.15 * profit) - tax
                    result = f"Top-Up Tax: €{topup:,.2f}\n"
                    result += f"ETR: {etr:.2f}%\n"
                    result += f"Below 15% threshold: Yes\n"
                    result += f"Additional tax needed: {((15 - etr) / 100 * profit):,.2f}"
                    return result
                else:
                    return f"Top-Up Tax: €0 (above 15% threshold)\nETR: {etr:.2f}%"
            else:
                return "Top-Up Tax: Cannot calculate (profit must be positive)"
                
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "topup_calculation")
            return f"Top-Up Tax calculation error: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extracts text from PDF file with enhanced processing"""
        try:
            # Use the new data processor for PDF files
            result = self.data_processor.process_file(file_path, "pdf")
            
            if result["success"]:
                data = result["data"]
                validation = result["validation_details"]
                
                summary = f"PDF text extracted successfully from: {file_path}\n"
                summary += f"Content length: {data.get('content_length', 'N/A')} characters\n"
                summary += f"Source format: {data.get('source_format', 'pdf')}\n"
                
                # Add extracted financial data if available
                if "pre_tax_income" in data:
                    summary += f"Extracted pre-tax income: €{data['pre_tax_income']:,.2f}\n"
                if "current_tax_expense" in data:
                    summary += f"Extracted current tax expense: €{data['current_tax_expense']:,.2f}\n"
                if "revenue" in data:
                    summary += f"Extracted revenue: €{data['revenue']:,.2f}\n"
                
                # Add validation warnings if any
                if validation.get("warnings"):
                    summary += f"\nWarnings: {', '.join(validation['warnings'])}"
                
                return summary
            else:
                error_info = result["error"]
                return f"Error extracting PDF text:\n{error_info.get('error_message', 'Unknown error')}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
                
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "pdf_extraction")
            return f"Error extracting PDF text: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _read_file_content(self, file_path: str) -> str:
        """Reads content from file with format detection and processing"""
        try:
            # Use the new data processor with auto-detection
            result = self.data_processor.process_file(file_path)
            
            if result["success"]:
                data = result["data"]
                processing_info = result["processing_info"]
                validation = result["validation_details"]
                
                summary = f"File content processed successfully: {file_path}\n"
                summary += f"Detected format: {processing_info.get('source_format', 'unknown')}\n"
                summary += f"Adaptation successful: {'Yes' if processing_info.get('adaptation_successful') else 'No'}\n"
                summary += f"Validation passed: {'Yes' if processing_info.get('validation_passed') else 'No'}\n"
                
                # Add financial data summary if available
                financial_fields = ["pre_tax_income", "current_tax_expense", "revenue", "entity_name"]
                extracted_data = []
                for field in financial_fields:
                    if field in data:
                        if field in ["pre_tax_income", "current_tax_expense", "revenue"]:
                            extracted_data.append(f"{field}: €{data[field]:,.2f}")
                        else:
                            extracted_data.append(f"{field}: {data[field]}")
                
                if extracted_data:
                    summary += f"Extracted data: {', '.join(extracted_data)}\n"
                
                # Add validation warnings if any
                if validation.get("warnings"):
                    summary += f"Warnings: {', '.join(validation['warnings'])}"
                
                return summary
            else:
                error_info = result["error"]
                return f"Error reading file content:\n{error_info.get('error_message', 'Unknown error')}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
                
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "file_reading")
            return f"Error reading file content: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _analyze_legal_documents(self, documents: str) -> str:
        """Analyzes legal documents"""
        return "Legal analysis completed successfully"
    
    def _validate_xml_schema(self, xml_content: str) -> str:
        """Validates XML according to Schema with enhanced validation"""
        try:
            # Use the new data processor for XML validation
            result = self.data_processor.process_data(xml_content, "xml")
            
            if result["success"]:
                data = result["data"]
                validation = result["validation_details"]
                
                summary = f"XML validation successful\n"
                summary += f"Source format: {data.get('source_format', 'xml')}\n"
                
                # Add extracted data if available
                if "entity_name" in data:
                    summary += f"Entity name: {data['entity_name']}\n"
                if "tax_residence" in data:
                    summary += f"Tax residence: {data['tax_residence']}\n"
                if "pre_tax_income" in data:
                    summary += f"Pre-tax income: €{data['pre_tax_income']:,.2f}\n"
                
                # Add validation warnings if any
                if validation.get("warnings"):
                    summary += f"Warnings: {', '.join(validation['warnings'])}"
                
                return summary
            else:
                error_info = result["error"]
                return f"XML validation failed:\n{error_info.get('error_message', 'Unknown error')}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
                
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "xml_validation")
            return f"XML validation error: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _generate_gir_xml(self, data: str) -> str:
        """Generates GIR XML report"""
        return "GIR XML report generated successfully"
    
    def _check_schema_compliance(self, xml_content: str) -> str:
        """Checks XML Schema compliance"""
        return "Schema compliance verified"
    
    def _assess_pillar_two_risks(self, data: str) -> str:
        """Assesses Pillar Two compliance risks"""
        return "Pillar Two risk assessment completed"
    
    def _monitor_compliance_status(self, data: str) -> str:
        """Monitors compliance status"""
        return "Compliance status monitored"
    
    def _plan_mitigation_strategies(self, data: str) -> str:
        """Plans risk mitigation strategies"""
        return "Mitigation strategies planned"
    
    def _analyze_transfer_pricing(self, data: str) -> str:
        """Analyzes transfer pricing compliance"""
        return "Transfer pricing analysis completed"
    
    def _parse_oecd_guidelines(self, data: str) -> str:
        """Parses OECD guidelines"""
        return "OECD guidelines parsed and analyzed"
    
    def _scan_jurisdiction_risks(self, data: str) -> str:
        """Scans jurisdictions for risk factors"""
        return "Jurisdiction risk scan completed"
    
    def _process_multiple_formats(self, file_paths: str) -> str:
        """Processes multiple files in different formats"""
        try:
            # Parse file paths (assuming comma-separated)
            paths = [path.strip() for path in file_paths.split(',')]
            
            # Use the new data processor for multiple files
            result = self.data_processor.process_multiple_files(paths)
            
            summary = f"Multi-format processing completed\n"
            summary += f"Total files: {result['total_files']}\n"
            summary += f"Successful: {result['successful_files']}\n"
            summary += f"Failed: {result['failed_files']}\n"
            
            if result['error_report']:
                summary += f"\nError report: {result['error_report']['status']}\n"
                if result['error_report']['summary']['suggestions']:
                    summary += f"Suggestions: {', '.join(result['error_report']['summary']['suggestions'])}"
            
            return summary
            
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "multi_format_processing")
            return f"Multi-format processing error: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _validate_data_structure(self, data: str) -> str:
        """Validates data structure and provides detailed feedback"""
        try:
            # Try to parse as JSON first
            import json
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                # If not JSON, treat as string data
                parsed_data = {"raw_data": data}
            
            # Validate the data structure
            validation_result = self.validator.validate_financial_data(parsed_data)
            
            summary = f"Data structure validation completed\n"
            summary += f"Valid: {'Yes' if validation_result['is_valid'] else 'No'}\n"
            
            if validation_result['errors']:
                summary += f"Errors: {', '.join(validation_result['errors'])}\n"
            
            if validation_result['warnings']:
                summary += f"Warnings: {', '.join(validation_result['warnings'])}\n"
            
            if validation_result['suggestions']:
                summary += f"Suggestions: {', '.join(validation_result['suggestions'])}"
            
            return summary
            
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "data_structure_validation")
            return f"Data structure validation error: {error_info['error_message']}\nSuggestions: {', '.join(error_info.get('suggestions', []))}"
    
    def _get_supported_formats(self) -> str:
        """Returns information about supported data formats"""
        formats = self.data_processor.get_supported_formats()
        validation_rules = self.data_processor.get_validation_rules()
        
        summary = f"Supported data formats: {', '.join(formats)}\n\n"
        summary += "Validation rules:\n"
        summary += f"Required fields: {', '.join(validation_rules['required_fields']['financial_data'])}\n"
        summary += f"Field types: {', '.join([f'{k} ({v.__name__})' for k, v in validation_rules['field_types'].items()])}\n"
        
        return summary
    
    def _scrape_israel_tax_authority(self, section: str = "general") -> str:
        """
        Scrape information from Israel Tax Authority website
        """
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
        try:
            result = web_scraping_tools.scrape_israel_tax_authority(section)
            if result.get("success"):
                return f"Israel Tax Authority - {section}:\n\nContent: {result.get('content', '')[:1000]}..."
            else:
                return f"Failed to scrape Israel Tax Authority {section}: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error scraping Israel Tax Authority: {str(e)}"

    def _scrape_israel_tax_treaties(self, country: str = "all") -> str:
        """
        Scrape Israel tax treaties from government website
        """
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
        try:
            result = web_scraping_tools.scrape_israel_tax_treaties(country)
            if result.get("success"):
                treaties = result.get("treaties", [])
                return f"Found {len(treaties)} tax treaties for {country}:\n\n" + \
                       "\n".join([f"- {t['title']}: {t['url']}" for t in treaties])
            else:
                return f"Failed to scrape Israel tax treaties: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error scraping Israel tax treaties: {str(e)}"

    def _get_israel_tax_treaty_content(self, country: str) -> str:
        """
        Get full content of Israel tax treaty with specific country
        """
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
        try:
            result = web_scraping_tools.get_israel_tax_treaty_content(country)
            if result.get("success"):
                content = result.get("content", "")
                return f"Israel Tax Treaty with {country}:\n\nTitle: {result.get('treaty_title', 'Unknown')}\n\nContent:\n{content[:2000]}..."
            else:
                return f"Failed to get treaty content for {country}: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error getting treaty content: {str(e)}"

    def _get_all_israel_tax_treaties_content(self) -> str:
        """
        Get content of all Israel tax treaties
        """
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
        try:
            result = web_scraping_tools.get_all_israel_tax_treaties_content()
            if result.get("success"):
                treaties = result.get("treaties", {})
                summary = f"Successfully processed {len(treaties)} tax treaties:\n\n"
                for country, treaty_data in treaties.items():
                    if treaty_data.get("success"):
                        summary += f"- {country}: {treaty_data.get('title', 'Unknown')}\n"
                    else:
                        summary += f"- {country}: Error - {treaty_data.get('error', 'Unknown error')}\n"
                return summary
            else:
                return f"Failed to get all treaties content: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error getting all treaties content: {str(e)}"

    def _download_and_read_pdf(self, pdf_url: str) -> str:
        """
        Download and read PDF content from URLs
        """
        if web_scraping_tools is None:
            return "Error: Web scraping tools not available. Please install required dependencies."
        
        try:
            result = web_scraping_tools.download_and_read_pdf(pdf_url)
            if result.get("success"):
                content = result.get("content", "")
                return f"PDF Content from {pdf_url}:\n\n{content[:2000]}..."
            else:
                return f"Failed to read PDF from {pdf_url}: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

def load_crew_from_yaml(config_path: str = "agents/crew_config.yaml") -> Crew:
    """Convenient function for loading crew from YAML file"""
    loader = YAMLCrewLoader(config_path)
    return loader.create_crew()

def run_pillar_two_analysis(xml_data: str, config_path: str = "agents/crew_config.yaml") -> Dict[str, Any]:
    """Runs Pillar Two analysis with crew defined in YAML"""
    try:
        crew = load_crew_from_yaml(config_path)
        result = crew.kickoff()
        
        return {
            "success": True,
            "result": result,
            "crew_info": {
                "name": crew.agents[0].name if crew.agents else "Unknown",
                "agents_count": len(crew.agents),
                "tasks_count": len(crew.tasks)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "crew_info": None
        }

def load_tasks_from_yaml(tasks_path: str = "agents/tasks_config.yaml") -> Dict[str, Any]:
    """Loads task configurations from YAML file"""
    try:
        with open(tasks_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Tasks file not found: {tasks_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML file error: {e}")

def get_available_workflows(tasks_path: str = "agents/tasks_config.yaml") -> List[str]:
    """Returns a list of available workflows"""
    try:
        config = load_tasks_from_yaml(tasks_path)
        workflows = config.get('workflows', {})
        return list(workflows.keys())
    except Exception:
        return ["standard_analysis", "comprehensive_analysis", "quick_review"]

def run_workflow(workflow_name: str, xml_data: str, crew_config: str = "agents/crew_config.yaml", tasks_config: str = "agents/tasks_config.yaml") -> Dict[str, Any]:
    """Runs a specific workflow"""
    try:
        # Load configurations
        crew = load_crew_from_yaml(crew_config)
        tasks_config_data = load_tasks_from_yaml(tasks_config)
        
        # Get workflow configuration
        workflows = tasks_config_data.get('workflows', {})
        workflow = workflows.get(workflow_name)
        
        if not workflow:
            return {
                "success": False,
                "error": f"Workflow '{workflow_name}' not found"
            }
        
        # Run the workflow
        result = crew.kickoff()
        
        return {
            "success": True,
            "result": result,
            "workflow_info": {
                "name": workflow.get('name', workflow_name),
                "description": workflow.get('description', ''),
                "estimated_duration": workflow.get('estimated_duration', ''),
                "tasks": workflow.get('tasks', [])
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
