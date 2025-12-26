import os
import base64
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user

def get_openai_client():
    """Get OpenAI client instance"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def encode_image_to_base64(image_path):
    """Encode image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None

def analyze_kidney_scan(image_path, demographics=None):
    """
    Analyze kidney-related medical scan using OpenAI Vision API
    Returns AI-generated analysis and recommendations
    """
    client = get_openai_client()
    
    if not client:
        return {
            'success': False,
            'error': 'OpenAI API key not configured',
            'analysis': None
        }
    
    try:
        # Encode image to base64
        base64_image = encode_image_to_base64(image_path)
        
        if not base64_image:
            return {
                'success': False,
                'error': 'Failed to encode image',
                'analysis': None
            }
        
        # Build context from demographics if available
        context = ""
        if demographics:
            context = f"""
Patient Context:
- Age: {demographics.get('age', 'Unknown')}
- Gender: {demographics.get('gender', 'Unknown')}
- Weight: {demographics.get('weight', 'Unknown')} kg
- Height: {demographics.get('height', 'Unknown')} cm
- Medical History: {demographics.get('medical_history', 'None provided')}
"""
        
        # Create analysis prompt
        prompt = f"""You are a medical imaging AI assistant specializing in kidney health analysis. 
Analyze this medical scan and provide a structured assessment.

{context}

Please provide a detailed analysis in JSON format with the following structure:
{{
    "scan_type": "type of medical scan (ultrasound/X-ray/CT/etc)",
    "image_quality": "assessment of image quality (excellent/good/fair/poor)",
    "key_findings": ["list of key observations"],
    "potential_concerns": ["list of any concerning findings or areas requiring attention"],
    "kidney_indicators": {{
        "size": "assessment of kidney size",
        "structure": "assessment of kidney structure",
        "abnormalities": "any visible abnormalities"
    }},
    "recommendations": ["list of recommended actions or follow-ups"],
    "risk_level": "overall risk assessment (low/moderate/high)",
    "confidence_score": "AI confidence in analysis (0-100)",
    "disclaimer": "important medical disclaimer"
}}

Important: This is for educational and monitoring purposes. Always emphasize the need for professional medical review."""
        
        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=2048
        )
        
        # Parse response
        analysis_result = json.loads(response.choices[0].message.content)
        
        return {
            'success': True,
            'error': None,
            'analysis': analysis_result
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Analysis failed: {str(e)}',
            'analysis': None
        }

def generate_health_insights(demographics, scan_analysis_list):
    """
    Generate comprehensive health insights based on demographics and scan analyses
    """
    client = get_openai_client()
    
    if not client:
        return None
    
    try:
        # Build context
        context = f"""
Patient Demographics:
- Age: {demographics.get('age', 'Unknown')}
- Gender: {demographics.get('gender', 'Unknown')}
- Weight: {demographics.get('weight', 'Unknown')} kg
- Height: {demographics.get('height', 'Unknown')} cm
- Daily Water Intake: {demographics.get('daily_water_intake', 'Unknown')} glasses
- Medical History: {demographics.get('medical_history', 'None provided')}

Scan Analysis History:
{json.dumps(scan_analysis_list, indent=2)}
"""
        
        prompt = f"""You are a kidney health specialist AI. Based on the patient's demographics and scan analysis history, 
provide comprehensive health insights and recommendations in JSON format:

{context}

Provide insights in this JSON structure:
{{
    "overall_health_status": "overall kidney health assessment",
    "risk_factors": ["identified risk factors"],
    "positive_indicators": ["positive health indicators"],
    "lifestyle_recommendations": ["specific lifestyle changes recommended"],
    "dietary_adjustments": ["specific dietary recommendations"],
    "monitoring_suggestions": ["what to monitor and how often"],
    "trends": "analysis of trends if multiple scans available",
    "next_steps": ["recommended next steps for care"]
}}"""
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=2048
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error generating insights: {str(e)}")
        return None

def assess_kidney_health_risk(demographics):
    """
    Assess kidney health risk based on demographics alone
    """
    client = get_openai_client()
    
    if not client:
        return None
    
    try:
        prompt = f"""Based on the following patient demographics, assess kidney health risk factors and provide recommendations:

Age: {demographics.get('age', 'Unknown')}
Gender: {demographics.get('gender', 'Unknown')}
Weight: {demographics.get('weight', 'Unknown')} kg
Height: {demographics.get('height', 'Unknown')} cm
Daily Water Intake: {demographics.get('daily_water_intake', 'Unknown')} glasses
Medical History: {demographics.get('medical_history', 'None provided')}

Provide assessment in JSON format:
{{
    "risk_level": "low/moderate/high",
    "risk_factors": ["list of identified risk factors"],
    "protective_factors": ["positive factors that reduce risk"],
    "personalized_recommendations": ["specific recommendations for this patient"],
    "warning_signs_to_watch": ["symptoms to monitor"],
    "preventive_measures": ["preventive actions to take"]
}}"""
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=1500
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error assessing risk: {str(e)}")
        return None
