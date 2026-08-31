#!/usr/bin/env python3
import requests
import json
import subprocess
import os
import shutil

# Replace with your own WeatherAPI key
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# City list - Keys are used in After Effects, values are search queries
cities = {
    "BEOGRAD": "Belgrade, Serbia",
    "NOVI SAD": "Novi Sad, Serbia",
    "KRAGUJEVAC": "Kragujevac, Serbia",
    "NIS": "Nis, Serbia",
    "SABAC": "Sabac, Serbia",
    "ZRENJANIN": "Zrenjanin, Serbia",
    "KRUSEVAC": "Krusevac, Serbia",
    "K MITROVICA": "Kosovska Mitrovica, Serbia",
    "ZAJECAR": "Zajecar, Serbia",
    "SOMBOR": "Sombor, Serbia",
    "UZICE": "Uzice, Serbia",
    "VALJEVO": "Valjevo, Serbia",
    "SUBOTICA": "Subotica, Serbia",
    "NEGOTIN": "Negotin, Serbia",
    "LESKOVAC": "Leskovac, Serbia",
    "VRANJE": "Vranje, Serbia",
    "LOZNICA": "Loznica, Serbia",
    "CACAK": "Cacak, Serbia",
    "NOVI PAZAR": "Novi Pazar, Serbia",
    "PIROT": "Pirot, Serbia",
    "KRALJEVO": "Kraljevo, Serbia",
    "SJENICA": "Sjenica, Serbia",
    "KOPAONIK": "Kopaonik, Serbia",
    "ZLATIBOR": "Zlatibor, Serbia"
}

# Values remain in Serbian as they are directly linked to AE Expressions
weather_conditions = {
    "Sunce": [1000],
    "Sunce-oblaci": [1003],
    "Oblaci": [1006, 1009, 1030, 1135, 1147, 1063, 1066, 1069, 1072, 1087, 1150, 1153, 1180, 1183, 1186, 1198, 1204, 1210, 1213, 1216, 1240, 1249, 1255, 1261, 1273, 1279],
    "Kisa": [1189, 1192, 1195, 1201, 1243, 1246, 1276],
    "Sneg": [1114, 1117, 1219, 1222, 1225, 1207, 1252, 1258, 1282]
}

def get_weather_condition(code):
    for key, values in weather_conditions.items():
        if code in values:
            return key
    return "Nepoznato"

# Current directory where the script is located (i.e., inside the (Footage) folder)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_weather():
    results = []
    print("Fetching weather data from API...")
    
    for city, query in cities.items():
        response = requests.get(BASE_URL, params={"key": API_KEY, "q": query, "aqi": "no"})
        if response.status_code == 200:
            data = response.json()
            current = data.get("current")
            if current:
                temperature = round(current.get("temp_c", 0))
                condition = current.get("condition")
                condition_code = condition.get("code") if condition else None
                sky = get_weather_condition(condition_code) if condition_code else "Nepoznato"
                
                # Keep keys in Serbian ("Grad", "Temperatura", "Nebo") for AE JSON import
                results.append({
                    "Grad": city,
                    "Temperatura": f"{temperature}°C",
                    "Nebo": sky
                })
            else:
                # If no data is available
                results.append({
                    "Grad": city,
                    "Temperatura": "N/A",
                    "Nebo": "Nepoznato"
                })
                print(f"No current data for {city}")
        else:
            # If API request fails
            results.append({
                "Grad": city,
                "Temperatura": "N/A",
                "Nebo": "Nepoznato"
            })
            print(f"Request error for {city} - status code {response.status_code}")
            
    # Save the JSON file in the exact same directory as this script
    json_path = os.path.join(CURRENT_DIR, "weather_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"Weather data successfully saved to {json_path}!")

# Run the fetch function
fetch_weather()

# ==========================================
# AFTER EFFECTS HEADLESS RENDER AUTOMATION
# ==========================================

# NOTE: Change this path if using Windows or a different AE version
AERENDER_PATH = "/Applications/Adobe After Effects 2026/aerender"

# Go one level up (Parent Directory) to find the AEP file in the main folder
PARENT_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_PATH = os.path.join(PARENT_DIR, "TEMPERATURE.aep")

# Create the render folder in the main directory (Parent Directory)
RENDER_FOLDER = os.path.join(PARENT_DIR, "Temperature_Render")
OUTPUT_PATH = os.path.join(RENDER_FOLDER, "TEMPERATURE_LOOP_[#####].png")
COMP_NAME = "Temperature" 

def start_render():
    # Create the output directory if it doesn't exist
    os.makedirs(RENDER_FOLDER, exist_ok=True)
    
    print("Starting After Effects headless render...")
    
    command = [
        AERENDER_PATH,
        "-project", PROJECT_PATH,
        "-comp", COMP_NAME,
        "-output", OUTPUT_PATH,
        "-OMtemplate", "Temperature"  
    ]
    
    try:
        subprocess.run(command, check=True)
        print("PNG sequence successfully rendered!")
        
        print("Zipping the render folder...")
        shutil.make_archive(RENDER_FOLDER, 'zip', RENDER_FOLDER)
        print(f"Folder successfully zipped into {os.path.basename(RENDER_FOLDER)}.zip!")
        
        print("Cleaning up the original render folder...")
        shutil.rmtree(RENDER_FOLDER)
        print("Process complete! Your ZIP file is ready in the project directory.")
        
    except subprocess.CalledProcessError as e:
        print(f"Render error occurred: {e}")
    except Exception as e:
        print(f"An error occurred during zipping or cleanup: {e}")

# Run the render function
start_render()











'''import requests
import json
import time
from bs4 import BeautifulSoup

gradovi = ['Beograd', 'Novi sad', 'Kragujevac', 'Nis', 'Sabac', 'Zrenjanin', 'Krusevac', 'Kosovska Mitrovica', 'Zajecar', 'Sombor', 'Uzice', 'Valjevo', 'Subotica', 'Negotin', 'Leskovac', 'Vranje', 'Loznica', 'Cacak', 'Novi Pazar', 'Pirot', 'Kraljevo', 'Sjenica', 'Kopaonik', 'Zlatibor']

def vremenska(Grad):
    # Enter city name
    city = Grad
    temp = None

    while temp is None:
        # Creating URL and requests instance
        url = "https://www.google.rs/search?q=" + "weather" + city
        html = requests.get(url).content

        # Getting raw data
        soup = BeautifulSoup(html, 'html.parser')
        temp_element = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})
        if temp_element is not None:
            temp = temp_element.text

        if temp is None:
            time.sleep(1)

    # Handle the sky condition
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    temperatura = temp[:-2] + '°C'

    data = str.split('\n')
    sky = data[1]

    if 'Делимично облачно' in sky or 'Претежно сунчано' in sky or 'Претежно облачно' in sky:
        sky = 'Sunce-oblaci'
    elif 'Слаби пљускови' in sky or 'Киша' in sky or 'киша' in sky:
        sky = 'Kisa'
    elif 'Сунчано' in sky or 'Ведро' in sky:
        sky = 'Sunce'
    elif 'Магла' in sky:
        sky = 'Magla'
    elif 'Облачно' in sky or 'Ветровито' in sky:
        sky = 'Oblaci'

    # Getting all div tags
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text

    return city, temperatura, sky

weather_data = []

for grad in gradovi:
    data = vremenska(grad)
    weather_data.append({
        "Grad": grad,
        "Temperatura": data[1],
        "Nebo": data[2]
    })
    time.sleep(1)

with open('weather_data.json', 'w', encoding='utf-8') as json_file:
    json_objekat = json.dumps(weather_data, ensure_ascii=False)
    dekodirani_objekat = json.loads(json_objekat)
    json.dump(dekodirani_objekat, json_file, indent=4, ensure_ascii=False)

print("Izbacen JSON")


# input = footage(“weather_data.json”).sourceData[0].Nebo;

# if (input == "Oblaci"){value = 100}
# else {0};
'''
'''
import requests
import json
import time

API_KEY = "API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

gradovi = [
    "Beograd", "Novi Sad", "Kragujevac", "Nis", "Sabac", "Zrenjanin", "Krusevac",
    "Kosovska Mitrovica", "Zajecar", "Sombor", "Uzice", "Valjevo", "Subotica",
    "Negotin", "Leskovac", "Vranje", "Loznica", "Cacak", "Novi Pazar", "Pirot",
    "Kraljevo", "Sjenica", "Kopaonik", "Zlatibor"
]

def vremenska(grad):
    params = {"q": grad, "appid": API_KEY, "units": "metric", "lang": "sr"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperatura = f"{data['main']['temp']}°C"
        vreme = data["weather"][0]["description"].lower()
        
        # Normalizacija naziva vremena
        if "oblačno" in vreme or "vetrovito" in vreme:
            nebo = "Oblaci"
        elif "kiša" in vreme or "pljuskovi" in vreme:
            nebo = "Kisa"
        elif "magla" in vreme:
            nebo = "Magla"
        elif "sunčano" in vreme or "vedro" in vreme:
            nebo = "Sunce"
        else:
            nebo = "Sunce-oblaci"

        return {"Grad": grad, "Temperatura": temperatura, "Nebo": nebo}
    else:
        return {"Grad": grad, "Temperatura": "N/A", "Nebo": "Nepoznato"}

weather_data = [vremenska(grad) for grad in gradovi]

with open("weather_data.json", "w", encoding="utf-8") as json_file:
    json.dump(weather_data, json_file, indent=4, ensure_ascii=False)

print("Izbacen JSON")

import requests
import json
import time

API_KEY = "API_KEY"

CITIES = {
    "BEOGRAD": "Belgrade, Serbia",
    "NOVI SAD": "Novi Sad, Serbia",
    "KRAGUJEVAC": "Kragujevac, Serbia",
    "NIS": "Nis, Serbia",
    "SABAC": "Sabac, Serbia",
    "ZRENJANIN": "Zrenjanin, Serbia",
    "KRUSEVAC": "Krusevac, Serbia",
    "K MITROVICA": "Kosovska Mitrovica, Serbia",
    "ZAJECAR": "Zajecar, Serbia",
    "SOMBOR": "Sombor, Serbia",
    "UZICE": "Uzice, Serbia",
    "VALJEVO": "Valjevo, Serbia",
    "SUBOTICA": "Subotica, Serbia",
    "NEGOTIN": "Negotin, Serbia",
    "LESKOVAC": "Leskovac, Serbia",
    "VRANJE": "Vranje, Serbia",
    "LOZNICA": "Loznica, Serbia",
    "CACAK": "Cacak, Serbia",
    "NOVI PAZAR": "Novi Pazar, Serbia",
    "PIROT": "Pirot, Serbia",
    "KRALJEVO": "Kraljevo, Serbia",
    "SJENICA": "Sjenica, Serbia",
    "KOPAONIK": "Kopaonik, Serbia",
    "ZLATIBOR": "Zlatibor, Serbia"
}

WEATHER_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city):
    response = requests.get(WEATHER_URL, params={"key": API_KEY, "q": city, "aqi": "no"})
    
    if response.status_code == 200 and response.json():
        data = response.json()
        return {
            "temperature": round(data["current"]["temp_c"]),
            "condition": data["current"]["condition"]["text"]
        }
    else:
        print(f"Error fetching weather data for {city}: {response.status_code} - {response.text}")
        return None

def main():
    weather_data = {}

    for city, query in CITIES.items():
        weather = get_weather(query)
        if weather:
            weather_data[city] = weather
        else:
            weather_data[city] = {"error": "Failed to fetch data"}
            print(f"Failed to fetch data for {city}")

        #time.sleep(1)  # 1-second delay between requests

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, indent=4, ensure_ascii=False)

    print("Weather data saved to weather_data.json")

if __name__ == "__main__":
    main()
'''
