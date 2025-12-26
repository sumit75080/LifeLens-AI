import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

def create_risk_level_timeline(analyses):
    """Create timeline chart showing risk level progression"""
    if not analyses:
        return None
    
    # Prepare data
    dates = []
    risk_levels = []
    risk_numeric = []
    
    for analysis in reversed(analyses):  # Oldest to newest
        dates.append(analysis['analyzed_at'][:10])
        risk_level = analysis.get('risk_level', 'unknown')
        risk_levels.append(risk_level.title())
        
        # Convert to numeric for plotting
        if risk_level == 'low':
            risk_numeric.append(1)
        elif risk_level == 'moderate':
            risk_numeric.append(2)
        elif risk_level == 'high':
            risk_numeric.append(3)
        else:
            risk_numeric.append(0)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=risk_numeric,
        mode='lines+markers',
        name='Risk Level',
        line=dict(color='rgb(31, 119, 180)', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Date:</b> %{x}<br><b>Risk:</b> %{text}<extra></extra>',
        text=risk_levels
    ))
    
    fig.update_layout(
        title='Kidney Health Risk Level Over Time',
        xaxis_title='Date',
        yaxis_title='Risk Level',
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3],
            ticktext=['Low', 'Moderate', 'High']
        ),
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_confidence_score_chart(analyses):
    """Create chart showing AI confidence scores over time"""
    if not analyses:
        return None
    
    dates = []
    scores = []
    
    for analysis in reversed(analyses):
        dates.append(analysis['analyzed_at'][:10])
        scores.append(analysis.get('confidence_score', 0))
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dates,
        y=scores,
        marker_color='rgb(55, 83, 109)',
        hovertemplate='<b>Date:</b> %{x}<br><b>Confidence:</b> %{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='AI Analysis Confidence Scores',
        xaxis_title='Date',
        yaxis_title='Confidence (%)',
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    return fig

def create_risk_distribution_pie(analyses):
    """Create pie chart showing distribution of risk levels"""
    if not analyses:
        return None
    
    risk_counts = {'Low': 0, 'Moderate': 0, 'High': 0}
    
    for analysis in analyses:
        risk_level = analysis.get('risk_level', 'unknown')
        if risk_level in ['low', 'moderate', 'high']:
            risk_counts[risk_level.title()] += 1
    
    # Remove zero values
    risk_counts = {k: v for k, v in risk_counts.items() if v > 0}
    
    if not risk_counts:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=list(risk_counts.keys()),
        values=list(risk_counts.values()),
        hole=0.3,
        marker=dict(colors=['#2ecc71', '#f39c12', '#e74c3c'])
    )])
    
    fig.update_layout(
        title='Risk Level Distribution',
        height=400
    )
    
    return fig

def create_bmi_trend_chart(demographics_history):
    """Create BMI trend chart if multiple demographic entries exist"""
    if not demographics_history or len(demographics_history) < 2:
        return None
    
    from diet_generator import calculate_bmi
    
    dates = []
    bmis = []
    
    for demo in demographics_history:
        if demo.get('weight') and demo.get('height'):
            bmi = calculate_bmi(demo['weight'], demo['height'])
            if bmi:
                dates.append(demo.get('updated_at', 'Unknown')[:10])
                bmis.append(bmi)
    
    if not dates:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=bmis,
        mode='lines+markers',
        name='BMI',
        line=dict(color='rgb(219, 64, 82)', width=3),
        marker=dict(size=10)
    ))
    
    # Add healthy BMI range
    fig.add_hrect(y0=18.5, y1=25, 
                  fillcolor="green", opacity=0.1,
                  annotation_text="Healthy Range", annotation_position="top left")
    
    fig.update_layout(
        title='Body Mass Index (BMI) Trend',
        xaxis_title='Date',
        yaxis_title='BMI',
        height=400
    )
    
    return fig

def create_water_intake_gauge(current_intake, target_intake=8):
    """Create gauge chart for water intake"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_intake,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Daily Water Intake (glasses)"},
        delta={'reference': target_intake},
        gauge={
            'axis': {'range': [None, 15]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 6], 'color': "lightgray"},
                {'range': [6, 8], 'color': "lightyellow"},
                {'range': [8, 15], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target_intake
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig

def create_health_metrics_comparison(analyses):
    """Create radar chart comparing different health metrics"""
    if not analyses or len(analyses) == 0:
        return None
    
    latest = analyses[0]
    analysis_data = latest.get('analysis_data', {})
    
    # Extract metrics (sample)
    categories = ['Overall Health', 'Kidney Size', 'Kidney Structure', 'Image Quality', 'Risk Assessment']
    
    # Convert qualitative assessments to scores (0-100)
    def quality_to_score(quality):
        quality_map = {
            'excellent': 100, 'good': 80, 'fair': 60, 'poor': 40,
            'normal': 90, 'abnormal': 30, 'concerning': 20,
            'low': 90, 'moderate': 60, 'high': 30
        }
        if isinstance(quality, str):
            return quality_map.get(quality.lower(), 50)
        return 50
    
    values = [
        quality_to_score(analysis_data.get('image_quality', 'fair')),
        quality_to_score(analysis_data.get('kidney_indicators', {}).get('size', 'normal')),
        quality_to_score(analysis_data.get('kidney_indicators', {}).get('structure', 'normal')),
        quality_to_score(analysis_data.get('image_quality', 'fair')),
        quality_to_score(latest.get('risk_level', 'moderate'))
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Assessment'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title='Health Metrics Overview',
        height=400
    )
    
    return fig

def create_findings_frequency_chart(analyses):
    """Create bar chart showing frequency of different findings"""
    if not analyses:
        return None
    
    findings_count = {}
    
    for analysis in analyses:
        findings = analysis.get('analysis_data', {}).get('key_findings', [])
        for finding in findings:
            # Simplify finding to first few words
            key = ' '.join(finding.split()[:4])
            findings_count[key] = findings_count.get(key, 0) + 1
    
    if not findings_count:
        return None
    
    # Get top 10 findings
    sorted_findings = sorted(findings_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[f[1] for f in sorted_findings],
            y=[f[0] for f in sorted_findings],
            orientation='h',
            marker_color='rgb(158, 202, 225)'
        )
    ])
    
    fig.update_layout(
        title='Most Common Findings',
        xaxis_title='Frequency',
        yaxis_title='Finding',
        height=400
    )
    
    return fig
