import sqlite3
import os
from datetime import datetime
from auth import hash_password, verify_password

DB_PATH = "lifelens_ai.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def init_database():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            security_question TEXT,
            security_answer_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Demographics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demographics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            daily_water_intake REAL,
            medical_history TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    
    # Uploads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    
    # Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            upload_id INTEGER,
            report_type TEXT NOT NULL,
            report_content TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users (email),
            FOREIGN KEY (upload_id) REFERENCES uploads (id)
        )
    ''')
    
    # AI Analysis table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_id INTEGER NOT NULL,
            user_email TEXT NOT NULL,
            analysis_data TEXT NOT NULL,
            risk_level TEXT,
            confidence_score INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (upload_id) REFERENCES uploads (id),
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(email, password, full_name):
    """Create a new user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
            (email, password_hash, full_name)
        )
        
        conn.commit()
        conn.close()
        return True, "User created successfully"
    
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_user(email, password):
    """Verify user credentials"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        
        if result and verify_password(password, result[0]):
            return True
        return False
    
    except Exception as e:
        print(f"Error verifying user: {str(e)}")
        return False

def save_demographics(user_email, demographics_data):
    """Save or update user demographics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if demographics already exist
        cursor.execute("SELECT id FROM demographics WHERE user_email = ?", (user_email,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute('''
                UPDATE demographics 
                SET age = ?, gender = ?, weight = ?, height = ?, 
                    daily_water_intake = ?, medical_history = ?, updated_at = ?
                WHERE user_email = ?
            ''', (
                demographics_data['age'],
                demographics_data['gender'],
                demographics_data['weight'],
                demographics_data['height'],
                demographics_data['daily_water_intake'],
                demographics_data['medical_history'],
                datetime.now(),
                user_email
            ))
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO demographics 
                (user_email, age, gender, weight, height, daily_water_intake, medical_history)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_email,
                demographics_data['age'],
                demographics_data['gender'],
                demographics_data['weight'],
                demographics_data['height'],
                demographics_data['daily_water_intake'],
                demographics_data['medical_history']
            ))
        
        conn.commit()
        conn.close()
        return True, "Demographics saved successfully"
    
    except Exception as e:
        return False, f"Error saving demographics: {str(e)}"

def get_user_demographics(user_email):
    """Get user demographics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT age, gender, weight, height, daily_water_intake, medical_history
            FROM demographics WHERE user_email = ?
        ''', (user_email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'age': result[0],
                'gender': result[1],
                'weight': result[2],
                'height': result[3],
                'daily_water_intake': result[4],
                'medical_history': result[5]
            }
        return None
    
    except Exception as e:
        print(f"Error getting demographics: {str(e)}")
        return None

def save_upload(user_email, filename, file_path, file_type):
    """Save upload information"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO uploads (user_email, filename, file_path, file_type)
            VALUES (?, ?, ?, ?)
        ''', (user_email, filename, file_path, file_type))
        
        upload_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return upload_id
    
    except Exception as e:
        print(f"Error saving upload: {str(e)}")
        return None

def get_user_uploads(user_email):
    """Get all uploads for a user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, file_type, upload_date, analysis_status
            FROM uploads WHERE user_email = ?
            ORDER BY upload_date DESC
        ''', (user_email,))
        
        results = cursor.fetchall()
        conn.close()
        
        uploads = []
        for row in results:
            uploads.append({
                'id': row[0],
                'filename': row[1],
                'file_type': row[2],
                'upload_date': row[3],
                'analysis_status': row[4]
            })
        
        return uploads
    
    except Exception as e:
        print(f"Error getting uploads: {str(e)}")
        return []

def save_report(user_email, upload_id, report_type, report_content):
    """Save a generated report"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reports (user_email, upload_id, report_type, report_content)
            VALUES (?, ?, ?, ?)
        ''', (user_email, upload_id, report_type, report_content))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return report_id
    
    except Exception as e:
        print(f"Error saving report: {str(e)}")
        return None

def get_user_reports(user_email):
    """Get all reports for a user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.id, r.report_type, r.report_content, r.generated_at, u.filename
            FROM reports r
            LEFT JOIN uploads u ON r.upload_id = u.id
            WHERE r.user_email = ?
            ORDER BY r.generated_at DESC
        ''', (user_email,))
        
        results = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in results:
            reports.append({
                'id': row[0],
                'report_type': row[1],
                'report_content': row[2],
                'generated_at': row[3],
                'filename': row[4] if row[4] else 'General Report'
            })
        
        return reports
    
    except Exception as e:
        print(f"Error getting reports: {str(e)}")
        return []

def save_ai_analysis(upload_id, user_email, analysis_data, risk_level=None, confidence_score=None):
    """Save AI analysis results"""
    try:
        import json
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ai_analysis (upload_id, user_email, analysis_data, risk_level, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (upload_id, user_email, json.dumps(analysis_data), risk_level, confidence_score))
        
        analysis_id = cursor.lastrowid
        
        # Update upload status to completed
        cursor.execute('''
            UPDATE uploads SET analysis_status = 'completed' WHERE id = ?
        ''', (upload_id,))
        
        conn.commit()
        conn.close()
        
        return analysis_id
    
    except Exception as e:
        print(f"Error saving AI analysis: {str(e)}")
        return None

def get_ai_analysis(upload_id):
    """Get AI analysis for a specific upload"""
    try:
        import json
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, analysis_data, risk_level, confidence_score, analyzed_at
            FROM ai_analysis WHERE upload_id = ?
            ORDER BY analyzed_at DESC LIMIT 1
        ''', (upload_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'analysis_data': json.loads(result[1]),
                'risk_level': result[2],
                'confidence_score': result[3],
                'analyzed_at': result[4]
            }
        return None
    
    except Exception as e:
        print(f"Error getting AI analysis: {str(e)}")
        return None

def get_all_user_analyses(user_email):
    """Get all AI analyses for a user"""
    try:
        import json
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.upload_id, a.analysis_data, a.risk_level, a.confidence_score, a.analyzed_at, u.filename
            FROM ai_analysis a
            JOIN uploads u ON a.upload_id = u.id
            WHERE a.user_email = ?
            ORDER BY a.analyzed_at DESC
        ''', (user_email,))
        
        results = cursor.fetchall()
        conn.close()
        
        analyses = []
        for row in results:
            analyses.append({
                'id': row[0],
                'upload_id': row[1],
                'analysis_data': json.loads(row[2]),
                'risk_level': row[3],
                'confidence_score': row[4],
                'analyzed_at': row[5],
                'filename': row[6]
            })
        
        return analyses
    
    except Exception as e:
        print(f"Error getting user analyses: {str(e)}")
        return []

def update_security_question(email, question, answer):
    """Update user's security question and answer"""
    try:
        from auth import hash_password
        conn = get_connection()
        cursor = conn.cursor()
        
        answer_hash = hash_password(answer.lower().strip())
        
        cursor.execute('''
            UPDATE users 
            SET security_question = ?, security_answer_hash = ?
            WHERE email = ?
        ''', (question, answer_hash, email))
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error updating security question: {str(e)}")
        return False

def get_security_question(email):
    """Get user's security question"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT security_question FROM users WHERE email = ?
        ''', (email,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result and result[0] else None
    
    except Exception as e:
        print(f"Error getting security question: {str(e)}")
        return None

def verify_security_answer(email, answer):
    """Verify user's security answer"""
    try:
        from auth import hash_password
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT security_answer_hash FROM users WHERE email = ?
        ''', (email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            answer_hash = hash_password(answer.lower().strip())
            return answer_hash == result[0]
        
        return False
    
    except Exception as e:
        print(f"Error verifying security answer: {str(e)}")
        return False

def reset_password(email, new_password):
    """Reset user's password"""
    try:
        from auth import hash_password
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(new_password)
        
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?
            WHERE email = ?
        ''', (password_hash, email))
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
        return False
