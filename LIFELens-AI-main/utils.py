import os
from datetime import datetime
import streamlit as st

def create_upload_directory():
    """Create upload directory if it doesn't exist"""
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

def save_uploaded_file(uploaded_file, user_email):
    """Save uploaded file to disk"""
    try:
        upload_dir = create_upload_directory()
        
        # Create user-specific directory
        user_dir = os.path.join(upload_dir, user_email.replace('@', '_at_').replace('.', '_'))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(user_dir, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path, filename
    
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None, None

def get_file_type(filename):
    """Get file type from filename"""
    extension = filename.lower().split('.')[-1]
    if extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        return 'image'
    elif extension == 'pdf':
        return 'pdf'
    else:
        return 'other'

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def generate_report_content(demographics, upload_info=None):
    """Generate sample report content"""
    content = f"""
# Health Report

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Patient Information
"""
    
    if demographics:
        content += f"""
- **Age:** {demographics.get('age', 'Not provided')}
- **Gender:** {demographics.get('gender', 'Not provided')}
- **Weight:** {demographics.get('weight', 'Not provided')} kg
- **Height:** {demographics.get('height', 'Not provided')} cm
- **Daily Water Intake:** {demographics.get('daily_water_intake', 'Not provided')} glasses
"""
        
        # Calculate BMI if possible
        from diet_generator import calculate_bmi, get_bmi_category
        weight = demographics.get('weight')
        height = demographics.get('height')
        if weight and height:
            bmi = calculate_bmi(weight, height)
            if bmi:
                content += f"- **BMI:** {bmi} ({get_bmi_category(bmi)})\n"
    
    if upload_info:
        content += f"""

## Uploaded Scan Information
- **Filename:** {upload_info.get('filename', 'Unknown')}
- **File Type:** {upload_info.get('file_type', 'Unknown')}
- **Upload Date:** {upload_info.get('upload_date', 'Unknown')}
"""
    
    content += """

## Health Recommendations

### Dietary Guidelines
- Follow a kidney-friendly diet low in sodium
- Monitor protein intake based on kidney function
- Stay adequately hydrated
- Limit processed foods

### Lifestyle Recommendations
- Regular exercise as tolerated
- Monitor blood pressure regularly
- Avoid smoking and limit alcohol
- Get adequate sleep

### Follow-up Care
- Schedule regular check-ups with your healthcare provider
- Monitor kidney function through lab tests
- Keep track of symptoms and report changes

---

*Note: This report is for informational purposes only and should not replace professional medical advice. Always consult with your healthcare provider for personalized recommendations.*
"""
    
    return content
