"""
Rally Copilot - Main Application Entry Point
A rally-style co-driver navigation app using Google Maps
"""
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.route_confirmation_screen import RouteConfirmationScreen
from screens.navigation_screen import NavigationScreen


class RallyCopilotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Rally Copilot"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        
    def build(self):
        """Build the application with screen manager"""
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RouteConfirmationScreen(name='confirmation'))
        sm.add_widget(NavigationScreen(name='navigation'))
        return sm


if __name__ == '__main__':
    RallyCopilotApp().run()
