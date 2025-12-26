import streamlit as st
import os
from database import init_database, create_user, verify_user, get_user_demographics
from auth import hash_password, verify_password, validate_email
import pages.home as home
import pages.demographics as demographics
import pages.upload_analyze as upload_analyze
import pages.diet_chart as diet_chart
import pages.reports as reports
import pages.ai_insights as ai_insights
import pages.health_tracking as health_tracking

# Initialize the database
init_database()

# Set page configuration
st.set_page_config(
    page_title="LIFELens-AI: Kidney Health Monitoring",
    page_icon="🫘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

def show_login_signup():
    """Display login and signup forms"""
    st.title("🫘 LIFELens-AI")
    st.subheader("Intelligent Kidney Health Monitoring and Assistance")
    
    # Create tabs for login, signup, and password recovery
    login_tab, signup_tab, recovery_tab = st.tabs(["Login", "Sign Up", "Forgot Password"])
    
    with login_tab:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if email and password:
                    if validate_email(email):
                        user = verify_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.username = email
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.error("Please enter a valid email address")
                else:
                    st.error("Please fill in all fields")
    
    with signup_tab:
        st.header("Sign Up")
        with st.form("signup_form"):
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            full_name = st.text_input("Full Name")
            
            # Security question for password recovery
            st.markdown("**Set up Password Recovery**")
            security_questions = [
                "What was the name of your first pet?",
                "What is your mother's maiden name?",
                "What city were you born in?",
                "What is your favorite color?",
                "What was your childhood nickname?"
            ]
            security_question = st.selectbox("Security Question", security_questions)
            security_answer = st.text_input("Security Answer", type="password", help="This will be used to recover your password if you forget it")
            
            signup_button = st.form_submit_button("Sign Up")
            
            if signup_button:
                if all([new_email, new_password, confirm_password, full_name, security_answer]):
                    if validate_email(new_email):
                        if new_password == confirm_password:
                            if len(new_password) >= 6:
                                success, message = create_user(new_email, new_password, full_name)
                                if success:
                                    # Save security question
                                    from database import update_security_question
                                    update_security_question(new_email, security_question, security_answer)
                                    st.success("Account created successfully! Please login.")
                                else:
                                    st.error(message)
                            else:
                                st.error("Password must be at least 6 characters long")
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please enter a valid email address")
                else:
                    st.error("Please fill in all fields including security answer")
    
    with recovery_tab:
        st.header("Password Recovery")
        st.write("Answer your security question to reset your password")
        
        with st.form("recovery_form"):
            recovery_email = st.text_input("Email", key="recovery_email")
            
            # Check if email exists and get security question
            if recovery_email and validate_email(recovery_email):
                from database import get_security_question
                security_question = get_security_question(recovery_email)
                
                if security_question:
                    st.info(f"**Security Question:** {security_question}")
                    security_answer_input = st.text_input("Your Answer", key="security_answer_input")
                    new_password_recovery = st.text_input("New Password", type="password", key="new_password_recovery")
                    confirm_password_recovery = st.text_input("Confirm New Password", type="password", key="confirm_password_recovery")
                    
                    recovery_button = st.form_submit_button("Reset Password")
                    
                    if recovery_button:
                        if all([security_answer_input, new_password_recovery, confirm_password_recovery]):
                            from database import verify_security_answer, reset_password
                            
                            if verify_security_answer(recovery_email, security_answer_input):
                                if new_password_recovery == confirm_password_recovery:
                                    if len(new_password_recovery) >= 6:
                                        if reset_password(recovery_email, new_password_recovery):
                                            st.success("✅ Password reset successfully! Please login with your new password.")
                                        else:
                                            st.error("Failed to reset password. Please try again.")
                                    else:
                                        st.error("Password must be at least 6 characters long")
                                else:
                                    st.error("Passwords do not match")
                            else:
                                st.error("Incorrect security answer. Please try again.")
                        else:
                            st.error("Please fill in all fields")
                elif recovery_email:
                    st.warning("No security question set for this account. Please contact support.")
            else:
                st.form_submit_button("Reset Password", disabled=True)
                if recovery_email and not validate_email(recovery_email):
                    st.error("Please enter a valid email address")

def show_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        st.title("🫘 LIFELens-AI")
        st.write(f"Welcome, {st.session_state.username}")
        
        # Navigation menu
        pages = ["Home", "Demographics", "Upload & Analyze", "AI Insights", "Health Tracking", "Diet Chart", "Reports"]
        
        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.divider()
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "Home"
            st.rerun()

def main():
    """Main application logic"""
    if not st.session_state.logged_in:
        show_login_signup()
    else:
        show_sidebar()
        
        # Display the selected page
        if st.session_state.current_page == "Home":
            home.show_page()
        elif st.session_state.current_page == "Demographics":
            demographics.show_page()
        elif st.session_state.current_page == "Upload & Analyze":
            upload_analyze.show_page()
        elif st.session_state.current_page == "AI Insights":
            ai_insights.show_page()
        elif st.session_state.current_page == "Health Tracking":
            health_tracking.show_page()
        elif st.session_state.current_page == "Diet Chart":
            diet_chart.show_page()
        elif st.session_state.current_page == "Reports":
            reports.show_page()

if __name__ == "__main__":
    main()
