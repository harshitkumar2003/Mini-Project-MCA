#doc2patient screen
import kivy
import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, ColorProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock  # <--- Required for dynamic updates

# --- Import Kivy Garden Graph ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot, MeshStemPlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Run: pip install kivy-garden && kivy garden install graph")
    exit(1)

kivy.require('2.1.0')

# --- LOAD KV FILE ROBUSTLY ---
current_dir = os.path.dirname(os.path.abspath(__file__))
kv_file_path = os.path.join(current_dir, 'doc2patient.kv')

try:
    Builder.load_file("kv/doc2patient.kv") # Loading the file path directly
except FileNotFoundError:
    print(f"\nERROR: Could not find 'doc2patient.kv' at: {kv_file_path}")
    exit(1)

# -----------------------------------

class RoundedBoxLayout(BoxLayout):
    background_color = ColorProperty([1, 1, 1, 1])
    radius = ListProperty([dp(15)])

class PatientHeader(RoundedBoxLayout):
    patient_name = StringProperty("Harshit")
    room_no = StringProperty("302 - ICU")
    blood_group = StringProperty("O+")
    aadhar = StringProperty("xxxx-xxxx-2374")
    gender = StringProperty("Male")
    phone = StringProperty("+91 9397123561")

class ReportCard(RoundedBoxLayout):
    icon = StringProperty("")
    title = StringProperty("")
    value = StringProperty("")
    text_color = ColorProperty([0, 0, 0, 1])

class BasicReportSection(GridLayout):
    pass

class AlertCard(RoundedBoxLayout):
    pass

class VitalsSection(BoxLayout):
    def on_kv_post(self, base_widget):
        """ Called after KV is loaded. Initialize data and start clock. """
        
        # 1. Initialize Data Buckets
        # We create a list of 20 initial '0' values for Heart Rate
        self.hr_data_points = [60 + random.randint(-5, 5) for _ in range(20)]
        
        # We create specific X-axis positions for the 4 bars of Blood Pressure
        self.bp_x_positions = [15, 35, 55, 75] 
        self.bp_data_points = [120, 118, 122, 119] # Initial Sys BP values

        # 2. Add the empty graphs to the UI
        self.add_graphs()

        # 3. Schedule the update function to run every 1 second
        Clock.schedule_interval(self.update_charts, 1)

    def add_graphs(self):
        # --- Heart Rate Setup ---
        hr_graph = Graph(
            xmin=0, xmax=20, ymin=40, ymax=140, # Adjusted Y range for realistic HR
            x_grid=False, y_grid=True, draw_border=False, padding=5,
            y_ticks_major=25
        )
        self.hr_plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        hr_graph.add_plot(self.hr_plot)
        self.ids.hr_container.add_widget(hr_graph)
        
        # --- Blood Pressure Setup ---
        bp_graph = Graph(
            xmin=0, xmax=100, ymin=50, ymax=180, # Adjusted Y range for BP
            x_grid=False, y_grid=True, draw_border=False, padding=5,
            y_ticks_major=50
        )
        # Using a Stem Plot (Bar-like)
        self.bp_plot = MeshStemPlot(color=get_color_from_hex("#E74C3C"))
        bp_graph.add_plot(self.bp_plot)
        self.ids.bp_container.add_widget(bp_graph)

    def update_charts(self, dt):
        """ Called every second by Kivy Clock """
        
        # --- Update Heart Rate (Sliding Window Logic) ---
        # 1. Generate a new random HR between 60 and 100
        new_hr = random.randint(60, 100)
        
        # 2. Remove the oldest point (index 0) and add the new one
        self.hr_data_points.pop(0)
        self.hr_data_points.append(new_hr)

        # 3. Re-map the data to X coordinates (0 to 19)
        # This creates the "scrolling" effect because index 0 is always X=0
        points_list = []
        for x_index, y_value in enumerate(self.hr_data_points):
            points_list.append((x_index, y_value))
        
        # 4. Apply to plot
        self.hr_plot.points = points_list

        # --- Update Blood Pressure (Bar Variation) ---
        # 1. Generate slightly different Sys BP for the bars
        new_bp = random.randint(110, 130)
        self.bp_data_points.pop(0)
        self.bp_data_points.append(new_bp)

        # 2. Map these to the fixed X positions
        bp_points = []
        for i, x_pos in enumerate(self.bp_x_positions):
            bp_points.append((x_pos, self.bp_data_points[i]))
            
        self.bp_plot.points = bp_points

class LabItem(BoxLayout):
    title = StringProperty("")
    subtitle = StringProperty("")

class LabsSection(BoxLayout):
    def on_kv_post(self, base_widget):
        labs = [
            ("Blood Analysis", "Hemoglobin & Platelets"),
            ("X-Ray Report", "Chest cavity scan"),
        ]
        for title, subtitle in labs:
            item = LabItem(title=title, subtitle=subtitle)
            self.ids.lab_container.add_widget(item)

class DashboardRoot(ScrollView):
    pass

class PatientDashboardApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex("#75D37D")
        Window.size = (400, 800)
        return DashboardRoot()

if __name__ == '__main__':
    PatientDashboardApp().run()
