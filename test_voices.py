"""
Test script to compare voice options
Run this to hear the difference between system TTS and Google Cloud TTS
"""
from services.rally_voice_service import RallyVoiceService
from services.enhanced_rally_voice_service import EnhancedRallyVoiceService

print("=" * 60)
print("RALLY COPILOT - Voice Comparison Test")
print("=" * 60)

# Test instruction
test_instruction = {
    'maneuver': 'turn-sharp-right',
    'distance': 150
}

print("\n1. Testing System TTS (pyttsx3)...")
print("-" * 60)
system_voice = RallyVoiceService()
callout = system_voice.generate_rally_callout(test_instruction)
print(f"Callout: {callout}")
system_voice.speak(callout)

print("\n2. Testing Enhanced Service (Google Cloud TTS if available)...")
print("-" * 60)
enhanced_voice = EnhancedRallyVoiceService(use_google_tts=True)
callout = enhanced_voice.generate_rally_callout(test_instruction)
print(f"Callout: {callout}")
enhanced_voice.speak(callout)

print("\n" + "=" * 60)
print("Test complete!")
print("\nFor best quality:")
print("  • Set up Google Cloud TTS (see README.md)")
print("  • Use enhanced_rally_voice_service.py")
print("  • On Android: Install 'Google Text-to-speech'")
print("=" * 60)
