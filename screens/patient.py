import kivy
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp # Import dp for consistent sizing
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

# We need to import the Graph and MeshLinePlot from the garden package
# Make sure you have installed it first using:
# pip install kivy-garden
# kivy garden install graph
try:
    from kivy_garden.graph import Graph, MeshLinePlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Please run the following commands:")
    print("pip install kivy-garden")
    print("kivy garden install graph")
    exit(1)

kivy.require('2.1.0') # Specify your Kivy version
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
current_dir = os.path.dirname(os.path.abspath("screens/patient.py"))
# This combines the directory with the filename
kv_file_path = os.path.join(current_dir, 'kv/patient.kv')

try:
    Builder.load_file("kv/patient.kv")
except FileNotFoundError:
    print(f"\nERROR: Could not find 'patient.kv' at: {"kv/patient.kv"}")
    print("Please ensure patient.kv is in the exact same folder as patient.py\n")
    exit(1)

<<<<<<< HEAD
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
=======
class PatientDashboardApp(App):
    """
    A Kivy app that displays a patient dashboard with vitals and graphs.
    """

    def build(self):
        """
        Builds the Kivy UI.
        """
        # --- Main Layout ---
        # This is the root widget
        root_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Set a white background color for the whole app
        with root_layout.canvas.before:
            Color(1, 1, 1, 1) # <<< FIX 1: Changed to WHITE background (1, 1, 1, 1)
            self.rect = Rectangle(size=root_layout.size, pos=root_layout.pos)
        
        # Update rect size on window resize
        def update_root_rect(instance, value):
            # This function correctly references self.rect created above
            self.rect.pos = instance.pos
            self.rect.size = instance.size
        
        # Bind the update function for resizing the background rectangle
        root_layout.bind(pos=update_root_rect, size=update_root_rect)

        # --- 1. Title Label ---
        title = Label(
            text='Patient Dashboard',
            font_size='32sp',  # sp = scale-independent pixels
            bold=True,
            size_hint=(1, 0.1), # Use 10% of vertical space
            color=get_color_from_hex("#000000") # <<< FIX 2: Set title text color to BLACK
        )
        root_layout.add_widget(title)

        # --- 2. Patient Info Section ---
        info_layout = GridLayout(
            cols=2,
            size_hint=(1, 0.2), # Use 20% of vertical space
            row_force_default=True,
            row_default_height=dp(40)
        )
        
        # Mock Patient Data
        patient_data = {
            "Patient Name:": "Chetan Sharma",
            "Age:": "25",
            "Room:": "305B",
            "Condition:": "Stable (Post-Op)"
        }
        
        # Populate patient info labels
        black_color = get_color_from_hex("#000000")
        for key, value in patient_data.items():
            info_layout.add_widget(
                Label(text=key, font_size='18sp', bold=True, halign='right', padding=[dp(20),0], color=black_color) # <<< FIX 3: Black text
            )
            info_layout.add_widget(
                Label(text=value, font_size='18sp', halign='left', padding=[dp(20),0], color=black_color) # <<< FIX 3: Black text
            )
            
        root_layout.add_widget(info_layout)

        # --- 3. Current Vitals Section ---
        vitals_title = Label(
            text='Current Vitals',
            font_size='24sp',
            bold=True,
            size_hint=(1, 0.1),
            color=black_color # <<< FIX 4: Black text
        )
        root_layout.add_widget(vitals_title)

        # We'll use a 2x2 grid for the main vitals
        vitals_layout = GridLayout(cols=2, size_hint=(1, 0.2), spacing=dp(10))

        # Helper function to create styled vital boxes
        def create_vital_box(name, value, unit, hex_color):
            box = BoxLayout(orientation='vertical')
            
            # This local function updates the box's background rectangle
            def update_box_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size

            with box.canvas.before:
                Color(rgb=get_color_from_hex(hex_color))
                # Store the Rectangle instance on the box widget
                box.rect = Rectangle(pos=box.pos, size=box.size, radius=[dp(10)])
            
            # Text must be white against the colorful backgrounds
            white_color = get_color_from_hex("#FFFFFF")

            box.add_widget(Label(text=name, font_size='20sp', bold=True, color=white_color)) # <<< FIX 5: White text
            box.add_widget(Label(text=value, font_size='28sp', bold=True, color=white_color)) # <<< FIX 5: White text
            box.add_widget(Label(text=unit, font_size='16sp', color=white_color)) # <<< FIX 5: White text
            
            # Bind the update function for resizing the background
            box.bind(pos=update_box_rect, size=update_box_rect)
            return box

        # Add vital boxes
        vitals_layout.add_widget(
            create_vital_box("Heart Rate", "78", "bpm", "#E74C3C") # Red
        )
        vitals_layout.add_widget(
            create_vital_box("Blood Pressure", "122/81", "mmHg", "#3498DB") # Blue
        )
        vitals_layout.add_widget(
            create_vital_box("SpO2", "97", "%", "#2ECC71") # Green
        )
        vitals_layout.add_widget(
            create_vital_box("Temperature", "98.4", "°F", "#F39C12") # Orange
        )
        
        root_layout.add_widget(vitals_layout)

        # --- 4. Vitals Graph Section ---
        graph_title = Label(
            text='Vitals Trend (Last 12 Hours)',
            font_size='24sp',
            bold=True,
            size_hint=(1, 0.1),
            color=black_color # <<< FIX 6: Black text
        )
        root_layout.add_widget(graph_title)

        # Mock data for the graphs
        heart_rate_data = [
            (0, 75), (1, 78), (2, 80), (3, 79), (4, 76), (5, 75),
            (6, 77), (7, 78), (8, 82), (9, 80), (10, 78), (11, 78)
        ]
        
        blood_pressure_data = [
            (0, 120), (1, 122), (2, 125), (3, 124), (4, 121), (5, 120),
            (6, 121), (7, 122), (8, 128), (9, 126), (10, 124), (11, 122)
        ]

        # Create the graph widget
        graph_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.4))
        
        graph = Graph(
            xlabel='Hour',
            ylabel='Value',
            x_ticks_minor=1,
            x_ticks_major=2,
            y_ticks_major=20,
            y_grid_label=True,
            x_grid_label=True,
            padding=dp(5),
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=11,
            ymin=60, # Min y-value
            ymax=140, # Max y-value
            label_options={'color': black_color}, # <<< FIX 7: Black labels on graph axes
            tick_color=get_color_from_hex("#CCCCCC") # Light gray grid lines for contrast
        )

        # Create the plots
        hr_plot = MeshLinePlot(color=get_color_from_hex("#E74C3C")) # Red
        hr_plot.points = heart_rate_data
        graph.add_plot(hr_plot)
        
        bp_plot = MeshLinePlot(color=get_color_from_hex("#3498DB")) # Blue
        bp_plot.points = blood_pressure_data
        graph.add_plot(bp_plot)

        # Add a simple legend
        legend_layout = BoxLayout(size_hint=(1, None), height=dp(30), spacing=dp(20), padding=[dp(50),0])
        legend_layout.add_widget(Label(text='[color=E74C3C]●[/color] Heart Rate (bpm)', markup=True, color=black_color)) # <<< FIX 8: Black text for legend
        legend_layout.add_widget(Label(text='[color=3498DB]●[/color] BP Systolic (mmHg)', markup=True, color=black_color)) # <<< FIX 8: Black text for legend
        root_layout.add_widget(legend_layout)

        # Add the graph to its layout, and the layout to the root
        graph_layout.add_widget(graph)
        root_layout.add_widget(graph_layout)

        return root_layout
>>>>>>> b9f1aa21604b514b4af488d01a44ec56a22a7df7


class PatientScreen(Screen):
    pass  # This screen
