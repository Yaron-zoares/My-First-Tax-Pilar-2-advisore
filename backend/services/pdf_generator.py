"""
PDF Generator Service
Generates PDF reports for financial analysis
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from typing import Dict, List, Any
from datetime import datetime
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class PDFGenerator:
    """PDF generator for financial reports"""

    def __init__(self):
        """Initialize PDF generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )

        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12
        )

        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )

    def generate_financial_report(self, data: Dict[str, Any],
                                  report_type: str = "standard") -> str:
        """
        Generate financial report PDF

        Args:
            data: Financial data for report generation
            report_type: Type of report (standard, detailed, summary)

        Returns:
            Path to generated PDF file
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = settings.REPORTS_DIR / "pdf"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_report_{report_type}_{timestamp}.pdf"
            filepath = output_dir / filename

            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            story = []

            # Add title
            story.append(Paragraph("Financial Analysis Report", self.title_style))
            story.append(Spacer(1, 12))

            # Add report metadata
            story.extend(self._add_metadata(data))

            # Add financial summary
            story.extend(self._add_financial_summary(data))

            # Add detailed analysis if requested
            if report_type in ["detailed", "comprehensive"]:
                story.extend(self._add_detailed_analysis(data))

            # Add tax calculations
            if report_type in ["detailed", "tax_focused"]:
                story.extend(self._add_tax_calculations(data))

            # Add recommendations
            if report_type in ["detailed", "comprehensive"]:
                story.extend(self._add_recommendations(data))

            # Build PDF
            doc.build(story)

            logger.info(f"PDF report generated successfully: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            raise

    def _add_metadata(self, data: Dict[str, Any]) -> List:
        """Add report metadata"""
        elements = []

        # Report information
        elements.append(Paragraph("Report Information", self.heading_style))

        metadata_data = [
            ["Report Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Report Type:", "Financial Analysis"],
            ["Entity Name:", data.get('entity_name', 'N/A')],
            ["Analysis Period:", data.get('period', 'Annual')]
        ]

        metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(metadata_table)
        elements.append(Spacer(1, 12))

        return elements

    def _add_financial_summary(self, data: Dict[str, Any]) -> List:
        """Add financial summary section"""
        elements = []

        elements.append(Paragraph("Financial Summary", self.heading_style))

        # Key financial metrics
        revenue = data.get('revenue', 0)
        expenses = data.get('expenses', 0)
        net_profit = data.get('net_profit', 0)

        summary_data = [
            ["Metric", "Amount (ILS)", "Percentage"],
            ["Revenue", f"{revenue:,.0f}", "100%"],
            ["Expenses", f"{expenses:,.0f}",
             f"{(expenses / revenue * 100) if revenue else 0:.1f}%"],
            ["Net Profit", f"{net_profit:,.0f}",
             f"{(net_profit / revenue * 100) if revenue else 0:.1f}%"]
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 12))

        return elements

    def _add_detailed_analysis(self, data: Dict[str, Any]) -> List:
        """Add detailed analysis section"""
        elements = []

        elements.append(Paragraph("Detailed Analysis", self.heading_style))

        # Add analysis details
        if 'details' in data:
            details = data['details']

            # Categories analysis
            if 'categories' in details:
                elements.append(Paragraph("Financial Categories", self.normal_style))
                category_data = [["Category", "Amount (ILS)"]]

                for category, info in details['categories'].items():
                    category_data.append([category.title(), f"{info['total']:,.0f}"])

                category_table = Table(category_data, colWidths=[3*inch, 3*inch])
                category_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                elements.append(category_table)
                elements.append(Spacer(1, 12))

            # Risk assessment
            if 'risks' in details:
                elements.append(Paragraph("Risk Assessment", self.normal_style))
                for risk in details['risks']:
                    elements.append(Paragraph(f"• {risk}", self.normal_style))
                elements.append(Spacer(1, 12))

        return elements

    def _add_tax_calculations(self, data: Dict[str, Any]) -> List:
        """Add tax calculations section"""
        elements = []

        elements.append(Paragraph("Tax Calculations", self.heading_style))

        # Tax metrics
        tax_data = [
            ["Tax Metric", "Value"],
            ["Effective Tax Rate", f"{data.get('effective_tax_rate', 0):.1%}"],
            ["Tax Liability", f"{data.get('tax_liability', 0):,.0f} ILS"],
            ["Tax Efficiency Score", f"{data.get('tax_efficiency_score', 0):.1%}"]
        ]

        tax_table = Table(tax_data, colWidths=[3*inch, 3*inch])
        tax_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(tax_table)
        elements.append(Spacer(1, 12))

        return elements

    def _add_recommendations(self, data: Dict[str, Any]) -> List:
        """Add recommendations section"""
        elements = []

        elements.append(Paragraph("Recommendations", self.heading_style))

        # Add recommendations
        recommendations = data.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.normal_style))
        else:
            elements.append(Paragraph(
                "No specific recommendations at this time.", self.normal_style))

        elements.append(Spacer(1, 12))

        return elements

    def generate_sample_data(self) -> Dict[str, Any]:
        """
        Generate sample data for testing

        Returns:
            Dictionary with sample financial data
        """
        return {
            'entity_name': 'Sample Corporation Ltd.',
            'period': 'Annual 2023',
            'revenue': 1000000,
            'expenses': 750000,
            'net_profit': 250000,
            'effective_tax_rate': 0.23,
            'tax_liability': 57500,
            'tax_efficiency_score': 0.85,
            'details': {
                'categories': {
                    'revenue': {'total': 1000000},
                    'expenses': {'total': 750000},
                    'assets': {'total': 2000000}
                },
                'risks': [
                    'Low profit margin detected',
                    'Revenue concentration risk'
                ]
            },
            'recommendations': [
                'Consider cost optimization strategies',
                'Review tax planning strategies',
                'Address identified financial risks'
            ]
        }
