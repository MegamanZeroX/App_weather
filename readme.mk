# IOS App Weather

This is a weather application built using Python and Kivy, designed to be packaged into an executable file for Windows and eventually deployed to an iPhone. The app allows users to get weather information for a specified city or for their current location.

## Features

- Fetches weather data for a given city using the OpenWeatherMap API.
- Fetches weather data for the user's current location based on IP.
- Displays a 5-day weather forecast including temperature, humidity, wind speed, and weather description.
- Includes an info button that provides information about PM Accelerator.

## Installation and Setup

### Prerequisites

- Python 3.7+
- Kivy and KivyMD libraries

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MegamanZeroX/IOS_App_weather.git

### Deploy the applicaiton on Windows:

1. In the main dictionary, open cmd and:

	```bash
	pip install pyinstaller 

	pyinstaller --onefile main.py

### Application file

In the main or dist dictionnary, the app(weather.exe) can be executed on Windows
