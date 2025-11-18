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

class PatientDashboardApp(App):
    
    def build(self):
        # Set the main window background color (the app background)
        Window.clearcolor = get_color_from_hex("#F7F7F9")
        # Set a fixed window size to simulate a phone
        Window.size = (400, 800)

        # 1. Root: A ScrollView to hold all content
        root_scroll = ScrollView(do_scroll_x=False)
        
        # 2. Main Content Layout (Vertical)
        # This GridLayout will grow vertically to fit all content
        main_content = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(20),
            padding=dp(15)
        )
        # This line is crucial for the ScrollView to work
        main_content.bind(minimum_height=main_content.setter('height'))
        
        # 3. Add all the dashboard sections
        main_content.add_widget(self.create_search_bar())
        main_content.add_widget(self.create_alert_card())
        main_content.add_widget(self.create_appointments_section())
        main_content.add_widget(self.create_vitals_section())
        main_content.add_widget(self.create_labs_section())
        
        root_scroll.add_widget(main_content)
        return root_scroll

    # ------------------
    # --- SEARCH BAR
    # ------------------
    def create_search_bar(self):
        search_bar = RoundedBoxLayout(
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex("#FFFFFF"),
            radius=[dp(10)],
            padding=[dp(10), 0],
            spacing=dp(10)
        )
        search_bar.add_widget(Label(
            text="🔍", # Using emoji for icon
            font_size='18sp',
            size_hint_x=None,
            width=dp(30),
            color=get_color_from_hex("#888888")
        ))
        search_bar.add_widget(TextInput(
            hint_text="Search Patient",
            background_color=[0,0,0,0], # Transparent background
            foreground_color=get_color_from_hex("#333333"),
            border=(0,0,0,0), # No border
            font_size='16sp',
            padding=[0, dp(15), 0, dp(5)] # Center text vertically
        ))
        search_bar.add_widget(Label(
            text="🎚️", # Using emoji for filter icon
            font_size='18sp',
            size_hint_x=None,
            width=dp(30),
            color=get_color_from_hex("#888888")
        ))
        return search_bar

    # ------------------
    # --- URGENT ALERT CARD
    # ------------------
    def create_alert_card(self):
        card = RoundedBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            radius=[dp(15)],
            background_color=get_color_from_hex("#E74C3C"), # Red color
            padding=dp(15),
            spacing=dp(5)
        )
        
        title_layout = BoxLayout(size_hint_y=None, height=dp(20), spacing=dp(10))
        title_layout.add_widget(Label(
            text="🔔", # Bell emoji
            font_size='16sp',
            size_hint_x=None,
            width=dp(20)
        ))
        title_layout.add_widget(Label(
            text="Urgent Alerts",
            font_size='16sp',
            bold=True,
            color=get_color_from_hex("#FFFFFF"), # White text
            halign='left',
            text_size=(dp(250), None)
        ))
        card.add_widget(title_layout)
        
        card.add_widget(Label(
            text="CRITICAL: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod.",
            font_size='12sp',
            color=get_color_from_hex("#FFFFFF"),
            text_size=(dp(300), None),
            halign='left',
            valign='top'
        ))
        return card

    # ------------------
    # --- APPOINTMENTS SECTION
    # ------------------
    def create_appointments_section(self):
        section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        # This bind allows the BoxLayout to grow with its content
        section.bind(minimum_height=section.setter('height'))
        
        section.add_widget(Label(
            text="Upcoming Appointments",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(350), None)
        ))
        
        # Mock Data
        appointments = [
            ("Monition", "11:15 AM", "👤"),
            ("Sod Nato", "11:15 AM", "👤"),
            ("Keh osw", "11:15 AM", "👤"),
        ]
        
        for name, time, icon in appointments:
            item = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
            
            item.add_widget(Label(
                text=icon,
                font_size='24sp',
                size_hint_x=None,
                width=dp(30),
                color=get_color_from_hex("#3498DB")
            ))
            item.add_widget(Label(
                text=f"{name}\n[size=12sp][color=888888]{time}[/color][/size]",
                markup=True,
                halign='left',
                valign='middle',
                text_size=(dp(120), None),
                color=get_color_from_hex("#333333")
            ))
            
            # Tags on the right
            tags_layout = BoxLayout(size_hint_x=None, width=dp(100), spacing=dp(5), padding=[0, dp(10)])
            
            # <<< --- FIX WAS HERE --- >>>
            # 1. Create the first tag
            tag_1 = RoundedBoxLayout(
                radius=[dp(8)], 
                background_color=get_color_from_hex("#E0EFFF"), 
                size_hint=(None, None), size=(dp(45), dp(25))
            )
            # 2. Add the label to it
            tag_1.add_widget(Label(text="18.6M", font_size='10sp', color=get_color_from_hex("#3498DB")))
            # 3. Add the tag to the layout
            tags_layout.add_widget(tag_1)

            # <<< --- AND FIX WAS HERE --- >>>
            # 1. Create the second tag
            tag_2 = RoundedBoxLayout(
                radius=[dp(8)], 
                background_color=get_color_from_hex("#E0EFFF"), 
                size_hint=(None, None), size=(dp(25), dp(25))
            )
            # 2. Add the label to it
            tag_2.add_widget(Label(text="$", font_size='10sp', color=get_color_from_hex("#3498DB")))
            # 3. Add the tag to the layout
            tags_layout.add_widget(tag_2)
            
            item.add_widget(tags_layout)
            section.add_widget(item)
            
        return section

    # ------------------
    # --- VITALS SECTION
    # ------------------
    def create_vitals_section(self):
        section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        section.bind(minimum_height=section.setter('height'))

        section.add_widget(Label(
            text="Patient Vitals Overview",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(350), None)
        ))
        
        # 2-column grid for the graphs
        grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=None, height=dp(180))
        
        # --- Heart Rate Card (Left) ---
        hr_card = RoundedBoxLayout(orientation='vertical', padding=dp(10), radius=[dp(10)])
        hr_card.add_widget(Label(
            text="Nacim Fcostesls", 
            font_size='12sp', 
            color=get_color_from_hex("#AAAAAA"),
            size_hint_y=None, height=dp(15),
            halign='left', text_size=(dp(150), None)
        ))
        hr_card.add_widget(self.create_line_graph())
        hr_card.add_widget(Label(
            text="Heart Rate", 
            font_size='12sp', 
            color=get_color_from_hex("#AAAAAA"),
            size_hint_y=None, height=dp(15)
        ))
        
        # --- Blood Pressure Card (Right) ---
        bp_card = RoundedBoxLayout(orientation='vertical', padding=dp(10), radius=[dp(10)])
        bp_card.add_widget(Label(
            text="Blood Pressure", 
            font_size='12sp', 
            color=get_color_from_hex("#AAAAAA"),
            size_hint_y=None, height=dp(15),
            halign='left', text_size=(dp(150), None)
        ))
        bp_card.add_widget(self.create_bar_graph())
        
        grid.add_widget(hr_card)
        grid.add_widget(bp_card)
        section.add_widget(grid)
        return section

    # ------------------
    # --- LABS SECTION
    # ------------------
    def create_labs_section(self):
        section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        section.bind(minimum_height=section.setter('height'))

        section.add_widget(Label(
            text="Recent Lab Results",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(dp(350), None)
        ))

        # Mock Data
        labs = [
            ("Lorem ipsum dolor sit", "Crownhavas topmakes"),
            ("Lorem ipsum dolor sit", "Crownhavas topmakes"),
        ]

        for title, subtitle in labs:
            item = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
            
            icon_bg = RoundedBoxLayout(
                size_hint=(None, None), 
                size=(dp(40), dp(40)), 
                radius=[dp(20)], 
                background_color=get_color_from_hex("#E0EFFF")
            )
            icon_bg.add_widget(Label(
                text="+", 
                font_size='24sp', 
                color=get_color_from_hex("#3498DB")
            ))
            item.add_widget(icon_bg)
            
            item.add_widget(Label(
                text=f"{title}\n[size=12sp][color=888888]{subtitle}[/color][/size]",
                markup=True,
                halign='left',
                valign='middle',
                text_size=(dp(180), None),
                color=get_color_from_hex("#333333")
            ))
            
            item.add_widget(Label(
                text="FEI - 0.9%\n[size=10sp][color=888888]MMI 11.10.11[/color][/size]",
                markup=True,
                font_size='12sp',
                halign='right',
                valign='middle',
                text_size=(dp(100), None),
                color=get_color_from_hex("#555555")
            ))
            section.add_widget(item)

        return section

    # ------------------
    # --- GRAPH HELPERS
    # ------------------
    def create_line_graph(self):
        graph = Graph(
            xmin=0, xmax=100, ymin=0, ymax=100,
            x_grid=False, y_grid=False,
            draw_border=False,
            padding=0
        )
        plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        plot.points = [(0, 20), (50, 20), (100, 80)]
        graph.add_plot(plot)
        return graph

    def create_bar_graph(self):
        graph = Graph(
            xmin=0, xmax=100, ymin=0, ymax=100,
            x_grid=False, y_grid=False,
            draw_border=False,
            padding=0,
            y_ticks_major=50,
            x_ticks_major=25
        )
        plot = MeshStemPlot(color=get_color_from_hex("#3498DB"))
        plot.points = [(25, 30), (50, 80), (75, 50)]
        graph.add_plot(plot)
        return graph

# ------------------
# --- RUN THE APP
# ------------------
if __name__ == '__main__':
    PatientDashboardApp().run()