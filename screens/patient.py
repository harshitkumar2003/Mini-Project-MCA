import kivy
import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView # Required for the Report Screen
from kivy.properties import StringProperty, ListProperty, ColorProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

# --- Import Kivy Garden Graph ---
try:
    from kivy_garden.graph import Graph, MeshLinePlot, MeshStemPlot
except ImportError:
    Graph = None
    MeshLinePlot = None

# --- LOAD KV FILE ---
if __name__ != '__main__':
    if os.path.exists('kv/patient.kv'):
        Builder.load_file('kv/patient.kv')
else:
    if os.path.exists('kv/patient.kv'):
        Builder.load_file('kv/patient.kv')

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
        if not Graph: return
        
        # 1. Initialize Data
        self.hr_data_points = [60 + random.randint(-5, 5) for _ in range(20)]
        self.bp_x_positions = [15, 35, 55, 75] 
        self.bp_data_points = [120, 118, 122, 119] 

        # 2. Add graphs
        self.add_graphs()

        # 3. Schedule updates
        Clock.schedule_interval(self.update_charts, 1)

    def add_graphs(self):
        # Heart Rate
        hr_graph = Graph(
            xmin=0, xmax=20, ymin=40, ymax=140,
            x_grid=False, y_grid=True, draw_border=False, padding=5,
            y_ticks_major=25
        )
        self.hr_plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        hr_graph.add_plot(self.hr_plot)
        self.ids.hr_container.add_widget(hr_graph)
        
        # Blood Pressure
        bp_graph = Graph(
            xmin=0, xmax=100, ymin=50, ymax=180,
            x_grid=False, y_grid=True, draw_border=False, padding=5,
            y_ticks_major=50
        )
        self.bp_plot = MeshStemPlot(color=get_color_from_hex("#E74C3C"))
        bp_graph.add_plot(self.bp_plot)
        self.ids.bp_container.add_widget(bp_graph)

    def update_charts(self, dt):
        if not hasattr(self, 'hr_plot'): return
        
        # Update HR
        new_hr = random.randint(60, 100)
        self.hr_data_points.pop(0)
        self.hr_data_points.append(new_hr)
        points_list = [(i, val) for i, val in enumerate(self.hr_data_points)]
        self.hr_plot.points = points_list

        # Update BP
        new_bp = random.randint(110, 130)
        self.bp_data_points.pop(0)
        self.bp_data_points.append(new_bp)
        bp_points = []
        for i, x_pos in enumerate(self.bp_x_positions):
            bp_points.append((x_pos, self.bp_data_points[i]))
        self.bp_plot.points = bp_points

# --- NEW: Lab Report Screen (Popup) ---
class LabReportPopup(ModalView):
    report_title = StringProperty("Lab Report")
    
    def close_popup(self):
        self.dismiss()

class LabItem(BoxLayout):
    title = StringProperty("")
    subtitle = StringProperty("")
    
    def view_report(self):
        """ Opens the report popup screen """
        popup = LabReportPopup()
        popup.report_title = self.title
        popup.open()

class LabsSection(BoxLayout):
    def on_kv_post(self, base_widget):
        labs = [
            ("Blood Analysis", "Hemoglobin & Platelets"),
            ("X-Ray Report", "Chest cavity scan"),
            ("Urinalysis", "Routine checkup"),
        ]
        for title, subtitle in labs:
            item = LabItem(title=title, subtitle=subtitle)
            self.ids.lab_container.add_widget(item)

class DashboardRoot(ScrollView):
    def update_patient_info(self, name_text):
        """ Helper function to find the Header and update the name. """
        if not self.children: return
        main_layout = self.children[0] 
        for widget in main_layout.children:
            if isinstance(widget, PatientHeader):
                widget.patient_name = name_text
                print(f"Updated Patient Dashboard to: {name_text}")
                return

class PatientDashboardApp(App):
    def build(self):
        Window.size = (400, 800)
        return DashboardRoot()

if __name__ == '__main__':
    PatientDashboardApp().run()