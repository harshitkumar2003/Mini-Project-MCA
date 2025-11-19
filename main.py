from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.factory import Factory

from kivy_garden.graph import Graph, LinePlot

#! Import Screens to manage navigation between them 
from screens.splash import SplashScreen          #todo: animation code for splash screen
from screens.login import LoginSignupScreen      #todo: login and signup functionality
from screens.dashboard import HomeDashboardScreen  #todo: user dashboard after login
#from screens.patient import PatientScreen
#from screens.doctor import DoctorScreen
#from screens.admin import AdminScreen

#! Output Screen Example: Mobile screen size (iPhone 14 approx)
#Window.size = (250, 540)  #! Width x Height in pixels

#! Register custom widgets from kivy_garden
Factory.register('Graph', cls=Graph)
Factory.register('LinePlot', cls=LinePlot)


#! Load KV files (make sure they are inside kv/ folder)
Builder.load_file("kv/splash.kv")
Builder.load_file("kv/login.kv")
Builder.load_file("kv/dashboard.kv")
#Builder.load_file("kv/patient.kv")
#Builder.load_file("kv/doctor.kv")
#Builder.load_file("kv/admin.kv")



#! Global background color (white)
Window.clearcolor = get_color_from_hex("#ffffff")

#! Screen Manager
class HealthcareApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginSignupScreen(name="login"))
        sm.add_widget(HomeDashboardScreen(name="dashboard"))
       # sm.add_widget(PatientScreen(name="patient"))
       # sm.add_widget(DoctorScreen(name="doctor"))
        #sm.add_widget(AdminScreen(name="admin"))
        return sm


if __name__ == "__main__":
    HealthcareApp().run()
