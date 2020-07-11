from tkinter import *
from PIL import ImageTk,Image 
import time
from datetime import datetime
import os
import threading
import playsound
import speech_recognition as sr
from gtts import gTTS
import apiai
import json
import random
import webbrowser
import urllib.request
import pytemperature as temp
import pyautogui
import pyperclip
import pygame
import sys


r = sr.Recognizer()


path = os.path.join(sys.path[0], "System_Files/")
with open(f"{path}intents.json") as file:
    data = json.load(file)


def tell_joke():
    req = urllib.request.Request("https://sv443.net/jokeapi/v2/joke/Any", headers={'User-Agent': 'Mozilla/76.0'})
    with urllib.request.urlopen(req) as response:
        source = response.read()
    data = json.loads(source)
    if data["type"] == "twopart":
        Kiara_speak(data["setup"])
        time.sleep(1)
        Kiara_speak(data["delivery"])
    else:
        Kiara_speak(data["joke"])


def take_note():
    Kiara_speak("What should I name the note?")
    file_name = get_sec_command()
    file_name+=".txt"
    path = os.path.join(sys.path[0], "Notes/")
    while file_name in os.listdir(path):
        Kiara_speak("A file with the same name already exists. Do you want to overwrite it?")
        con = get_sec_command()
        if con == "yes":
            break
        else:
            Kiara_speak("Give a new name")
            file_name = get_sec_command()
            file_name+=".txt"
    Kiara_speak("What do you want to take a note of?")
    text = get_sec_command()
    note = open(f"{path}{file_name}", "w+")
    note.write(text)
    note.close()
    Kiara_speak("Note has been saved")
    Kiara_speak("Do you want me to show you the note?")
    con = get_sec_command()
    if con == "yes":
        os.startfile(f'{path}{file_name}')


def search_google():
    Kiara_speak("What do you want to search for?")
    search = get_sec_command()
    Kiara_speak("Here is what I found on google")
    webbrowser.get().open("https://www.google.co.in/search?q="+search)


def search_youtube():
    Kiara_speak("What do you want to search for?")
    search = get_sec_command()
    Kiara_speak("Bringing up search results from youtube")
    webbrowser.get().open("https://www.youtube.com/results?search_query="+search)


def get_direction():
    Kiara_speak("What is your starting location?")
    loc = get_sec_command()
    start_loc = [i+"+" for i in loc.split(" ")]
    Kiara_speak("What is your destination?")
    loc = get_sec_command()
    dest_loc = [i+"+" for i in loc.split(" ")]
    Kiara_speak("Searching for best route in google maps!")
    webbrowser.get().open(f"https://www.google.com/maps/dir/{start_loc}/{dest_loc}")


def get_weather():
    api_key = "52b2943c289311edf37344e1f0ab256a"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    Kiara_speak("Which location do you want to find the weather of?")
    city_name = get_sec_command()
    url = base_url + "appid=" + api_key + "&q=" + city_name
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/76.0'})
    with urllib.request.urlopen(req) as response:
        source = response.read()
    raw_data = json.loads(source)
    if raw_data["cod"] != "404":
        data = raw_data["main"]
        tem = data["temp"]
        Kiara_speak(f"The temerature of {city_name} is {str('%.2f'%temp.k2c(tem))} celcius")
    else:
        Kiara_speak("Location is not registered in the database")


def get_meaning():
    path = os.path.join(sys.path[0], "System_Files/")
    app_id = "e1612a46"
    app_key = "4543e619d2dd3b3f7e9595bba105e281"
    Kiara_speak("Which word do you want the meaning of?")
    word = get_sec_command()
    try:
        url = f"https://od-api.oxforddictionaries.com:443/api/v2/entries/en/{word}?fields=definitions,examples"
        req = urllib.request.Request(url, headers={'app_id' : app_id, 'app_key' : app_key, 'User-Agent': 'Mozilla/76.0'})
        with urllib.request.urlopen(req) as response:
            source = response.read()
        data = json.loads(source)
        Kiara_speak(f"Here is the most common meaning of the word {word}")
        define = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        Kiara_speak(define)
        ex_avail = True
        try:
            ex = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"]
        except:
            Kiara_speak(f"Sorry, but I don't have an example of the use of the word {word}")
            ex_avail = False
        if ex_avail:
            Kiara_speak("Do you want an example of its use?")
            con = get_sec_command()
            if con == "yes":
                Kiara_speak(f"Here is an example of use of the word {word}")
                Kiara_speak(ex)
        Kiara_speak("Did you get that or do you want me to write it down for you?")
        con = get_sec_command()
        if con == "yes":
            file_name = "meaning.txt"
            meaning = open(file_name, "w+")
            text = f"{word}:\ndefinition: {define}"
            if ex_avail:
                text+=f"\nexample: {ex}"
            meaning.write(text)
            meaning.close()
            os.startfile(f'{path}{file_name}')
    except:
        Kiara_speak("I dont have this word listed in my dictionary database. Do you want me to search in google?")
        con = get_sec_command()
        if con == "yes":
            Kiara_speak("Here is what I found on google")
            webbrowser.get().open(f"https://www.google.co.in/search?q=meaning+of+{word}")


def get_date_time(voice_data):
    now = datetime.now()
    day = now.strftime("%A")
    date = now.strftime("%d")
    mon = now.strftime("%B")
    hr = now.strftime("%I")
    mint = now.strftime("%M")
    ampm = now.strftime("%p")
    if "date" in voice_data and "time" in voice_data:
        Kiara_speak(f"Today is {day} and the date is {date} of {mon}. The current time is {hr} {mint} {ampm}")
    elif "date" in voice_data:
        Kiara_speak(f"Today's date is {date} of {mon}")
    elif "day" in voice_data:
        Kiara_speak(f"Today is {day}")
    elif "time" in voice_data:
        Kiara_speak(f"The current system time is {hr} {mint} {ampm}")


def take_ss():
    ss = pyautogui.screenshot()
    now = datetime.now()
    date = now.strftime("%d")
    mon = now.strftime("%B")
    hr = now.strftime("%I")
    mint = now.strftime("%M")
    file_name = f"Screenshot-{date}{mon}{hr}{mint}.png"
    path = os.path.join(sys.path[0], "Screenshots/")
    ss.save(f"{path}{file_name}")
    Kiara_speak("Screenshot has been saved")
    Kiara_speak("Do you want me to show you the screenshot?")
    con = get_sec_command()
    if con == "yes":
        os.startfile(f'{path}{file_name}')


def read_selected():
    text = ''
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    var = pyperclip.paste()
    text+=var
    Kiara_speak(text)


def calculate():
    Kiara_speak("What do you want to calculate?")
    def get_operator(op):
        return {
            '+' : '+',
            '-' : '-',
            'x' : '*',
            'by' : '/',
        }[op]
    eq = get_sec_command().split(" ")
    for words in range(1, len(eq), 2):
        eq[words] = get_operator(eq[words])
    equation = " ".join(eq)
    Kiara_speak(eval(equation))
        
    
def intro_video():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    path = os.path.join(sys.path[0], "Intro_Images/")
    images = [pygame.image.load(path+f) for f in os.listdir(path)]
    screen_width = 430
    screen_height = 200
    black = (0,0,0)
    clock = pygame.time.Clock()
    win = pygame.display.set_mode([screen_width,screen_height], pygame.NOFRAME)
    for i in range(len(images)):
        win.fill(black)
        clock.tick(30)
        win.blit(images[i], (0,0))
        pygame.display.update()
    pygame.quit()


def start_up():
    Kiara_speak("This is Kiyara")
    Kiara_speak("Initiating start up sequence")
    time.sleep(0.5)
    Kiara_speak("Waiting for all systems to come online")
    time.sleep(1)
    Kiara_speak("Loading system libraries")
    time.sleep(0.5)
    Kiara_speak("All systems online")
    now = datetime.now()
    day = now.strftime("%A")
    date = now.strftime("%d")
    mon = now.strftime("%B")
    hr = now.strftime("%I")
    mint = now.strftime("%M")
    ampm = now.strftime("%p")
    intro_video()
    Kiara_speak(f"Today is {day} and the date is {date} of {mon}. The current time is {hr} {mint} {ampm}")
    start_response = ["How are you today?", "What can I do for you?", "Nice to meet you again", "Have a task for me?"]
    Kiara_speak(f"Hello!! {random.choice(start_response)}")


def get_tag(voice_data):
    for tag in list(data["intents"].keys()):
        if voice_data in data["intents"][tag]["patterns"]:
            return tag
    for tag in list(data["intents"].keys()):
        for words in voice_data.split(" "):
            if words in data["intents"][tag]["patterns"]:
                return tag


def apiai_conc(voice_data):
    CLIENT_ACCESS_TOKEN = "a07ffdb472254af2b3dd8c7c7077b928 "
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = "de"
    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = voice_data
    source = request.getresponse()
    source_data = source.read()
    response = json.loads(source_data)
    return response["result"]["fulfillment"]["speech"]


def get_primary_command():
    while True:
        with sr.Microphone() as source:
            status.place_forget()
            status["text"] = "Listening..."
            status.place(x=40, y=13)
            time.sleep(1)
            audio = r.listen(source)
            voice_data = ""
            try:
                status.place_forget()
                voice_data = r.recognize_google(audio)
                return voice_data.lower()
            except:
                Kiara_speak("Sorry, I did not get that")


def get_sec_command():
    sound_path = os.path.join(sys.path[0], "System_Files/")
    while True:
        with sr.Microphone() as source:
            playsound.playsound(f"{sound_path}google_now_voice.mp3")
            status.place_forget()
            status["text"] = "Listening..."
            status.place(x=40, y=13)
            time.sleep(1)
            audio = r.listen(source)
            playsound.playsound(f"{sound_path}google_glass_success.mp3")
            voice_data = ""
            try:
                status.place_forget()
                voice_data = r.recognize_google(audio)
                return voice_data.lower()
            except:
                Kiara_speak("Sorry, I did not get that")


def wake_command():
    with sr.Microphone() as source:
        status.place_forget()
        status["text"] = "Say Hey Kiara to activate her..."
        status.place(x=40, y=13)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except:
            pass
        return voice_data.lower()


def Kiara_speak(text):
    tts = gTTS(text=text, lang="en-us")
    file_name = "voice.mp3"
    path = os.path.join(sys.path[0], "System_Files/")
    tts.save(path+file_name)
    playsound.playsound(path+file_name)
    os.remove(f"{path}{file_name}")


def Kiara_respond():
    global Kiara_ready
    sound_path = os.path.join(sys.path[0], "System_Files/")
    while True:
        tag = None
        voice_data = wake_command()
        if Kiara_ready == True or voice_data.count("hey kiara") > 0 or voice_data.count("hi kiara") > 0 or voice_data.count("hay kiara")> 0 or voice_data.count("hay kya ra") > 0 or voice_data.count("hey 11") > 0:
            Kiara_ready = False
            playsound.playsound(f"{sound_path}google_now_voice.mp3")
            voice_data = get_primary_command()
            playsound.playsound(f"{sound_path}google_glass_success.mp3")
            try:
                tag = get_tag(voice_data)
                if tag == "g_search":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    search_google()
                elif tag == "note":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    take_note()
                elif tag == "joke":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    tell_joke()
                elif tag == "g_direction":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    get_direction()
                elif tag == "youtube_search":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    search_youtube()
                elif tag == "weather":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    get_weather()
                elif tag == "meaning":
                    Kiara_speak(random.choice(data["intents"][tag]["responses"]))
                    get_meaning()
                elif tag == "date_time":
                    get_date_time(voice_data)
                elif tag == "ss":
                    Kiara_speak("Taking screenshot now")
                    take_ss()
                elif tag == "read_selected":
                    Kiara_speak("Reading")
                    read_selected()
                elif tag == "calculator":
                    calculate()
                elif tag == "quit":
                    os._exit(0)
                else:
                    res = apiai_conc(voice_data)
                    Kiara_speak(res)
            except:
                Kiara_speak("Sorry, but I did not get what you just said")




#                             ###GUI###                                #
#Variables
note_button_x = about_button_x = home_button_x = ss_button_x = -2
home_button_y = 106
note_button_y = 172
about_button_y = 348
ss_button_y = 242

menu_color = "#2c2b34"
bottom_frame_color = "#28262e"
font_color = "#06dff5"
internal_box_color = "#2b2a31"

screen_state = "home"

time1 = ''

ss_f_button = []
note_f_button = []
note_text = None

Kiara_ready = False


#functions
def change_Kiara_ready():
    global Kiara_ready
    Kiara_ready = True


def get_time():
    global time1
    while True:
        time2 = time.strftime('%H:%M:%S')
        if time2 != time1:
            time1 = time2
            now = datetime.now()
            hr = now.strftime("%I")
            mint = now.strftime("%M")
            day = now.strftime("%A")
            date = now.strftime("%d")
            mon = now.strftime("%B")
            time_display.config(text=f"{hr}:{mint}")
            day_display.config(text=f"{day},")
            date_display.config(text=f"{date} {mon}")

def drawHome():
    global note_text, note_f_button, ss_f_button
    if note_text != None:
        note_text.place_forget()
        note_text = None
    while note_f_button != []:
        for widget in note_f_button:
            widget.place_forget()
            note_f_button.remove(widget)
    while ss_f_button != []:
        for widget in ss_f_button:
            widget.place_forget()
            ss_f_button.remove(widget)
    menu_home_activated.place(x=0, y=0)
    menu_note_activated.place_forget()
    menu_ss_activated.place_forget()
    menu_about_activated.place_forget()
    home_button.place_forget()
    note_button.place(x=note_button_x, y=note_button_y)
    ss_button.place(x=ss_button_x, y=ss_button_y)
    about_button.place(x=about_button_x, y=about_button_y)
    home_button.place_forget()
    home_screen.place(x=0, y=0)
    note_screen.place_forget()
    ss_screen.place_forget()
    about_screen.place_forget()

def drawNote():
    global note_text, note_f_button, ss_f_button
    if note_text != None:
        note_text.place_forget()
        note_text = None
    while note_f_button != []:
        for widget in note_f_button:
            widget.place_forget()
            note_f_button.remove(widget)
    while ss_f_button != []:
        for widget in ss_f_button:
            widget.place_forget()
            ss_f_button.remove(widget)
    menu_home_activated.place_forget()
    menu_note_activated.place(x=0, y=0)
    menu_about_activated.place_forget()
    menu_ss_activated.place_forget()
    note_button.place_forget()
    home_button.place(x=home_button_x, y=home_button_y)
    ss_button.place(x=ss_button_x, y=ss_button_y)
    about_button.place(x=about_button_x, y=about_button_y)
    note_button.place_forget()
    home_screen.place_forget
    note_screen.place(x=0, y=0)
    ss_screen.place_forget()
    about_screen.place_forget()
    note_window()

def drawSS():
    global note_text, note_f_button, ss_f_button
    if note_text != None:
        note_text.place_forget()
        note_text = None
    while note_f_button != []:
        for widget in note_f_button:
            widget.place_forget()
            note_f_button.remove(widget)
    while ss_f_button != []:
        for widget in ss_f_button:
            widget.place_forget()
            ss_f_button.remove(widget)
    menu_home_activated.place_forget()
    menu_note_activated.place_forget()
    menu_ss_activated.place(x=0, y=0)
    menu_about_activated.place_forget()
    ss_button.place_forget()
    home_button.place(x=home_button_x, y=home_button_y)
    note_button.place(x=note_button_x, y=note_button_y)
    about_button.place(x=about_button_x, y=about_button_y)
    home_screen.place_forget()
    note_screen.place_forget()
    ss_screen.place(x=0, y=0)
    about_screen.place_forget()
    ss_window()

def drawAbout():
    global note_text, note_f_button, ss_f_button
    if note_text != None:
        note_text.place_forget()
        note_text = None
    if note_f_button != []:
        for widget in note_f_button:
            widget.place_forget()
            note_f_button.remove(widget)
    if ss_f_button != []:
        for widget in ss_f_button:
            widget.place_forget()
            ss_f_button.remove(widget)
    menu_home_activated.place_forget()
    menu_note_activated.place_forget()
    menu_ss_activated.place_forget()
    menu_about_activated.place(x=0, y=0)
    about_button.place_forget()
    home_button.place(x=home_button_x, y=home_button_y)
    ss_button.place(x=ss_button_x, y=ss_button_y)
    note_button.place(x=note_button_x, y=note_button_y)
    about_button.place_forget()
    home_screen.place_forget()
    note_screen.place_forget()
    ss_screen.place_forget()
    about_screen.place(x=0, y=0)

def note_window():  #To operate Note Window
    global note_f_button, note_text
    if note_text != None:
        note_text.place_forget()
        note_text = None
    path = os.path.join(sys.path[0], "Notes/")
    note_files = [f for f in os.listdir(path)]
    if len(note_files)>0:
        y=60
        for i in range(len(note_files)):
            note_f_button.append(HoverButton(MainFrameCanvas, bg=internal_box_color, fg=font_color, activebackground=internal_box_color, activeforeground=font_color, bd ="0", text=note_files[i], font=("Helvetica Neue Bold", "10"), cursor="hand2", command=lambda file_name=note_files[i]: open_note(file_name)))
            note_f_button[i].place(x=55, y=y)
            y+=20
    root.update()

def open_note(f_name): #To operate Note Window
    global note_text
    if note_text != None:
        note_text.place_forget()
        note_text = None
    path = os.path.join(sys.path[0], "Notes/")
    with open(f"{path}{f_name}", "r") as file:
        note_text = file.read()
    note_text = Label(MainFrameCanvas, text=note_text, bg=internal_box_color, fg=font_color, font=("Helvetica Neue Bold", "11"))
    note_text.place(x=340, y=60)
    root.update()

def ss_window():
    global ss_f_button
    path = os.path.join(sys.path[0], "Screenshots/")
    ss_files = [f for f in os.listdir(path)]
    ss_f_button = []
    if len(ss_files)>0:
        y=60
        for i in range(len(ss_files)):
            ss_f_button.append(HoverButton(MainFrameCanvas, bg=internal_box_color, fg=font_color, activebackground=internal_box_color, activeforeground=font_color, bd=0, text=ss_files[i], font=("Helvetica Neue Bold", "10"), cursor="hand2", command=lambda ss_name=ss_files[i]: open_ss(ss_name)))
            ss_f_button[i].place(x=55, y=y)
            y+=20
    root.update()

def open_ss(f_name):
    path = os.path.join(sys.path[0], "Screenshots/")
    os.startfile(f"{path}{f_name}")


class HoverButton(Button):
    def __init__(self, master, **kwargs):
        Button.__init__(self, master = master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self["background"] = self["activebackground"]
    
    def on_leave(self, e):
        self["background"] = self.defaultBackground


#threading classes
class GetTime(threading.Thread):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def run(self):
        get_time()

class Kiara(threading.Thread):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
    
    def run(self):
        Kiara_respond()


display_time = GetTime()
Kiara_response = Kiara()

#start_up()

#GUI
root = Tk()
root.title("Kiara")
root.geometry("706x462")
root.resizable(False, False)
icon_path = os.path.join(sys.path[0], "System_Files/")
root.call('wm', 'iconphoto', root._w, PhotoImage(file=f"{icon_path}logo.png"))


MenuCanvas = Canvas(root, width=68, height=462)
MenuCanvas.place(x=0, y=0)
TopFrameCanvas = Canvas(root, width=638, height=66)
TopFrameCanvas.place(x=68, y=0)
MainFrameCanvas = Canvas(root, width=638, height=357)
MainFrameCanvas.place(x=68, y=66)
BottomFrameCanvas = Canvas(root, width=638, height=39)
BottomFrameCanvas.place(x=68, y=423)


#Images
image_path = os.path.join(sys.path[0], "Screens/")
home_button_image = ImageTk.PhotoImage(Image.open(f"{image_path}home_button.png"))
note_button_image = ImageTk.PhotoImage(Image.open(f"{image_path}note_button.png"))
about_button_image = ImageTk.PhotoImage(Image.open(f"{image_path}about_button.png"))
ss_button_image = ImageTk.PhotoImage(Image.open(f"{image_path}ss_button.png"))
mic_button_image = ImageTk.PhotoImage(Image.open(f"{image_path}mic_button.png"))
menu_home_activated_image = ImageTk.PhotoImage(Image.open(f"{image_path}menu_home_activated2.png"))
menu_note_activated_image = ImageTk.PhotoImage(Image.open(f"{image_path}menu_note_activated2.png"))
menu_about_activated_image = ImageTk.PhotoImage(Image.open(f"{image_path}menu_about_activated2.png"))
menu_ss_activated_image = ImageTk.PhotoImage(Image.open(f"{image_path}menu_ss_activated2.png"))
top_frame_image = ImageTk.PhotoImage(Image.open(f"{image_path}top_frame.png"))
bottom_frame_image = ImageTk.PhotoImage(Image.open(f"{image_path}bottom_frame2.png"))
home_screen_image = ImageTk.PhotoImage(Image.open(f"{image_path}home_screen.png"))
note_screen_image = ImageTk.PhotoImage(Image.open(f"{image_path}notes_screen.png"))
about_screen_image = ImageTk.PhotoImage(Image.open(f"{image_path}about_screen.png"))
ss_screen_image = ImageTk.PhotoImage(Image.open(f"{image_path}ss_screen.png"))


#Buttons
home_button = Button(root, image=home_button_image, bd=0, bg=menu_color, cursor="hand2", activebackground=menu_color, command= drawHome)
note_button = Button(root, image=note_button_image, bd=0, bg=menu_color, cursor="hand2", activebackground=menu_color, command= drawNote)
about_button = Button(root, image=about_button_image, bd=0, bg=menu_color, cursor="hand2", activebackground=menu_color, command= drawAbout)
ss_button = Button(root, image=ss_button_image, bd=0, bg=menu_color, cursor="hand2", activebackground=menu_color, command=drawSS)
mic_button = Button(root, image=mic_button_image, bd=0, bg=bottom_frame_color, cursor="hand2", activebackground=bottom_frame_color, command=change_Kiara_ready)
mic_button.place(x=641, y=431)


#Frames
top_frame = Label(TopFrameCanvas, image=top_frame_image, bd=0)
top_frame.place(x=0, y=0)
bottom_frame = Label(BottomFrameCanvas, image=bottom_frame_image, bd=0)
bottom_frame.place(x=0, y=0)


#Labels
menu_home_activated = Label(MenuCanvas, image=menu_home_activated_image, bd=0)
menu_note_activated = Label(MenuCanvas, image=menu_note_activated_image, bd=0)
menu_about_activated = Label(MenuCanvas, image=menu_about_activated_image, bd=0)
menu_ss_activated = Label(MenuCanvas, image=menu_ss_activated_image, bd=0)
home_screen = Label(MainFrameCanvas, image=home_screen_image, bd=0)
note_screen = Label(MainFrameCanvas, image=note_screen_image, bd=0)
about_screen = Label(MainFrameCanvas, image=about_screen_image, bd=0)
ss_screen = Label(MainFrameCanvas, image=ss_screen_image, bd=0)

status = Label(bottom_frame, bd=0, fg=font_color, bg=bottom_frame_color, font=("Calibri", "10"))


drawHome()

day_display = Label(root, fg=font_color, bg=bottom_frame_color, font=("Helvetica Neue Bold", "11"))
day_display.place(x=590, y=7)
time_display = Label(root, fg=font_color, bg=bottom_frame_color, font=("Helvetica Neue Bold", "32"))
time_display.place(x=470, y=0)
date_display = Label(root, fg=font_color, bg=bottom_frame_color, font=("Helvetica Neue Bold", "11"))
date_display.place(x=590, y=28)


#threading
display_time.start()
Kiara_response.start()


root.update()

root.mainloop()

os._exit(0)