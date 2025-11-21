# Commit: Starting admin_full.py - Admin panel with DB integrated for patients & doctors111
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

#Window.size = (360, 700)
Window.clearcolor = (1, 1, 1, 1)

DB_PATH = "users.db"  # single DB for both login and profiles

# ----------------------- UTIL: DB SETUP -----------------------
# Commit: DB setup - Ensure all required tables exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # users table (login) - mirror of your login.py
    c.execute("""
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
    # patient personal
    c.execute("""
        CREATE TABLE IF NOT EXISTS patient_personal (
            aadhaar TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            blood_group TEXT,
            marital_status TEXT,
            phone TEXT,
            location TEXT,
            password TEXT
        )
    """)
    # patient medical
    c.execute("""
        CREATE TABLE IF NOT EXISTS patient_medical (
            aadhaar TEXT PRIMARY KEY,
            allergies TEXT,
            current_medication TEXT,
            past_medication TEXT,
            chronic_disease TEXT,
            injuries TEXT,
            surgeries TEXT,
            FOREIGN KEY(aadhaar) REFERENCES patient_personal(aadhaar)
        )
    """)
    # patient lifestyle
    c.execute("""
        CREATE TABLE IF NOT EXISTS patient_lifestyle (
            aadhaar TEXT PRIMARY KEY,
            smoking TEXT,
            alcohol TEXT,
            activity_level TEXT,
            food_preference TEXT,
            occupation TEXT,
            FOREIGN KEY(aadhaar) REFERENCES patient_personal(aadhaar)
        )
    """)
    # doctor_info
    c.execute("""
        CREATE TABLE IF NOT EXISTS doctor_info (
            aadhaar TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            gender TEXT,
            specialization TEXT,
            qualification TEXT,
            experience TEXT,
            clinic TEXT,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# initialize DB at import
init_db()

# ----------------------- Simple popup helper -----------------------
def show_popup(title, message):
    Popup(title=title, content=Label(text=message),
          size_hint=(0.7, 0.4)).open()

# ----------------------- EDIT/ADD POPUP (small/simple) -----------------------
class EditPopup(Popup):
    def __init__(self, fields, values, save_callback, **kwargs):
        super().__init__(title="Edit Information", size_hint=(0.9, 0.9), **kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.inputs = []
        grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for field, value in zip(fields, values):
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=80)
            box.add_widget(Label(text=field, size_hint_y=None, height=20, color=(0,0,0,1)))
            ti = TextInput(text=value, multiline=False)
            self.inputs.append(ti)
            box.add_widget(ti)
            grid.add_widget(box)

        scroll = ScrollView()
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        btn = Button(text="Save", size_hint_y=None, height=50)
        btn.bind(on_release=lambda x: save_callback(self))
        layout.add_widget(btn)
        self.add_widget(layout)

# ----------------------- TABLE WITH EDIT + DELETE (reuse) -----------------------
class EditableTable(GridLayout):
    def __init__(self, headers, row_data, edit_callback, delete_callback, **kwargs):
        super().__init__(cols=len(headers) + 2, spacing=5, padding=5, size_hint_y=None, **kwargs)
        self.bind(minimum_height=self.setter("height"))
        self.headers = headers

        # header
        for h in headers:
            self.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=40, color=(0,0,0,1)))

        self.add_widget(Label(text="[b]Edit[/b]", markup=True, size_hint_y=None, height=40, color=(0,0,0,1)))
        self.add_widget(Label(text="[b]Delete[/b]", markup=True, size_hint_y=None, height=40, color=(0,0,0,1)))

        # rows
        for idx, row in enumerate(row_data):
            for col in row:
                self.add_widget(Label(text=str(col), color=(0,0,0,1), size_hint_y=None, height=30))
            btn_edit = Button(text="Edit", size_hint_y=None, height=30)
            btn_edit.bind(on_release=lambda x, i=idx: edit_callback(i))
            self.add_widget(btn_edit)
            btn_del = Button(text="X", size_hint_y=None, height=30)
            btn_del.bind(on_release=lambda x, i=idx: delete_callback(i))
            self.add_widget(btn_del)

# ----------------------- HOME SCREEN -----------------------
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Commit: Home screen UI bana raha hoon - buttons for patient & doctor
        #layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        #layout.add_widget(Label(text="[b]Admin Dashboard[/b]", markup=True, font_size=28, size_hint_y=None, height=80, color=(0,0,0,1)))
        #btn1 = Button(text="Patient Information", size_hint_y=None, height=60)
        #btn1.bind(on_release=lambda x: setattr(self.manager, "current", "patient_list"))
        #btn2 = Button(text="Doctor Information", size_hint_y=None, height=60)
        #btn2.bind(on_release=lambda x: setattr(self.manager, "current", "doctor_list"))
        #layout.add_widget(btn1)
        #layout.add_widget(btn2)
        #self.add_widget(layout)

# ----------------------- PATIENT LIST SCREEN (EditableTable) -----------------------
class PatientListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields = ["Name", "Age", "Blood Group", "Condition", "Aadhaar"]
        # Commit: Load patient data from DB
        self.build()

    # Commit: Build patient list UI
    def build(self):
        self.clear_widgets()
        main = BoxLayout(orientation="vertical", padding=10, spacing=8)
        main.add_widget(Label(text="[b]Patient Information[/b]", markup=True, font_size=22, size_hint_y=None, height=50, color=(0,0,0,1)))

        # search row
        search_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
        self.search_input = TextInput(hint_text="Search by Aadhaar", multiline=False)
        btn_search = Button(text="Search", size_hint_x=None, width=100)
        btn_search.bind(on_release=lambda x: self.search_patient())
        btn_clear = Button(text="Clear", size_hint_x=None, width=100)
        btn_clear.bind(on_release=lambda x: self.clear_search())
        search_row.add_widget(self.search_input)
        search_row.add_widget(btn_search)
        search_row.add_widget(btn_clear)

        # add button
        btn_add = Button(text="Add New Patient", size_hint_y=None, height=50)
        btn_add.bind(on_release=lambda x: setattr(self.manager, "current", "patient_add"))

        # table
        scroll = ScrollView()
        # data from DB
        rows = self.fetch_all_patients_short()
        table = EditableTable(self.fields, rows, self.edit_patient, self.delete_patient)
        scroll.add_widget(table)

        btn_back = Button(text="Back", size_hint_y=None, height=50)
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "home"))

        main.add_widget(search_row)
        main.add_widget(btn_add)
        main.add_widget(scroll)
        main.add_widget(btn_back)
        self.add_widget(main)

    # Commit: Fetch brief patient data for table (name, age, blood_group, condition, aadhaar)
    def fetch_all_patients_short(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT p.name, '', p.blood_group, m.chronic_disease, p.aadhaar FROM patient_personal p LEFT JOIN patient_medical m ON p.aadhaar = m.aadhaar")
        rows = c.fetchall()
        conn.close()
        return rows

    # Commit: search by aadhaar
    def search_patient(self):
        aadhaar = self.search_input.text.strip()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT p.name, '', p.blood_group, m.chronic_disease, p.aadhaar FROM patient_personal p LEFT JOIN patient_medical m ON p.aadhaar = m.aadhaar WHERE p.aadhaar=?", (aadhaar,))
        rows = c.fetchall()
        conn.close()
        # rebuild table
        self.clear_widgets()
        main = BoxLayout(orientation="vertical", padding=10, spacing=8)
        main.add_widget(Label(text="[b]Patient Information[/b]", markup=True, font_size=22, size_hint_y=None, height=50, color=(0,0,0,1)))
        search_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
        self.search_input = TextInput(text=aadhaar, multiline=False)
        btn_search = Button(text="Search", size_hint_x=None, width=100)
        btn_search.bind(on_release=lambda x: self.search_patient())
        btn_clear = Button(text="Clear", size_hint_x=None, width=100)
        btn_clear.bind(on_release=lambda x: self.clear_search())
        search_row.add_widget(self.search_input)
        search_row.add_widget(btn_search)
        search_row.add_widget(btn_clear)
        btn_add = Button(text="Add New Patient", size_hint_y=None, height=50)
        btn_add.bind(on_release=lambda x: setattr(self.manager, "current", "patient_add"))
        scroll = ScrollView()
        table = EditableTable(self.fields, rows, self.edit_patient, self.delete_patient)
        scroll.add_widget(table)
        btn_back = Button(text="Back", size_hint_y=None, height=50)
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "home"))
        main.add_widget(search_row)
        main.add_widget(btn_add)
        main.add_widget(scroll)
        main.add_widget(btn_back)
        self.add_widget(main)

    def clear_search(self):
        self.search_input.text = ""
        self.build()

    # Commit: Edit patient - open add-screen in edit mode with aadhaar
    def edit_patient(self, index):
        # fetch corresponding aadhaar from current table
        rows = self.fetch_all_patients_short()
        if index < 0 or index >= len(rows):
            show_popup("Error", "Invalid index")
            return
        aadhaar = rows[index][4]
        self.manager.get_screen('patient_add').load_for_edit(aadhaar)
        self.manager.current = 'patient_add'

    # Commit: Delete patient - remove from all three tables and from users table
    def delete_patient(self, index):
        rows = self.fetch_all_patients_short()
        if index < 0 or index >= len(rows):
            show_popup("Error", "Invalid index")
            return
        aadhaar = rows[index][4]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # delete from child tables if exist
        c.execute("DELETE FROM patient_medical WHERE aadhaar=?", (aadhaar,))
        c.execute("DELETE FROM patient_lifestyle WHERE aadhaar=?", (aadhaar,))
        c.execute("DELETE FROM patient_personal WHERE aadhaar=?", (aadhaar,))
        # also remove login record
        c.execute("DELETE FROM users WHERE aadhaar=?", (aadhaar,))
        conn.commit()
        conn.close()
        show_popup("Success", "Patient deleted.")
        self.build()

# ----------------------- PATIENT ADD / EDIT Multi-Page Screen -----------------------
class PatientAddScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Commit: keeping form state here
        self.page = 1  # 1: personal, 2: medical, 3: lifestyle
        self.edit_mode = False
        self.edit_aadhaar = None
        # create UI
        self.build()

    # Commit: Build initial layout placeholders
    def build(self):
        self.clear_widgets()
        self.main = BoxLayout(orientation="vertical", padding=10, spacing=8)

        header = Label(text="[b]Add / Edit Patient[/b]", markup=True, font_size=20, size_hint_y=None, height=40, color=(0,0,0,1))
        self.main.add_widget(header)

        # content area (we will replace per page)
        self.content = BoxLayout()
        self.main.add_widget(self.content)

        # navigation buttons
        nav = BoxLayout(size_hint_y=None, height=50, spacing=8)
        self.btn_prev = Button(text="Previous", size_hint_x=0.3)
        self.btn_prev.bind(on_release=lambda x: self.prev_page())
        self.btn_next = Button(text="Next", size_hint_x=0.3)
        self.btn_next.bind(on_release=lambda x: self.next_page())
        btn_cancel = Button(text="Cancel", size_hint_x=0.4)
        btn_cancel.bind(on_release=lambda x: self.cancel())
        nav.add_widget(self.btn_prev)
        nav.add_widget(self.btn_next)
        nav.add_widget(btn_cancel)
        self.main.add_widget(nav)

        self.add_widget(self.main)
        self.load_page(1)

    # Commit: Helper to create TextInputs for personal info
    def personal_widgets(self):
        grid = GridLayout(cols=1, spacing=6, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        # fields: name, aadhaar, email, gender, dob, blood_group, marital_status, phone, location, password
        self.p_name = TextInput(multiline=False, hint_text="Name")
        self.p_aadhaar = TextInput(multiline=False, hint_text="Aadhaar (no dashes)")
        self.p_email = TextInput(multiline=False, hint_text="Email")
        self.p_gender = TextInput(multiline=False, hint_text="Gender")
        self.p_dob = TextInput(multiline=False, hint_text="DOB (YYYY-MM-DD)")
        self.p_blood = TextInput(multiline=False, hint_text="Blood Group")
        self.p_marital = TextInput(multiline=False, hint_text="Marital Status")
        self.p_phone = TextInput(multiline=False, hint_text="Phone")
        self.p_location = TextInput(multiline=False, hint_text="Location")
        self.p_password = TextInput(multiline=False, hint_text="Password")

        for w in [("Name", self.p_name), ("Aadhaar", self.p_aadhaar), ("Email", self.p_email),
                  ("Gender", self.p_gender), ("DOB", self.p_dob), ("Blood Group", self.p_blood),
                  ("Marital Status", self.p_marital), ("Phone", self.p_phone), ("Location", self.p_location),
                  ("Password", self.p_password)]:
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=70)
            box.add_widget(Label(text=w[0], size_hint_y=None, height=20, color=(0,0,0,1)))
            box.add_widget(w[1])
            grid.add_widget(box)
        scroll = ScrollView()
        scroll.add_widget(grid)
        return scroll

    # Commit: Medical widgets
    def medical_widgets(self):
        grid = GridLayout(cols=1, spacing=6, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.m_allergies = TextInput(multiline=False, hint_text="Allergies")
        self.m_current = TextInput(multiline=False, hint_text="Current Medication")
        self.m_past = TextInput(multiline=False, hint_text="Past Medications")
        self.m_chronic = TextInput(multiline=False, hint_text="Chronic Disease")
        self.m_injuries = TextInput(multiline=False, hint_text="Injuries")
        self.m_surgeries = TextInput(multiline=False, hint_text="Surgeries")
        for label, widget in [("Allergies", self.m_allergies), ("Current Medication", self.m_current),
                              ("Past Medications", self.m_past), ("Chronic Disease", self.m_chronic),
                              ("Injuries", self.m_injuries), ("Surgeries", self.m_surgeries)]:
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=70)
            box.add_widget(Label(text=label, size_hint_y=None, height=20, color=(0,0,0,1)))
            box.add_widget(widget)
            grid.add_widget(box)
        scroll = ScrollView()
        scroll.add_widget(grid)
        return scroll

    # Commit: Lifestyle widgets
    def lifestyle_widgets(self):
        grid = GridLayout(cols=1, spacing=6, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.l_smoking = TextInput(multiline=False, hint_text="Smoking habits")
        self.l_alcohol = TextInput(multiline=False, hint_text="Alcohol consumption")
        self.l_activity = TextInput(multiline=False, hint_text="Activity level")
        self.l_food = TextInput(multiline=False, hint_text="Food preference")
        self.l_occupation = TextInput(multiline=False, hint_text="Occupation")
        for label, widget in [("Smoking", self.l_smoking), ("Alcohol", self.l_alcohol),
                              ("Activity Level", self.l_activity), ("Food Preference", self.l_food),
                              ("Occupation", self.l_occupation)]:
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=70)
            box.add_widget(Label(text=label, size_hint_y=None, height=20, color=(0,0,0,1)))
            box.add_widget(widget)
            grid.add_widget(box)
        scroll = ScrollView()
        scroll.add_widget(grid)
        return scroll

    # Commit: Load particular page UI
    def load_page(self, page_no):
        self.page = page_no
        self.content.clear_widgets()
        if page_no == 1:
            # personal
            self.content.add_widget(self.personal_widgets())
            self.btn_prev.disabled = True
            self.btn_next.text = "Next"
        elif page_no == 2:
            self.content.add_widget(self.medical_widgets())
            self.btn_prev.disabled = False
            self.btn_next.text = "Next"
        elif page_no == 3:
            self.content.add_widget(self.lifestyle_widgets())
            self.btn_prev.disabled = False
            self.btn_next.text = "Save"
        # if editing, fill fields from DB if edit_mode True
        if self.edit_mode:
            self.prefill_fields_if_needed()

    def next_page(self):
        if self.page < 3:
            # save temporarily? we're keeping inputs in instance variables
            self.page += 1
            self.load_page(self.page)
        else:
            # Save all to DB
            self.save_patient()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_page(self.page)

    def cancel(self):
        self.edit_mode = False
        self.edit_aadhaar = None
        self.manager.current = "patient_list"

    # Commit: Save patient to DB (insert or update)
    def save_patient(self):
        # gather values
        aadhaar = self.p_aadhaar.text.strip()
        name = self.p_name.text.strip()
        email = self.p_email.text.strip()
        gender = self.p_gender.text.strip()
        dob = self.p_dob.text.strip()
        blood = self.p_blood.text.strip()
        marital = self.p_marital.text.strip()
        phone = self.p_phone.text.strip()
        location = self.p_location.text.strip()
        password = self.p_password.text.strip()
        # medical
        allergies = self.m_allergies.text.strip()
        current_med = self.m_current.text.strip()
        past_med = self.m_past.text.strip()
        chronic = self.m_chronic.text.strip()
        injuries = self.m_injuries.text.strip()
        surgeries = self.m_surgeries.text.strip()
        # lifestyle
        smoking = self.l_smoking.text.strip()
        alcohol = self.l_alcohol.text.strip()
        activity = self.l_activity.text.strip()
        food = self.l_food.text.strip()
        occupation = self.l_occupation.text.strip()

        if not aadhaar or not name or not password:
            show_popup("Error", "Aadhaar, Name and Password are required.")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            if self.edit_mode and self.edit_aadhaar:
                # Commit: Editing existing patient - update all tables
                # Update personal
                c.execute("""
                    UPDATE patient_personal SET name=?, email=?, gender=?, dob=?, blood_group=?, marital_status=?, phone=?, location=?, password=? WHERE aadhaar=?
                """, (name, email, gender, dob, blood, marital, phone, location, password, self.edit_aadhaar))
                # If aadhaar changed, we need to move records. For now, disallow aadhaar change in edit.
                # Update medical
                c.execute("""
                    INSERT OR REPLACE INTO patient_medical (aadhaar, allergies, current_medication, past_medication, chronic_disease, injuries, surgeries)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.edit_aadhaar, allergies, current_med, past_med, chronic, injuries, surgeries))
                # Update lifestyle
                c.execute("""
                    INSERT OR REPLACE INTO patient_lifestyle (aadhaar, smoking, alcohol, activity_level, food_preference, occupation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.edit_aadhaar, smoking, alcohol, activity, food, occupation))
                # also update users table password / name / phone if exists
                c.execute("UPDATE users SET name=?, email=?, phone=?, password=? WHERE aadhaar=?", (name, email, phone, password, self.edit_aadhaar))
                conn.commit()
                show_popup("Success", "Patient updated.")
            else:
                # Insert new records - ensure aadhaar not duplicate
                c.execute("SELECT aadhaar FROM patient_personal WHERE aadhaar=?", (aadhaar,))
                if c.fetchone():
                    show_popup("Error", "Aadhaar already exists. Use edit.")
                    conn.close()
                    return
                # personal
                c.execute("""
                    INSERT INTO patient_personal (aadhaar, name, email, gender, dob, blood_group, marital_status, phone, location, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (aadhaar, name, email, gender, dob, blood, marital, phone, location, password))
                # medical
                c.execute("""
                    INSERT INTO patient_medical (aadhaar, allergies, current_medication, past_medication, chronic_disease, injuries, surgeries)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (aadhaar, allergies, current_med, past_med, chronic, injuries, surgeries))
                # lifestyle
                c.execute("""
                    INSERT INTO patient_lifestyle (aadhaar, smoking, alcohol, activity_level, food_preference, occupation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (aadhaar, smoking, alcohol, activity, food, occupation))
                # add to users table for login
                c.execute("""
                    INSERT OR REPLACE INTO users (name, email, aadhaar, phone, password, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, email, aadhaar, phone, password, "Patient"))
                conn.commit()
                show_popup("Success", "Patient added and login created.")
            conn.close()
            # reset and go back
            self.edit_mode = False
            self.edit_aadhaar = None
            self.manager.get_screen('patient_list').build()
            self.manager.current = "patient_list"
        except sqlite3.IntegrityError as e:
            conn.close()
            show_popup("Error", f"DB error: {e}")
        except Exception as e:
            conn.close()
            show_popup("Error", f"Save failed: {e}")

# Commit: Pre-fill fields when editing
def load_for_edit(self, aadhaar):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, email, gender, dob, blood_group, marital_status, phone, location, password FROM patient_personal WHERE aadhaar=?", (aadhaar,))
    p = c.fetchone()
    c.execute("SELECT allergies, current_medication, past_medication, chronic_disease, injuries, surgeries FROM patient_medical WHERE aadhaar=?", (aadhaar,))
    m = c.fetchone()
    c.execute("SELECT smoking, alcohol, activity_level, food_preference, occupation FROM patient_lifestyle WHERE aadhaar=?", (aadhaar,))
    l = c.fetchone()
    conn.close()
    if not p:
        show_popup("Error", "Patient data not found.")
        return
    # set edit mode
    self.edit_mode = True
    self.edit_aadhaar = aadhaar
    # show page1 and then prefill fields after widgets created
    self.load_page(1)
    # we call prefill helper which uses instance widgets
    # but widgets are only created when load_page called for those pages; we created page1 now
    self.p_name.text = p[0] or ""
    self.p_email.text = p[1] or ""
    self.p_gender.text = p[2] or ""
    self.p_dob.text = p[3] or ""
    self.p_blood.text = p[4] or ""
    self.p_marital.text = p[5] or ""
    self.p_phone.text = p[6] or ""
    self.p_location.text = p[7] or ""
    self.p_password.text = p[8] or ""
    # medical & lifestyle will fill when those pages are loaded; store temp
    self._medical_prefill = m or ("", "", "", "", "", "")
    self._lifestyle_prefill = l or ("", "", "", "", "")

def prefill_fields_if_needed(self):
    # When navigating to medical or lifestyle pages during edit, prefill
    if self.page == 2 and hasattr(self, "_medical_prefill"):
        self.m_allergies.text = self._medical_prefill[0] or ""
        self.m_current.text = self._medical_prefill[1] or ""
        self.m_past.text = self._medical_prefill[2] or ""
        self.m_chronic.text = self._medical_prefill[3] or ""
        self.m_injuries.text = self._medical_prefill[4] or ""
        self.m_surgeries.text = self._medical_prefill[5] or ""
    if self.page == 3 and hasattr(self, "_lifestyle_prefill"):
        self.l_smoking.text = self._lifestyle_prefill[0] or ""
        self.l_alcohol.text = self._lifestyle_prefill[1] or ""
        self.l_activity.text = self._lifestyle_prefill[2] or ""
        self.l_food.text = self._lifestyle_prefill[3] or ""
        self.l_occupation.text = self._lifestyle_prefill[4] or ""


# ----------------------- DOCTOR LIST & ADD / EDIT (Full screen single page) -----------------------
class DoctorListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields = ["Name", "Specialization", "Phone", "Aadhaar"]
        self.build()


    def build(self):
        self.clear_widgets()
        main = BoxLayout(orientation="vertical", padding=10, spacing=8)
        main.add_widget(Label(text="[b]Doctor Information[/b]", markup=True, font_size=22, size_hint_y=None, height=50, color=(0,0,0,1)))

        btn_add = Button(text="Add New Doctor", size_hint_y=None, height=50)
        btn_add.bind(on_release=lambda x: setattr(self.manager, "current", "doctor_add"))

        scroll = ScrollView()
        rows = self.fetch_all_doctors_short()
        table = EditableTable(self.fields, rows, self.edit_doctor, self.delete_doctor)
        scroll.add_widget(table)

        btn_back = Button(text="Back", size_hint_y=None, height=50)
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "home"))

        main.add_widget(btn_add)
        main.add_widget(scroll)
        main.add_widget(btn_back)
        self.add_widget(main)

    def fetch_all_doctors_short(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name, specialization, phone, aadhaar FROM doctor_info")
        rows = c.fetchall()
        conn.close()
        return rows

    def edit_doctor(self, index):
        rows = self.fetch_all_doctors_short()
        if index < 0 or index >= len(rows):
            show_popup("Error", "Invalid index")
            return
        aadhaar = rows[index][3]
        self.manager.get_screen('doctor_add').load_for_edit(aadhaar)
        self.manager.current = 'doctor_add'

    def delete_doctor(self, index):
        rows = self.fetch_all_doctors_short()
        if index < 0 or index >= len(rows):
            show_popup("Error", "Invalid index")
            return
        aadhaar = rows[index][3]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM doctor_info WHERE aadhaar=?", (aadhaar,))
        c.execute("DELETE FROM users WHERE aadhaar=?", (aadhaar,))
        conn.commit()
        conn.close()
        show_popup("Success", "Doctor deleted.")
        self.build()


# ----------------------- DOCTOR ADD / EDIT SCREEN -----------------------
class DoctorAddScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.edit_mode = False
        self.edit_aadhaar = None
        self.build()


    def build(self):
        self.clear_widgets()
        main = BoxLayout(orientation="vertical", padding=10, spacing=8)
        main.add_widget(Label(text="[b]Add / Edit Doctor[/b]", markup=True, font_size=20, size_hint_y=None, height=40, color=(0,0,0,1)))

        grid = GridLayout(cols=1, spacing=6, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        # fields: name, aadhaar, phone, gender, specialization, qualification, experience, clinic, email, password
        self.d_name = TextInput(multiline=False, hint_text="Name")
        self.d_aadhaar = TextInput(multiline=False, hint_text="Aadhaar")
        self.d_phone = TextInput(multiline=False, hint_text="Phone")
        self.d_gender = TextInput(multiline=False, hint_text="Gender")
        self.d_special = TextInput(multiline=False, hint_text="Specialization")
        self.d_qual = TextInput(multiline=False, hint_text="Qualification")
        self.d_exp = TextInput(multiline=False, hint_text="Experience")
        self.d_clinic = TextInput(multiline=False, hint_text="Clinic/Hospital")
        self.d_email = TextInput(multiline=False, hint_text="Email")
        self.d_password = TextInput(multiline=False, hint_text="Password")

        for label, widget in [("Name", self.d_name), ("Aadhaar", self.d_aadhaar), ("Phone", self.d_phone),
                              ("Gender", self.d_gender), ("Specialization", self.d_special),
                              ("Qualification", self.d_qual), ("Experience", self.d_exp),
                              ("Clinic", self.d_clinic), ("Email", self.d_email), ("Password", self.d_password)]:
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=70)
            box.add_widget(Label(text=label, size_hint_y=None, height=20, color=(0,0,0,1)))
            box.add_widget(widget)
            grid.add_widget(box)

        scroll = ScrollView()
        scroll.add_widget(grid)
        main.add_widget(scroll)

        nav = BoxLayout(size_hint_y=None, height=50, spacing=8)
        btn_save = Button(text="Save", size_hint_x=0.4)
        btn_cancel = Button(text="Cancel", size_hint_x=0.6)
        btn_save.bind(on_release=lambda x: self.save_doctor())
        btn_cancel.bind(on_release=lambda x: self.cancel())
        nav.add_widget(btn_save)
        nav.add_widget(btn_cancel)
        main.add_widget(nav)

        self.add_widget(main)


    def save_doctor(self):
        aadhaar = self.d_aadhaar.text.strip()
        name = self.d_name.text.strip()
        phone = self.d_phone.text.strip()
        gender = self.d_gender.text.strip()
        special = self.d_special.text.strip()
        qual = self.d_qual.text.strip()
        exp = self.d_exp.text.strip()
        clinic = self.d_clinic.text.strip()
        email = self.d_email.text.strip()
        password = self.d_password.text.strip()

        if not aadhaar or not name or not password:
            show_popup("Error", "Aadhaar, Name and Password required.")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            if self.edit_mode and self.edit_aadhaar:
                c.execute("""
                    UPDATE doctor_info SET name=?, phone=?, gender=?, specialization=?, qualification=?, experience=?, clinic=?, email=?, password=? WHERE aadhaar=?
                """, (name, phone, gender, special, qual, exp, clinic, email, password, self.edit_aadhaar))
                c.execute("UPDATE users SET name=?, email=?, phone=?, password=?, role=? WHERE aadhaar=?",
                          (name, email, phone, password, "Doctor", self.edit_aadhaar))
                conn.commit()
                show_popup("Success", "Doctor updated.")
            else:
                # check duplicate
                c.execute("SELECT aadhaar FROM doctor_info WHERE aadhaar=?", (aadhaar,))
                if c.fetchone():
                    show_popup("Error", "Aadhaar exists.")
                    conn.close()
                    return
                c.execute("""
                    INSERT INTO doctor_info (aadhaar, name, phone, gender, specialization, qualification, experience, clinic, email, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (aadhaar, name, phone, gender, special, qual, exp, clinic, email, password))
                # insert into users table
                c.execute("""
                    INSERT OR REPLACE INTO users (name, email, aadhaar, phone, password, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, email, aadhaar, phone, password, "Doctor"))
                conn.commit()
                show_popup("Success", "Doctor added and login created.")
            conn.close()
            self.edit_mode = False
            self.edit_aadhaar = None
            self.manager.get_screen('doctor_list').build()
            self.manager.current = 'doctor_list'
        except sqlite3.IntegrityError as e:
            conn.close()
            show_popup("Error", f"DB error: {e}")
        except Exception as e:
            conn.close()
            show_popup("Error", f"Save failed: {e}")

    def cancel(self):
        self.edit_mode = False
        self.edit_aadhaar = None
        self.manager.current = 'doctor_list'

    def load_for_edit(self, aadhaar):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name, phone, gender, specialization, qualification, experience, clinic, email, password FROM doctor_info WHERE aadhaar=?", (aadhaar,))
        r = c.fetchone()
        conn.close()
        if not r:
            show_popup("Error", "Doctor data not found.")
            return
        self.edit_mode = True
        self.edit_aadhaar = aadhaar
        # fill fields
        self.d_name.text = r[0] or ""
        self.d_phone.text = r[1] or ""
        self.d_gender.text = r[2] or ""
        self.d_special.text = r[3] or ""
        self.d_qual.text = r[4] or ""
        self.d_exp.text = r[5] or ""
        self.d_clinic.text = r[6] or ""
        self.d_email.text = r[7] or ""
        self.d_password.text = r[8] or ""

# ----------------------- APP MANAGER -----------------------
class AdminApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PatientListScreen(name="patient_list"))
        sm.add_widget(PatientAddScreen(name="patient_add"))
        sm.add_widget(DoctorListScreen(name="doctor_list"))
        sm.add_widget(DoctorAddScreen(name="doctor_add"))
        return sm

if __name__ == "__main__":
    AdminApp().run()
