import streamlit as st
from database import get_all_user_analyses, get_user_demographics
from ai_analyzer import generate_health_insights, assess_kidney_health_risk
import json

def show_page():
    """Display AI-powered health insights page"""
    st.title("🤖 AI Health Insights")
    st.subheader("Comprehensive kidney health analysis powered by artificial intelligence")
    
    # Get user data
    demographics = get_user_demographics(st.session_state.username)
    analyses = get_all_user_analyses(st.session_state.username)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scans Analyzed", len(analyses))
    
    with col2:
        if analyses:
            latest_risk = analyses[0].get('risk_level', 'Unknown')
            st.metric("Latest Risk Level", latest_risk.title() if latest_risk else "N/A")
    
    with col3:
        if analyses:
            avg_confidence = sum([a.get('confidence_score', 0) for a in analyses]) / len(analyses)
            st.metric("Avg Confidence", f"{int(avg_confidence)}%")
    
    with col4:
        high_risk_count = len([a for a in analyses if a.get('risk_level') == 'high'])
        st.metric("High Risk Alerts", high_risk_count)
    
    st.markdown("---")
    
    # Risk Assessment based on demographics
    if demographics:
        st.subheader("📊 Personal Risk Assessment")
        
        with st.spinner("Generating risk assessment..."):
            risk_assessment = assess_kidney_health_risk(demographics)
        
        if risk_assessment:
            risk_level = risk_assessment.get('risk_level', 'Unknown')
            
            # Display risk level with color coding
            if risk_level == 'low':
                st.success(f"🟢 **Risk Level:** {risk_level.upper()}")
            elif risk_level == 'moderate':
                st.warning(f"🟡 **Risk Level:** {risk_level.upper()}")
            else:
                st.error(f"🔴 **Risk Level:** {risk_level.upper()}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ⚠️ Risk Factors")
                for factor in risk_assessment.get('risk_factors', []):
                    st.write(f"• {factor}")
                
                if not risk_assessment.get('risk_factors'):
                    st.info("No significant risk factors identified")
            
            with col2:
                st.markdown("#### ✅ Protective Factors")
                for factor in risk_assessment.get('protective_factors', []):
                    st.write(f"• {factor}")
                
                if not risk_assessment.get('protective_factors'):
                    st.info("Consider adopting healthier lifestyle habits")
            
            # Recommendations
            st.markdown("#### 💡 Personalized Recommendations")
            for rec in risk_assessment.get('personalized_recommendations', []):
                st.info(f"💊 {rec}")
            
            # Warning signs
            if risk_assessment.get('warning_signs_to_watch'):
                st.markdown("#### ⚠️ Warning Signs to Monitor")
                for sign in risk_assessment.get('warning_signs_to_watch', []):
                    st.warning(f"👁️ {sign}")
            
            # Preventive measures
            if risk_assessment.get('preventive_measures'):
                st.markdown("#### 🛡️ Preventive Measures")
                for measure in risk_assessment.get('preventive_measures', []):
                    st.success(f"✓ {measure}")
    
    else:
        st.warning("⚠️ Please complete your demographics to get personalized risk assessment!")
        if st.button("📝 Go to Demographics"):
            st.session_state.current_page = "Demographics"
            st.rerun()
    
    # Comprehensive health insights from all analyses
    if analyses and len(analyses) > 0:
        st.markdown("---")
        st.subheader("🔍 Comprehensive Health Insights")
        
        with st.spinner("Generating comprehensive insights from your scan history..."):
            # Prepare analysis data for insights generation
            analysis_summaries = []
            for analysis in analyses:
                analysis_summaries.append({
                    'date': analysis.get('analyzed_at'),
                    'risk_level': analysis.get('risk_level'),
                    'confidence': analysis.get('confidence_score'),
                    'key_findings': analysis['analysis_data'].get('key_findings', []),
                    'concerns': analysis['analysis_data'].get('potential_concerns', [])
                })
            
            insights = generate_health_insights(demographics, analysis_summaries)
        
        if insights:
            # Overall health status
            st.markdown("#### 🏥 Overall Health Status")
            st.info(insights.get('overall_health_status', 'Analysis in progress...'))
            
            # Trends
            if insights.get('trends'):
                st.markdown("#### 📈 Health Trends")
                st.write(insights['trends'])
            
            # Recommendations in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🍽️ Dietary Adjustments")
                for adj in insights.get('dietary_adjustments', []):
                    st.write(f"• {adj}")
            
            with col2:
                st.markdown("#### 🏃 Lifestyle Recommendations")
                for rec in insights.get('lifestyle_recommendations', []):
                    st.write(f"• {rec}")
            
            # Monitoring suggestions
            st.markdown("#### 📊 Monitoring Suggestions")
            for suggestion in insights.get('monitoring_suggestions', []):
                st.info(f"📌 {suggestion}")
            
            # Next steps
            st.markdown("#### 🚀 Recommended Next Steps")
            for step in insights.get('next_steps', []):
                st.success(f"→ {step}")
    
    # Individual scan analyses
    if analyses:
        st.markdown("---")
        st.subheader("📋 Individual Scan Analyses")
        
        for i, analysis in enumerate(analyses):
            analysis_data = analysis['analysis_data']
            
            with st.expander(f"🔬 Analysis #{i+1}: {analysis['filename']} - {analysis['analyzed_at'][:19]}"):
                
                # Basic info
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Scan Type:** {analysis_data.get('scan_type', 'Unknown')}")
                    st.write(f"**Image Quality:** {analysis_data.get('image_quality', 'Unknown')}")
                
                with col2:
                    risk_level = analysis.get('risk_level', 'Unknown')
                    if risk_level == 'low':
                        st.success(f"**Risk Level:** {risk_level.upper()}")
                    elif risk_level == 'moderate':
                        st.warning(f"**Risk Level:** {risk_level.upper()}")
                    else:
                        st.error(f"**Risk Level:** {risk_level.upper()}")
                
                with col3:
                    confidence = analysis.get('confidence_score', 0)
                    st.metric("AI Confidence", f"{confidence}%")
                
                # Key findings
                st.markdown("##### 🔍 Key Findings")
                for finding in analysis_data.get('key_findings', []):
                    st.write(f"• {finding}")
                
                # Potential concerns
                if analysis_data.get('potential_concerns'):
                    st.markdown("##### ⚠️ Potential Concerns")
                    for concern in analysis_data['potential_concerns']:
                        st.warning(f"⚠️ {concern}")
                
                # Kidney indicators
                if analysis_data.get('kidney_indicators'):
                    st.markdown("##### 🫘 Kidney Indicators")
                    indicators = analysis_data['kidney_indicators']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Size:** {indicators.get('size', 'N/A')}")
                    with col2:
                        st.write(f"**Structure:** {indicators.get('structure', 'N/A')}")
                    with col3:
                        st.write(f"**Abnormalities:** {indicators.get('abnormalities', 'None detected')}")
                
                # Recommendations
                if analysis_data.get('recommendations'):
                    st.markdown("##### 💡 Recommendations")
                    for rec in analysis_data['recommendations']:
                        st.info(f"→ {rec}")
                
                # Disclaimer
                if analysis_data.get('disclaimer'):
                    st.markdown("##### ⚕️ Medical Disclaimer")
                    st.caption(analysis_data['disclaimer'])
    
    else:
        st.info("📭 No AI analyses available yet. Upload and analyze medical scans to see insights here!")
    
    # Footer
    st.markdown("---")
    st.error("""
    🚨 **Important Medical Disclaimer**
    
    All AI-generated analyses and insights are for informational and educational purposes only. 
    They do not constitute medical advice, diagnosis, or treatment. Always consult with qualified 
    healthcare professionals for medical decisions and interpretations of medical scans.
    
    In case of medical emergencies, contact your healthcare provider immediately or call emergency services.
    """)
