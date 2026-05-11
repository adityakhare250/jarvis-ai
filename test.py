

# ==========================================
# 🔥 ULTRA ADVANCED JARVIS AI
# ==========================================

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings("ignore")

import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import datetime
import wikipedia
import pywhatkit
import psutil
import pyautogui
import random
from groq import Groq

# ==========================================
# 🔑 GROQ API
# ==========================================

API_KEY = "YOUR_GROQ_API_KEY"

client = Groq(api_key=API_KEY)

# ==========================================
# 🔊 SPEAK ENGINE
# ==========================================

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 180)

def speak(text):

    print(f"Jarvis: {text}")

    engine.say(text)
    engine.runAndWait()

# ==========================================
# 🎤 LISTEN
# ==========================================

recognizer = sr.Recognizer()

def listen():

    try:

        with sr.Microphone() as source:

            print("[ Listening... ]")

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)

            print("User:", command)

            return command.lower()

    except Exception as e:

        print("ERROR:", e)

        return ""

# ==========================================
# 🤖 AI CHAT
# ==========================================

chat_memory = []

def ask_ai(prompt):

    try:

        chat_memory.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        messages = [
            {
                "role": "system",
                "content": """
                You are Jarvis AI assistant.
                Be smart, short and helpful.
                Help in coding, education, tech, life and productivity.
                """
            }
        ] + chat_memory

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=messages

        )

        answer = response.choices[0].message.content

        chat_memory.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer

    except Exception as e:

        print("AI ERROR:", e)

        return "Groq AI error"

# ==========================================
# 🌐 OPEN WEBSITES
# ==========================================

def open_websites(command):

    websites = {

        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "linkedin": "https://linkedin.com",
        "github": "https://github.com",
        "instagram": "https://instagram.com",
        "facebook": "https://facebook.com",
        "chatgpt": "https://chat.openai.com"

    }

    for site in websites:

        if site in command:

            speak(f"Opening {site}")

            webbrowser.open(websites[site])

            return True

    return False

# ==========================================
# 💻 OPEN APPS
# ==========================================

def open_apps(command):

    try:

        if "notepad" in command:

            subprocess.Popen("notepad.exe")

        elif "calculator" in command:

            subprocess.Popen("calc.exe")

        elif "cmd" in command:

            subprocess.Popen("cmd.exe")

        elif "paint" in command:

            subprocess.Popen("mspaint.exe")

        elif "chrome" in command:

            subprocess.Popen(
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            )

        elif "python" in command:

            subprocess.Popen("python")

        elif "vs code" in command:

            subprocess.Popen(
                r"C:\Users\ADITYA\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            )

        else:

            return False

        speak("Application opened")

        return True

    except Exception as e:

        print("APP ERROR:", e)

        speak("Unable to open application")

        return True

# ==========================================
# 🔎 GOOGLE SEARCH
# ==========================================

def google_search(command):

    query = command.replace("search", "")

    speak(f"Searching {query}")

    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )

# ==========================================
# ▶️ PLAY YOUTUBE
# ==========================================

def play_youtube(command):

    song = command.replace("play", "")

    speak(f"Playing {song}")

    pywhatkit.playonyt(song)

# ==========================================
# 📚 WIKIPEDIA
# ==========================================

def wiki_search(command):

    try:

        query = command.replace("who is", "")
        query = query.replace("what is", "")

        result = wikipedia.summary(query, sentences=2)

        speak(result)

    except:

        speak("No result found")

# ==========================================
# 🕒 TIME
# ==========================================

def tell_time():

    current = datetime.datetime.now().strftime("%I:%M %p")

    speak(f"The time is {current}")

# ==========================================
# 📅 DATE
# ==========================================

def tell_date():

    today = datetime.datetime.now().strftime("%d %B %Y")

    speak(f"Today's date is {today}")

# ==========================================
# 🔋 BATTERY
# ==========================================

def battery_status():

    battery = psutil.sensors_battery()

    percent = battery.percent

    speak(f"Battery is at {percent} percent")

# ==========================================
# 📸 SCREENSHOT
# ==========================================

def take_screenshot():

    image = pyautogui.screenshot()

    image.save("screenshot.png")

    speak("Screenshot saved")

# ==========================================
# 😂 JOKES
# ==========================================

def tell_joke():

    jokes = [

        "Why do programmers hate nature? Too many bugs.",

        "Why was the computer cold? It forgot to close windows.",

        "Why do Java developers wear glasses? Because they cannot C."

    ]

    speak(random.choice(jokes))

# ==========================================
# 🔴 SHUTDOWN
# ==========================================

def shutdown_pc():

    speak("Shutting down computer")

    os.system("shutdown /s /t 5")

# ==========================================
# 🔁 RESTART
# ==========================================

def restart_pc():

    speak("Restarting computer")

    os.system("shutdown /r /t 5")

# ==========================================
# 🚀 START
# ==========================================

speak("Jarvis online. How can I help you?")

while True:

    command = listen()

    if command == "":
        continue

    # EXIT

    if "exit" in command or "bye" in command:

        speak("Goodbye")

        break

    # TIME

    elif "time" in command:

        tell_time()

    # DATE

    elif "date" in command:

        tell_date()

    # BATTERY

    elif "battery" in command:

        battery_status()

    # SCREENSHOT

    elif "screenshot" in command:

        take_screenshot()

    # JOKE

    elif "joke" in command:

        tell_joke()

    # SHUTDOWN

    elif "shutdown" in command:

        shutdown_pc()

    # RESTART

    elif "restart" in command:

        restart_pc()

    # PLAY SONG

    elif "play" in command:

        play_youtube(command)

    # GOOGLE SEARCH

    elif "search" in command:

        google_search(command)

    # WIKIPEDIA

    elif "who is" in command or "what is" in command:

        wiki_search(command)

    # OPEN WEBSITE

    elif "open" in command:

        opened = open_websites(command)

        if not opened:

            opened = open_apps(command)

        if not opened:

            answer = ask_ai(command)

            speak(answer)

    # AI CHAT

    else:

        answer = ask_ai(command)

        speak(answer)