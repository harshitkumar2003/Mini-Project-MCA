import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp # For density-independent pixels
from kivy.core.window import Window
from kivy.properties import ListProperty, ColorProperty

# --- Import Kivy Garden Graph ---
# Make sure you have installed it first:
# pip install kivy-garden
# kivy garden install graph
try:
    from kivy_garden.graph import Graph, MeshLinePlot, MeshStemPlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Please run the following commands:")
    print("pip install kivy-garden")
    print("kivy garden install graph")
    exit(1)

kivy.require('2.1.0')

# -------------------------------------------------------------------
# --- CUSTOM WIDGET FOR ROUNDED CORNERS (Solves canvas errors) ---
# -------------------------------------------------------------------

class RoundedBoxLayout(BoxLayout):
    """
    A BoxLayout with a rounded rectangle background.
    This widget solves the "no attribute 'rect'" error
    by correctly creating the graphic in __init__ and
    binding its update.
    """
    # Property to hold the background color
    background_color = ColorProperty(get_color_from_hex("#FFFFFF"))
    # Property to hold the corner radius
    radius = ListProperty([dp(15)])

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

class ModernDoctorDashboardApp(App):
    
    def build(self):
        # Set the main window background color (the border area)
        Window.clearcolor = get_color_from_hex("#F0F0F0") # Light grey background

        # 1. Root Layout (to hold the main panel with padding)
        root_layout = BoxLayout(padding=dp(20))
        
        # 2. Main Content Panel (the large light-grey card)
        main_panel = RoundedBoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(20),
            background_color=get_color_from_hex("#F7F7F9"),
            radius=[dp(20)]
        )
        
        # 3. Add Header
        main_panel.add_widget(self.create_header())
        
        # 4. Add Main Content (3-column layout)
        main_panel.add_widget(self.create_main_content())
        
        root_layout.add_widget(main_panel)
        return root_layout

    # ------------------
    # --- HEADER WIDGET
    # ------------------
    def create_header(self):
        header_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(20))
        
        # Search Bar (Left)
        search_bar = RoundedBoxLayout(
            size_hint_x=0.7,
            padding=[dp(10), 0],
            radius=[dp(10)]
        )
        search_bar.add_widget(Label(
            text="🔍", # Using emoji for icon
            font_size='20sp',
            size_hint_x=None,
            width=dp(40),
            color=get_color_from_hex("#888888")
        ))
        search_bar.add_widget(TextInput(
            hint_text="Search Patient",
            background_color=[0,0,0,0], # Transparent background
            foreground_color=get_color_from_hex("#333333"),
            border=(0,0,0,0), # No border
            font_size='16sp',
            padding=[0, dp(15), 0, 0] # Center text vertically
        ))
        
        # Doctor Info (Right)
        doctor_info = BoxLayout(
            size_hint_x=0.3,
            spacing=dp(15),
            padding=[dp(10), 0]
        )
        doctor_info.add_widget(Label(
            text="👤", # Using emoji for icon
            font_size='35sp',
            size_hint_x=None,
            width=dp(40),
            color=get_color_from_hex("#333333")
        ))
        doctor_info.add_widget(Label(
            text="Doctor Name\n[size=12sp][color=888888]Cardiologist[/color][/size]",
            markup=True,
            halign='left',
            valign='middle',
            color=get_color_from_hex("#333333"),
            size_hint_x=0.7
        ))
        
        header_layout.add_widget(search_bar)
        header_layout.add_widget(doctor_info)
        return header_layout

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

# ------------------
# --- RUN THE APP
# ------------------
if __name__ == '__main__':
    ModernDoctorDashboardApp().run()