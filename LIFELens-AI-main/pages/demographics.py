import streamlit as st
from database import get_user_demographics, save_demographics
from diet_generator import calculate_bmi, get_bmi_category

def show_page():
    """Display the demographics page"""
    st.title("👤 Demographics & Health Information")
    st.subheader("Help us personalize your kidney health recommendations")
    
    # Get existing demographics
    existing_demographics = get_user_demographics(st.session_state.username)
    
    # Create form for demographics
    with st.form("demographics_form"):
        st.markdown("### Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input(
                "Age (years)",
                min_value=1,
                max_value=120,
                value=existing_demographics.get('age', 30) if existing_demographics else 30,
                help="Your age helps us provide age-appropriate recommendations"
            )
            
            weight = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=300.0,
                value=float(existing_demographics.get('weight', 70.0)) if existing_demographics and existing_demographics.get('weight') else 70.0,
                step=0.1,
                help="Your current weight in kilograms"
            )
            
            daily_water_intake = st.number_input(
                "Daily Water Intake (glasses)",
                min_value=0,
                max_value=20,
                value=existing_demographics.get('daily_water_intake', 8) if existing_demographics and existing_demographics.get('daily_water_intake') else 8,
                help="Number of 8oz glasses of water you drink per day"
            )
        
        with col2:
            gender = st.selectbox(
                "Gender",
                options=["Male", "Female", "Other", "Prefer not to say"],
                index=0 if not existing_demographics else (
                    ["Male", "Female", "Other", "Prefer not to say"].index(existing_demographics.get('gender', 'Male'))
                    if existing_demographics.get('gender') in ["Male", "Female", "Other", "Prefer not to say"]
                    else 0
                ),
                help="Biological sex can affect kidney health recommendations"
            )
            
            height = st.number_input(
                "Height (cm)",
                min_value=50,
                max_value=250,
                value=existing_demographics.get('height', 170) if existing_demographics and existing_demographics.get('height') else 170,
                help="Your height in centimeters"
            )
        
        st.markdown("### Medical Information")
        
        medical_history = st.text_area(
            "Medical History",
            value=existing_demographics.get('medical_history', '') if existing_demographics else '',
            height=100,
            help="Please list any relevant medical conditions, medications, or previous kidney-related issues",
            placeholder="e.g., diabetes, hypertension, kidney stones, family history of kidney disease..."
        )
        
        # BMI calculation preview
        if weight and height:
            bmi = calculate_bmi(weight, height)
            if bmi:
                st.info(f"**BMI Preview:** {bmi} ({get_bmi_category(bmi)})")
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Demographics", use_container_width=True)
        
        if submitted:
            # Prepare demographics data
            demographics_data = {
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'daily_water_intake': daily_water_intake,
                'medical_history': medical_history.strip()
            }
            
            # Save to database
            success, message = save_demographics(st.session_state.username, demographics_data)
            
            if success:
                st.success(message)
                st.success("Your demographics have been updated! This will help us provide better recommendations.")
                
                # Show updated BMI
                bmi = calculate_bmi(weight, height)
                if bmi:
                    st.metric("Your BMI", f"{bmi}", help=f"Category: {get_bmi_category(bmi)}")
                
            else:
                st.error(message)
    
    # Display current demographics if they exist
    if existing_demographics:
        st.markdown("---")
        st.subheader("📋 Current Demographics Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Age", f"{existing_demographics.get('age', 'Not set')} years" if existing_demographics.get('age') else "Not set")
            st.metric("Gender", existing_demographics.get('gender', 'Not set'))
        
        with col2:
            st.metric("Weight", f"{existing_demographics.get('weight', 'Not set')} kg" if existing_demographics.get('weight') else "Not set")
            st.metric("Height", f"{existing_demographics.get('height', 'Not set')} cm" if existing_demographics.get('height') else "Not set")
        
        with col3:
            st.metric("Water Intake", f"{existing_demographics.get('daily_water_intake', 'Not set')} glasses/day" if existing_demographics.get('daily_water_intake') else "Not set")
            
            # BMI calculation
            weight = existing_demographics.get('weight')
            height = existing_demographics.get('height')
            if weight and height:
                bmi = calculate_bmi(weight, height)
                if bmi:
                    st.metric("BMI", f"{bmi}", help=f"Category: {get_bmi_category(bmi)}")
        
        # Medical history
        if existing_demographics.get('medical_history'):
            st.subheader("🏥 Medical History")
            st.info(existing_demographics['medical_history'])
        
        # Health recommendations based on demographics
        st.subheader("💡 Personalized Recommendations")
        
        recommendations = []
        
        # Age-based recommendations
        age = existing_demographics.get('age', 0)
        if age > 65:
            recommendations.append("🧓 Consider more frequent kidney function monitoring as recommended by your doctor")
        elif age < 30:
            recommendations.append("💪 Establish healthy habits early for long-term kidney health")
        
        # BMI-based recommendations
        if weight and height:
            bmi = calculate_bmi(weight, height)
            if bmi and bmi > 25:
                recommendations.append("⚖️ Consider weight management strategies to reduce kidney disease risk")
            elif bmi and bmi < 18.5:
                recommendations.append("🍎 Consider consulting with a nutritionist about healthy weight gain")
        
        # Water intake recommendations
        water_intake = existing_demographics.get('daily_water_intake', 0)
        if water_intake < 8:
            recommendations.append("💧 Increase water intake to at least 8 glasses per day (unless restricted by doctor)")
        elif water_intake > 12:
            recommendations.append("⚠️ Very high water intake - consult your doctor if this is due to excessive thirst")
        
        # Medical history recommendations
        medical_history = existing_demographics.get('medical_history', '').lower()
        if 'diabetes' in medical_history:
            recommendations.append("🩺 Monitor blood sugar levels regularly to protect kidney function")
        if 'hypertension' in medical_history or 'high blood pressure' in medical_history:
            recommendations.append("💊 Follow blood pressure medication regimen strictly")
        
        if recommendations:
            for rec in recommendations:
                st.warning(rec)
        else:
            st.success("✅ Your demographics look good! Keep up the healthy lifestyle.")
    
    else:
        st.info("📝 Please fill out your demographics to get personalized kidney health recommendations!")
