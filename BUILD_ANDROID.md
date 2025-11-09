# Building Android APK

Due to threading limitations in Docker on Windows, the recommended approach is to use WSL2 (Windows Subsystem for Linux).

## Option 1: Using WSL2 (Recommended)

### Prerequisites
1. Install WSL2 with Ubuntu:
   ```powershell
   wsl --install
   ```

2. Open WSL Ubuntu terminal and navigate to your project:
   ```bash
   cd /mnt/d/Personal/Coding/cockpit-copilot
   ```

3. Install buildozer dependencies:
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   pip3 install --user --upgrade buildozer cython
   ```

4. Build the APK:
   ```bash
   buildozer -v android debug
   ```

   This will take 15-30 minutes on first run as it downloads:
   - Android SDK
   - Android NDK
   - Python-for-Android

5. The APK will be in `bin/rallycopilot-0.1-debug.apk`

### Transfer to Phone
- USB: Connect phone, enable file transfer, copy APK
- Email: Email the APK to yourself
- Cloud: Upload to Google Drive/Dropbox

## Option 2: Using GitHub Actions (Alternative)

If WSL doesn't work, you can use GitHub Actions to build the APK in the cloud:

1. Create `.github/workflows/build-android.yml`:
```yaml
name: Build Android APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          pip install --upgrade buildozer cython
      
      - name: Build APK
        run: buildozer -v android debug
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: rally-copilot-apk
          path: bin/*.apk
```

2. Push to GitHub
3. Go to Actions tab → Build Android APK → Run workflow
4. Download the APK from the workflow artifacts

## Option 3: Online Build Services

- **Replit**: Create a Repl, upload files, run `buildozer android debug`
- **Gitpod**: Open workspace, install buildozer, build APK

## Testing on Android

1. Install the APK on your phone
2. Enable "Install from Unknown Sources" in Settings
3. Launch "Rally Copilot"
4. Grant location permissions
5. Enter destination and test

### Expected Voice Behavior
- Android has native TTS with better male voices than Windows
- Go to Settings → Accessibility → Text-to-speech to configure
- Recommended: Google Text-to-speech with British English (en-GB)
- Voice will speak at 2.5x normal speed for urgency

## Troubleshooting

### "Build failed"
- Check you have at least 10GB free disk space
- Ensure Java 17 is installed: `java -version`

### "Permission denied"
- Make buildozer executable: `chmod +x $(which buildozer)`

### "No space left on device"
- Clean buildozer cache: `rm -rf .buildozer`
- Try again

### Voice issues on Android
- Install "Google Text-to-speech" from Play Store
- Go to Settings → System → Languages → Text-to-speech
- Select "Google Text-to-speech Engine"
- Download "English (UK)" voice data
