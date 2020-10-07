import requests
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.ERROR, format='%(levelname)s:%(name)s:%(message)s')


def main():
    try:
        location = input("""Enter the name of location for temperature.
Enter in this format (city,country code). For example: minneapolis,us: """)  # Get location from user
        url = "http://api.openweathermap.org/data/2.5/forecast"              # URL for API call

        # API key for authentication, Fetched from environment variable, Should be kept private
        key = os.environ.get("WEATHER_KEY")

        # Query parameter, for passing location, units of data and API key for authentication in request
        query = {"q": location, "units": "imperial", "appid": key}

        # Fetching data with URL and query parameters and converting it in JSON format
        request = requests.get(url, params=query).json()

        # There might be chances that there is some exception happened during fetching API key,
        # maybe API key is not available in environment variables or it's incorrect.
        # All these messages are only of interest to the developer
        if request.get("cod") == 401:  # code is 401, means API key is invalid.
            logging.error("Invalid API key or API key is not available.\n")  # As API key is sensitive and private
                                                                             # so, we can't log it. only a message will be logged

        elif request.get("cod") == "404":  # code is 404, means entered city not found
            print("City not found.")

        else:
            forecast_list = request.get("list")  # Extracting data from JSON for printing

            for forecast in forecast_list:
                # forecast["dt"] is Unix timestamp
                # Convert to a datetime, for humans readability
                # Convert datetime to UTC time, user can be from any location
                # UTC time will be best to show instead of Minnesota local time
                timestamp = datetime.utcfromtimestamp(forecast["dt"]).strftime("%D %H:%M:%S")

                # Fetching temperature, unit is imperial so, temperature is in Fahrenheit
                temperature = str(forecast["main"]["temp"])

                weather_description = forecast["weather"][0]["description"]  # Fetching weather description
                wind_speed = forecast["wind"]["speed"]                       # Fetching wind speed

                print(f"At {timestamp} UTC, the weather will be {weather_description}, the temperature will be {temperature}°F"
                      f" and wind speed may be {wind_speed} miles/hour\n")     # printing all values in correct format

    except (requests.ConnectionError, KeyError):
        # system is not connected to the internet, ConnectionError will be raised,
        # we'll print a message and main will be called again.
        if requests.ConnectionError:
            print("Internet is not available.\n")  # Message is not in developer interest so, print is used.
        main()


if __name__ == '__main__':
    main()
