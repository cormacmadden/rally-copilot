"""
Home Screen - Destination input and app configuration
"""
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_enter(self):
        """Build UI when screen is entered"""
        if not self.children:
            self.build_ui()
        
    def build_ui(self):
        """Build the home screen UI"""
        # Main layout with padding
        layout = BoxLayout(
            orientation='vertical',
            padding=[40, 60, 40, 60],
            spacing=30,
            size_hint=(1, 1)
        )
        
        # Title
        title = MDLabel(
            text="RALLY COPILOT",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=80,
            font_size="36sp",
            bold=True
        )
        
        # Subtitle
        subtitle = MDLabel(
            text="Navigate with rally-style pace notes",
            halign="center",
            theme_text_color="Secondary",
            size_hint=(1, None),
            height=40,
            font_size="16sp"
        )
        
        # Spacer
        spacer1 = BoxLayout(size_hint=(1, 0.3))
        
        # Destination input
        self.destination_input = MDTextField(
            hint_text="Enter destination (e.g., 'Warwick University')",
            mode="filled",
            size_hint=(1, None),
            height=60,
            font_size="18sp",
            text="Warwick University"  # Default destination
        )
        
        # Example text
        example = MDLabel(
            text="Examples: 'Warwick University' - 'Coventry' - 'Birmingham'",
            halign="center",
            theme_text_color="Hint",
            size_hint=(1, None),
            height=30,
            font_size="12sp"
        )
        
        # Spacer
        spacer2 = BoxLayout(size_hint=(1, 0.2))
        
        # Start navigation button (using standard Kivy button for compatibility)
        start_button = Button(
            text="START RALLY MODE",
            size_hint=(0.8, None),
            height=60,
            pos_hint={'center_x': 0.5},
            background_color=(0.8, 0, 0, 1),
            font_size="18sp",
            bold=True
        )
        start_button.bind(on_release=self.start_navigation)
        
        # Add all widgets
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(spacer1)
        layout.add_widget(self.destination_input)
        layout.add_widget(example)
        layout.add_widget(spacer2)
        layout.add_widget(start_button)
        
        self.add_widget(layout)
        
    def start_navigation(self, instance):
        """Handle start navigation button press"""
        destination = self.destination_input.text
        if destination:
            # Fetch route and show confirmation screen
            from services.navigation_service import NavigationService
            nav_service = NavigationService()
            route = nav_service.get_route(destination)
            
            if route:
                # Show confirmation screen with route
                confirmation_screen = self.manager.get_screen('confirmation')
                confirmation_screen.set_route(route)
                self.manager.current = 'confirmation'
            else:
                # Show error (route fetch failed)
                print("Failed to get route")
