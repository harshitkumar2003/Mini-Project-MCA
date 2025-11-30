import sqlite3
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput

# ==============================================================================
#! Custom TextInput for Aadhaar Formatting 
# ==============================================================================
class AadhaarInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = ''.join(filter(str.isdigit, self.text + substring))
        if len(s) > 12:
            s = s[:12]
        groups = [s[i:i+4] for i in range(0, len(s), 4)]
        s = '-'.join(groups)
        self.text = s
        self.cursor = (len(self.text), 0)

#! login and signup screen with OTP and password reset
class LoginSignupScreen(Screen):
    temp_otp = StringProperty('')
    current_reset_phone = ''  # Track phone for resetting password
    #! NEW PROPERTY: Landing page se select kiya gaya role store karega
    selected_role = StringProperty('') # Default empty string
    #! NEW: User ID counter for auto-generation
    last_user_id = StringProperty('UPTH1500')

    #temporary fix k liye jo purana database hai usme schema update krdega
    def update_users_table_schema(self):
        """Adds the missing user_id column to the existing table."""
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            # FIX: Temporarily remove 'UNIQUE' constraint during migration.
            # We will rely on Python/future inserts to enforce uniqueness for now.
            cursor.execute("ALTER TABLE users ADD COLUMN user_id TEXT") 
            
            # 🌟 IMPORTANT: After adding the column, update existing rows to be non-NULL
            # This is crucial if you later want to fully restore the UNIQUE constraint.
            cursor.execute("UPDATE users SET user_id = 'TEMP_MIG_' || id WHERE user_id IS NULL")
            
            conn.commit()
            print("Database migration successful: Added 'user_id' column without UNIQUE.")
        except sqlite3.OperationalError as e:
            if "duplicate column name: user_id" in str(e):
                print("Column user_id already exists (migration skipped).")
            else:
                raise e 
        finally:
            conn.close()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_users_table()
        # 🌟 TEMPORARY FIX: Call this once to update your old database file
        #self.update_users_table_schema()
        self.load_last_user_id()


    def load_last_user_id(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        # Find the latest generated user ID
        cursor.execute("SELECT user_id FROM users WHERE role='User' ORDER BY user_id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            full_id = result[0]
            if '-' in full_id:
                # Assuming format is 'UPTH-000001'. Split and take the last part.
                numeric_part = full_id.split('-')[-1]
            else:
                # Assuming format is 'UPTH1500'. Remove all non-digits.
                numeric_part = ''.join(filter(str.isdigit, full_id))
            
            # Store the parsed numerical part (e.g., '000001' or '1500')
            self.last_user_id = numeric_part if numeric_part.isdigit() else '15000'
        else:
            self.last_user_id = '00000' # No users yet, start from 0 


    def create_users_table(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
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
        conn.commit()
        conn.close()

    def generate_user_id(self):
        """Generates a new sequential User ID (e.g., UPTH-000001)."""
        
        # Safely convert to integer. If conversion fails, start from 0.
        try:
            current_num = int(self.last_user_id)
        except ValueError:
            current_num = 0
            
        current_num += 1
        
        prefix = "THU" 
        new_id = f"{prefix}-{current_num:06d}"
        
        self.last_user_id = f"{current_num:06d}" # Store only the number for the next run
        return new_id
    
    #! otp ko auto move krne k liye next box me focus hojaye
    def on_otp_text(self, instance, value):
        if len(value) > 1:
            instance.text = value[:1]
        if len(instance.text) == 1:
            try:
                current_id = instance.id 
                next_index = int(current_id[-1]) + 1
                next_id = f'otp{next_index}'
                if next_id in self.ids:
                    self.ids[next_id].focus = True
            except Exception:
                pass

    def on_enter(self):
    # Clear fields on enter
        self.reset_fields()
        role = self.selected_role.lower()
    
        # 1. First, handle non-User roles (Doctor/Patient/Admin) - always show Login
        if role != 'user':
            self.ids.login_views.current = 'login_view'
            return
    
        # 2. Handle 'User' role dynamically: Check if any user exists
    
        user_exists = False
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
    
        # Check if any user with role 'User' exists in the database
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='User'")
        count = cursor.fetchone()[0]
        conn.close()
    
        if count > 0:
            user_exists = True
    
        # 3. Redirect based on existence
        if user_exists:
            # User already exists, show Login page by default
            self.ids.login_views.current = 'login_view'
        else:
            # First time, no users exist, force Signup
            self.ids.login_views.current = 'signup_view'

    #! validate  krega login credentials and redirect based on role
    def validate_login(self):
        role = self.selected_role.lower()
        password = self.ids.password_input.text.strip()

        # 🌟 CHANGE 1: Login ID Field based on role
        if role == 'user':
            login_id = self.ids.user_id_input.text.strip() # User login by User ID
            lookup_field = "user_id"
        else:
            # For Doctor/Patient/Admin, assuming they also login with a fixed User ID field (no Aadhaar)
            login_id = self.ids.user_id_input.text.strip()
            lookup_field = "user_id"

        #! --- Developer Admin Login (Direct Access without DB) ---
        if login_id == "UPTHAD00" and password == "admin2003" and role == "admin":
            self.manager.current = "admin"
            return

        if not login_id or not password or role not in ['user', 'admin', 'doctor', 'patient']:
            self.show_popup("Error", "Please fill all details.")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # 🌟 CHANGE 2: Look up by user_id instead of aadhaar
        cursor.execute(f"SELECT password, role FROM users WHERE {lookup_field}=?", (login_id,))
        result = cursor.fetchone()

        if result is None:
            # 🌟 CHANGE 3: Changed error message
            self.show_popup("Error", f"{role.capitalize()} ID not found.")
        else:
            stored_password, stored_role = result

            if stored_password == password:
                if stored_role.lower() != role:
                    self.show_popup("Error", "You do not have permission for this role.")
                    conn.close()
                    return

                #! Redirect based on role
                r = stored_role.lower()
                if r == 'patient':
                    self.manager.current = 'patient'
                elif r == 'doctor':
                    self.manager.current = 'doctor'
                elif r == 'admin':
                    self.manager.current = 'admin'
                elif r == 'user':
                    self.manager.current = 'dashboard'
            else:
                self.show_popup("Error", "Incorrect password.")
        
        conn.close()

    #! validate krega signup details and store in database
    def validate_signup(self):
        role = self.selected_role.lower()
        if role != 'user':
            self.show_popup("Error", "Signup is only available for User role.")
            return

        name = self.ids.name_input.text.strip()
        email = self.ids.email_input.text.strip()
        adhar = self.ids.signup_adhar_input.text.strip().replace("-", "").replace(" ", "")
        phone = self.ids.phone_input.text.strip()
        password = self.ids.signup_password_input.text.strip()

        if not (name and email and adhar and phone and password):
            self.show_popup("Error", "All fields are required.")
            return
        
        new_user_id = self.generate_user_id() # NEW: Auto-generate User ID

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            
            # 🌟 CHANGE 4: Insert user_id and keep aadhaar
            cursor.execute("""
                INSERT INTO users (name, email, aadhaar, phone, password, role, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, adhar, phone, password, role.capitalize(), new_user_id))
            
            conn.commit()
            conn.close()
            self.show_popup("Success", f"Signup successful! Your User ID is {new_user_id}. Please login.")
            self.screen_switch('login_view')
            self.ids.user_id_input.text = new_user_id # Pre-fill login ID
        except sqlite3.IntegrityError as e:
            if "aadhaar" in str(e):
                self.show_popup("Error", "Aadhaar already registered.")
            elif "phone" in str(e):
                self.show_popup("Error", "Phone number already registered.")
            else:
                self.show_popup("Error", "Signup failed due to duplicate entry.")
        except Exception as e:
            self.show_popup("Error", f"Signup failed: {e}")

    #! OTP generation and verification for password reset krna
    def send_otp(self):
        phone = self.ids.forgot_phone_input.text.strip() # Using phone number for OTP
        if not phone or len(phone) != 10 or not phone.isdigit():
            self.show_popup("Error", "Please enter a valid 10-digit phone number.")
            return

        #! Check if Phone exists in database before sending OTP
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone=?", (phone,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            self.show_popup("Error", "Phone number not found.")
            return

        self.temp_otp = str(random.randint(1000, 9999))
        self.ids.otp_notice.text = f"(Test OTP: {self.temp_otp})"
        self.current_reset_phone = phone # Store phone number for reset
        self.show_popup("OTP Generated", "Check OTP displayed below and enter to verify.")

    #! OTP verification
    def verify_otp(self):
        
        
        entered_otp_list = [self.ids[f'otp{i}'].text.strip() for i in range(1, 5)]
        entered_otp = ''.join(entered_otp_list)
        
        # --- Check if OTP fields are empty ---
        if not entered_otp or len(entered_otp) < 4:
            self.show_popup("Error", "Please enter the complete 4-digit OTP.")
            return
        
        # --- Check if a phone number was registered for reset ---
        if not self.current_reset_phone:
            self.show_popup("Error", "Please first enter your phone number and send OTP.")
            return

        # --- Check against the generated OTP ---
        if entered_otp == self.temp_otp:
            self.show_popup("Success", "OTP verified. Please reset your password.")
            self.screen_switch("reset_password_view")
        else:
            self.show_popup("Error", "Incorrect OTP.")

#! password reset functionality
    def reset_password(self):
        new_password = self.ids.new_password_input.text.strip()
        confirm_password = self.ids.confirm_password_input.text.strip()
        phone_to_reset = self.current_reset_phone # Use stored phone number

        if not new_password or not confirm_password:
            self.show_popup("Error", "Please fill all password fields.")
            return

        if new_password != confirm_password:
            self.show_popup("Error", "Passwords do not match.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            # Update password based on phone number
            cursor.execute("UPDATE users SET password=? WHERE phone=?", (new_password, phone_to_reset))
            conn.commit()
            conn.close()
            self.show_popup("Success", "Password reset successfully. Please login.")
            self.screen_switch("login_view")
            
            self.ids.new_password_input.text = ""
            self.ids.confirm_password_input.text = ""
        except Exception as e:
            self.show_popup("Error", f"Failed to reset password: {e}")

#! screen switching between login, signup, otp, reset views
    def screen_switch(self, target):
        self.ids.login_views.current = target

    def show_popup(self, title, message):
        content_label = Label(text=message, color=(1, 1, 1, 1))
        Popup(title=title, content=content_label,
              size_hint=(0.6, 0.4)).open()
        
    def reset_fields(self):
        # Clear fields for Login view
        self.ids.user_id_input.text = ""
        self.ids.password_input.text = ""
        
        # Clear fields for Signup view
        self.ids.name_input.text = ""
        self.ids.email_input.text = ""
        self.ids.signup_adhar_input.text = ""
        self.ids.phone_input.text = ""
        self.ids.signup_password_input.text = ""
        
        # Clear fields for Forgot Password
        self.ids.forgot_phone_input.text = ""
        self.ids.otp_notice.text = ""
        for i in range(1, 5):
            self.ids[f'otp{i}'].text = ""
        self.ids.new_password_input.text = ""
        self.ids.confirm_password_input.text = ""
        self.current_reset_phone = ""
    
