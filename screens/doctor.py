import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp # For density-independent pixels
from kivy.core.window import Window # <<< FIX 1: Import the Window object

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

class DoctorDashboardApp(App):
    """
    A Kivy app that displays a Doctor Dashboard with patient overviews and quick actions.
    """

    def build(self):
        """
        Builds the Kivy UI for the Doctor Dashboard.
        """
        # --- Main Layout ---
        root_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Set a dark grey background color for the whole app
        with root_layout.canvas.before:
            Color(1, 1, 1, 1) # white background
            self.root_rect = Rectangle(size=root_layout.size, pos=root_layout.pos) # Stored on the app instance
        
        # Update root_rect size on window resize
        def update_root_rect(instance, value):
            self.root_rect.pos = instance.pos
            self.root_rect.size = instance.size
        root_layout.bind(pos=update_root_rect, size=update_root_rect)

        # --- 1. Title Label ---
        title = Label(
            text='Doctor Dashboard',
            font_size='32sp',
            bold=True,
            color=get_color_from_hex("#020202"), # White text
            size_hint=(1, 0.1)
        )
        root_layout.add_widget(title)

        # --- 2. Doctor Info Section ---
        doctor_info_layout = GridLayout(
            cols=2,
            size_hint=(1, 0.15),
            row_force_default=True,
            row_default_height=dp(30),
            padding=[dp(10), dp(0)]
        )
        
        doctor_data = {
            "Doctor Name:": "Dr. Alex Smith",
            "Specialization:": "Cardiology",
            "Active Patients:": "12",
            "Shift Status:": "[color=2ECC71]Active[/color]" # Green for active
        }
        
        for key, value in doctor_data.items():
            doctor_info_layout.add_widget(
                Label(text=key, font_size='18sp', bold=True, halign='right', padding=[dp(20),0], color=get_color_from_hex("#000000")) # Lighter grey
            )
            doctor_info_layout.add_widget(
                Label(text=value, font_size='18sp', halign='left', padding=[dp(20),0], markup=True, color=get_color_from_hex("#262525")) # White or colored
            )
            
        root_layout.add_widget(doctor_info_layout)

        # --- 3. Patient List Overview ---
        patient_list_title = Label(
            text='My Patients Overview',
            font_size='24sp',
            bold=True,
            color=get_color_from_hex("#000000"),
            size_hint=(1, 0.1)
        )
        root_layout.add_widget(patient_list_title)

        # Scrollable list for patients
        scroll_view = ScrollView(size_hint=(1, 0.4), do_scroll_x=False)
        
        # <<< FIX 2: Changed self.height to Window.height
        patient_grid = GridLayout(cols=1, spacing=dp(5), size_hint_y=None, height=Window.height) 
        
        patient_grid.bind(minimum_height=patient_grid.setter('height')) # Allow grid to grow

        mock_patients = [
            {"name": "Jane Doe", "status": "Stable", "status_color": "#2ECC71", "room": "305B"},
            {"name": "John Smith", "status": "Critical", "status_color": "#E74C3C", "room": "210A"},
            {"name": "Emily White", "status": "Monitoring", "status_color": "#F39C12", "room": "412C"},
            {"name": "Michael Brown", "status": "Stable", "status_color": "#2ECC71", "room": "101D"},
            {"name": "Sophia Lee", "status": "Stable", "status_color": "#2ECC71", "room": "301E"},
            {"name": "David Green", "status": "Monitoring", "status_color": "#F39C12", "room": "205F"},
            {"name": "Olivia Black", "status": "Critical", "status_color": "#E74C3C", "room": "115G"},
            {"name": "William Blue", "status": "Stable", "status_color": "#2ECC71", "room": "402H"},
            {"name": "Ava Pink", "status": "Monitoring", "status_color": "#F39C12", "room": "310I"},
            {"name": "Liam Grey", "status": "Stable", "status_color": "#2ECC71", "room": "208J"},
            # Add more patients to test scrolling
        ]

        # Helper function to create a patient entry
        def create_patient_entry(name, status, status_color, room):
            entry_box = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(5), spacing=dp(10))
            
            # Background for each patient entry
            with entry_box.canvas.before:
                Color(1, 1, 1, 1) # Slightly lighter grey for entry background
                entry_box.rect = Rectangle(pos=entry_box.pos, size=entry_box.size, radius=[dp(5)])
            
            # Update background on resize
            def update_entry_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size
            entry_box.bind(pos=update_entry_rect, size=update_entry_rect)

            entry_box.add_widget(Label(text=name, font_size='18sp', bold=True, halign='left', size_hint_x=0.5, color=get_color_from_hex("#000000")))
            entry_box.add_widget(Label(text=f'Room: {room}', font_size='16sp', halign='center', size_hint_x=0.25, color=get_color_from_hex("#000000")))
            entry_box.add_widget(Label(text=status, font_size='16sp', bold=True, halign='right', size_hint_x=0.25, color=get_color_from_hex(status_color)))
            return entry_box

        for patient in mock_patients:
            patient_grid.add_widget(
                create_patient_entry(
                    patient["name"], patient["status"], patient["status_color"], patient["room"]
                )
            )
        
        scroll_view.add_widget(patient_grid)
        root_layout.add_widget(scroll_view)

        # --- 4. Quick Actions / Notifications ---
        actions_title = Label(
            text='Quick Actions & Alerts',
            font_size='24sp',
            bold=True,
            color=get_color_from_hex("#000000"),
            size_hint=(1, 0.1)
        )
        root_layout.add_widget(actions_title)

        actions_layout = GridLayout(cols=3, size_hint=(1, None), height=dp(60), spacing=dp(10))
        
        # Helper function to create styled buttons
        def create_action_button(text, hex_color):
            btn = Button(
                text=text,
                background_normal='',
                background_color=get_color_from_hex(hex_color),
                color=get_color_from_hex("#000000"),
                font_size='16sp',
                bold=True,
                size_hint_y=None, height=dp(50)
            )
            return btn

        actions_layout.add_widget(create_action_button("New Alert (2)", "#E74C3C")) # Red for alerts
        actions_layout.add_widget(create_action_button("Appointments (3)", "#3498DB")) # Blue for appointments
        actions_layout.add_widget(create_action_button("View Reports", "#2ECC71")) # Green for reports
        
        root_layout.add_widget(actions_layout)

        # --- 5. Overall Trend Graph (e.g., Average Vitals) ---
        trend_graph_title = Label(
            text='Overall Patient Vitals Trend',
            font_size='24sp',
            bold=True,
            color=get_color_from_hex("#000000"),
            size_hint=(1, 0.1)
        )
        root_layout.add_widget(trend_graph_title)

        # Mock data for an overall trend graph (e.g., average heart rate)
        overall_trend_data = [
            (0, 70), (1, 71), (2, 69), (3, 72), (4, 70), (5, 73),
            (6, 71), (7, 74), (8, 72), (9, 75), (10, 73), (11, 76)
        ]

        graph_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.4))
        
        graph = Graph(
            xlabel='Hour',
            ylabel='Avg. HR',
            x_ticks_minor=1,
            x_ticks_major=2,
            y_ticks_major=5,
            y_grid_label=True,
            x_grid_label=True,
            padding=dp(5),
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=11,
            ymin=60,
            ymax=80,
            # Customize colors for the graph background and labels
            background_color=[1, 1, 1, 1], # Slightly lighter dark grey
            label_options={'color': [0.1, 0.1, 0.1, 1], 'bold': True}, # black labels
            tick_color=[0.5, 0.5, 0.5, 1], # Grey ticks
        )

        overall_plot = MeshLinePlot(color=get_color_from_hex("#F35212")) # Orange line
        overall_plot.points = overall_trend_data
        graph.add_plot(overall_plot)

        graph_layout.add_widget(graph)
        root_layout.add_widget(graph_layout)

        return root_layout


if __name__ == '__main__':
    DoctorDashboardApp().run()