import kivy
import os  # <--- ADDED THIS
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, ColorProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder

# --- Import Kivy Garden Graph ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot, MeshStemPlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Run: pip install kivy-garden && kivy garden install graph")
    exit(1)

kivy.require('2.1.0')

# --- FIX: LOAD KV FILE ROBUSTLY ---
# This gets the directory where patient.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# This combines the directory with the filename
kv_file_path = os.path.join(current_dir, 'kv/patient.kv')

try:
    Builder.load_file("kv/patient.kv")
except FileNotFoundError:
    print(f"\nERROR: Could not find 'patient.kv' at: {"kv/patient.kv"}")
    print("Please ensure patient.kv is in the exact same folder as patient.py\n")
    exit(1)

# -----------------------------------

class RoundedBoxLayout(BoxLayout):
    """ Custom Widget: Properties are defined here, styling in KV """
    background_color = ColorProperty([1, 1, 1, 1])
    radius = ListProperty([dp(15)])

class SearchBar(RoundedBoxLayout):
    pass

class AlertCard(RoundedBoxLayout):
    pass

class AppointmentItem(BoxLayout):
    """ Represents a single row in the appointments list """
    name = StringProperty("")
    time = StringProperty("")
    icon = StringProperty("")

class AppointmentsSection(BoxLayout):
    def on_kv_post(self, base_widget):
        """ Called after KV is fully loaded. Safe to access IDs here. """
        # Mock Data
        appointments = [
            ("Monition", "11:15 AM", "👤"),
            ("Sod Nato", "12:30 PM", "👤"),
            ("Chetan Sharma", "02:00 PM", "👤"),
            ("Harshit Kumar", "3:00 PM", "👤"),

        ]
        # Populate list dynamically
        for name, time, icon in appointments:
            item = AppointmentItem(name=name, time=time, icon=icon)
            self.ids.appt_container.add_widget(item)

class VitalsSection(BoxLayout):
    def on_kv_post(self, base_widget):
        """ Called after KV is loaded to inject graphs """
        self.add_graphs()

    def add_graphs(self):
        # 1. Heart Rate Graph
        hr_graph = self.create_line_graph()
        self.ids.hr_container.add_widget(hr_graph)
        
        # 2. Blood Pressure Graph
        bp_graph = self.create_bar_graph()
        self.ids.bp_container.add_widget(bp_graph)

    def create_line_graph(self):
        graph = Graph(
            xmin=0, xmax=100, ymin=0, ymax=100,
            x_grid=False, y_grid=False, draw_border=False, padding=5
        )
        plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        plot.points = [(0, 20), (50, 20), (100, 80)]
        graph.add_plot(plot)
        return graph

    def create_bar_graph(self):
        graph = Graph(
            xmin=0, xmax=100, ymin=0, ymax=100,
            x_grid=False, y_grid=False, draw_border=False, padding=5,
            y_ticks_major=50, x_ticks_major=25
        )
        plot = MeshStemPlot(color=get_color_from_hex("#3498DB"))
        plot.points = [(25, 30), (50, 80), (75, 50)]
        graph.add_plot(plot)
        return graph

class LabItem(BoxLayout):
    """ Represents a single row in the labs list """
    title = StringProperty("")
    subtitle = StringProperty("")

class LabsSection(BoxLayout):
    def on_kv_post(self, base_widget):
        """ Populate labs list """
        labs = [
            ("Blood Analysis", "Crownhavas topmakes"),
            ("X-Ray Report", "Chest cavity scan"),
        ]
        for title, subtitle in labs:
            item = LabItem(title=title, subtitle=subtitle)
            self.ids.lab_container.add_widget(item)

class DashboardRoot(ScrollView):
    pass

class PatientDashboardApp(App):
    def build(self):
        # Set App Background Color
        Window.clearcolor = get_color_from_hex("#F7F7F9")
        # Simulate Mobile Size
        Window.size = (400, 800)
        return DashboardRoot()

if __name__ == '__main__':
    PatientDashboardApp().run()