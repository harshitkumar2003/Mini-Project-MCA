import kivy
import os
import random
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout # Changed from BoxLayout to FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ColorProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# Set a standard size for testing on PC, remove this for mobile
Window.size = (400, 750)

# --- Import Kivy Garden Graph ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot
except ImportError:
    # Create a dummy class so the app doesn't crash if graph isn't installed
    class Graph(BoxLayout): pass
    class MeshLinePlot(object): 
        def __init__(self, **kwargs): pass
        points = []
    print("Warning: kivy_garden.graph not found. Graphs will not render.")

kivy.require('2.1.0')

class VitalBox(BoxLayout):
    title = StringProperty('')
    value = StringProperty('')
    unit = StringProperty('')
    box_color = ColorProperty((0, 0, 0, 1))

# INHERITANCE CHANGED: Now inherits from Screen to allow layering
class PatientDashboard(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule graph setup to run after the KV layout is fully loaded
        Clock.schedule_once(self.setup_graphs, 0)

    def setup_graphs(self, dt):
        # 1. Setup Vitals Trend Graph (Top Graph)
        if 'vitals_graph' in self.ids:
            graph = self.ids.vitals_graph
            
            # Create plots
            self.hr_plot = MeshLinePlot(color=get_color_from_hex("#E74C3C"))
            self.bp_plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
            
            # Initial Data
            self.hr_plot.points = [(i, random.randint(70, 85)) for i in range(12)]
            self.bp_plot.points = [(i, random.randint(110, 130)) for i in range(12)]

            # Add to graph
            try:
                graph.add_plot(self.hr_plot)
                graph.add_plot(self.bp_plot)
            except AttributeError:
                pass # Handle case where graph lib is missing

        # 2. Setup Health Overview Graph (Bottom Graph)
        if 'health_graph' in self.ids:
            health_graph = self.ids.health_graph
            health_plot = MeshLinePlot(color=[0.2, 0.6, 0.4, 1])
            health_plot.points = [(x, (x * 2 + 50) % 100) for x in range(30)]
            try:
                health_graph.add_plot(health_plot)
            except AttributeError:
                pass

        # Start live update
        Clock.schedule_interval(self.update_graph, 1.5)

    def update_graph(self, dt):
        # Update Heart Rate
        if hasattr(self, 'hr_plot'):
            current_hr_y = [point[1] for point in self.hr_plot.points]
            new_hr_y = current_hr_y[1:] + [random.randint(70, 90)]
            self.hr_plot.points = [(i, y) for i, y in enumerate(new_hr_y)]

        # Update BP
        if hasattr(self, 'bp_plot'):
            current_bp_y = [point[1] for point in self.bp_plot.points]
            new_bp_y = current_bp_y[1:] + [random.randint(115, 135)]
            self.bp_plot.points = [(i, y) for i, y in enumerate(new_bp_y)]

class PatientDashboardApp(App):
    def build(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kv_file_path = os.path.join(current_dir, 'kv', 'patient.kv')
        
        # Robust KV loading
        try:
            Builder.load_file(kv_file_path)
        except FileNotFoundError:
            try:
                Builder.load_file("kv/patient.kv")
            except Exception as e:
                print(f"KV Load Error: {e}")
                return BoxLayout() 

        return PatientDashboard()
    
    def go_back(self):
        self.manager.current = 'landing'

if __name__ == '__main__':
    PatientDashboardApp().run()