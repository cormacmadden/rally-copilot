"""
Navigation Screen - Map display and active navigation
"""
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from services.navigation_service import NavigationService
from services.rally_voice_service import RallyVoiceService


class NavigationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.navigation_service = NavigationService()
        self.voice_service = RallyVoiceService()
        self.destination = None
        
    def on_enter(self):
        """Build UI when screen is entered"""
        if not self.children:
            self.build_ui()
        
    def build_ui(self):
        """Build the navigation screen UI"""
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint=(1, 1)
        )
        
        # Header
        header = MDLabel(
            text="NAVIGATING",
            halign="center",
            size_hint=(1, None),
            height=60,
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            font_size="28sp",
            bold=True
        )
        
        # Map placeholder
        self.map_label = MDLabel(
            text="[MAP VIEW]\n\nGoogle Maps integration",
            halign="center",
            valign="center",
            size_hint=(1, 0.5),
            theme_text_color="Secondary",
            font_size="18sp"
        )
        
        # Status/instruction display
        self.status_label = MDLabel(
            text="Ready to navigate...",
            halign="center",
            valign="top",
            size_hint=(1, 0.3),
            theme_text_color="Primary",
            font_size="24sp",
            bold=True
        )
        
        # Back button
        back_button = Button(
            text="← BACK TO HOME",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5},
            background_color=(0.3, 0.3, 0.3, 1),
            font_size="14sp"
        )
        back_button.bind(on_release=self.go_back)
        
        layout.add_widget(header)
        layout.add_widget(self.map_label)
        layout.add_widget(self.status_label)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
        
    def go_back(self, instance):
        """Go back to home screen"""
        self.navigation_service.stop_navigation()
        self.manager.current = 'home'
        
    def set_destination(self, destination):
        """Set destination and start navigation (legacy method)"""
        self.destination = destination
        
        # Update status if UI is built
        if hasattr(self, 'status_label'):
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'text', f"Navigating to:\n{destination}")
            )
        
        # Start navigation service
        self.navigation_service.start_navigation(
            destination=destination,
            on_instruction=self.handle_instruction
        )
        
    def start_with_route(self, route_data):
        """Start navigation with pre-fetched route"""
        # Extract route data
        self.navigation_service.current_route = route_data
        self.navigation_service.extract_waypoints(route_data)
        
        # Update UI
        leg = route_data['legs'][0]
        destination = leg['end_address']
        
        if hasattr(self, 'status_label'):
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'text', f"Navigating to:\n{destination}")
            )
        
        # Start GPS tracking and simulation
        self.navigation_service.instruction_callback = self.handle_instruction
        self.navigation_service.is_navigating = True
        self.navigation_service.start_gps_tracking()
        
        # Simulate navigation on desktop
        from services.navigation_service import IS_MOBILE
        if not IS_MOBILE and self.navigation_service.waypoints:
            self.navigation_service.simulate_navigation()
        
    def handle_instruction(self, instruction):
        """Handle navigation instruction from service"""
        # Convert to rally callout
        rally_callout = self.voice_service.generate_rally_callout(instruction)
        
        # Update status (from main thread) if UI exists
        if hasattr(self, 'status_label'):
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'text', f">> {rally_callout}")
            )
        
        # Speak the callout (async)
        self.voice_service.speak_async(rally_callout)
