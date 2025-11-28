from kivy.uix.screenmanager import Screen

class LandingScreen(Screen):
    # ... (other init/methods if any)

    def select_role(self, role_name):
        """
        Landing card se role select karke Login screen par bhejta hai.
        """  
        login_screen = self.manager.get_screen('login')
        # 2. LoginSignupScreen par ek nayi property (e.g., selected_role) banayenge 
        login_screen.selected_role = role_name
        
        # 3. Login Screen par switch karein
        self.manager.current = 'login' 