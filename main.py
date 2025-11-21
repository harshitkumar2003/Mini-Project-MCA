from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.factory import Factory

from kivy_garden.graph import Graph, LinePlot

#! Import Screens to manage navigation between them 
from screens.splash import SplashScreen            #todo: animation code for splash screen
from screens.login import LoginSignupScreen        #todo: login and signup functionality
from screens.dashboard import HomeDashboardScreen  #todo: user dashboard after login
from screens.landing import LandingScreen          #todo: import landing screen
from screens.patient import PatientDashboard
from screens.doctor import DoctorDashboard

#! import admin screens
from screens.admin import (    #todo: admin panel for managing users
    HomeScreen,
    PatientListScreen,
    PatientAddScreen,
    DoctorListScreen,
    DoctorAddScreen
)


#! Output Screen Example: Mobile screen size (iPhone 14 approx)
#Window.size = (490, 600)  #! Width x Height in pixels

# Window.size = (250, 540)  #! Width x Height in pixels

#! Register custom widgets from kivy_garden
Factory.register('Graph', cls=Graph)
Factory.register('LinePlot', cls=LinePlot)


#! Load KV files (make sure they are inside kv/ folder)
Builder.load_file("kv/splash.kv")
Builder.load_file("kv/login.kv")
Builder.load_file("kv/dashboard.kv")
Builder.load_file("kv/landing.kv")
Builder.load_file("kv/admin.kv")
Builder.load_file("kv/patient.kv")
Builder.load_file("kv/doctor.kv")



#! Global background color (white)
Window.clearcolor = get_color_from_hex("#ffffff")

#! Screen Manager
class HealthcareApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LandingScreen(name="landing"))
        sm.add_widget(LoginSignupScreen(name="login"))
        sm.add_widget(HomeDashboardScreen(name="dashboard"))
        sm.add_widget(PatientDashboard(name="patient"))     
        sm.add_widget(DoctorDashboard(name="doctor"))

        #! Admin Screens (Danger Zone) - Access only for Admin Role -> 
        sm.add_widget(HomeScreen(name="admin"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PatientListScreen(name="patient_list"))
        sm.add_widget(PatientAddScreen(name="patient_add"))
        sm.add_widget(DoctorListScreen(name="doctor_list"))
        sm.add_widget(DoctorAddScreen(name="doctor_add"))
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    HealthcareApp().run()
