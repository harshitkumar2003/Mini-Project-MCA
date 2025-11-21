import kivy
import os
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout # Changed from BoxLayout to FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ColorProperty
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# --- Import Kivy Garden Graph ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Run: pip install kivy-garden && kivy garden install graph")
    exit(1)

kivy.require('2.1.0')

class VitalBox(BoxLayout):
    title = StringProperty('')
    value = StringProperty('')
    unit = StringProperty('')
    box_color = ColorProperty((0, 0, 0, 1))

# INHERITANCE CHANGED: Now inherits from FloatLayout to allow layering
class PatientDashboard(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.setup_graph, 0)

    def setup_graph(self, dt):
        # IDs are still accessible even inside the nested layout
        graph = self.ids.vitals_graph

        self.hr_plot = MeshLinePlot(color=get_color_from_hex("#E74C3C"))
        self.hr_plot.points = [(i, random.randint(70, 85)) for i in range(12)]
        
        self.bp_plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        self.bp_plot.points = [(i, random.randint(110, 130)) for i in range(12)]

        graph.add_plot(self.hr_plot)
        graph.add_plot(self.bp_plot)

        Clock.schedule_interval(self.update_graph, 1.0)

    def update_graph(self, dt):
        current_hr_y = [point[1] for point in self.hr_plot.points]
        new_hr_y = current_hr_y[1:] + [random.randint(70, 90)]
        self.hr_plot.points = [(i, y) for i, y in enumerate(new_hr_y)]

        current_bp_y = [point[1] for point in self.bp_plot.points]
        new_bp_y = current_bp_y[1:] + [random.randint(115, 135)]
        self.bp_plot.points = [(i, y) for i, y in enumerate(new_bp_y)]

class PatientDashboardApp(App):
    def build(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kv_file_path = os.path.join(current_dir, 'kv', 'doc2patient.kv')
        
        try:
            Builder.load_file("kv/patient.kv")
        except FileNotFoundError:
            print(f"\nERROR: Could not find KV file at: {kv_file_path}")
            print("Please create a folder named 'kv' and place 'doc2patient.kv' inside it.\n")
            exit(1)

        return PatientDashboard()

if __name__ == '__main__':
    PatientDashboardApp().run()
  