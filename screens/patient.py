from datetime import datetime
import kivy
import os
import shutil #!for download module location handling
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView # Required for the Report Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, ColorProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

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

    def download_report(self):
        try:
            # 1. Source File Path
            # Use os.path.join with App.get_running_app().directory for app-relative paths
            app_dir = App.get_running_app().directory
            source_filename = 'DReport.png'
            source_path = os.path.join(app_dir, 'assets', source_filename)
            
            # 🌟 PATH CHECK 1: Ensure Source File Exists
            if not os.path.exists(source_path):
                self.show_download_popup("Download Failed", 
                                         f"Source PDF file not found at:\n{source_path}")
                return

            # 2. Destination Directory: Prioritize Downloads, then Desktop/Home
            # os.path.expanduser('~') is reliable for home directory.
            
            download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            if not os.path.isdir(download_dir):
                 download_dir = os.path.join(os.path.expanduser('~'), 'Desktop') 
            
            # Fallback to home directory if Desktop/Downloads are inaccessible
            if not os.path.isdir(download_dir):
                download_dir = os.path.expanduser('~')

            # 3. Destination filename (Using self.report_title for unique naming)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Report_{self.report_title.replace(' ', '_')}_{timestamp}.png"
            destination_path = os.path.join(download_dir, filename)

            # 4. Copy the file
            shutil.copyfile(source_path, destination_path)
            
            # 5. Success message
            self.show_download_popup("Success", 
                                     f"Report saved to:\n{download_dir}\nFile: {filename}")
            
        except Exception as e:
            # Show the specific exception message for debugging
            self.show_download_popup("Download Failed", 
                                     f"Could not save file:\n{type(e).__name__}: {e}")
            
    def show_download_popup(self, title, message):
        # Simple popup utility for feedback
        Popup(title=title, content=Label(text=message),
              size_hint=(0.7, 0.4)).open()
              
        # Close the report view after showing the download status
        Clock.schedule_once(lambda dt: self.dismiss(), 2) # Close after 2 seconds

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

class PatientDashboard(Screen):
    def update_patient_info(self, name_text):
        """ Helper function to find the Header and update the name. """
        if not self.children: return 
        main_layout = self.children[0] 
        # Check widgets inside the main layout
        for widget in main_layout.children:
            if isinstance(widget, ScrollView): # Assuming the main ScrollView is the immediate child
                # Search inside the ScrollView content
                scroll_content = widget.children[0] 
                for sub_widget in scroll_content.children:
                    if isinstance(sub_widget, PatientHeader):
                        sub_widget.patient_name = name_text
                        print(f"Updated Patient Dashboard to: {name_text}")
                        return

class PatientDashboardApp(App):
    def build(self):
        Window.size = (400, 800)
        return PatientDashboard()

if __name__ == '__main__':
    PatientDashboardApp().run()