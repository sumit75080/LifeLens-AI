import streamlit as st
from database import get_all_user_analyses, get_user_demographics
from health_charts import (
    create_risk_level_timeline,
    create_confidence_score_chart,
    create_risk_distribution_pie,
    create_water_intake_gauge,
    create_health_metrics_comparison,
    create_findings_frequency_chart
)

def show_page():
    """Display health tracking and charts page"""
    st.title("📊 Health Tracking & Trends")
    st.subheader("Visualize your kidney health journey over time")
    
    # Get user data
    demographics = get_user_demographics(st.session_state.username)
    analyses = get_all_user_analyses(st.session_state.username)
    
    if not analyses or len(analyses) == 0:
        st.info("📭 No analysis data available yet. Upload and analyze medical scans to start tracking your health!")
        
        if st.button("📤 Go to Upload & Analyze", use_container_width=True):
            st.session_state.current_page = "Upload & Analyze"
            st.rerun()
        
        return
    
    # Summary metrics
    st.markdown("### 📈 Health Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scans", len(analyses))
    
    with col2:
        latest_risk = analyses[0].get('risk_level', 'Unknown')
        risk_icon = "🟢" if latest_risk == 'low' else ("🟡" if latest_risk == 'moderate' else "🔴")
        st.metric("Latest Risk", f"{risk_icon} {latest_risk.title()}")
    
    with col3:
        avg_confidence = sum([a.get('confidence_score', 0) for a in analyses]) / len(analyses)
        st.metric("Avg Confidence", f"{int(avg_confidence)}%")
    
    with col4:
        # Calculate trend (improving, stable, declining)
        if len(analyses) >= 2:
            risk_map = {'low': 1, 'moderate': 2, 'high': 3}
            latest_risk_val = risk_map.get(analyses[0].get('risk_level', 'moderate'), 2)
            prev_risk_val = risk_map.get(analyses[1].get('risk_level', 'moderate'), 2)
            
            if latest_risk_val < prev_risk_val:
                trend = "📈 Improving"
                trend_color = "normal"
            elif latest_risk_val > prev_risk_val:
                trend = "📉 Attention"
                trend_color = "inverse"
            else:
                trend = "➡️ Stable"
                trend_color = "off"
            
            st.metric("Trend", trend, delta_color=trend_color)
        else:
            st.metric("Trend", "N/A")
    
    st.markdown("---")
    
    # Main charts
    st.markdown("### 📉 Risk Level Timeline")
    risk_timeline = create_risk_level_timeline(analyses)
    if risk_timeline:
        st.plotly_chart(risk_timeline, use_container_width=True)
    else:
        st.info("Not enough data for timeline visualization")
    
    # Two column layout for additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 AI Confidence Scores")
        confidence_chart = create_confidence_score_chart(analyses)
        if confidence_chart:
            st.plotly_chart(confidence_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🥧 Risk Distribution")
        risk_pie = create_risk_distribution_pie(analyses)
        if risk_pie:
            st.plotly_chart(risk_pie, use_container_width=True)
    
    # Water intake gauge
    if demographics and demographics.get('daily_water_intake'):
        st.markdown("---")
        st.markdown("### 💧 Water Intake Monitor")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            water_gauge = create_water_intake_gauge(demographics['daily_water_intake'])
            if water_gauge:
                st.plotly_chart(water_gauge, use_container_width=True)
        
        # Hydration recommendation
        if demographics['daily_water_intake'] < 8:
            st.warning(f"⚠️ Current intake is {demographics['daily_water_intake']} glasses. Aim for at least 8 glasses daily for optimal kidney health.")
        else:
            st.success(f"✅ Great! You're meeting the recommended daily water intake of 8+ glasses.")
    
    # Health metrics radar
    st.markdown("---")
    st.markdown("### 🎯 Latest Health Metrics")
    
    metrics_radar = create_health_metrics_comparison(analyses)
    if metrics_radar:
        st.plotly_chart(metrics_radar, use_container_width=True)
    
    # Findings frequency
    st.markdown("---")
    st.markdown("### 🔍 Common Findings")
    
    findings_chart = create_findings_frequency_chart(analyses)
    if findings_chart:
        st.plotly_chart(findings_chart, use_container_width=True)
    else:
        st.info("No repeated findings to display")
    
    # Historical comparison table
    st.markdown("---")
    st.markdown("### 📅 Historical Analysis Comparison")
    
    if len(analyses) >= 2:
        # Create comparison table
        comparison_data = []
        
        for i, analysis in enumerate(analyses[:5]):  # Show last 5
            analysis_data = analysis.get('analysis_data', {})
            comparison_data.append({
                'Date': analysis['analyzed_at'][:10],
                'Risk Level': analysis.get('risk_level', 'Unknown').title(),
                'Confidence': f"{analysis.get('confidence_score', 0)}%",
                'Scan Type': analysis_data.get('scan_type', 'Unknown'),
                'Image Quality': analysis_data.get('image_quality', 'Unknown').title(),
                'Concerns': len(analysis_data.get('potential_concerns', []))
            })
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
    
    # Export options
    st.markdown("---")
    st.markdown("### 📥 Export Health Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export as CSV
        import pandas as pd
        import datetime
        
        export_data = []
        for analysis in analyses:
            analysis_data = analysis.get('analysis_data', {})
            export_data.append({
                'Date': analysis['analyzed_at'][:19],
                'Filename': analysis.get('filename', 'Unknown'),
                'Risk Level': analysis.get('risk_level', 'Unknown'),
                'Confidence': analysis.get('confidence_score', 0),
                'Scan Type': analysis_data.get('scan_type', 'Unknown'),
                'Image Quality': analysis_data.get('image_quality', 'Unknown'),
                'Key Findings': '; '.join(analysis_data.get('key_findings', [])),
                'Concerns': '; '.join(analysis_data.get('potential_concerns', []))
            })
        
        df_export = pd.DataFrame(export_data)
        csv = df_export.to_csv(index=False)
        
        st.download_button(
            label="📊 Download Data (CSV)",
            data=csv,
            file_name=f"lifelens_health_data_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Export comprehensive PDF report
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating comprehensive PDF report..."):
                from pdf_generator import generate_comprehensive_health_report
                from ai_analyzer import generate_health_insights
                
                # Generate insights for the report
                analysis_summaries = []
                for analysis in analyses:
                    analysis_summaries.append({
                        'date': analysis.get('analyzed_at'),
                        'risk_level': analysis.get('risk_level'),
                        'confidence': analysis.get('confidence_score'),
                        'key_findings': analysis['analysis_data'].get('key_findings', []),
                        'concerns': analysis['analysis_data'].get('potential_concerns', [])
                    })
                
                insights = generate_health_insights(demographics, analysis_summaries) if demographics else None
                
                # Generate PDF
                pdf_bytes = generate_comprehensive_health_report(
                    st.session_state.username,
                    demographics,
                    analyses,
                    insights
                )
                
                if pdf_bytes:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"lifelens_health_report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ PDF report generated successfully!")
    
    # Health tips
    st.markdown("---")
    st.markdown("### 💡 Health Tracking Tips")
    
    tips = [
        "📅 Regular Monitoring: Upload scans regularly to track trends effectively",
        "📊 Review Trends: Check your risk level timeline to understand your health journey",
        "💧 Stay Hydrated: Monitor your water intake and aim for 8+ glasses daily",
        "📈 Track Progress: Compare historical data to see improvements over time",
        "👨‍⚕️ Consult Healthcare Provider: Share these insights with your doctor for better care",
        "🔄 Update Demographics: Keep your health information current for accurate insights"
    ]
    
    for tip in tips:
        st.info(tip)
    
    # Footer disclaimer
    st.markdown("---")
    st.caption("""
    **Note:** These visualizations and trends are for informational purposes only. 
    They supplement, but do not replace, professional medical advice. Always consult 
    with healthcare professionals for medical decisions.
    """)
