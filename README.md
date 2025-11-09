# Rally Copilot 🏁

A rally-style co-driver navigation app that transforms standard GPS directions into exciting rally pace notes!

## Features

- 🗺️ Google Maps integration for accurate routing
- 🎙️ Rally-style voice callouts (e.g., "Hard right 200 meters!")
- 📱 Cross-platform (iOS & Android via Python/Kivy)
- 🔄 Automatic rerouting on wrong turns
- 📍 Real-time GPS tracking

## How It Works

Instead of boring "Turn right in 500 feet," you'll hear:
- "Three right, 150 meters"
- "Hairpin left now!"
- "Flat right, don't cut"

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Maps API key ([Get one here](https://developers.google.com/maps/documentation/directions/get-api-key))

### Installation

1. **Clone the repository**
```bash
cd cockpit-copilot
```

2. **Create virtual environment** (if not already created)
```bash
python -m venv .venv
```

3. **Activate virtual environment**

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:
```cmd
.venv\Scripts\activate.bat
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure Google Maps API Key**

Open `services/navigation_service.py` and replace:
```python
self.google_maps_api_key = "YOUR_GOOGLE_MAPS_API_KEY"
```
with your actual API key.

### Running on Desktop (Testing)

```bash
python main.py
```

### Building for Mobile

#### Android

1. **Install Buildozer dependencies** (Linux/Mac or WSL on Windows)

2. **Initialize buildozer**
```bash
buildozer init
```

3. **Build APK**
```bash
buildozer -v android debug
```

4. **Install on device**
```bash
buildozer android deploy run
```

#### iOS (Mac only)

1. **Install kivy-ios**
```bash
toolchain build kivy
```

2. **Create Xcode project**
```bash
toolchain create RallyCopilot .
```

3. **Open in Xcode and build**

## Project Structure

```
cockpit-copilot/
├── main.py                          # Application entry point
├── screens/
│   ├── home_screen.py              # Destination input screen
│   └── navigation_screen.py        # Active navigation screen
├── services/
│   ├── navigation_service.py       # Google Maps integration
│   └── rally_voice_service.py      # Rally callout generation & TTS
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Rally Terminology

The app uses authentic rally pace note terminology:

- **Flat**: Very gentle turn (< 30°)
- **1-6**: Turn severity scale
- **Hairpin**: Very sharp turn (> 150°)
- **Don't cut**: Warning about inside of corner
- **Crest**: Hill peak ahead
- **Tightens**: Turn gets sharper

## Configuration

### Voice Options

The app supports two TTS engines:

**1. Google Cloud Text-to-Speech (Recommended - Realistic Neural Voices)**
- High-quality, natural-sounding British male voice
- Requires Google Cloud account (free tier available)
- Perfect for authentic rally co-driver experience
- Set up: See "Google Cloud TTS Setup" section below

**2. System TTS (pyttsx3 - Fallback)**
- Uses Windows/Android built-in voices
- Free, no API required
- Quality varies by platform
- Works offline

To switch to Google Cloud TTS, update `screens/navigation_screen.py`:
```python
from services.enhanced_rally_voice_service import EnhancedRallyVoiceService
self.voice_service = EnhancedRallyVoiceService(use_google_tts=True)
```

### Voice Settings

Edit voice service file:
- `rate` / `speaking_rate`: Speech speed (1.0-2.0 for Google, 180-300 for pyttsx3)
- `pitch`: Voice pitch (-20 to +20, lower = more masculine)
- `volume`: Volume level (0.0 - 1.0)

### Distance Callouts

Modify thresholds in `generate_rally_callout()`:
- `> 500m`: Full distance callout
- `100-500m`: Short callout
- `< 100m`: "Now!" callout

## Known Limitations

- **Desktop Testing**: GPS simulation needed for desktop testing
- **API Costs**: Google Maps API has usage limits/costs
- **TTS Quality**: System TTS may vary by platform
- **Background Mode**: Mobile OS restrictions may limit background operation
- **Voice Gender**: By default, Windows may only have female TTS voices installed

### Installing Male TTS Voices (Windows)

To get a proper male co-driver voice:

1. Open **Settings** > **Time & Language** > **Speech**
2. Click **Manage voices** or **Add voices**
3. Download additional voices (look for: David, Mark, or George)
4. Restart the app

Alternatively, on Windows 10/11:
1. **Settings** > **Accessibility** > **Narrator** > **Narrator voice**
2. Install "Microsoft David" or other male voices

The app will automatically detect and use male voices if available.

### Android Voice Options

On Android, the app uses **Android TTS** (via plyer/pyttsx3):

- **Default**: Google TTS (usually high quality)
- **Available voices**: Depends on Android version and language packs installed
- **To change**: Android Settings > System > Languages & input > Text-to-speech output
- **Recommended**: Install "Google Text-to-speech" from Play Store for best quality

Android typically has better default voices than Windows. The British English voice on Android is often quite good for the rally co-driver effect.

### Google Cloud TTS Setup (Optional - Best Quality)

For the most realistic rally co-driver voice:

1. **Create Google Cloud account** (free tier includes 1 million characters/month)
2. **Enable Text-to-Speech API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Enable "Cloud Text-to-Speech API"
3. **Create service account key**:
   - IAM & Admin > Service Accounts > Create
   - Grant "Text-to-Speech User" role
   - Create JSON key, download to project folder
4. **Set environment variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```
5. **Update code to use enhanced service** (see Voice Options above)

**Available realistic voices:**
- `en-GB-Neural2-B` - British male (recommended for rally)
- `en-GB-Neural2-D` - British male (alternative)
- `en-US-Neural2-D` - American male
- `en-AU-Neural2-B` - Australian male

## Future Enhancements

- [ ] Custom voice packs (famous co-drivers)
- [ ] Elevation analysis (crests, jumps, dips)
- [ ] Community pace notes
- [ ] Route recording and sharing
- [ ] Different rally styles (WRC, Dakar, etc.)
- [ ] CarPlay/Android Auto integration

## Contributing

Pull requests welcome! Please test on both Android and iOS if possible.

## License

MIT License - Feel free to modify and use!

## Disclaimer

⚠️ **This app is for entertainment purposes. Always drive safely and obey traffic laws.** Do not attempt rally-style driving on public roads.

## Support

For issues or questions, please open a GitHub issue.

---

**Made with ❤️ for rally enthusiasts**
