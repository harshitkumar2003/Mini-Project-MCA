import sqlite3

def test_login():
    # Test database connection and login
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM users WHERE user_id='UPTHAD00'")
        admin = cursor.fetchone()
        
        if admin:
            print("✅ Admin user found in database")
            print(f"Admin details: {admin}")
        else:
            print("❌ Admin user not found!")
            
        # Check if users table has required columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        required_columns = ['id', 'name', 'email', 'user_id', 'aadhaar', 'phone', 'password', 'role']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {', '.join(missing_columns)}")
        else:
            print("✅ All required columns exist in users table")
            
    except Exception as e:
        print(f"❌ Error testing database: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=== Testing Database and Login ===")
    test_login()
