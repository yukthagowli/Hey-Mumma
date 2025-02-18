import sqlite3
import datetime
from pathlib import Path
import os
import time

def get_db_path():
    return Path(__file__).parent / "users.db"

def recreate_database():
    """Recreate the database with the current schema"""
    db_path = get_db_path()
    
    # Try to delete the database if it exists
    if db_path.exists():
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                os.remove(db_path)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(1)  # Wait a bit before retrying
                else:
                    # If we can't delete, try to alter the existing table instead
                    try:
                        conn = sqlite3.connect(db_path)
                        c = conn.cursor()
                        
                        # Add profile_completed column if it doesn't exist
                        try:
                            c.execute('ALTER TABLE users ADD COLUMN profile_completed INTEGER DEFAULT 0')
                            conn.commit()
                        except sqlite3.OperationalError:
                            # Column might already exist
                            pass
                        
                        conn.close()
                        return
                    except Exception:
                        # If altering fails, we'll have to work with the existing schema
                        return
    
    # Create new database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create users table with all fields
    c.execute('''CREATE TABLE users
                 (email TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  password TEXT NOT NULL,
                  age INTEGER,
                  height REAL,
                  weight REAL,
                  pregnancies INTEGER,
                  due_date TEXT,
                  registration_date TEXT,
                  profile_completed INTEGER DEFAULT 0)''')
    
    conn.commit()
    conn.close()

def init_db():
    """Initialize the database if it doesn't exist"""
    db_path = get_db_path()
    
    if not db_path.exists():
        recreate_database()
    else:
        # Check if the profile_completed column exists
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        try:
            c.execute('SELECT profile_completed FROM users LIMIT 1')
            conn.close()
        except sqlite3.OperationalError:
            # Column doesn't exist, try to add it
            conn.close()
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute('ALTER TABLE users ADD COLUMN profile_completed INTEGER DEFAULT 0')
                conn.commit()
            except sqlite3.OperationalError:
                # If we can't alter the table, try to recreate the database
                conn.close()
                recreate_database()
            finally:
                if conn:
                    conn.close()

def add_user(email, name, password, age=None, height=None, weight=None, pregnancies=None, due_date=None):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        profile_completed = 1 if all(x is not None for x in [age, height, weight, pregnancies, due_date]) else 0
        
        # Check if profile_completed column exists
        try:
            c.execute('SELECT profile_completed FROM users LIMIT 1')
        except sqlite3.OperationalError:
            # Add the column if it doesn't exist
            c.execute('ALTER TABLE users ADD COLUMN profile_completed INTEGER DEFAULT 0')
            conn.commit()
        
        c.execute('''INSERT INTO users 
                     (email, name, password, age, height, weight, pregnancies, due_date, registration_date, profile_completed)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (email, name, password, age, height, weight, pregnancies, due_date, 
                  datetime.datetime.now().strftime('%Y-%m-%d'), profile_completed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()
    conn.close()
    
    return user

def check_profile_completed(email):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        # First check if the column exists
        try:
            c.execute('SELECT profile_completed FROM users WHERE email = ?', (email,))
            result = c.fetchone()
            return result and result[0] == 1
        except sqlite3.OperationalError:
            # If column doesn't exist, check if all profile fields are filled
            c.execute('''SELECT age, height, weight, pregnancies, due_date 
                        FROM users WHERE email = ?''', (email,))
            result = c.fetchone()
            return result and all(x is not None for x in result)
    finally:
        conn.close()

def get_user_info(email):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        
        if user:
            # Get column names
            columns = [description[0] for description in c.description]
            user_dict = {
                'email': user[columns.index('email')],
                'name': user[columns.index('name')],
                'age': user[columns.index('age')] if 'age' in columns else None,
                'height': user[columns.index('height')] if 'height' in columns else None,
                'weight': user[columns.index('weight')] if 'weight' in columns else None,
                'pregnancies': user[columns.index('pregnancies')] if 'pregnancies' in columns else None,
                'due_date': user[columns.index('due_date')] if 'due_date' in columns else None,
                'registration_date': user[columns.index('registration_date')] if 'registration_date' in columns else None,
            }
            
            # Add profile_completed if it exists
            try:
                user_dict['profile_completed'] = user[columns.index('profile_completed')]
            except ValueError:
                # If profile_completed column doesn't exist, calculate it
                user_dict['profile_completed'] = 1 if all(user_dict[k] is not None for k in ['age', 'height', 'weight', 'pregnancies', 'due_date']) else 0
            
            return user_dict
        return None
    finally:
        conn.close()

def update_user_info(email, age=None, height=None, weight=None, pregnancies=None, due_date=None):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        if age is not None:
            update_fields.append('age = ?')
            values.append(age)
        if height is not None:
            update_fields.append('height = ?')
            values.append(height)
        if weight is not None:
            update_fields.append('weight = ?')
            values.append(weight)
        if pregnancies is not None:
            update_fields.append('pregnancies = ?')
            values.append(pregnancies)
        if due_date is not None:
            update_fields.append('due_date = ?')
            values.append(due_date)
        
        if update_fields:
            # Check if all profile fields are filled
            c.execute('''SELECT age, height, weight, pregnancies, due_date 
                         FROM users WHERE email = ?''', (email,))
            current_data = c.fetchone()
            
            # Update profile_completed status
            if current_data and all(x is not None for x in current_data):
                # Check if profile_completed column exists
                try:
                    c.execute('SELECT profile_completed FROM users LIMIT 1')
                    update_fields.append('profile_completed = 1')
                except sqlite3.OperationalError:
                    # Add the column if it doesn't exist
                    c.execute('ALTER TABLE users ADD COLUMN profile_completed INTEGER DEFAULT 0')
                    update_fields.append('profile_completed = 1')
                    conn.commit()
            
            values.append(email)
            query = f'''UPDATE users SET {', '.join(update_fields)} WHERE email = ?'''
            c.execute(query, values)
            conn.commit()
    finally:
        conn.close()

# Initialize or migrate the database
init_db()
