import streamlit as st
from database import get_user_demographics
from diet_generator import get_kidney_health_tips, calculate_bmi, get_bmi_category

def show_page():
    """Display the home page"""
    st.title("🏠 Welcome to LIFELens-AI")
    st.subheader("Your Personal Kidney Health Assistant")
    
    # Get user demographics for personalized display
    demographics = get_user_demographics(st.session_state.username)
    
    # Welcome message
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Welcome to LIFELens-AI, your comprehensive kidney health monitoring platform. 
        Our AI-powered system helps you track your health, analyze medical scans, and 
        receive personalized recommendations for better kidney care.
        """)
        
        # Quick stats if demographics are available
        if demographics:
            st.subheader("📊 Your Health Overview")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                age = demographics.get('age')
                if age:
                    st.metric("Age", f"{age} years")
                else:
                    st.metric("Age", "Not set")
            
            with col_b:
                water_intake = demographics.get('daily_water_intake')
                if water_intake:
                    st.metric("Daily Water Intake", f"{water_intake} glasses")
                    if water_intake < 8:
                        st.caption("⚠️ Consider increasing water intake")
                else:
                    st.metric("Daily Water Intake", "Not set")
            
            with col_c:
                weight = demographics.get('weight')
                height = demographics.get('height')
                if weight and height:
                    bmi = calculate_bmi(weight, height)
                    if bmi:
                        st.metric("BMI", f"{bmi}")
                        st.caption(f"{get_bmi_category(bmi)}")
                else:
                    st.metric("BMI", "Not calculated")
        else:
            st.info("📝 Complete your demographics to see personalized health insights!")
    
    with col2:
        st.info("🫘 **LIFELens-AI**\n\nYour comprehensive kidney health monitoring platform powered by AI technology.")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📝 Update Demographics", use_container_width=True):
            st.session_state.current_page = "Demographics"
            st.rerun()
    
    with action_col2:
        if st.button("📤 Upload Scan", use_container_width=True):
            st.session_state.current_page = "Upload & Analyze"
            st.rerun()
    
    with action_col3:
        if st.button("🍽️ View Diet Chart", use_container_width=True):
            st.session_state.current_page = "Diet Chart"
            st.rerun()
    
    # Health tips section
    st.subheader("💡 Kidney Health Tips")
    
    tips = get_kidney_health_tips()
    
    # Display tips in a nice format
    tip_col1, tip_col2 = st.columns(2)
    
    for i, tip in enumerate(tips):
        if i % 2 == 0:
            with tip_col1:
                st.info(tip)
        else:
            with tip_col2:
                st.info(tip)
    
    # Recent activity placeholder
    st.subheader("📈 Recent Activity")
    
    # Import here to avoid circular imports
    from database import get_user_uploads
    
    recent_uploads = get_user_uploads(st.session_state.username)
    
    if recent_uploads:
        st.success(f"You have {len(recent_uploads)} uploaded scans. Visit the Reports page to view them.")
        
        # Show most recent upload
        latest_upload = recent_uploads[0]
        with st.expander("Latest Upload"):
            st.write(f"**Filename:** {latest_upload['filename']}")
            st.write(f"**Upload Date:** {latest_upload['upload_date']}")
            st.write(f"**Status:** {latest_upload['analysis_status'].title()}")
    else:
        st.info("No uploads yet. Start by uploading your first medical scan!")
    
    # System status
    st.subheader("🔧 System Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.success("✅ Database Connected")
    
    with status_col2:
        st.success("✅ User Authenticated")
    
    with status_col3:
        if demographics:
            st.success("✅ Profile Complete")
        else:
            st.warning("⚠️ Profile Incomplete")
