import requests
import customtkinter as ctk

user_input = ""

def get_info():
    api_key = "API KEY"

    try:
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
        weather_data.raise_for_status()
        data = weather_data.json()

        if data['cod'] == '404':
            return "No City Found", "", "", "", ""
        else:
            weather = data['weather'][0]['main']
            description = data['weather'][0]['description']
            temp = round(data['main']['temp'])
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            return weather, description, temp, humidity, wind_speed

    except requests.exceptions.HTTPError as err:
        if weather_data.status_code == 401:
            return "Invalid API key.", "", "", "", ""
        else:
            return f"HTTP error", "", "", "", ""
    except requests.exceptions.ConnectionError as err:
        return f"Connection error", "", "", "", ""
    except requests.exceptions.Timeout as err:
        return f"Timeout error", "", "", "", ""
    except requests.exceptions.RequestException as err:
        return f"Error", "", "", "", ""


def retrieve_input():
    global user_input

    user_input = entry.get()
    weather_data = get_info()

    if weather_data[-1] == "":
        label.configure(text=weather_data[0])
    else:
        label.configure(text=f"Weather: {weather_data[0]}\n"
                             f"Description: {weather_data[1].capitalize()}\n"
                             f"Temperature: {weather_data[2]}\n"
                             f"Humidity: {weather_data[3]}\n"
                             f"Wind speed: {weather_data[4]}")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("CustomTkinter Weather App")

entry = ctk.CTkEntry(root, width=200)
entry.pack(pady=10)

button = ctk.CTkButton(root, text="Submit", command=retrieve_input)
button.pack(pady=5)

label = ctk.CTkLabel(root, text="")
label.pack(pady=10)

root.mainloop()
