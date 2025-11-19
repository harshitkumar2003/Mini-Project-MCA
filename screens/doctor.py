import kivy
from kivy.uix.screenmanager import Screen
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

<<<<<<< HEAD
    def __init__(self, **kwargs):
        super(RoundedBoxLayout, self).__init__(**kwargs)
        
        # This is the correct way to add a background
        with self.canvas.before:
            # Set the color from the property
            self.color_instruction = Color(rgba=self.background_color)
            # Create the RoundedRectangle
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        
        # Bind the update_rect function to changes in pos and size
        self.bind(pos=self.update_rect, size=self.update_rect)
        # Bind the update_color function to changes in background_color
        self.bind(background_color=self.update_color)
        # Bind the update_radius function to changes in radius
        self.bind(radius=self.update_radius)

    def update_rect(self, *args):
        """ Update the position and size of the rounded rectangle. """
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_color(self, *args):
        """ Update the color of the rounded rectangle. """
        self.color_instruction.rgba = self.background_color

    def update_radius(self, *args):
        """ Update the radius of the rounded rectangle. """
        self.bg_rect.radius = self.radius

# -------------------------------------------------------------------
# --- MAIN APPLICATION CLASS ---
# -------------------------------------------------------------------

class DoctorDashboard(App):
    
=======
>>>>>>> b9f1aa21604b514b4af488d01a44ec56a22a7df7
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


<<<<<<< HEAD
    # ------------------
    # --- MAIN CONTENT (3 COLUMNS)
    # ------------------
    def create_main_content(self):
        content_layout = BoxLayout(spacing=dp(20))
        
        # --- Column 1: Appointments ---
        col_1 = self.create_appointments_column()
        
        # --- Column 2: Vitals ---
        col_2 = self.create_vitals_column()
        
        # --- Column 3: Results & Alerts ---
        col_3 = self.create_results_column()
        
        content_layout.add_widget(col_1)
        content_layout.add_widget(col_2)
        content_layout.add_widget(col_3)
        return content_layout

    # ------------------
    # --- COLUMN 1: APPOINTMENTS
    # ------------------
    def create_appointments_column(self):
        col_layout = BoxLayout(
            orientation='vertical',
            size_hint_x=0.3,
            spacing=dp(10)
        )
        
        col_layout.add_widget(Label(
            text="Upcoming Appointments",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(250), None)
        ))
        
        # Card for the list
        list_card = RoundedBoxLayout(padding=dp(10))
        
        # ScrollView for appointment items
        scroll_view = ScrollView(do_scroll_x=False)
        list_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(10))
        list_grid.bind(minimum_height=list_grid.setter('height')) # Makes it scrollable
        
        # Mock Data
        appointments = [
            ("Camily", "OUVY 2021", "1:00 pm"),
            ("Mamly", "OUVY 2021", "1:00 pm"),
            ("Mart Ray", "OUVY 2021", "1:30 pm"),
            ("Caing Sandore", "OUVY 2021", "1:30 pm"),
            ("Cammine", "OUVY 2021", "1:30 pm"),
            ("Hawer Saoe", "OUVY 2021", "1:30 pm"),
            ("Grolare", "OUVY 2021", "1:30 pm"),
        ]
        
        for name, date, time in appointments:
            item = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
            item.add_widget(Label(
                text="👤", # Emoji icon
                font_size='24sp',
                size_hint_x=None,
                width=dp(30),
                color=get_color_from_hex("#555555")
            ))
            item.add_widget(Label(
                text=f"{name}\n[size=12sp][color=888888]{date}[/color][/size]",
                markup=True,
                halign='left',
                valign='middle',
                text_size=(dp(120), None),
                color=get_color_from_hex("#333333")
            ))
            item.add_widget(Label(
                text=time,
                font_size='14sp',
                color=get_color_from_hex("#555555"),
                size_hint_x=0.3
            ))
            list_grid.add_widget(item)
            
        scroll_view.add_widget(list_grid)
        list_card.add_widget(scroll_view)
        col_layout.add_widget(list_card)
        return col_layout

    # ------------------
    # --- COLUMN 2: VITALS
    # ------------------
    def create_vitals_column(self):
        col_layout = BoxLayout(
            orientation='vertical',
            size_hint_x=0.4,
            spacing=dp(20)
        )
        
        # --- Heart Rate Card ---
        hr_card = RoundedBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        hr_card.add_widget(Label(
            text="Heart Rate",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(300), None)
        ))
        
        graph_hr = self.create_line_graph()
        hr_card.add_widget(graph_hr)
        col_layout.add_widget(hr_card)
        
        # --- Blood Pressure Card ---
        bp_card = RoundedBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        bp_card.add_widget(Label(
            text="Blood Pressure",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(300), None)
        ))
        
        graph_bp = self.create_bar_graph()
        bp_card.add_widget(graph_bp)
        col_layout.add_widget(bp_card)
        
        return col_layout

    # ------------------
    # --- COLUMN 3: RESULTS & ALERTS
    # ------------------
    def create_results_column(self):
        col_layout = BoxLayout(
            orientation='vertical',
            size_hint_x=0.3,
            spacing=dp(20)
        )
        
        # --- Lab Results Card ---
        lab_card = RoundedBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        lab_card.add_widget(Label(
            text="Recent Lab Results",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(250), None)
        ))
        
        # Mock Results
        results = ["• Coat Hb results", "• Hest 1gb results", "• Cirod pred results", "• Pest o results"]
        for result in results:
            lab_card.add_widget(Label(
                text=result,
                color=get_color_from_hex("#555555"),
                font_size='15sp',
                halign='left',
                text_size=(dp(240), None),
                size_hint_y=None,
                height=dp(25)
            ))
        
        # --- Urgent Alerts Card ---
        alert_card = RoundedBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        alert_card.add_widget(Label(
            text="Urgent Alerts",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(250), None)
        ))
        
        # Mock Alert
        alert_box = BoxLayout(spacing=dp(10), padding=[0, dp(10)])
        alert_box.add_widget(Label(
            text="❗", # Emoji icon
            font_size='24sp',
            color=get_color_from_hex("#E74C3C"), # Red color
            size_hint_x=None,
            width=dp(30)
        ))
        alert_box.add_widget(Label(
            text="Alert: Avertit alian ceius consesciat escihnt oerat.",
            color=get_color_from_hex("#555555"),
            font_size='14sp',
            halign='left',
            valign='top',
            text_size=(dp(200), None)
        ))
        alert_card.add_widget(alert_box)
        
        col_layout.add_widget(lab_card)
        col_layout.add_widget(alert_card)
        
        return col_layout

    # ------------------
    # --- GRAPH CREATION HELPERS
    # ------------------
    def create_line_graph(self):
        graph = Graph(
            xmin=0, xmax=100, ymin=0, ymax=100,
            x_grid=False, y_grid=False,
            draw_border=False,
            padding=dp(5)
        )
        plot = MeshLinePlot(color=get_color_from_hex("#555555"))
        plot.points = [
            (0, 30), (10, 60), (20, 40), (30, 70), (40, 50),
            (50, 80), (60, 60), (70, 75), (80, 55), (90, 85), (100, 70)
        ]
        graph.add_plot(plot)
        return graph

    def create_bar_graph(self):
        graph = Graph(
            xmin=0, xmax=100, ymin=0, ymax=100,
            x_ticks_major=10,
            x_grid=False, y_grid=True,
            y_ticks_major=25,
            draw_border=False,
            padding=dp(5)
        )
        plot = MeshStemPlot(color=get_color_from_hex("#3498DB")) # Blue bars
        plot.points = [
            (5, 30), (15, 60), (25, 40), (35, 70), (45, 50),
            (55, 80), (65, 60), (75, 75), (85, 55), (95, 85)
        ]
        graph.add_plot(plot)
        return graph

class DoctorScreen(Screen):
    pass  # This screen loads doctor.kv and contains widgets defined before
=======
if __name__ == '__main__':
    DoctorDashboardApp().run()
>>>>>>> b9f1aa21604b514b4af488d01a44ec56a22a7df7
