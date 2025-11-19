import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import ColorProperty, ListProperty, StringProperty

# Garden Graph imports
try:
    from kivy_garden.graph import Graph, MeshLinePlot, MeshStemPlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Run: pip install kivy-garden && kivy garden install graph")
    exit(1)

kivy.require('2.1.0')

# Load patient.kv once; change path as appropriate
try:
    Builder.load_file("kv/patient.kv")
except FileNotFoundError:
    print("\nERROR: Could not find 'patient.kv'")
    exit(1)


class RoundedBoxLayout(BoxLayout):
    background_color = ColorProperty([1, 1, 1, 1])
    radius = ListProperty([dp(15)])


class PatientScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        black_color = get_color_from_hex("#000000")

        root_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # White bg rectangle for root
        with root_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=root_layout.size, pos=root_layout.pos)

        def update_rect(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        root_layout.bind(pos=update_rect, size=update_rect)

        # Title
        title = Label(
            text='Patient Dashboard',
            font_size='32sp',
            bold=True,
            size_hint=(1, 0.1),
            color=black_color
        )
        root_layout.add_widget(title)

        # Patient Info Grid
        info_layout = GridLayout(
            cols=2,
            size_hint=(1, 0.2),
            row_force_default=True,
            row_default_height=dp(40)
        )
        patient_data = {
            "Patient Name:": "Chetan Sharma",
            "Age:": "25",
            "Room:": "305B",
            "Condition:": "Stable (Post-Op)"
        }
        for key, value in patient_data.items():
            info_layout.add_widget(Label(text=key, font_size='18sp', bold=True, halign='right', padding=[dp(20), 0], color=black_color))
            info_layout.add_widget(Label(text=value, font_size='18sp', halign='left', padding=[dp(20), 0], color=black_color))
        root_layout.add_widget(info_layout)

        # Current Vitals label
        vitals_title = Label(text='Current Vitals', font_size='24sp', bold=True, size_hint=(1, 0.1), color=black_color)
        root_layout.add_widget(vitals_title)

        # Vital boxes grid 2x2
        vitals_layout = GridLayout(cols=2, size_hint=(1, 0.2), spacing=dp(10))

        def create_vital_box(name, value, unit, hex_color):
            box = BoxLayout(orientation='vertical')

            def update_box_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size

            with box.canvas.before:
                Color(rgb=get_color_from_hex(hex_color))
                box.rect = Rectangle(pos=box.pos, size=box.size, radius=[dp(10)])

            white_color = get_color_from_hex("#FFFFFF")

            box.add_widget(Label(text=name, font_size='20sp', bold=True, color=white_color))
            box.add_widget(Label(text=value, font_size='28sp', bold=True, color=white_color))
            box.add_widget(Label(text=unit, font_size='16sp', color=white_color))
            box.bind(pos=update_box_rect, size=update_box_rect)
            return box

        vitals_layout.add_widget(create_vital_box("Heart Rate", "78", "bpm", "#F1250E"))
        vitals_layout.add_widget(create_vital_box("Blood Pressure", "122/81", "mmHg", "#2097E7"))
        vitals_layout.add_widget(create_vital_box("SpO2", "97", "%", "#21EB75"))
        vitals_layout.add_widget(create_vital_box("Temperature", "98.4", "°F", "#E6920D"))

        root_layout.add_widget(vitals_layout)

        # Graph section label
        graph_title = Label(text='Vitals Trend (Last 12 Hours)', font_size='24sp', bold=True, size_hint=(1, 0.1), color=black_color)
        root_layout.add_widget(graph_title)

        # Graph container placeholder to add the graph dynamically
        from kivy.uix.boxlayout import BoxLayout
        self.graph_container = BoxLayout(size_hint=(1, 0.4))
        root_layout.add_widget(self.graph_container)

        # Add root layout to the screen
        self.add_widget(root_layout)

    def on_enter(self):
        # Called whenever screen is entered; refresh graph dynamically
        self.graph_container.clear_widgets()

        graph = Graph(
            xlabel='Hour',
            ylabel='Value',
            x_ticks_minor=1,
            x_ticks_major=2,
            y_ticks_major=20,
            y_grid=True,
            x_grid=True,
            xmin=0,
            xmax=11,
            ymin=60,
            ymax=140,
            padding=dp(5),
            label_options={'color': get_color_from_hex("#000000")},
            tick_color=get_color_from_hex("#CCCCCC")
        )

        heart_rate_data = [(0, 75), (1, 78), (2, 80), (3, 79), (4, 76), (5, 75), (6, 77), (7, 78), (8, 82), (9, 80), (10, 78), (11, 78)]
        blood_pressure_data = [(0, 120), (1, 122), (2, 125), (3, 124), (4, 121), (5, 120), (6, 121), (7, 122), (8, 128), (9, 126), (10, 124), (11, 122)]

        hr_plot = MeshLinePlot(color=get_color_from_hex("#E74C3C"))
        hr_plot.points = heart_rate_data
        graph.add_plot(hr_plot)

        bp_plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        bp_plot.points = blood_pressure_data
        graph.add_plot(bp_plot)

        self.graph_container.add_widget(graph)
