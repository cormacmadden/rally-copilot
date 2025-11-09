"""
Route Confirmation Screen - Shows route details
"""
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class RouteConfirmationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route_data = None
        
    def on_enter(self):
        """Build UI when screen is entered"""
        self.clear_widgets()
        self.build_ui()
        
        # Update route info if already set
        if self.route_data:
            self.set_route(self.route_data)
        
    def build_ui(self):
        """Build the route confirmation screen UI"""
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(1, 1)
        )
        
        # Header
        header = MDLabel(
            text="ROUTE CONFIRMATION",
            halign="center",
            size_hint=(1, None),
            height=50,
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            font_size="24sp",
            bold=True
        )
        
        # Route details
        self.info_label = MDLabel(
            text="Loading route...",
            halign="center",
            valign="top",
            size_hint=(1, 1),
            font_size="16sp",
            markup=True
        )
        
        # Buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint=(1, None),
            height=60
        )
        
        cancel_button = Button(
            text="CANCEL",
            size_hint=(0.4, 1),
            background_color=(0.5, 0.5, 0.5, 1),
            font_size="16sp",
            bold=True
        )
        cancel_button.bind(on_release=self.cancel_route)
        
        confirm_button = Button(
            text="START RALLY!",
            size_hint=(0.6, 1),
            background_color=(0.8, 0, 0, 1),
            font_size="18sp",
            bold=True
        )
        confirm_button.bind(on_release=self.confirm_route)
        
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(confirm_button)
        
        layout.add_widget(header)
        layout.add_widget(self.info_label)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
        
    def set_route(self, route_data):
        """Set route data and render map preview"""
        self.route_data = route_data
        
        if not route_data:
            if hasattr(self, 'info_label'):
                self.info_label.text = "No route available"
            return
            
        # Extract route info
        leg = route_data['legs'][0]
        distance = leg['distance']['text']
        duration = leg['duration']['text']
        start_addr = leg['start_address']
        end_addr = leg['end_address']
        
        # Update info label if UI is built
        if hasattr(self, 'info_label'):
            self.info_label.text = (
                f"[b][size=20sp][color=ff0000]RALLY MODE READY[/color][/size][/b]\n\n"
                f"[b]Distance:[/b] {distance}\n"
                f"[b]Duration:[/b] {duration}\n\n"
                f"[b]From:[/b]\n{start_addr}\n\n"
                f"[b]To:[/b]\n{end_addr}"
            )
            
    def cancel_route(self, instance):
        """Cancel and go back to home"""
        self.manager.current = 'home'
        
    def confirm_route(self, instance):
        """Confirm route and start navigation"""
        if self.route_data:
            nav_screen = self.manager.get_screen('navigation')
            nav_screen.start_with_route(self.route_data)
            self.manager.current = 'navigation'
