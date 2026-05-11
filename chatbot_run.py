import json
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle

# ---------- LOAD FILES ----------
model = tf.keras.models.load_model("chatbot_model.keras")

with open("intents.json") as file:
    data = json.load(file)

# ⚠️ tokenizer + label encoder must be same as training
with open("tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

with open("label_encoder.pickle", "rb") as enc:
    lbl_encoder = pickle.load(enc)

max_len = 20

# ---------- CHAT FUNCTION ----------
def chatbot_response(text):
    text = text.lower()
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, truncating='post', maxlen=max_len)

    result = model.predict(padded, verbose=0)
    tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

    for intent in data["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "I don't understand."

# ---------- CHAT LOOP ----------
print("🤖 Jarvis Chatbot Started! (type quit to exit)")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Jarvis: Goodbye 😎")
        break

    response = chatbot_response(user_input)
    print("Jarvis:", response)
