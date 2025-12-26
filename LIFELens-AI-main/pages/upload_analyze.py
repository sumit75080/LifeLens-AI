import streamlit as st
from utils import save_uploaded_file, get_file_type, format_file_size
from database import save_upload, get_user_uploads
import os

def show_page():
    """Display the upload and analyze page"""
    st.title("📤 Upload & Analyze Medical Scans")
    st.subheader("Upload your medical scans for AI-powered analysis")
    
    # Upload section
    st.markdown("### 📁 Upload New Scan")
    
    uploaded_file = st.file_uploader(
        "Choose a medical scan file",
        type=['png', 'jpg', 'jpeg', 'pdf', 'bmp', 'gif'],
        help="Supported formats: PNG, JPG, JPEG, PDF, BMP, GIF"
    )
    
    if uploaded_file is not None:
        # Display file information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**File size:** {format_file_size(uploaded_file.size)}")
            st.write(f"**File type:** {uploaded_file.type}")
        
        with col2:
            # Show image preview if it's an image
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="Preview", width=200)
        
        # Upload button
        if st.button("📤 Upload File", use_container_width=True, type="primary"):
            try:
                # Save file to disk
                file_path, filename = save_uploaded_file(uploaded_file, st.session_state.username)
                
                if file_path and filename:
                    # Save upload information to database
                    file_type = get_file_type(filename)
                    upload_id = save_upload(
                        st.session_state.username,
                        filename,
                        file_path,
                        file_type
                    )
                    
                    if upload_id:
                        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
                        st.info("🔄 File has been saved and is ready for analysis. AI analysis features will be available in future updates.")
                        
                        # Generate a simple report
                        from database import save_report, get_user_demographics
                        from utils import generate_report_content
                        
                        demographics = get_user_demographics(st.session_state.username)
                        upload_info = {
                            'filename': filename,
                            'file_type': file_type,
                            'upload_date': 'Just now'
                        }
                        
                        report_content = generate_report_content(demographics, upload_info)
                        report_id = save_report(
                            st.session_state.username,
                            upload_id,
                            "Upload Report",
                            report_content
                        )
                        
                        if report_id:
                            st.success("📋 Initial report generated! View it in the Reports section.")
                        
                        # Clear the uploader
                        st.rerun()
                    else:
                        st.error("❌ Error saving upload information to database")
                else:
                    st.error("❌ Error saving file")
                    
            except Exception as e:
                st.error(f"❌ Upload failed: {str(e)}")
    
    # Divider
    st.markdown("---")
    
    # Display upload history
    st.markdown("### 📚 Upload History")
    
    uploads = get_user_uploads(st.session_state.username)
    
    if uploads:
        st.write(f"You have **{len(uploads)}** uploaded files:")
        
        for i, upload in enumerate(uploads):
            with st.expander(f"📄 {upload['filename']} - {upload['upload_date'][:19]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**File ID:** {upload['id']}")
                    st.write(f"**Filename:** {upload['filename']}")
                    st.write(f"**File Type:** {upload['file_type'].title()}")
                
                with col2:
                    st.write(f"**Upload Date:** {upload['upload_date'][:19]}")
                    st.write(f"**Analysis Status:** {upload['analysis_status'].title()}")
                
                # Action buttons
                button_col1, button_col2, button_col3 = st.columns(3)
                
                with button_col1:
                    if st.button(f"🔍 Analyze", key=f"analyze_{upload['id']}"):
                        # Import AI analyzer
                        from ai_analyzer import analyze_kidney_scan
                        from database import get_ai_analysis, save_ai_analysis, get_user_demographics
                        
                        # Check if already analyzed
                        existing_analysis = get_ai_analysis(upload['id'])
                        
                        if existing_analysis:
                            st.success("✅ Scan already analyzed! View results in the Reports section.")
                        else:
                            with st.spinner("🔄 Analyzing scan with AI..."):
                                # Get user demographics for context
                                demographics = get_user_demographics(st.session_state.username)
                                
                                # Find the file path
                                from database import get_connection
                                conn = get_connection()
                                cursor = conn.cursor()
                                cursor.execute("SELECT file_path FROM uploads WHERE id = ?", (upload['id'],))
                                result = cursor.fetchone()
                                conn.close()
                                
                                if result:
                                    file_path = result[0]
                                    
                                    # Perform AI analysis
                                    analysis_result = analyze_kidney_scan(file_path, demographics)
                                    
                                    if analysis_result['success']:
                                        analysis_data = analysis_result['analysis']
                                        
                                        # Save analysis to database
                                        analysis_id = save_ai_analysis(
                                            upload['id'],
                                            st.session_state.username,
                                            analysis_data,
                                            risk_level=analysis_data.get('risk_level'),
                                            confidence_score=analysis_data.get('confidence_score')
                                        )
                                        
                                        if analysis_id:
                                            st.success("✅ AI Analysis completed successfully!")
                                            st.rerun()
                                        else:
                                            st.error("Failed to save analysis results")
                                    else:
                                        st.error(f"Analysis failed: {analysis_result['error']}")
                                else:
                                    st.error("File not found")
                
                with button_col2:
                    if st.button(f"📋 View Report", key=f"report_{upload['id']}"):
                        st.session_state.current_page = "Reports"
                        st.rerun()
                
                with button_col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{upload['id']}", type="secondary"):
                        st.warning("Delete functionality will be implemented in future updates.")
        
    else:
        st.info("📭 No files uploaded yet. Upload your first medical scan to get started!")
    
    # Information about AI analysis
    st.markdown("---")
    st.markdown("### 🤖 About AI Analysis")
    
    st.info("""
    **Current Status:** Upload and storage functionality is active.
    
    **Coming Soon:**
    - AI-powered analysis of kidney-related scans
    - Automated detection of potential health indicators
    - Detailed analysis reports with visualizations
    - Integration with healthcare provider systems
    
    **Supported Analysis Types (Future):**
    - Kidney ultrasound analysis
    - X-ray interpretation
    - CT scan assessment
    - Blood test result analysis
    """)
    
    # Guidelines for uploads
    st.markdown("### 📋 Upload Guidelines")
    
    guidelines = [
        "🎯 **Quality:** Ensure scans are clear and high-resolution",
        "📏 **Size:** Maximum file size is 10MB per upload",
        "🏥 **Source:** Only upload scans from certified medical facilities",
        "🔒 **Privacy:** All uploads are securely encrypted and stored",
        "📱 **Format:** Supported formats: PNG, JPG, JPEG, PDF, BMP, GIF",
        "⚠️ **Important:** This platform supplements, not replaces, professional medical advice"
    ]
    
    for guideline in guidelines:
        st.write(guideline)
    
    # Emergency notice
    st.error("""
    🚨 **Emergency Notice**
    
    This platform is for monitoring and educational purposes only. 
    In case of medical emergencies, contact your healthcare provider immediately or call emergency services.
    """)
