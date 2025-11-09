"""
Route Confirmation Screen - Shows map preview and route details
"""
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from io import BytesIO
import staticmap
import tempfile


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
            text="ROUTE PREVIEW",
            halign="center",
            size_hint=(1, None),
            height=50,
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            font_size="24sp",
            bold=True
        )
        
        # Route info
        self.info_label = MDLabel(
            text="Loading route...",
            halign="center",
            size_hint=(1, None),
            height=60,
            font_size="14sp"
        )
        
        # Map preview
        self.map_image = Image(
            size_hint=(1, 0.6),
            allow_stretch=True
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
        layout.add_widget(self.map_image)
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
            self.info_label.text = f"{distance} - {duration}\nFrom: {start_addr}\nTo: {end_addr}"
        
        # Render map if UI is built
        if hasattr(self, 'map_image'):
            self.render_route_map(route_data)
        
    def render_route_map(self, route_data):
        """Render static map with route polyline"""
        try:
            # Create static map
            m = staticmap.StaticMap(600, 400, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
            
            # Extract polyline points
            points = []
            for leg in route_data['legs']:
                for step in leg['steps']:
                    start_loc = step['start_location']
                    end_loc = step['end_location']
                    points.append((start_loc['lng'], start_loc['lat']))
                    points.append((end_loc['lng'], end_loc['lat']))
            
            # Add line to map
            if points:
                line = staticmap.Line(points, 'red', 4)
                m.add_line(line)
                
                # Add start marker
                start_point = points[0]
                m.add_marker(staticmap.CircleMarker(start_point, 'green', 12))
                
                # Add end marker
                end_point = points[-1]
                m.add_marker(staticmap.CircleMarker(end_point, 'red', 12))
            
            # Render to image
            image_data = m.render()
            
            # Convert to Kivy image
            data = BytesIO()
            image_data.save(data, format='png')
            data.seek(0)
            
            core_image = CoreImage(BytesIO(data.read()), ext='png')
            self.map_image.texture = core_image.texture
            
        except Exception as e:
            print(f"Error rendering map: {e}")
            self.info_label.text += f"\n(Map preview unavailable)"
            
    def cancel_route(self, instance):
        """Cancel and go back to home"""
        self.manager.current = 'home'
        
    def confirm_route(self, instance):
        """Confirm route and start navigation"""
        if self.route_data:
            nav_screen = self.manager.get_screen('navigation')
            nav_screen.start_with_route(self.route_data)
            self.manager.current = 'navigation'
