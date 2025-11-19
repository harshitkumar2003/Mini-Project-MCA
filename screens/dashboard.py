from kivy.uix.screenmanager import Screen
from kivy_garden.graph import Graph, LinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class InfoCard(BoxLayout):
    title = StringProperty('')
    value = StringProperty('')
    icon_source = StringProperty('')


class HomeDashboardScreen(Screen):
    def on_enter(self):
        graph = self.ids.health_graph
        
        # Clear existing plots
        graph.plots.clear()
        
        plot = LinePlot(line_width=2, color=[0, 0.8, 0, 1])
        plot.points = [(x, (x * 2 + 5) % 100) for x in range(40)]
        graph.add_plot(plot)
        
        # Update info cards dynamically
        self.ids.appointments_card.value = "7"
        self.ids.reports_card.value = "15"
        self.ids.doctors_card.value = "4"
        self.ids.new_disease_card.value = "2"
