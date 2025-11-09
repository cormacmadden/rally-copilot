"""
Enhanced Rally Voice Service - Uses Google Cloud TTS for realistic voices
Falls back to pyttsx3 if Google Cloud is not configured
"""
import pyttsx3
import re
from typing import Dict
import os
from pathlib import Path
import tempfile

# Try to import Google Cloud TTS
try:
    from google.cloud import texttospeech
    from google.oauth2 import service_account
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False

# Try to import pygame for audio playback
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class EnhancedRallyVoiceService:
    def __init__(self, use_google_tts=True, google_api_key=None):
        """
        Initialize voice service
        
        Args:
            use_google_tts: Try to use Google Cloud TTS if available
            google_api_key: Path to Google Cloud service account JSON key
        """
        self.use_google_tts = use_google_tts and GOOGLE_TTS_AVAILABLE
        self.google_client = None
        
        # Try to initialize Google Cloud TTS
        if self.use_google_tts:
            try:
                if google_api_key and os.path.exists(google_api_key):
                    credentials = service_account.Credentials.from_service_account_file(google_api_key)
                    self.google_client = texttospeech.TextToSpeechClient(credentials=credentials)
                else:
                    # Try default credentials
                    self.google_client = texttospeech.TextToSpeechClient()
                
                print("✓ Using Google Cloud Text-to-Speech (Realistic neural voices)")
            except Exception as e:
                print(f"⚠ Google Cloud TTS not available: {e}")
                print("  Falling back to pyttsx3")
                self.use_google_tts = False
        
        # Fallback to pyttsx3
        if not self.use_google_tts:
            self.engine = pyttsx3.init()
            self.setup_pyttsx3_voice()
            print("Using pyttsx3 (System TTS)")
    
    def setup_pyttsx3_voice(self):
        """Configure pyttsx3 for urgent delivery"""
        self.engine.setProperty('rate', 250)
        self.engine.setProperty('volume', 1.0)
        
        voices = self.engine.getProperty('voices')
        print(f"\n🎙️ Available voices ({len(voices)}):")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name}")
        
        # Try to find male voice
        for voice in voices:
            if any(name in voice.name.lower() for name in ['david', 'mark', 'george']):
                self.engine.setProperty('voice', voice.id)
                print(f"\n✓ Selected: {voice.name}")
                return
        
        if voices:
            self.engine.setProperty('voice', voices[0].id)
            print(f"\n✓ Using: {voices[0].name}")
    
    def generate_rally_callout(self, instruction: Dict) -> str:
        """Convert navigation instruction to rally-style callout"""
        maneuver = instruction.get('maneuver', 'straight')
        distance = instruction.get('distance', 0)
        
        distance_m = int(distance)
        rally_call = self.classify_turn(maneuver)
        
        if distance_m > 500:
            callout = f"{rally_call}, {distance_m} meters"
        elif distance_m > 100:
            callout = f"{rally_call}, {distance_m}"
        else:
            callout = f"{rally_call} now!"
            
        if 'roundabout' in maneuver:
            callout = f"Roundabout ahead, {distance_m}"
            
        return callout
    
    def classify_turn(self, maneuver: str) -> str:
        """Classify turn into rally terminology"""
        maneuver = maneuver.lower()
        
        if 'left' in maneuver:
            direction = 'left'
        elif 'right' in maneuver:
            direction = 'right'
        else:
            return 'straight'
        
        if 'sharp' in maneuver or 'hairpin' in maneuver:
            return f"HAIRPIN {direction}!"
        elif 'slight' in maneuver:
            return f"Flat {direction}"
        elif 'turn' in maneuver:
            return f"Three {direction}!"
        else:
            return f"Two {direction}"
    
    def speak_google(self, text: str):
        """Speak using Google Cloud TTS (realistic voice)"""
        try:
            # Configure voice - British male for rally authenticity
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-GB",
                name="en-GB-Neural2-B",  # British male neural voice
                ssml_gender=texttospeech.SsmlGender.MALE
            )
            
            # Configure audio with faster speaking rate
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.5,  # 1.5x speed for urgency
                pitch=-2.0,  # Lower pitch for masculine sound
            )
            
            # Generate speech
            synthesis_input = texttospeech.SynthesisInput(text=text)
            response = self.google_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Play audio
            if PYGAME_AVAILABLE:
                # Save to temp file and play with pygame
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                    f.write(response.audio_content)
                    temp_path = f.name
                
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Cleanup
                os.unlink(temp_path)
            else:
                print(f"[Would speak]: {text}")
                
        except Exception as e:
            print(f"Error with Google TTS: {e}")
            # Fallback to pyttsx3
            if hasattr(self, 'engine'):
                self.engine.say(text)
                self.engine.runAndWait()
    
    def speak_pyttsx3(self, text: str):
        """Speak using pyttsx3 (system TTS)"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def speak(self, text: str, urgency: int = 1):
        """Speak text with appropriate urgency"""
        if self.use_google_tts and self.google_client:
            self.speak_google(text)
        else:
            self.speak_pyttsx3(text)
    
    def speak_async(self, text: str):
        """Speak without blocking"""
        import threading
        
        def speak_thread():
            self.speak(text)
            
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
