import sqlite3
import os

def check_and_fix_database():
    db_path = 'users.db'
    needs_setup = False
    
    # Check if database exists
    if not os.path.exists(db_path):
        needs_setup = True
    else:
        # Check if the table has all required columns
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Get table info
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            
            required_columns = ['id', 'name', 'email', 'user_id', 'aadhaar', 'phone', 'password', 'role']
            
            for col in required_columns:
                if col not in columns:
                    print(f"Missing column: {col}")
                    needs_setup = True
                    break
                    
        except sqlite3.OperationalError:
            # Table doesn't exist
            needs_setup = True
        finally:
            conn.close()
    
    if needs_setup:
        print("Setting up database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Create new table with all required columns
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                user_id TEXT UNIQUE,
                aadhaar TEXT,
                phone TEXT,
                password TEXT,
                role TEXT
            )
        """)
        
        # Add default admin user if not exists
        cursor.execute("""
            INSERT OR IGNORE INTO users (name, email, user_id, aadhaar, phone, password, role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Admin', 'admin@example.com', 'UPTHAD00', '000000000000', '0000000000', 'admin2003', 'admin'))
        
        conn.commit()
        conn.close()
        print("Database setup complete!")
    else:
        print("Database is already properly configured.")

if __name__ == "__main__":
    check_and_fix_database()
