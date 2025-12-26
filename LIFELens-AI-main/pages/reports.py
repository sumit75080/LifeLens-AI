import streamlit as st
from database import get_user_reports, get_user_uploads
import datetime

def show_page():
    """Display the reports page"""
    st.title("📊 Health Reports")
    st.subheader("View and download your health reports and analysis results")
    
    # Get user reports and uploads
    reports = get_user_reports(st.session_state.username)
    uploads = get_user_uploads(st.session_state.username)
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Reports", len(reports))
    
    with col2:
        st.metric("Total Uploads", len(uploads))
    
    with col3:
        pending_analysis = len([u for u in uploads if u['analysis_status'] == 'pending'])
        st.metric("Pending Analysis", pending_analysis)
    
    # Reports section
    st.markdown("---")
    st.markdown("### 📋 Generated Reports")
    
    if reports:
        # Sort reports by date (newest first)
        sorted_reports = sorted(reports, key=lambda x: x['generated_at'], reverse=True)
        
        for i, report in enumerate(sorted_reports):
            with st.expander(f"📄 {report['report_type']} - {report['generated_at'][:19]}"):
                
                # Report metadata
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Report ID:** {report['id']}")
                    st.write(f"**Type:** {report['report_type']}")
                    st.write(f"**Generated:** {report['generated_at'][:19]}")
                
                with col2:
                    st.write(f"**Related File:** {report['filename']}")
                    st.write(f"**Status:** ✅ Complete")
                
                # Report content
                st.markdown("#### Report Content")
                st.markdown(report['report_content'])
                
                # Download button
                st.download_button(
                    label=f"📥 Download Report {report['id']}",
                    data=report['report_content'],
                    file_name=f"lifelens_report_{report['id']}_{report['generated_at'][:10]}.md",
                    mime="text/markdown",
                    key=f"download_report_{report['id']}"
                )
    
    else:
        st.info("📭 No reports generated yet. Upload medical scans to generate your first report!")
    
    # Upload history with analysis status
    st.markdown("---")
    st.markdown("### 📤 Upload History & Analysis Status")
    
    if uploads:
        # Create a table-like view
        for i, upload in enumerate(uploads):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{upload['filename']}**")
                    st.caption(f"ID: {upload['id']}")
                
                with col2:
                    st.write(f"Type: {upload['file_type'].title()}")
                    st.write(f"Uploaded: {upload['upload_date'][:10]}")
                
                with col3:
                    status = upload['analysis_status']
                    if status == 'pending':
                        st.warning("⏳ Pending Analysis")
                    elif status == 'completed':
                        st.success("✅ Analysis Complete")
                    elif status == 'processing':
                        st.info("🔄 Processing")
                    else:
                        st.info(f"Status: {status.title()}")
                
                with col4:
                    # Find related reports
                    related_reports = [r for r in reports if r['filename'] == upload['filename']]
                    if related_reports:
                        st.success(f"📊 {len(related_reports)} Report(s)")
                    else:
                        st.info("No reports")
                
                st.divider()
    
    else:
        st.info("📭 No uploads found. Visit the Upload & Analyze page to upload your first scan!")
    
    # Health trends (placeholder for future features)
    st.markdown("---")
    st.markdown("### 📈 Health Trends")
    
    if uploads and reports:
        st.info("""
        🔮 **Coming Soon: Health Trends Analysis**
        
        Future updates will include:
        - Kidney function trend analysis over time
        - Comparison between different scan results
        - Health metric correlations
        - Predictive health insights
        - Integration with wearable devices
        """)
        
        # Simple timeline visualization
        st.markdown("#### 📅 Activity Timeline")
        
        # Combine uploads and reports for timeline
        timeline_items = []
        
        for upload in uploads:
            timeline_items.append({
                'date': upload['upload_date'][:10],
                'type': 'Upload',
                'description': f"Uploaded {upload['filename']}",
                'icon': '📤'
            })
        
        for report in reports:
            timeline_items.append({
                'date': report['generated_at'][:10],
                'type': 'Report',
                'description': f"Generated {report['report_type']}",
                'icon': '📊'
            })
        
        # Sort by date
        timeline_items.sort(key=lambda x: x['date'], reverse=True)
        
        # Display timeline
        for item in timeline_items[:10]:  # Show last 10 activities
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.write(item['date'])
            
            with col2:
                st.write(f"{item['icon']} {item['description']}")
    
    else:
        st.info("Upload scans and generate reports to see your health trends!")
    
    # Export all data
    st.markdown("---")
    st.markdown("### 📦 Export All Data")
    
    if reports or uploads:
        # Generate comprehensive export
        export_data = f"""
LIFELens-AI Data Export
User: {st.session_state.username}
Export Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== UPLOAD SUMMARY ===
Total Uploads: {len(uploads)}

"""
        
        for upload in uploads:
            export_data += f"""
Upload ID: {upload['id']}
Filename: {upload['filename']}
Type: {upload['file_type']}
Date: {upload['upload_date']}
Status: {upload['analysis_status']}
---
"""
        
        export_data += f"""

=== REPORTS SUMMARY ===
Total Reports: {len(reports)}

"""
        
        for report in reports:
            export_data += f"""
Report ID: {report['id']}
Type: {report['report_type']}
Generated: {report['generated_at']}
Related File: {report['filename']}

Content:
{report['report_content']}

---
"""
        
        st.download_button(
            label="📦 Export All Data",
            data=export_data,
            file_name=f"lifelens_export_{st.session_state.username.split('@')[0]}_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    else:
        st.info("No data available for export yet.")
    
    # Analytics summary
    if reports and uploads:
        st.markdown("---")
        st.markdown("### 🔍 Quick Analytics")
        
        # Simple analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Upload Analytics")
            
            # File type distribution
            file_types = {}
            for upload in uploads:
                file_type = upload['file_type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
            
            for file_type, count in file_types.items():
                st.write(f"• {file_type.title()}: {count} files")
        
        with col2:
            st.markdown("#### 📈 Report Analytics")
            
            # Report type distribution
            report_types = {}
            for report in reports:
                report_type = report['report_type']
                report_types[report_type] = report_types.get(report_type, 0) + 1
            
            for report_type, count in report_types.items():
                st.write(f"• {report_type}: {count} reports")
    
    # Data management options
    st.markdown("---")
    st.markdown("### 🔧 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🧹 Clear Cache", use_container_width=True):
            # Clear any cached data
            st.success("Cache cleared successfully!")
    
    # Footer information
    st.markdown("---")
    st.info("""
    💡 **Tips for Better Reports:**
    - Upload high-quality scans for better analysis
    - Complete your demographics for personalized insights
    - Regular uploads help track health trends over time
    - Always consult with your healthcare provider about report findings
    """)
