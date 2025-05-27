from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # ✅ Required import
import time
import os
from dotenv import load_dotenv

# List of allowed websites (predefined)
ALLOWED_WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "wikipedia": "https://www.wikipedia.org"
}

# Path to your chromedriver
CHROMEDRIVER_PATH = "C:/Users/i/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

# Initialize a global driver variable to hold the web browser session
driver = None

# Function to open the website
def open_website(query, update_status=None, update_output=None):
    global driver
    try:
        # Extract the site name from the query (after "open website")
        site_name = query.lower().replace("start website", "").strip()
        print(f"Debug: site_name extracted: {site_name}")

        # Check if the site name is in the allowed list
        site_url = ALLOWED_WEBSITES.get(site_name)

        if site_url:
            # Initialize the WebDriver if not already initialized
            if driver is None:
                service = Service(CHROMEDRIVER_PATH)  # ✅ Correct way
                driver = webdriver.Chrome(service=service)  # ✅ Pass service object

            # Open the website in the browser
            driver.get(site_url)
            if update_status:
                update_status(f"Opening {site_name}...")
            if update_output:
                update_output(f"Opened website: {site_name} ({site_url})")
        else:
            if update_status:
                update_status(f"{site_name} is not an allowed website.")
            if update_output:
                update_output(f"Website {site_name} is not in the allowed list.")
    except Exception as e:
        if update_output:
            update_output(f"Failed to open website: {e}")

# Function to close the website
def close_website(query, update_status=None, update_output=None):
    global driver
    try:
        if driver:
            site_name = query.lower().replace("stop website", "").strip()
            print(f"Debug: site_name extracted: {site_name}")

            tabs = driver.window_handles

            for tab in tabs:
                driver.switch_to.window(tab)
                if site_name in driver.current_url.lower():
                    driver.close()
                    if update_status:
                        update_status(f"Closed the {site_name} website.")
                    if update_output:
                        update_output(f"Closed {site_name} website.")
                    break
            else:
                if update_status:
                    update_status(f"{site_name} website is not open.")
                if update_output:
                    update_output(f"{site_name} website is not open.")
        else:
            if update_status:
                update_status("No browser session is open.")
            if update_output:
                update_output("No browser session is open.")
    except Exception as e:
        if update_output:
            update_output(f"Error closing website: {e}")


import pywhatkit

def play_youtube_video(query, update_status=None, update_output=None):
    try:
        query_lower = query.lower()

        # Check if both 'play' and 'youtube' are in the query
        if "play" in query_lower and "youtube" in query_lower:
            # Extract what's between 'play' and 'youtube'
            play_index = query_lower.find("play") + len("play")
            youtube_index = query_lower.find("youtube")
            search_term = query[play_index:youtube_index].strip()

            # Fallback if nothing is between 'play' and 'youtube'
            if not search_term:
                search_term = "latest songs"
                message = "Playing latest songs on YouTube."
            else:
                message = f"Playing {search_term} on YouTube."

            pywhatkit.playonyt(search_term)

            if update_status:
                update_status(message)
            if update_output:
                update_output(message)

    except Exception as e:
        if update_output:
            update_output(f"Error playing YouTube video: {e}")



import os
import requests

import requests

def get_weather(city):
    try:
        api_key = "0569f7fb68d7ef89066d133f8976f168"  # Replace with your actual Weatherstack API key
        url = "http://api.weatherstack.com/current"
        querystring = {"access_key": api_key, "query": city}

        response = requests.get(url, params=querystring)
        data = response.json()
        print(data)  # Debug output

        if 'error' in data:
            return f"City '{city}' not found or API error: {data['error'].get('info', 'Unknown error')}"

        location = data["location"]["name"]
        country = data["location"]["country"]
        temp = data["current"]["temperature"]
        feelslike = data["current"]["feelslike"]
        condition = data["current"]["weather_descriptions"][0]
        humidity = data["current"]["humidity"]

        return (
            f"Weather in {location}, {country}:\n"
            f"Temperature: {temp}°C (feels like {feelslike}°C), "
            f"Condition: {condition}, Humidity: {humidity}%"
        )

    except Exception as e:
        return f"Failed to get weather info: {e}"


