from groq import Groq
import os

# Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",   # Free Groq model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("REAL ERROR:", e)
        return "Groq AI error"