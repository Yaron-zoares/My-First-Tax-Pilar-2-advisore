"""
XML Generator Service
Generates GIR XML reports for regulatory compliance
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

class XMLGenerator:
    """XML generator for GIR reports"""
    
    def __init__(self):
        """Initialize XML generator"""
        self.namespace = {
            'gir': 'http://www.oecd.org/tax/beps/gir'
        }
    
    def generate_gir_xml(self, data: Dict[str, Any], report_type: str = "standard") -> str:
        """
        Generate GIR XML report
        
        Args:
            data: Financial data for XML generation
            report_type: Type of report (standard, detailed, gir)
            
        Returns:
            XML string
        """
        try:
            # Create root element
            root = ET.Element('gir:Report', {
                'xmlns:gir': self.namespace['gir'],
                'version': settings.GIR_XML_VERSION,
                'reportingPeriod': settings.REPORTING_PERIOD
            })
            
            # Add header information
            self._add_header(root, data)
            
            # Add financial data
            self._add_financial_data(root, data)
            
            # Add tax calculations
            if report_type in ["detailed", "gir"]:
                self._add_tax_calculations(root, data)
            
            # Add adjustments
            if report_type == "gir":
                self._add_adjustments(root, data)
            
            # Format XML
            xml_string = self._format_xml(root)
            
            logger.info(f"GIR XML generated successfully for {report_type} report")
            return xml_string
            
        except Exception as e:
            logger.error(f"XML generation error: {str(e)}")
            raise
    
    def _add_header(self, root: ET.Element, data: Dict[str, Any]):
        """Add header information to XML"""
        try:
            header = ET.SubElement(root, 'gir:Header')
            
            # Report metadata
            metadata = ET.SubElement(header, 'gir:Metadata')
            ET.SubElement(metadata, 'gir:ReportDate').text = datetime.now().isoformat()
            ET.SubElement(metadata, 'gir:ReportType').text = 'Financial Analysis Report'
            ET.SubElement(metadata, 'gir:Version').text = settings.APP_VERSION
            
            # Entity information
            entity = ET.SubElement(header, 'gir:Entity')
            ET.SubElement(entity, 'gir:EntityName').text = data.get('entity_name', 'Unknown Entity')
            ET.SubElement(entity, 'gir:EntityType').text = data.get('entity_type', 'Corporation')
            
        except Exception as e:
            logger.error(f"Header generation error: {str(e)}")
    
    def _add_financial_data(self, root: ET.Element, data: Dict[str, Any]):
        """Add financial data to XML"""
        try:
            financial = ET.SubElement(root, 'gir:FinancialData')
            
            # Revenue information
            if 'revenue' in data:
                revenue = ET.SubElement(financial, 'gir:Revenue')
                ET.SubElement(revenue, 'gir:Amount').text = str(data['revenue'])
                ET.SubElement(revenue, 'gir:Currency').text = 'ILS'
            
            # Expense information
            if 'expenses' in data:
                expenses = ET.SubElement(financial, 'gir:Expenses')
                ET.SubElement(expenses, 'gir:Amount').text = str(data['expenses'])
                ET.SubElement(expenses, 'gir:Currency').text = 'ILS'
            
            # Net profit information
            if 'net_profit' in data:
                net_profit = ET.SubElement(financial, 'gir:NetProfit')
                ET.SubElement(net_profit, 'gir:Amount').text = str(data['net_profit'])
                ET.SubElement(net_profit, 'gir:Currency').text = 'ILS'
            
        except Exception as e:
            logger.error(f"Financial data generation error: {str(e)}")
    
    def _add_tax_calculations(self, root: ET.Element, data: Dict[str, Any]):
        """Add tax calculations to XML"""
        try:
            tax_calc = ET.SubElement(root, 'gir:TaxCalculations')
            
            # Effective tax rate
            if 'effective_tax_rate' in data:
                etr = ET.SubElement(tax_calc, 'gir:EffectiveTaxRate')
                ET.SubElement(etr, 'gir:Rate').text = str(data['effective_tax_rate'])
                ET.SubElement(etr, 'gir:CalculationMethod').text = 'Standard'
            
            # Tax liability
            if 'tax_liability' in data:
                liability = ET.SubElement(tax_calc, 'gir:TaxLiability')
                ET.SubElement(liability, 'gir:Amount').text = str(data['tax_liability'])
                ET.SubElement(liability, 'gir:Currency').text = 'ILS'
            
        except Exception as e:
            logger.error(f"Tax calculations generation error: {str(e)}")
    
    def _add_adjustments(self, root: ET.Element, data: Dict[str, Any]):
        """Add tax adjustments to XML"""
        try:
            adjustments = ET.SubElement(root, 'gir:Adjustments')
            
            # Add adjustment categories
            adjustment_categories = [
                'depreciation', 'provisions', 'capital_gains', 
                'foreign_income', 'loss_carryforward'
            ]
            
            for category in adjustment_categories:
                if category in data:
                    adj = ET.SubElement(adjustments, f'gir:{category.title()}')
                    ET.SubElement(adj, 'gir:Amount').text = str(data[category])
                    ET.SubElement(adj, 'gir:Description').text = f'{category.title()} adjustment'
            
        except Exception as e:
            logger.error(f"Adjustments generation error: {str(e)}")
    
    def _format_xml(self, root: ET.Element) -> str:
        """Format XML with proper indentation"""
        try:
            # Convert to string
            rough_string = ET.tostring(root, 'unicode')
            
            # Parse and format
            reparsed = minidom.parseString(rough_string)
            formatted_xml = reparsed.toprettyxml(indent="  ")
            
            return formatted_xml
            
        except Exception as e:
            logger.error(f"XML formatting error: {str(e)}")
            return ET.tostring(root, 'unicode')
    
    def validate_xml(self, xml_string: str) -> bool:
        """
        Validate generated XML
        
        Args:
            xml_string: XML string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Basic validation - check if it's well-formed
            ET.fromstring(xml_string)
            logger.info("XML validation successful")
            return True
            
        except ET.ParseError as e:
            logger.error(f"XML validation error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"XML validation error: {str(e)}")
            return False
    
    def generate_sample_data(self) -> Dict[str, Any]:
        """
        Generate sample data for testing
        
        Returns:
            Dictionary with sample financial data
        """
        return {
            'entity_name': 'Sample Corporation Ltd.',
            'entity_type': 'Corporation',
            'revenue': 1000000,
            'expenses': 750000,
            'net_profit': 250000,
            'effective_tax_rate': 0.23,
            'tax_liability': 57500,
            'depreciation': 50000,
            'provisions': 25000,
            'capital_gains': 0,
            'foreign_income': 0,
            'loss_carryforward': 0
        }
