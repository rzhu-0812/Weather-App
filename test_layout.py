import customtkinter as ctk
import os
from PIL import Image

APP_WIDTH = 915
APP_HEIGHT = 550

SEARCH_ICON_SIZE = (15, 15)
WEATHER_ICON_SIZE = (150, 150)

THEME_FILE = 'theme.json'
SEARCH_IMG = 'search.png'
WEATHER_IMG = '01d.png'

DEGREE_SYMBOL = str(b'\xc2\xb0', 'utf8')

FONT = ('Monaspace Neon', 15)
FONT_BOLD = ('Monaspace Neon', 15, 'bold')

APP_THEME_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), THEME_FILE)
SEARCH_IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Images/Misc', SEARCH_IMG)
WEATHER_IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Images/Weather Icons', WEATHER_IMG)

ctk.set_appearance_mode('light')
ctk.set_default_color_theme(APP_THEME_PATH)

root = ctk.CTk()
root.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
root.title('Weather App')

def on_enter(event):
    entry_text = search_entry.get()
    city_name_label.configure(text=entry_text)
    search_entry.delete(0, ctk.END)

def load_image(image_path, size):
    try:
        img = Image.open(image_path)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except FileNotFoundError:
        print(f'Error: File {image_path} not found')
        return None

def day_frame():
    frame = ctk.CTkFrame(frame_r, width=115, height=120, corner_radius=20, fg_color='#FFFFFF')
    return frame

def info_frame():
    frame =  ctk.CTkFrame(frame_r, width=195, height=150, corner_radius=20, fg_color="#FFFFFF")
    return frame

frame_r = ctk.CTkFrame(root, width=615, height=APP_HEIGHT, corner_radius=0, bg_color='gray')
frame_r.place(x=300, y=0)

search_img = load_image(SEARCH_IMG_PATH, SEARCH_ICON_SIZE)
search_label = ctk.CTkLabel(root, width=30, height=30, bg_color='#F9F9FA', text='', image=search_img)
search_label.place(x=20, y=20)

search_entry = ctk.CTkEntry(root, width=225, height=15, placeholder_text='City Name', border_width=0)
search_entry.place(x=45, y=26)

city_name_label = ctk.CTkLabel(root, text='', font=('Monaspace Neon', 20, 'bold'))
city_name_label.place(x=45, y=80)

weather_img = load_image(WEATHER_IMG_PATH, WEATHER_ICON_SIZE)
weather_icon_label = ctk.CTkLabel(root, width=75, height=75, bg_color='#F9F9FA', text='', image=weather_img)
weather_icon_label.place(x=70, y=130)

temp_label = ctk.CTkLabel(root, text='86°F', font=('Monaspace Argon', 40))
temp_label.place(x=49, y=320)

dt_label = ctk.CTkLabel(root, text='Monday, 13:20', font=FONT_BOLD)
dt_label.place(x=50, y=370)

desc_label = ctk.CTkLabel(root, text='Sunny', font=FONT, text_color='gray50')
desc_label.place(x=50, y=430)

rain_label = ctk.CTkLabel(root, text='Rain - 30%', font=FONT, text_color='gray50')
rain_label.place(x=50, y=455)

weekly_weather = ctk.CTkLabel(frame_r, text='5-Day Forecast', font=FONT_BOLD)
weekly_weather.place(x=20, y=10)

day_1 = day_frame()
day_1.place(x=10, y=50)

day_2 = day_frame()
day_2.place(x=130, y=50)

day_3 = day_frame()
day_3.place(x=250, y=50)

day_4 = day_frame()
day_4.place(x=370, y=50)

day_5 = day_frame()
day_5.place(x=490, y=50)

units = ctk.CTkSegmentedButton(frame_r, values=['Metric: °C, m/s', 'Imperial: °F, mph'], font=('Monaspace Neon', 10))
units.place(x=370, y=10)
units.set('Metric: °C, m/s')

highlights = ctk.CTkLabel(frame_r, text='Today\'s Highlights', font=FONT_BOLD)
highlights.place(x=20, y=190)

infobox_1 = info_frame()
infobox_1.place(x=10, y=225)

infobox_2 = info_frame()
infobox_2.place(x=210, y=225)

infobox_3 = info_frame()
infobox_3.place(x=410, y=225)

infobox_4 = info_frame()
infobox_4.place(x=10, y=380)

infobox_5 = info_frame()
infobox_5.place(x=210, y=380)

infobox_6 = info_frame()
infobox_6.place(x=410, y=380)

search_entry.bind('<Return>', on_enter)

root.mainloop()