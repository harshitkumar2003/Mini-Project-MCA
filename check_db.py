import sqlite3

def print_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    all_rows = cursor.fetchall()
    conn.close()

    print("Users in the database:")
    for row in all_rows:
        print(row)

# Check users after deletion
print_all_users()
