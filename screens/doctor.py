import kivy
import random
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
import os

# Set a standard size for testing on PC, remove this for mobile
Window.size = (400, 750)

# --- Import Graph Components ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot
except ImportError:
    print("Error: kivy_garden.graph is not installed.")
    print("Please run: pip install kivy-garden && kivy garden install graph")
    exit()

# --- Load the KV file ---
# Ensures it loads doctor.kv regardless of where you run the script from
if os.path.exists('doctor.kv'):
    Builder.load_file('doctor.kv')
elif os.path.exists('kv/doctor.kv'):
    Builder.load_file('kv/doctor.kv')
else:
    # Fallback string loading if file is missing (Optional, but good for debugging)
    print("Warning: doctor.kv not found, ensure it is in the same directory.")

class PatientRow(BoxLayout):
    """ Represents a single row in the patient list """
    def __init__(self, name, condition, status, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        self.padding = dp(5)
        
        # Simple styling for the row
        self.add_widget(Label(text=name, color=(0,0,0,1), size_hint_x=0.4, halign='left', valign='middle'))
        self.add_widget(Label(text=condition, color=(0.3,0.3,0.3,1), size_hint_x=0.3, valign='middle'))
        
        status_color = (0, 0.7, 0, 1) if status == "Stable" else (0.9, 0.1, 0.1, 1)
        self.add_widget(Label(text=status, color=status_color, size_hint_x=0.3, bold=True, valign='middle'))

class DoctorDashboard(Screen):
    def on_kv_post(self, base_widget):
        """ Called once the KV file is fully loaded. """
        
        # 1. SETUP THE GRAPH
        self.graph = self.ids.trend_graph
        
        # Create the line plot (Red color)
        self.plot = MeshLinePlot(color=get_color_from_hex("#E74C3C"))
        self.plot.points = [] 
        self.graph.add_plot(self.plot)
        
        # Initialize data storage
        self.data_points = [65] * 12 
        
        # 2. POPULATE PATIENTS
        self.populate_patients()

        # 3. START THE CLOCK
        Clock.schedule_interval(self.update_graph, 1)

    def populate_patients(self):
        """ Adds your specific data to the list """
        patients = [
            ("Harshit", "Fracture", "Stable"),
            ("Chetan", "Cardiac", "Critical"),
            ("Atul", "Fracture", "Stable"),
            ("Anshul", "Migraine", "Stable"),
            ("Shivam", "Diabetes", "Critical"),
            ("Rahul", "Viral", "Stable"), # Added to demonstrate scrolling
            ("Priya", "Dengue", "Critical"),
            ("Amit", "Ortho", "Stable"),
        ]
        grid = self.ids.patient_grid_id
        # Clear widgets first to prevent duplicates if re-run
        grid.clear_widgets()
        
        for name, cond, stat in patients:
            row = PatientRow(name, cond, stat)
            grid.add_widget(row)

    def update_graph(self, dt):
        """ Called every second to update the graph line """
        new_val = random.randint(62, 78)
        self.data_points.pop(0)
        self.data_points.append(new_val)
        
        new_points = []
        for i, y_value in enumerate(self.data_points):
            new_points.append((i, y_value))
            
        self.plot.points = new_points

    def open_reports(self):
        self.manager.current = "doc2patient"


    def go_back(self):
        self.manager.current = "landing"


class DoctorApp(App):
    def build(self):
        # Set window background to white as a fallback
        Window.clearcolor = (1, 1, 1, 1)
        return DoctorDashboard()

if __name__ == '__main__':
    DoctorApp().run()
