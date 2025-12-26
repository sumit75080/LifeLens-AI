from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io

def generate_comprehensive_health_report(user_email, demographics, analyses, insights=None):
    """
    Generate comprehensive PDF health report
    Returns bytes buffer of the PDF
    """
    
    # Create PDF buffer
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    elements.append(Paragraph("🫘 LIFELens-AI", title_style))
    elements.append(Paragraph("Comprehensive Kidney Health Report", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    # Report metadata
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['Normal']))
    elements.append(Paragraph(f"<b>Patient:</b> {user_email}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Patient Demographics Section
    elements.append(Paragraph("Patient Demographics", heading_style))
    
    if demographics:
        from diet_generator import calculate_bmi, get_bmi_category
        
        demo_data = [
            ['Age', f"{demographics.get('age', 'Not provided')} years"],
            ['Gender', demographics.get('gender', 'Not provided')],
            ['Weight', f"{demographics.get('weight', 'Not provided')} kg"],
            ['Height', f"{demographics.get('height', 'Not provided')} cm"],
            ['Daily Water Intake', f"{demographics.get('daily_water_intake', 'Not provided')} glasses"],
        ]
        
        # Add BMI if available
        if demographics.get('weight') and demographics.get('height'):
            bmi = calculate_bmi(demographics['weight'], demographics['height'])
            if bmi:
                demo_data.append(['BMI', f"{bmi} ({get_bmi_category(bmi)})"])
        
        demo_table = Table(demo_data, colWidths=[2*inch, 4*inch])
        demo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (1, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(demo_table)
        
        if demographics.get('medical_history'):
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("<b>Medical History:</b>", styles['Normal']))
            elements.append(Paragraph(demographics['medical_history'], styles['Normal']))
    else:
        elements.append(Paragraph("No demographic information available.", styles['Normal']))
    
    elements.append(Spacer(1, 20))
    
    # Analysis Summary Section
    elements.append(Paragraph("AI Analysis Summary", heading_style))
    
    if analyses and len(analyses) > 0:
        elements.append(Paragraph(f"Total Scans Analyzed: <b>{len(analyses)}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Latest analysis
        latest = analyses[0]
        elements.append(Paragraph(f"<b>Latest Analysis ({latest['analyzed_at'][:19]})</b>", styles['Normal']))
        elements.append(Spacer(1, 6))
        
        analysis_data = latest.get('analysis_data', {})
        
        # Risk level with color
        risk_level = latest.get('risk_level', 'Unknown').upper()
        risk_color = 'green' if risk_level == 'LOW' else ('orange' if risk_level == 'MODERATE' else 'red')
        elements.append(Paragraph(f"Risk Level: <font color='{risk_color}'><b>{risk_level}</b></font>", styles['Normal']))
        elements.append(Paragraph(f"AI Confidence: <b>{latest.get('confidence_score', 0)}%</b>", styles['Normal']))
        elements.append(Paragraph(f"Scan Type: <b>{analysis_data.get('scan_type', 'Unknown')}</b>", styles['Normal']))
        elements.append(Paragraph(f"Image Quality: <b>{analysis_data.get('image_quality', 'Unknown')}</b>", styles['Normal']))
        
        elements.append(Spacer(1, 12))
        
        # Key findings
        if analysis_data.get('key_findings'):
            elements.append(Paragraph("<b>Key Findings:</b>", styles['Normal']))
            for finding in analysis_data['key_findings']:
                elements.append(Paragraph(f"• {finding}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Potential concerns
        if analysis_data.get('potential_concerns'):
            elements.append(Paragraph("<b>Potential Concerns:</b>", styles['Normal']))
            for concern in analysis_data['potential_concerns']:
                elements.append(Paragraph(f"⚠️ {concern}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Kidney indicators
        if analysis_data.get('kidney_indicators'):
            elements.append(Paragraph("<b>Kidney Health Indicators:</b>", styles['Normal']))
            indicators = analysis_data['kidney_indicators']
            elements.append(Paragraph(f"• Size: {indicators.get('size', 'N/A')}", styles['Normal']))
            elements.append(Paragraph(f"• Structure: {indicators.get('structure', 'N/A')}", styles['Normal']))
            elements.append(Paragraph(f"• Abnormalities: {indicators.get('abnormalities', 'None detected')}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Recommendations
        if analysis_data.get('recommendations'):
            elements.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
            for rec in analysis_data['recommendations']:
                elements.append(Paragraph(f"→ {rec}", styles['Normal']))
    else:
        elements.append(Paragraph("No AI analyses available.", styles['Normal']))
    
    elements.append(Spacer(1, 20))
    
    # Health Insights Section
    if insights:
        elements.append(PageBreak())
        elements.append(Paragraph("Comprehensive Health Insights", heading_style))
        
        if insights.get('overall_health_status'):
            elements.append(Paragraph("<b>Overall Health Status:</b>", styles['Normal']))
            elements.append(Paragraph(insights['overall_health_status'], styles['Normal']))
            elements.append(Spacer(1, 12))
        
        if insights.get('risk_factors'):
            elements.append(Paragraph("<b>Risk Factors:</b>", styles['Normal']))
            for factor in insights['risk_factors']:
                elements.append(Paragraph(f"• {factor}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        if insights.get('lifestyle_recommendations'):
            elements.append(Paragraph("<b>Lifestyle Recommendations:</b>", styles['Normal']))
            for rec in insights['lifestyle_recommendations']:
                elements.append(Paragraph(f"• {rec}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        if insights.get('dietary_adjustments'):
            elements.append(Paragraph("<b>Dietary Adjustments:</b>", styles['Normal']))
            for adj in insights['dietary_adjustments']:
                elements.append(Paragraph(f"• {adj}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        if insights.get('next_steps'):
            elements.append(Paragraph("<b>Recommended Next Steps:</b>", styles['Normal']))
            for step in insights['next_steps']:
                elements.append(Paragraph(f"→ {step}", styles['Normal']))
    
    # Disclaimer
    elements.append(Spacer(1, 30))
    elements.append(PageBreak())
    elements.append(Paragraph("Medical Disclaimer", heading_style))
    
    disclaimer_text = """
    This report is generated by LIFELens-AI for informational and educational purposes only. 
    The AI-generated analyses and insights do not constitute medical advice, diagnosis, or treatment. 
    All medical scans should be reviewed by qualified healthcare professionals. 
    Always consult with your healthcare provider for medical decisions and interpretations of medical scans.
    
    In case of medical emergencies, contact your healthcare provider immediately or call emergency services.
    
    This report should be used as a supplementary tool to support, not replace, professional medical care.
    """
    
    elements.append(Paragraph(disclaimer_text, styles['Normal']))
    
    # Footer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Report generated by LIFELens-AI on {report_date}", 
                             ParagraphStyle('Footer', parent=styles['Normal'], 
                                          fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def generate_analysis_report_pdf(analysis, demographics=None):
    """Generate PDF report for a single analysis"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("LIFELens-AI - Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Analysis details
    analysis_data = analysis.get('analysis_data', {})
    
    elements.append(Paragraph(f"Analysis Date: {analysis['analyzed_at'][:19]}", styles['Normal']))
    elements.append(Paragraph(f"File: {analysis.get('filename', 'Unknown')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Key information
    elements.append(Paragraph(f"Risk Level: {analysis.get('risk_level', 'Unknown').upper()}", styles['Heading2']))
    elements.append(Paragraph(f"Confidence Score: {analysis.get('confidence_score', 0)}%", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Findings
    if analysis_data.get('key_findings'):
        elements.append(Paragraph("Key Findings:", styles['Heading3']))
        for finding in analysis_data['key_findings']:
            elements.append(Paragraph(f"• {finding}", styles['Normal']))
        elements.append(Spacer(1, 12))
    
    # Build and return
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
