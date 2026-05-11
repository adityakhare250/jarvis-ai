# ==========================================
# 🔥 ULTRA CONNECTED JARVIS AI (FINAL FIXED)
# ==========================================

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import json
import random
import pickle
import webbrowser
import subprocess
import datetime

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI

# ==============================
# LOAD ENV
# ==============================
load_dotenv()


class JarvisAssistant:

    def __init__(self):

        # 🔊 VOICE
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)

        self.voice_enabled = True
        self.max_len = 20
        self.memory = []

        # ==============================
        # OFFLINE MODEL
        # ==============================
        try:
            self.model = tf.keras.models.load_model("chatbot_model.keras")

            with open("tokenizer.pickle", "rb") as f:
                self.tokenizer = pickle.load(f)

            with open("label_encoder.pickle", "rb") as f:
                self.lbl_encoder = pickle.load(f)

            with open("intents.json") as f:
                self.intents = json.load(f)

            print("✅ Offline chatbot loaded")

        except Exception as e:
            print("⚠️ Offline model missing:", e)
            self.model = None

        # ==============================
        # OPENAI
        # ==============================
        key = os.getenv("OPENAI_API_KEY")

        if key:
            self.client = OpenAI(api_key=key)
            print("✅ OpenAI Connected")
        else:
            self.client = None
            print("⚠️ No API Key")

    # ==============================
    def speak(self, text):
        print("Jarvis:", text)
        if self.voice_enabled:
            self.engine.say(text)
            self.engine.runAndWait()

    # ==============================
    def listen(self):

        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("[Listening...]")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=6)
                query = r.recognize_google(audio, language='en-in')
                return query.lower()
            except:
                return "none"

    # ==============================
    def open_websites(self, query):

        sites = {
            "youtube":"https://youtube.com",
            "google":"https://google.com",
            "gmail":"https://mail.google.com",
            "drive":"https://drive.google.com",
            "amazon":"https://amazon.in",
            "flipkart":"https://flipkart.com",
            "netflix":"https://netflix.com",
            "spotify":"https://open.spotify.com",
            "github":"https://github.com",

            # EXTRA
            "whatsapp":"https://web.whatsapp.com",
            "instagram":"https://instagram.com",
            "facebook":"https://facebook.com",
            "twitter":"https://x.com",
            "linkedin":"https://linkedin.com",

            "chatgpt":"https://chat.openai.com",
            "gemini":"https://gemini.google.com",
            "perplexity":"https://perplexity.ai",

            "leetcode":"https://leetcode.com",
            "geeksforgeeks":"https://geeksforgeeks.org",

            "notion":"https://notion.so",
            "trello":"https://trello.com",

            "swiggy":"https://swiggy.com",
            "zomato":"https://zomato.com",

            "irctc":"https://irctc.co.in",
            "weather":"https://weather.com"
        }

        for name, url in sites.items():
            if name in query:
                self.speak(f"Opening {name}")
                webbrowser.open(url)
                return True

        return False

    # ==============================
    def system_commands(self, query):

        # BASIC
        if "shutdown" in query:
            subprocess.call("shutdown /s /t 5", shell=True)
            return True

        if "restart" in query:
            subprocess.call("shutdown /r /t 5", shell=True)
            return True

        if "open cmd" in query:
            subprocess.Popen("cmd")
            self.speak("Opening command prompt")
            return True

        # TIME
        if "time" in query:
            t = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"The time is {t}")
            return True

        # CHAT
        if "who are you" in query:
            self.speak("I am Jarvis, your AI assistant")
            return True

        if "what can you do" in query:
            self.speak("I can open apps and control system")
            return True

        # MICROSOFT
        if "open notepad" in query:
            subprocess.Popen("notepad")
            return True

        if "open word" in query:
            subprocess.Popen("start winword", shell=True)
            return True

        if "open excel" in query:
            subprocess.Popen("start excel", shell=True)
            return True

        # SYSTEM
        if "task manager" in query:
            subprocess.Popen("taskmgr")
            return True

        if "file explorer" in query:
            subprocess.Popen("explorer")
            return True

        # CMD
        if "ip address" in query:
            subprocess.Popen("ipconfig", shell=True)
            return True

        if "system info" in query:
            subprocess.Popen("systeminfo", shell=True)
            return True

        # LOCK
        if "lock pc" in query:
            subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")
            return True

        return False

    # ==============================
    def local_chatbot(self, text):

        if not self.model:
            return None

        seq = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=self.max_len, truncating='post')
        result = self.model.predict(padded, verbose=0)

        if np.max(result) < 0.75:
            return None

        tag = self.lbl_encoder.inverse_transform([np.argmax(result)])[0]

        for intent in self.intents["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])

        return None

    # ==============================
    def ask_ai(self, prompt):

        if not self.client:
            return "API key missing."

        try:
            self.memory.append(prompt)
            if len(self.memory) > 5:
                self.memory.pop(0)

            context = "\n".join(self.memory)

            res = self.client.responses.create(
                model="gpt-5-mini",
                input=context
            )

            return res.output_text

        except:
            return "Cloud AI error"

    # ==============================
    def run(self):

        self.speak("Jarvis online hi harsh how can i help you can ? you can open google youhte ans cmd and note pad")
        self.speak(" hello harsh gund how are you ?")
        while True:

            query = self.listen()

            if query == "none":
                continue

            print("User:", query)

            if "exit" in query:
                self.speak("Goodbye")
                break

            if self.system_commands(query):
                continue

            if self.open_websites(query):
                continue

            reply = self.local_chatbot(query)

            if reply:
                self.speak(reply)
            else:
                self.speak(self.ask_ai(query))


# ==============================
if __name__ == "__main__":
    JarvisAssistant().run()