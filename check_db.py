import sqlite3

def delete_user_by_user_id(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    print(f"User with User ID {user_id} deleted.")

# Example usage: delete user with user_id 'UPTH-000001'
delete_user_by_user_id("")

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
