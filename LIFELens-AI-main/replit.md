# LIFELens-AI: Intelligent Kidney Health Monitoring and Assistance

## Overview
LIFELens-AI is a comprehensive AI-powered healthcare platform designed to assist patients and healthcare providers in monitoring kidney health, analyzing medical scans, and managing personalized health data. Built with Streamlit and powered by OpenAI's GPT-5 Vision API.

## Features

### Core Functionality
- **User Authentication**: Secure signup/login system with password hashing and email validation
- **Password Recovery**: Security question-based password reset system
- **Personalized Dashboard**: Comprehensive health overview with quick access to all features

### Demographics & Health Tracking
- **Demographics Management**: Track age, gender, weight, height, water intake, and medical history
- **BMI Calculation**: Automatic BMI calculation and categorization
- **Real-time Updates**: Changes reflected immediately across the platform

### Medical Scan Analysis
- **Upload & Storage**: Support for JPEG, PNG, PDF, BMP, GIF formats
- **AI-Powered Analysis**: OpenAI Vision API analyzes kidney-related medical scans
- **Automated Detection**: Identifies potential kidney conditions and health indicators
- **Risk Assessment**: Low/Moderate/High risk categorization with confidence scores

### AI Health Insights
- **Personalized Risk Assessment**: AI-driven kidney health risk evaluation
- **Comprehensive Insights**: Health trends, dietary recommendations, lifestyle changes
- **Risk Factors Analysis**: Identifies protective and risk factors
- **Warning Signs**: Monitors symptoms to watch for

### Health Tracking & Visualization
- **Risk Level Timeline**: Track kidney health risk progression over time
- **Confidence Score Charts**: Visualize AI analysis confidence levels
- **Risk Distribution**: Pie charts showing risk level distribution
- **Water Intake Monitoring**: Track daily hydration levels
- **Health Metrics Radar**: Comprehensive health indicator visualization
- **Findings Frequency**: Track common medical findings

### Diet & Nutrition
- **Personalized Diet Plans**: Kidney-friendly meal recommendations
- **Customized Guidelines**: Based on age, weight, BMI, and medical history
- **Dietary Restrictions**: Accounts for diabetes, hypertension, kidney stones
- **Downloadable Plans**: Export diet charts as text files

### Reports & Export
- **Upload History**: View all uploaded scans with analysis status
- **AI Analysis Reports**: Detailed reports with findings and recommendations
- **PDF Export**: Comprehensive health reports in PDF format
- **CSV Export**: Download health data for analysis
- **Historical Comparison**: Compare analyses over time

## Technology Stack

### Backend
- **Python 3.11**: Core programming language
- **SQLite**: Local database for data persistence
- **OpenAI GPT-5**: AI-powered medical scan analysis
- **ReportLab**: PDF report generation

### Frontend
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data processing and export

### Security
- **Password Hashing**: SHA-256 with salt for secure password storage
- **Email Validation**: Regex-based email format validation
- **Security Questions**: Password recovery mechanism
- **Session Management**: Secure user session handling

## Database Schema

### Tables
1. **users**: User credentials and security information
2. **demographics**: User health demographics
3. **uploads**: Medical scan uploads metadata
4. **reports**: Generated health reports
5. **ai_analysis**: AI analysis results and risk assessments

## Project Structure

```
.
├── app.py                      # Main application entry point
├── auth.py                     # Authentication utilities
├── database.py                 # Database operations
├── ai_analyzer.py             # OpenAI Vision integration
├── diet_generator.py          # Diet recommendation engine
├── health_charts.py           # Plotly chart generation
├── pdf_generator.py           # PDF report generation
├── utils.py                   # Utility functions
├── pages/
│   ├── home.py               # Home dashboard
│   ├── demographics.py       # Demographics management
│   ├── upload_analyze.py     # Scan upload and analysis
│   ├── ai_insights.py        # AI health insights
│   ├── health_tracking.py    # Health visualization
│   ├── diet_chart.py         # Diet recommendations
│   └── reports.py            # Reports and history
└── .streamlit/
    └── config.toml           # Streamlit configuration
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for AI analysis (required for AI features)
- `SESSION_SECRET`: Salt for password hashing

### Streamlit Config (.streamlit/config.toml)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Usage

### First Time Setup
1. Create an account with email, password, full name, and security question
2. Complete demographics form for personalized recommendations
3. Upload medical scans for AI analysis

### Daily Use
1. Login with credentials
2. Check dashboard for health overview
3. Upload new scans for analysis
4. View AI insights and risk assessment
5. Track health trends over time
6. Download reports as needed

### Password Recovery
1. Go to "Forgot Password" tab
2. Enter your email
3. Answer security question
4. Set new password

## AI Analysis Features

### Scan Analysis
- Scan type detection (ultrasound, X-ray, CT)
- Image quality assessment
- Key findings identification
- Potential concerns flagging
- Kidney size and structure evaluation
- Risk level categorization
- Confidence score (0-100%)

### Health Insights
- Overall health status assessment
- Risk factor identification
- Lifestyle and dietary recommendations
- Monitoring suggestions
- Trend analysis across multiple scans
- Next steps recommendations

## Best Practices

### For Users
1. Upload high-quality, clear medical scans
2. Keep demographics information current
3. Review AI insights with healthcare providers
4. Track trends regularly for better health monitoring
5. Maintain adequate hydration (8+ glasses daily)
6. Follow personalized dietary recommendations

### For Healthcare Integration
- AI analysis supplements, not replaces, professional medical care
- All findings should be reviewed by qualified healthcare providers
- Use as educational and monitoring tool
- Share insights with your medical team

## Disclaimers

⚠️ **Medical Disclaimer**: This platform is for informational and educational purposes only. AI-generated analyses and insights do not constitute medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

🚨 **Emergency Notice**: In case of medical emergencies, contact your healthcare provider immediately or call emergency services. Do not rely on this platform for urgent medical situations.

## Recent Updates (October 2025)

### Version 2.0 Features
- ✅ OpenAI GPT-5 Vision integration for medical scan analysis
- ✅ AI-powered health insights and risk assessment
- ✅ Interactive health tracking charts and visualizations
- ✅ PDF export for comprehensive health reports
- ✅ Password recovery with security questions
- ✅ Enhanced navigation with AI Insights and Health Tracking pages

### Version 1.0 Features (Initial Release)
- ✅ User authentication and authorization
- ✅ Demographics management
- ✅ Medical scan upload and storage
- ✅ Personalized kidney-friendly diet recommendations
- ✅ Basic health reports and monitoring

## Development Notes

### Key Implementation Details
- OpenAI GPT-5 model used for vision analysis (released August 7, 2025)
- Uses `max_tokens` parameter (not `max_completion_tokens`)
- JSON response format for structured AI output
- Base64 image encoding for Vision API
- SHA-256 password hashing with environment salt
- SQLite for local data persistence

### Future Enhancements
- Email verification system
- Integration with wearable devices
- Multi-language support
- Mobile app version
- Advanced predictive analytics
- Healthcare provider portal
- Real-time blood pressure and kidney function monitoring

## Support

For technical issues or questions:
- Check the AI Insights page for health-related queries
- Review the Reports page for analysis history
- Ensure OPENAI_API_KEY is properly configured for AI features
- Contact support for account-related issues

---

**Built with ❤️ for better kidney health monitoring and patient care**
