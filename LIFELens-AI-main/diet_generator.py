def generate_kidney_friendly_diet(demographics):
    """Generate personalized kidney-friendly diet recommendations"""
    
    # Base recommendations
    base_diet = {
        "breakfast": [
            "Low-sodium oatmeal with berries",
            "Egg whites with vegetables",
            "Fresh fruit salad",
            "Herbal tea or water"
        ],
        "lunch": [
            "Grilled chicken or fish (3-4 oz)",
            "Steamed vegetables (cauliflower, cabbage)",
            "White rice or quinoa (1/2 cup)",
            "Fresh cucumber salad"
        ],
        "dinner": [
            "Lean protein (turkey, fish)",
            "Green beans or asparagus",
            "Sweet potato (small portion)",
            "Mixed greens salad"
        ],
        "snacks": [
            "Apple slices",
            "Unsalted crackers",
            "Fresh berries",
            "Herbal tea"
        ]
    }
    
    # Personalize based on demographics
    if demographics:
        age = demographics.get('age', 0)
        weight = demographics.get('weight', 0)
        gender = demographics.get('gender', '')
        medical_history = demographics.get('medical_history', '').lower()
        
        # Adjust portions based on age and weight
        if age > 65:
            base_diet["general_notes"] = "Consider smaller, more frequent meals. Focus on easily digestible foods."
        
        if weight > 80:  # kg
            base_diet["portion_control"] = "Monitor portion sizes. Consider reducing carbohydrate portions."
        
        # Adjust based on medical history
        if 'diabetes' in medical_history:
            base_diet["diabetes_note"] = "Monitor carbohydrate intake. Choose complex carbs over simple sugars."
            base_diet["breakfast"].insert(0, "Check blood sugar before meals")
        
        if 'hypertension' in medical_history or 'high blood pressure' in medical_history:
            base_diet["hypertension_note"] = "Strictly limit sodium intake. Avoid processed foods."
        
        if 'kidney stones' in medical_history:
            base_diet["kidney_stones_note"] = "Increase water intake. Limit oxalate-rich foods like spinach and nuts."
    
    # General kidney-friendly guidelines
    base_diet["guidelines"] = [
        "Limit sodium to less than 2,300mg per day",
        "Monitor protein intake (consult with healthcare provider)",
        "Stay well-hydrated with water",
        "Limit phosphorus and potassium if advised by doctor",
        "Avoid processed and packaged foods",
        "Choose fresh fruits and vegetables",
        "Cook without added salt - use herbs and spices"
    ]
    
    # Water intake recommendation
    water_intake = demographics.get('daily_water_intake', 0) if demographics else 0
    if water_intake < 8:
        base_diet["hydration_note"] = f"Current intake: {water_intake} glasses. Recommended: 8-10 glasses of water daily (unless restricted by doctor)."
    
    return base_diet

def get_kidney_health_tips():
    """Get general kidney health tips"""
    return [
        "🚰 Stay hydrated with plenty of water",
        "🧂 Limit sodium intake to protect kidney function",
        "🥗 Eat a balanced diet rich in fruits and vegetables",
        "💊 Take medications as prescribed by your doctor",
        "🏃‍♂️ Exercise regularly to maintain healthy blood pressure",
        "🚭 Avoid smoking and limit alcohol consumption",
        "🩺 Regular check-ups with your healthcare provider",
        "📊 Monitor blood pressure and blood sugar levels",
        "⚖️ Maintain a healthy weight",
        "😴 Get adequate sleep for overall health"
    ]

def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    if weight and height and height > 0:
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)
        return round(bmi, 1)
    return None

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
