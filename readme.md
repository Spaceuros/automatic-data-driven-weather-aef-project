# Data-Driven Broadcast Weather Graphics

An automated pipeline that fetches live weather data via an API, updates an Adobe After Effects project, and performs a headless background render to output a zipped PNG sequence with an Alpha channel, ready for live broadcast.

## Features
* Automated Data Fetching: A Python script fetches current weather data for various cities using WeatherAPI.
* Data-Driven Design: The generated JSON file directly drives the After Effects compositions via Expressions, updating both temperatures and weather icons automatically.
* Headless Rendering: The script utilizes `aerender` to process the AE composition in the background without opening the user interface.
* Auto-Archiving: The rendered PNG sequence is automatically zipped and the raw files are cleaned up, leaving you with a broadcast-ready file in about 60 seconds.

## Prerequisites
1. Python 3.x installed.
2. Adobe After Effects installed (The script uses the 2026 version path by default; adjust if necessary).
3. Font Requirement: Ensure you have "Gotham Rounded (Bold)" installed on your system to prevent layout issues in After Effects.
4. Weather API Key: Obtain a free API key from weatherapi.com.

## Setup Instructions
1. Clone this repository.
2. Open `weather_data.py` in a text editor.
3. Locate `API_KEY = "YOUR_API_KEY_HERE"` and replace it with your actual WeatherAPI key.
4. If you are on Windows, update the `AERENDER_PATH` variable to point to your `aerender.exe` (e.g., `C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe`).

## How to Run
Execute the Python script from your terminal:
```bash
python3 weather_data.py
