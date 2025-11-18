from kivy_garden.graph import Graph, LinePlot
from kivy.uix.screenmanager import Screen

class HomeDashboardScreen(Screen):
    def on_enter(self):
        graph = self.ids.health_graph
        
        # Remove existing plots if any
        graph.plots.clear()
        
        plot = LinePlot(line_width=2, color=[0, 0.8, 0, 1])
        plot.points = [(x, (x * 2 + 5) % 100) for x in range(40)]
        graph.add_plot(plot)
        
        # Update other widgets dynamically here 
        self.ids.appointments_card.value = "3"
        self.ids.reports_card.value = "7"
        self.ids.doctors_card.value = "2"
