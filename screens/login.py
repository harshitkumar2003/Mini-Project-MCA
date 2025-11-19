import sqlite3
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput


class AadhaarInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Only digits allowed, combine existing and new input
        s = ''.join(filter(str.isdigit, self.text + substring))

        # Restrict max 12 digits
        if len(s) > 12:
            s = s[:12]

        # Insert dash after every 4 digits
        groups = [s[i:i+4] for i in range(0, len(s), 4)]
        s = '-'.join(groups)

        # Update text and cursor position
        self.text = s
        self.cursor = (len(self.text), 0)


class LoginSignupScreen(Screen):
    temp_otp = StringProperty('')
    current_reset_adhar = ''  # Track Aadhaar for resetting password

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_users_table()

    def create_users_table(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                aadhaar TEXT UNIQUE,
                phone TEXT,
                password TEXT,
                role TEXT
            )
        """)
        conn.commit()
        conn.close()

    def on_otp_text(self, instance, value):
        if len(value) > 1:
            instance.text = value[:1]

        if len(instance.text) == 1:
            try:
                current_id = instance.id  # e.g., otp1
                next_index = int(current_id[-1]) + 1
                next_id = f'otp{next_index}'
                if next_id in self.ids:
                    self.ids[next_id].focus = True
            except Exception:
                pass

def validate_login(self):
    adhar = self.ids.adhar_input.text.strip().replace("-", "").replace(" ", "")
    password = self.ids.password_input.text.strip()
    role = self.ids.role_spinner.text.strip()

    if not adhar or not password or role not in ['User', 'Admin', 'Doctor', 'Patient']:
        self.show_popup("Error", "Please fill all details and select a valid role.")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE aadhaar=?", (adhar,))
    result = cursor.fetchone()

    if result is None:
        self.show_popup("Error", "User not found.")
    else:
        stored_password, stored_role = result
        if stored_password == password:
            # Role based screen redirection with typical permissions
            stored_role_lower = stored_role.lower()
            if stored_role_lower == 'patient':
                self.manager.current = 'patient'  # Patient dashboard
            elif stored_role_lower == 'doctor':
                self.manager.current = 'doctor'  # Doctor dashboard
            elif stored_role_lower == 'admin':
                self.manager.current = 'admin'   # Admin dashboard
            elif stored_role_lower == 'user':
                self.manager.current = 'dashboard'  # General user/customer dashboard
            else:
                self.show_popup("Error", "Invalid role assigned to user.")
        else:
            self.show_popup("Error", "Incorrect password.")

    conn.close()


    def validate_signup(self):
        name = self.ids.name_input.text.strip()
        email = self.ids.email_input.text.strip()
        adhar = self.ids.signup_adhar_input.text.strip().replace("-", "").replace(" ", "")
        phone = self.ids.phone_input.text.strip()
        password = self.ids.signup_password_input.text.strip()
        role = self.ids.signup_role_spinner.text.strip()

        if not (name and email and adhar and phone and password and role in ["User"]):
            self.show_popup("Error", "All fields are required, and a valid role must be selected.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, aadhaar, phone, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, adhar, phone, password, role))
            conn.commit()
            conn.close()
            self.show_popup("Success", "Signup successful! Please login.")
            self.screen_switch('login_view')
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Aadhaar already registered.")
        except Exception as e:
            self.show_popup("Error", f"Signup failed: {e}")

    def send_otp(self):
        adhar = self.ids.forgot_adhar_input.text.strip().replace("-", "").replace(" ", "")
        if not adhar:
            self.show_popup("Error", "Please enter Aadhaar number.")
            return

        # Check if Aadhaar exists in database before sending OTP
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE aadhaar=?", (adhar,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            self.show_popup("Error", "Aadhaar not found. Please check and try again.")
            return

        self.temp_otp = str(random.randint(1000, 9999))
        self.ids.otp_notice.text = f"(Test OTP: {self.temp_otp})"
        self.show_popup("OTP Generated", "Check OTP displayed below and enter to verify.")

    def verify_otp(self):
        entered_otp = ''.join([self.ids[f'otp{i}'].text for i in range(1, 5)])
        if entered_otp == self.temp_otp:
            self.show_popup("Success", "OTP verified. Please reset your password.")
            self.current_reset_adhar = self.ids.forgot_adhar_input.text.strip().replace("-", "").replace(" ", "")
            self.screen_switch("reset_password_view")
        else:
            self.show_popup("Error", "Incorrect OTP.")

    def reset_password(self):
        new_password = self.ids.new_password_input.text.strip()
        confirm_password = self.ids.confirm_password_input.text.strip()

        if not new_password or not confirm_password:
            self.show_popup("Error", "Please fill all password fields.")
            return

        if new_password != confirm_password:
            self.show_popup("Error", "Passwords do not match.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE aadhaar=?", (new_password, self.current_reset_adhar))
            conn.commit()
            conn.close()
            self.show_popup("Success", "Password reset successfully. Please login.")
            self.screen_switch("login_view")
            # Clear password fields after reset
            self.ids.new_password_input.text = ""
            self.ids.confirm_password_input.text = ""
        except Exception as e:
            self.show_popup("Error", f"Failed to reset password: {e}")

    def screen_switch(self, target):
        self.ids.login_views.current = target
        # Optionally clear inputs when switching screens here

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message),
              size_hint=(0.6, 0.4)).open()
    
    def reset_fields(self):
        self.ids.adhar_input.text = ""
        self.ids.password_input.text = ""
        self.ids.role_spinner.text = "Select Role"  # or default value
        # Reset other fields if required
    
