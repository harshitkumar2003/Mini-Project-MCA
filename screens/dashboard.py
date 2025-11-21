from kivy.uix.screenmanager import Screen
from kivy_garden.graph import Graph, LinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty


class InfoCard(BoxLayout):
    title = StringProperty('')
    value = StringProperty('')
    icon_source = StringProperty('')


class ActivityItem(BoxLayout):
    icon = StringProperty('')
    text = StringProperty('')


class HomeDashboardScreen(Screen):
    def on_enter(self, *args):
        # Initialize health graph
        self.init_health_graph()
        
        # Update info cards
        self.update_info_cards()
    
    def init_health_graph(self):
        graph = self.ids.health_graph
        if graph.plots:
            graph.plots.clear()
        
        # Add sample data to the graph
        plot = LinePlot(line_width=2, color=[0.2, 0.6, 0.4, 1])
        plot.points = [(x, (x * 2 + 5) % 100) for x in range(30)]
        graph.add_plot(plot)
    
    def update_info_cards(self):
        # Update all info cards with sample data
        cards_data = {
            'appointments_card': '5',
            'reports_card': '12',
            'doctors_card': '7',
            'symptoms_card': '8',
            'medicines_card': '15',
            'diseases_card': '3'
        }
        
        for card_id, value in cards_data.items():
            if hasattr(self.ids, card_id):
                self.ids[card_id].value = value
