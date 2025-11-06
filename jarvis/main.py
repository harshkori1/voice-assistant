import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import os
import musicLibary
import pywhatkit
import pyautogui
from client import ask_ai      # 👈 Now using Mistral
from whatapp import contacts   # WhatsApp contact list


# ✅ Text-to-speech
def speak(text):
    try:
        print("Assistant:", text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Male voice
        engine.setProperty('rate', 175)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech Error:", e)


# ✅ Process Commands
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "play" in c:
        song = c.replace("play", "").strip()
        if song in musicLibary.music:
            speak(f"Playing {song}")
            webbrowser.open(musicLibary.music[song])
        else:
            speak("Song not found in your library")

    elif "send message to" in c:
        try:
            name = c.replace("send message to", "").strip()
            if name in contacts:
                speak(f"What message should I send to {name}?")
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source)
                    message = recognizer.recognize_google(audio)

                speak(f"Sending message to {name}: {message}")
                phone_no = contacts[name]

                webbrowser.open("https://web.whatsapp.com")
                speak("Please wait while I open WhatsApp Web...")
                time.sleep(10)
                pywhatkit.sendwhatmsg_instantly(phone_no, message, wait_time=15, tab_close=False)
                pyautogui.press('enter')
                speak("Message sent successfully.")
            else:
                speak("I don’t have that contact saved.")
        except Exception as e:
            speak("Sorry, I couldn’t send the message.")
            print("Error:", e)

    elif "ask ai" in c or "chat ai" in c:
        question = c.replace("ask ai", "").replace("chat ai", "").strip()
        if question:
            speak("Let me think...")
            answer = ask_ai(question)
            speak(answer)
        else:
            speak("Please say what you want to ask the AI.")

    else:
        speak("Sorry, I didn’t understand that.")


# ✅ Voice Assistant Loop
if __name__ == "__main__":
    speak("Voice assistant activated. Say 'google' to start.")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("🎧 Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "google":
                speak("Yes sir, how can I help you?")
                time.sleep(1)
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("🎙️ Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except Exception as e:
            print("Error:", e)
