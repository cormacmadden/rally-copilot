"""
Navigation Service - Handles Google Maps routing and real-time navigation
"""
import urllib.request
import urllib.parse
import json
from typing import Callable, Dict, List, Optional
import threading
import time
import platform

# Only import GPS on mobile platforms
IS_MOBILE = platform.system() not in ['Windows', 'Darwin', 'Linux']
if IS_MOBILE:
    from plyer import gps


class NavigationService:
    def __init__(self):
        self.google_maps_api_key = "AIzaSyB7X7k7YDpGsbFlREN4mFHF71eEuiXgaMs"  # TODO: Replace with actual key
        self.current_route = None
        self.current_position = None
        self.waypoints = []
        self.is_navigating = False
        self.instruction_callback = None
        
    def start_navigation(self, destination: str, on_instruction: Callable):
        """Start navigation to destination"""
        self.instruction_callback = on_instruction
        self.is_navigating = True
        
        # Get route from Google Maps Directions API
        self.get_route(destination)
        
        # Start GPS tracking
        self.start_gps_tracking()
        
        # On desktop, simulate some instructions for testing
        if not IS_MOBILE and self.waypoints:
            self.simulate_navigation()
        
    def get_route(self, destination: str, origin: str = None):
        """Fetch route from Google Maps Directions API"""
        # Use provided origin or simulate for desktop testing
        if not origin:
            if IS_MOBILE and self.current_position:
                origin = f"{self.current_position['lat']},{self.current_position['lon']}"
            else:
                # Default test location (Beauchamp Ave, Leamington Spa)
                origin = "Beauchamp Ave, Leamington Spa, UK"
                print(f"Desktop mode: Using test origin: {origin}")
        
        params = {
            "origin": origin,
            "destination": destination,
            "key": self.google_maps_api_key,
            "mode": "driving"
        }
        
        url = "https://maps.googleapis.com/maps/api/directions/json?" + urllib.parse.urlencode(params)
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            if data['status'] == 'OK':
                route = data['routes'][0]
                self.current_route = route
                self.extract_waypoints(route)
                
                # Print route summary
                leg = route['legs'][0]
                print(f"✅ Route found: {leg['distance']['text']}, {leg['duration']['text']}")
                print(f"   From: {leg['start_address']}")
                print(f"   To: {leg['end_address']}")
                print(f"   Steps: {len(self.waypoints)} waypoints")
                
                return route
            else:
                error_msg = {
                    'ZERO_RESULTS': f"❌ No route found to '{destination}'. Try being more specific (e.g., 'Times Square, NY' or 'Boston, MA')",
                    'NOT_FOUND': "❌ Location not found. Check your destination.",
                    'INVALID_REQUEST': "❌ Invalid request. Check your input.",
                    'OVER_QUERY_LIMIT': "❌ API quota exceeded.",
                    'REQUEST_DENIED': "❌ API key issue. Check your Google Maps API key.",
                }.get(data['status'], f"❌ Error: {data['status']}")
                
                print(error_msg)
                return None
                
        except Exception as e:
            print(f"❌ Error fetching route: {e}")
            return None
            
    def extract_waypoints(self, route: Dict):
        """Extract waypoints and instructions from route"""
        self.waypoints = []
        
        for leg in route['legs']:
            for step in leg['steps']:
                waypoint = {
                    'location': step['end_location'],
                    'instruction': step['html_instructions'],
                    'distance': step['distance']['value'],
                    'duration': step['duration']['value'],
                    'maneuver': step.get('maneuver', 'straight')
                }
                self.waypoints.append(waypoint)
                
    def start_gps_tracking(self):
        """Start GPS tracking in background thread"""
        if not IS_MOBILE:
            print("Desktop mode: GPS tracking disabled (mobile only)")
            # Simulate being at Beauchamp Ave, Leamington Spa
            self.current_position = {'lat': 52.2855, 'lon': -1.5373}
            return
            
        def gps_loop():
            try:
                gps.configure(on_location=self.on_location_update)
                gps.start()
                
                while self.is_navigating:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"GPS error: {e}")
                
        thread = threading.Thread(target=gps_loop, daemon=True)
        thread.start()
        
    def on_location_update(self, **kwargs):
        """Handle GPS location updates"""
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        
        if lat and lon:
            self.current_position = {'lat': lat, 'lon': lon}
            self.check_waypoints()
            
    def check_waypoints(self):
        """Check if we're approaching any waypoints"""
        if not self.current_position or not self.waypoints:
            return
            
        # Check distance to next waypoint
        next_waypoint = self.waypoints[0]
        distance = self.calculate_distance(
            self.current_position,
            next_waypoint['location']
        )
        
        # Trigger instruction when within 200m
        if distance < 200 and self.instruction_callback:
            self.instruction_callback(next_waypoint)
            
    def calculate_distance(self, pos1: Dict, pos2: Dict) -> float:
        """Calculate distance between two points in meters"""
        # Haversine formula
        from math import radians, cos, sin, asin, sqrt
        
        lat1, lon1 = radians(pos1['lat']), radians(pos1['lon'])
        lat2, lon2 = radians(pos2['lat']), radians(pos2['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radius of earth in meters
        r = 6371000
        
        return c * r
        
    def simulate_navigation(self):
        """Simulate navigation instructions for desktop testing"""
        def simulate():
            print("\n🏁 Desktop Testing Mode: Simulating rally callouts...")
            time.sleep(2)
            
            # Play first few instructions
            for i, waypoint in enumerate(self.waypoints[:5]):
                if not self.is_navigating:
                    break
                    
                if self.instruction_callback:
                    print(f"\n[Waypoint {i+1}/{len(self.waypoints)}]")
                    self.instruction_callback(waypoint)
                    
                # Wait before next instruction (simulate driving)
                time.sleep(5)
                
        thread = threading.Thread(target=simulate, daemon=True)
        thread.start()
        
    def stop_navigation(self):
        """Stop navigation"""
        self.is_navigating = False
        if IS_MOBILE:
            try:
                gps.stop()
            except:
                pass
