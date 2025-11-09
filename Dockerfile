FROM kivy/buildozer:latest

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Set environment variable to allow buildozer to run as root
ENV BUILDOZER_WARN_ON_ROOT=0

# Build the APK
CMD ["buildozer", "-v", "android", "debug"]
