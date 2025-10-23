"""
Report generation for FLAVYR MVP.
Creates PDF and HTML reports with performance analysis.
"""

from fpdf import FPDF
from datetime import datetime
from typing import Dict
import pandas as pd


class FlavyrReport(FPDF):
    """Custom PDF report class for FLAVYR."""

    def header(self):
        """Add header to each page."""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'FLAVYR Performance Analysis Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def generate_executive_summary(analysis_results: Dict, recommendation_results: Dict) -> str:
    """
    Generate executive summary text.

    Args:
        analysis_results: Results from analyzer
        recommendation_results: Results from recommender

    Returns:
        Executive summary text
    """
    cuisine = analysis_results['cuisine_type']
    model = analysis_results['dining_model']
    grade = analysis_results['performance_grade']

    summary = f"""
EXECUTIVE SUMMARY

Restaurant Type: {cuisine} - {model}
Overall Performance Grade: {grade}

{analysis_results['summary']}

Key Recommendations:
{create_recommendation_text(recommendation_results)}
"""

    return summary


def create_kpi_comparison_table(analysis_results: Dict) -> list:
    """
    Create KPI comparison table data.

    Args:
        analysis_results: Results from analyzer

    Returns:
        List of lists for table rows
    """
    gaps = analysis_results['gaps']

    table_data = [['KPI', 'Your Value', 'Benchmark', 'Gap %', 'Status']]

    for kpi, data in gaps.items():
        kpi_name = data['kpi_name']
        rest_val = f"{data['restaurant_value']:.2f}"
        bench_val = f"{data['benchmark_value']:.2f}"
        gap_pct = f"{data['gap_pct']:.1f}%"

        # Determine status
        if data['gap_pct'] >= 10:
            status = 'Excellent'
        elif data['gap_pct'] >= 0:
            status = 'Good'
        elif data['gap_pct'] >= -10:
            status = 'Needs Attention'
        else:
            status = 'Critical'

        table_data.append([kpi_name, rest_val, bench_val, gap_pct, status])

    return table_data


def create_recommendation_text(recommendation_results: Dict) -> str:
    """
    Format recommendations as text.

    Args:
        recommendation_results: Results from recommender

    Returns:
        Formatted recommendation text
    """
    recommendations = recommendation_results['recommendations']

    if not recommendations:
        return "Your performance is strong across all metrics. No specific recommendations at this time."

    lines = []
    for i, rec in enumerate(recommendations[:3], 1):
        lines.append(f"\n{i}. {rec['business_problem']}")
        lines.append(f"   Suggested Deals: {rec['deal_types']}")
        lines.append(f"   Rationale: {rec['rationale']}")

    return '\n'.join(lines)


def export_to_pdf(analysis_results: Dict, recommendation_results: Dict, output_path: str):
    """
    Generate and save PDF report.

    Args:
        analysis_results: Results from analyzer
        recommendation_results: Results from recommender
        output_path: Path to save PDF file
    """
    pdf = FlavyrReport()
    pdf.add_page()

    # Set up fonts
    pdf.set_font('Arial', '', 10)

    # Executive Summary
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Executive Summary', 0, 1)
    pdf.set_font('Arial', '', 10)

    cuisine = analysis_results['cuisine_type']
    model = analysis_results['dining_model']
    grade = analysis_results['performance_grade']

    pdf.multi_cell(0, 6, f"Restaurant Type: {cuisine} - {model}")
    pdf.multi_cell(0, 6, f"Overall Performance Grade: {grade}")
    pdf.ln(5)

    pdf.multi_cell(0, 6, "Top Performance Issues:")
    pdf.multi_cell(0, 6, analysis_results['summary'])
    pdf.ln(10)

    # KPI Comparison Table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'KPI Comparison', 0, 1)
    pdf.set_font('Arial', '', 9)

    table_data = create_kpi_comparison_table(analysis_results)

    # Table header
    col_widths = [60, 30, 30, 25, 35]
    for i, header in enumerate(table_data[0]):
        pdf.cell(col_widths[i], 8, header, 1, 0, 'C')
    pdf.ln()

    # Table rows
    for row in table_data[1:]:
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 8, str(cell), 1, 0, 'C')
        pdf.ln()

    pdf.ln(10)

    # Recommendations
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Deal Recommendations', 0, 1)
    pdf.set_font('Arial', '', 10)

    recommendations = recommendation_results['recommendations']
    if recommendations:
        for i, rec in enumerate(recommendations[:5], 1):
            pdf.set_font('Arial', 'B', 11)
            pdf.multi_cell(0, 6, f"{i}. {rec['business_problem']}")
            pdf.set_font('Arial', '', 10)

            # Split deal types if too long
            deal_types = rec['deal_types']
            if len(deal_types) > 80:
                deal_types = deal_types[:80] + "..."

            pdf.multi_cell(0, 5, f"Suggested Deals: {deal_types}")

            # Split rationale if too long
            rationale = rec['rationale']
            pdf.multi_cell(0, 5, f"Rationale: {rationale}")
            pdf.ln(5)
    else:
        pdf.multi_cell(0, 6, "Your performance is strong across all metrics.")

    # Save PDF
    pdf.output(output_path)


def export_to_html(analysis_results: Dict, recommendation_results: Dict) -> str:
    """
    Generate HTML report.

    Args:
        analysis_results: Results from analyzer
        recommendation_results: Results from recommender

    Returns:
        HTML string
    """
    cuisine = analysis_results['cuisine_type']
    model = analysis_results['dining_model']
    grade = analysis_results['performance_grade']
    date = datetime.now().strftime('%Y-%m-%d')

    # Create KPI table
    table_data = create_kpi_comparison_table(analysis_results)
    table_html = '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">'
    table_html += '<thead><tr style="background-color: #f0f0f0;">'

    for header in table_data[0]:
        table_html += f'<th>{header}</th>'
    table_html += '</tr></thead><tbody>'

    for row in table_data[1:]:
        # Color code by status
        status = row[4]
        row_color = '#ffffff'
        if status == 'Critical':
            row_color = '#ffcccc'
        elif status == 'Needs Attention':
            row_color = '#fff4cc'
        elif status == 'Excellent':
            row_color = '#ccffcc'

        table_html += f'<tr style="background-color: {row_color};">'
        for cell in row:
            table_html += f'<td>{cell}</td>'
        table_html += '</tr>'

    table_html += '</tbody></table>'

    # Create recommendations HTML
    recommendations = recommendation_results['recommendations']
    rec_html = ''

    if recommendations:
        for i, rec in enumerate(recommendations[:5], 1):
            rec_html += f'''
            <div style="margin-bottom: 20px; padding: 15px; border-left: 4px solid #0066cc; background-color: #f9f9f9;">
                <h3>{i}. {rec['business_problem']}</h3>
                <p><strong>Suggested Deals:</strong> {rec['deal_types']}</p>
                <p><strong>Rationale:</strong> {rec['rationale']}</p>
            </div>
            '''
    else:
        rec_html = '<p>Your performance is strong across all metrics. No specific recommendations at this time.</p>'

    # Complete HTML
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FLAVYR Performance Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1 {{ color: #333; border-bottom: 3px solid #0066cc; padding-bottom: 10px; }}
            h2 {{ color: #0066cc; margin-top: 30px; }}
            .summary {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; margin: 20px 0; }}
            table {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>FLAVYR Performance Analysis Report</h1>
        <p><strong>Date:</strong> {date}</p>

        <div class="summary">
            <h2>Executive Summary</h2>
            <p><strong>Restaurant Type:</strong> {cuisine} - {model}</p>
            <p><strong>Overall Performance Grade:</strong> {grade}</p>
            <h3>Top Performance Issues:</h3>
            <pre>{analysis_results['summary']}</pre>
        </div>

        <h2>KPI Comparison</h2>
        {table_html}

        <h2>Deal Recommendations</h2>
        {rec_html}

        <hr style="margin-top: 40px;">
        <p style="color: #666; font-size: 12px;">Generated by FLAVYR Performance Analytics</p>
    </body>
    </html>
    '''

    return html
