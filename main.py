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
from screens.doctor import DoctorDashboard, PatientDetailScreenWrapper

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
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition())
        
        # Add screens
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LandingScreen(name='landing'))
        
        # Initialize login screen first
        login_screen = LoginSignupScreen(name='login')
        sm.add_widget(login_screen)
        
        # Initialize dashboard screens
        dashboard = HomeDashboardScreen(name='dashboard')
        sm.add_widget(dashboard)
        
        # Initialize other screens
        sm.add_widget(PatientDashboard(name='patient_dashboard'))
        sm.add_widget(DoctorDashboard(name='doctor_dashboard'))
        
        # Create a placeholder for patient detail content
        from kivy.uix.label import Label
        placeholder_content = Label(text='Select a patient to view details',
                                 font_size=20,
                                 color=(0.5, 0.5, 0.5, 1))
        
        # Initialize the patient detail wrapper with the placeholder content
        sm.add_widget(PatientDetailScreenWrapper(
            name='patient_detail',
            dashboard_content=placeholder_content
        ))
        
        # Store reference to the patient detail screen for later updates
        self.patient_detail_screen = sm.get_screen('patient_detail')
        
        # Add admin screens
        sm.add_widget(HomeScreen(name='admin_home'))
        sm.add_widget(PatientListScreen(name='admin_patient_list'))
        sm.add_widget(PatientAddScreen(name='admin_patient_add'))
        sm.add_widget(DoctorListScreen(name='admin_doctor_list'))
        sm.add_widget(DoctorAddScreen(name='admin_doctor_add'))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PatientListScreen(name="patient_list"))
        sm.add_widget(PatientAddScreen(name="patient_add"))
        sm.add_widget(DoctorListScreen(name="doctor_list"))
        sm.add_widget(DoctorAddScreen(name="doctor_add"))
        
        # Store references to important screens
        self.dashboard = dashboard
        self.login_screen = login_screen
        
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    HealthcareApp().run()