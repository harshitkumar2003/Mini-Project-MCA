import kivy
import random
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView # Required for Popups
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from functools import partial
from kivy.uix.screenmanager import Screen


# --- Import Graph Components ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot
except ImportError:
    print("Error: kivy_garden.graph is not installed.")
    Graph = None
    MeshLinePlot = None


# --- POPUP CLASSES ---
class AlertsPopup(ModalView):
    pass

class AppointmentsPopup(ModalView):
    pass

class PatientRow(BoxLayout):
    """ Represents a single row in the patient list with a Select button """
    def __init__(self, name, condition, status, callback_func, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(45)
        self.padding = dp(5)
        self.spacing = dp(5)
        
        self.add_widget(Label(
            text=name, color=(0,0,0,1), size_hint_x=0.3, 
            halign='left', valign='middle', text_size=(None, None)
        ))

        self.add_widget(Label(
            text=condition, color=(0.3,0.3,0.3,1), size_hint_x=0.25, valign='middle'
        ))
        
        status_color = (0, 0.7, 0, 1) if status == "Stable" else (0.9, 0.1, 0.1, 1)
        self.add_widget(Label(
            text=status, color=status_color, size_hint_x=0.25, bold=True, valign='middle'
        ))

        btn = Button(
            text="Select", size_hint_x=0.2,
            background_normal='', background_color=get_color_from_hex("#3498DB"),
            color=(1,1,1,1), bold=True, font_size='11sp'
        )
        btn.bind(on_release=partial(callback_func, name))
        self.add_widget(btn)

class DoctorDashboard(Screen):
    def on_kv_post(self, base_widget):
        if Graph:
            self.graph = self.ids.trend_graph
            self.plot = MeshLinePlot(color=get_color_from_hex("#E74C3C"))
            self.plot.points = [] 
            self.graph.add_plot(self.plot)
            self.data_points = [65] * 12 
            Clock.schedule_interval(self.update_graph, 1)
        
        self.populate_patients()

    def populate_patients(self):
        # Saved as self.patients_list so we can filter it for alerts later
        self.patients_list = [
            ("Harshit", "Fracture", "Stable"),
            ("Chetan", "Cardiac", "Critical"),
            ("Atul", "Fracture", "Stable"),
            ("Anshul", "Migraine", "Stable"),
            ("Shivam", "Diabetes", "Critical"),
            ("Rahul", "Viral", "Stable"),
            ("Priya", "Dengue", "Critical"),
        ]
        grid = self.ids.patient_grid_id
        grid.clear_widgets()
        
        for name, cond, stat in self.patients_list:
            row = PatientRow(name, cond, stat, self.view_patient_report)
            grid.add_widget(row)

    # --- NEW: SHOW ALERTS POPUP ---
    def show_alerts(self):
        popup = AlertsPopup()
        container = popup.ids.alert_container
        
        # Filter for 'Critical' patients
        critical_count = 0
        for name, cond, stat in self.patients_list:
            if stat == "Critical":
                critical_count += 1
                # Create a simple layout for the alert row
                row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
                row.add_widget(Label(text="⚠️", size_hint_x=None, width=dp(30)))
                row.add_widget(Label(text=f"{name} ({cond})", color=(0,0,0,1), halign='left', text_size=(None, None)))
                container.add_widget(row)
        
        if critical_count == 0:
             container.add_widget(Label(text="No Critical Alerts", color=(0,0,0,0.5)))
             
        popup.open()

    # --- NEW: SHOW APPOINTMENTS POPUP ---
    def show_appointments(self):
        popup = AppointmentsPopup()
        container = popup.ids.appt_container
        
        # Dummy Appointment Data
        appointments = [
            ("10:00 AM", "Rohit Verma", "General Checkup"),
            ("11:30 AM", "Sneha Gupta", "Follow-up"),
            ("02:00 PM", "Amit Kumar", "Report Review"),
        ]
        
        for time, name, reason in appointments:
            row = BoxLayout(size_hint_y=None, height=dp(50), orientation='vertical', padding=[0, dp(5)])
            
            # Top line: Time and Name
            top = BoxLayout()
            top.add_widget(Label(text=time, bold=True, color=get_color_from_hex("#3498DB"), size_hint_x=0.3))
            top.add_widget(Label(text=name, bold=True, color=(0,0,0,1), size_hint_x=0.7))
            
            # Bottom line: Reason
            bot = Label(text=reason, color=(0.5,0.5,0.5,1), font_size='12sp')
            
            row.add_widget(top)
            row.add_widget(bot)
            container.add_widget(row)
            
            # Separator
            div = BoxLayout(size_hint_y=None, height=dp(1))
            with div.canvas:
                from kivy.graphics import Color, Rectangle
                Color(0.9, 0.9, 0.9, 1)
                Rectangle(pos=div.pos, size=div.size)
            container.add_widget(div)

        popup.open()

    def view_patient_report(self, patient_name, instance):
        print(f"Selecting: {patient_name}")
        # yahan se current ScreenManager se patient_details_screen lo
        patient_screen = self.manager.get_screen("patient_details_screen")
        # uske andar PatientDashboard ka instance kv se hona chahiye (neeche explain kar rha hoon)
        if hasattr(patient_screen, "patient_content"):
            patient_screen.patient_content.update_patient_info(patient_name)
        self.manager.current = "patient_details_screen"

    def update_graph(self, dt):
        if not hasattr(self, 'plot'): return
        new_val = random.randint(62, 78)
        self.data_points.pop(0)
        self.data_points.append(new_val)
        new_points = [(i, val) for i, val in enumerate(self.data_points)]
        self.plot.points = new_points

    def go_back(self):
        print("At Root Level")

class PatientDetailScreenWrapper(Screen):
    def __init__(self, dashboard_content, **kwargs):
        super().__init__(**kwargs)
        self.patient_content = dashboard_content  
        layout = BoxLayout(orientation='vertical')
        
        # Top Nav
        nav_bar = BoxLayout(size_hint_y=None, height=dp(50), padding=[dp(10),0])
        with nav_bar.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(rgba=get_color_from_hex("#2ECC71"))
            Rectangle(pos=nav_bar.pos, size=nav_bar.size)
            
        btn_back = Button(
            text="< Back to List",
            size_hint_x=None, width=dp(120),
            background_normal='', background_color=(0,0,0,0),
            bold=True
        )
        btn_back.bind(on_release=self.go_to_doctor)
        nav_bar.add_widget(btn_back)
        layout.add_widget(nav_bar)
        
        # Patient Content
        layout.add_widget(dashboard_content)
        self.add_widget(layout)
        
    def go_to_doctor(self, instance):
        self.manager.current = 'doctor'
