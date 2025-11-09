"""
Rally Voice Service - Converts navigation instructions to rally-style callouts
"""
import pyttsx3
import re
from typing import Dict


class RallyVoiceService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        
    def setup_voice(self):
        """Configure TTS engine for distressed/urgent rally co-driver delivery"""
        # Set properties for distressed, rapid-fire delivery
        # Higher rate = more panicked/urgent sound
        self.engine.setProperty('rate', 250)  # Very fast - distressed delivery
        self.engine.setProperty('volume', 1.0)  # Full volume
        
        # List all available voices
        voices = self.engine.getProperty('voices')
        print(f"\n🎙️ Available voices ({len(voices)}):")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} (ID: {voice.id})")
        
        # Try to find a male voice
        male_voice_found = False
        
        # Strategy 1: Look for specific male voice names
        male_names = ['david', 'mark', 'george', 'james', 'richard']
        for voice in voices:
            for name in male_names:
                if name in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    male_voice_found = True
                    print(f"\n✅ Selected voice: {voice.name}")
                    break
            if male_voice_found:
                break
        
        # Strategy 2: Look for "male" but not "female"
        if not male_voice_found:
            for voice in voices:
                name_lower = voice.name.lower()
                if 'male' in name_lower and 'female' not in name_lower:
                    self.engine.setProperty('voice', voice.id)
                    male_voice_found = True
                    print(f"\n✅ Selected voice: {voice.name}")
                    break
        
        # Strategy 3: On Windows, voice 0 is often male (David), voice 1 is female (Zira)
        if not male_voice_found and len(voices) > 0:
            # Try voice index 0 (often David on Windows)
            self.engine.setProperty('voice', voices[0].id)
            print(f"\n✅ Using default male voice: {voices[0].name}")
        
        if not male_voice_found:
            print("\n⚠️ Warning: Could not find male voice, using system default")
                
    def generate_rally_callout(self, instruction: Dict) -> str:
        """
        Convert Google Maps instruction to rally-style callout
        
        Args:
            instruction: Dict with 'instruction', 'distance', 'maneuver'
            
        Returns:
            Rally-style callout string
        """
        maneuver = instruction.get('maneuver', 'straight')
        distance = instruction.get('distance', 0)
        
        # Convert distance to meters
        distance_m = int(distance)
        
        # Classify turn severity based on maneuver type
        rally_call = self.classify_turn(maneuver)
        
        # Add distance callout
        if distance_m > 500:
            callout = f"{rally_call}, {distance_m} meters"
        elif distance_m > 100:
            callout = f"{rally_call}, {distance_m}"
        else:
            callout = f"{rally_call} now!"
            
        # Add special warnings
        if 'roundabout' in maneuver:
            callout = f"Roundabout ahead, {distance_m}"
            
        return callout
        
    def classify_turn(self, maneuver: str) -> str:
        """
        Classify turn type into rally terminology
        
        Rally scale:
        - Flat: Very gentle turn (< 30 degrees)
        - 1-6: Increasing severity
        - Hairpin: Very sharp turn (> 150 degrees)
        """
        maneuver = maneuver.lower()
        
        # Determine direction
        if 'left' in maneuver:
            direction = 'left'
        elif 'right' in maneuver:
            direction = 'right'
        else:
            return 'straight'
            
        # Determine severity with more urgent language
        if 'sharp' in maneuver or 'hairpin' in maneuver:
            return f"HAIRPIN {direction}!"
        elif 'slight' in maneuver:
            return f"Flat {direction}"
        elif 'turn' in maneuver:
            # Regular turn - medium severity
            return f"Three {direction}!"
        else:
            return f"Two {direction}"
            
    def speak(self, text: str, urgency: int = 1):
        """
        Speak the rally callout with appropriate urgency
        
        Args:
            text: Text to speak
            urgency: 1-3, affects speech rate
        """
        # Adjust rate based on urgency
        base_rate = 180
        rate = base_rate + (urgency * 20)
        self.engine.setProperty('rate', rate)
        
        # Speak
        self.engine.say(text)
        self.engine.runAndWait()
        
    def speak_async(self, text: str):
        """Speak without blocking"""
        import threading
        
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
            
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
