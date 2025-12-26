import hashlib
import re
import os

def hash_password(password):
    """Hash a password using SHA-256"""
    # Add a salt from environment or use a default
    salt = os.getenv("SESSION_SECRET", "lifelens_ai_salt")
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return hash_password(password) == password_hash

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
