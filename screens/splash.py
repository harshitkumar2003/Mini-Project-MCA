from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock

LOGO_FILE = "assets/logo.png"

class SplashScreen(Screen):
    def on_enter(self):
        # FloatLayout for free positioning
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Logo - bigger initial size
        self.logo = Image(
            source=LOGO_FILE,
            size_hint=(None, None),
            size=(250, 250),         # bigger starting size
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.logo)

        # Animation: fade + zoom + move up
        anim = Animation(
            opacity=1,
            size=(400, 400),                # zoom bigger
            y=self.logo.y + 150,            # slide up
            duration=4,
            t='out_elastic'
        )
        anim.start(self.logo)

        # Switch to login after animation
        Clock.schedule_once(self.switch_to_next, 3)

    def switch_to_next(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'landing'
