
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from weather_service import get_weather_by_city, get_weather_by_coordinates, get_current_location
import ipinfo
from datetime import datetime
from kivymd.uix.label import MDLabel
pm_accelerator_description = (
    "       The Product Manager Accelerator Program is designed to support PM professionals through every stage of their career. "
    "From students looking for entry-level jobs to Directors looking to take on a leadership role, our program has helped over hundreds of students fulfill their career aspirations."
)
KV = '''
ScreenManager:
    MainScreen:
<MainScreen>:
    name: 'main'
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        BoxLayout:
            orientation: 'vertical'
            padding: [20, 20, 20, 20]  # Add padding to the top (left, top, right, bottom)
            spacing: 20
            size_hint_y: None
            height: self.minimum_height  # Set height based on content
        
            TextInput:
                id: city_name
                hint_text: "Enter city name"
                size_hint: 1, None
                height: 40
                multiline: False  # Single-line input
                foreground_color: 1, 1, 1, 1  # White text color
                background_color: 0.1, 0.1, 0.1, 1  # Dark background color
                cursor_color: 1, 1, 1, 1  # White cursor color
                hint_text_color: 0.7, 0.7, 0.7, 1  # Gray hint text color
            Button:
                text: "Get Weather"
                size_hint: 1, None
                height: 50
                on_release: app.show_weather()
            Button:
                text: "Get Current Location Weather"
                size_hint: 1, None
                height: 50
                on_release: app.show_weather_by_location()
            Button:
                text: "Info"
                size_hint: 1, None
                height: 50
                on_release: app.show_info()
            Label:
                id: location_label
                text: ""
                halign: "center"
                size_hint: 1, None
                height: 40
            BoxLayout:
                id: forecast_box
                orientation: 'vertical'
                size_hint_y: None
                height: 500
                spacing: 10
                
            Label:
                text: "Weather App by Yunhao Zhang"
                halign: "center"
                size_hint: 1, None
                height: 40
'''
class MainScreen(Screen):
    pass
class WeatherApp(MDApp):
    def build(self):
        return Builder.load_string(KV)
    def show_weather(self):
        city_name = self.root.get_screen('main').ids.city_name.text
        if city_name:
            weather_data = get_weather_by_city(city_name)
            if weather_data and 'list' in weather_data:
                self.display_forecast(weather_data, city_name)
            else:
                self.root.get_screen('main').ids.location_label.text = "City not found or error retrieving data."
        else:
            self.root.get_screen('main').ids.location_label.text = "Please enter a city name."
    def show_weather_by_location(self):
        ipinfo_token = '5e86b18434edfc'  
        try:
            latitude, longitude = get_current_location(ipinfo_token)
            weather_data = get_weather_by_coordinates(latitude, longitude)
            if weather_data and 'list' in weather_data:
                location_name = weather_data['city']['name']
                self.display_forecast(weather_data, location_name)
            else:
                self.root.get_screen('main').ids.location_label.text = "Error retrieving data for current location."
        except Exception as e:
            print(f"An error occurred: {e}")
            self.root.get_screen('main').ids.location_label.text = "Could not determine location."
    def show_info(self):
        content = Label(
            text=pm_accelerator_description,
            halign="left",
            valign="top",
            text_size=(400, None),  
            size_hint_y=None,
            padding_y=('10', '0'),
        )
        content.bind(size=content.setter('text_size'))  
        popup = Popup(
            title='About PM Accelerator',
            content=content,
            size_hint=(0.9, 0.5),
            auto_dismiss=True
        )
        popup.open()
    def display_forecast(self, weather_data, location_name):
        forecast = weather_data['list']
        forecast_by_day = {}
        
        for entry in forecast:
            date = entry['dt_txt'].split(' ')[0]
            temp = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind_speed = entry['wind']['speed']
            wind_deg = entry['wind'].get('deg', 'N/A')
            wind_gust = entry['wind'].get('gust', 'N/A')
            description = entry['weather'][0]['description']
            icon = entry['weather'][0]['icon']
            
            if date not in forecast_by_day:
                forecast_by_day[date] = {
                    'temps': [],
                    'humidities': [],
                    'wind_speeds': [],
                    'wind_degs': [],
                    'wind_gusts': [],
                    'descriptions': [],
                    'icons': []
                }
            forecast_by_day[date]['temps'].append(temp)
            forecast_by_day[date]['humidities'].append(humidity)
            forecast_by_day[date]['wind_speeds'].append(wind_speed)
            forecast_by_day[date]['wind_degs'].append(wind_deg)
            forecast_by_day[date]['wind_gusts'].append(wind_gust)
            forecast_by_day[date]['descriptions'].append(description)
            forecast_by_day[date]['icons'].append(icon)
        
        self.root.get_screen('main').ids.location_label.text = f"Weather forecast for {location_name}"
        
        forecast_box = self.root.get_screen('main').ids.forecast_box
        forecast_box.clear_widgets()
        
        for date, data in forecast_by_day.items():
            avg_temp = sum(data['temps']) / len(data['temps'])
            avg_humidity = sum(data['humidities']) / len(data['humidities'])
            avg_wind_speed = sum(data['wind_speeds']) / len(data['wind_speeds'])
            wind_deg = data['wind_degs'][0]
            wind_gust = data['wind_gusts'][0] if data['wind_gusts'][0] != 'N/A' else 'No data'
            common_description = max(set(data['descriptions']), key=data['descriptions'].count)
            icon = data['icons'][0]
            day_layout = BoxLayout(orientation='horizontal', spacing=10)
            weather_icon = AsyncImage(
                source=f"http://openweathermap.org/img/wn/{icon}@2x.png",
                size_hint=(None, None),
                size=(50, 50)
            )
            weather_info = Label(
                text=(
                    f"{date}: {avg_temp:.2f}°C, {common_description.capitalize()}\n"
                    f"Humidity: {avg_humidity:.2f}%, Wind: {avg_wind_speed:.2f} m/s, "
                    f"Direction: {wind_deg}°, Gust: {wind_gust:.2f} m/s"
                ),
                halign="center",
                size_hint_y=None,
                height=50
            )
            day_layout.add_widget(weather_icon)
            day_layout.add_widget(weather_info)
            forecast_box.add_widget(day_layout)
if __name__ == '__main__':
    WeatherApp().run()
'''pt Exception as e:
print(f"An error occurred: {e}")
input("Press Enter to exit...")'''
