# main.py
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import ollama
import os
import traceback
from datetime import datetime

# --- SETUP ---

# Initialize Recognizer and Text-to-Speech Engine
recognizer = sr.Recognizer()
# Explicitly initialize the engine with the 'sapi5' driver for Windows stability
engine = pyttsx3.init('sapi5')

# --- Control Speech Rate ---
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

# This helps the recognizer adapt to changing noise levels
recognizer.dynamic_energy_threshold = True

# --- CORE FUNCTIONS ---

def speak(text):
    """
    Converts text to speech using the fast, offline pyttsx3 engine.
    """
    if not text:
        return
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def get_ai_response(prompt):
    """
    Gets a short response from the local Ollama AI for general queries.
    """
    try:
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant named Jarvis. Keep your answers brief.'},
            {'role': 'user', 'content': prompt},
        ]
        response = ollama.chat(model='llama3', messages=messages)
        return response['message']['content']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "I'm having trouble connecting to my local AI services. Make sure Ollama is running."

def get_news_summary():
    """
    Uses the local AI to generate a summary of today's news.
    """
    print("Generating news summary with local AI...")
    today = datetime.now().strftime("%A, %B %d, %Y")
    prompt = f"Please act as a news anchor. Provide a brief summary of 3 major world news headlines for today, {today}. Keep it concise."
    return get_ai_response(prompt)

def process_command(command):
    """
    Processes the user's command.
    """
    command = command.lower()

    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    elif "play" in command:
        try:
            song_name = command.split("play", 1)[1].strip()
            if song_name in musicLibrary.music:
                speak(f"Playing {song_name}.")
                link = musicLibrary.music[song_name]
                webbrowser.open(link)
            else:
                speak(f"Sorry, I don't have '{song_name}' in my library.")
        except IndexError:
            speak("What song would you like me to play?")
    elif "news" in command:
        speak("Getting a news summary from my local intelligence.")
        news = get_news_summary()
        speak(news)
    else:
        speak("One moment...")
        ai_answer = get_ai_response(command)
        speak(ai_answer)

# --- MAIN LOOP ---

if __name__ == "__main__":
    speak("Initializing Jarvis. System running locally.")
    
    with sr.Microphone() as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibration complete.")

    speak("Awaiting your command, sir.")

    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            
            word = recognizer.recognize_google(audio)
            print(f"User said: {word}")

            if "jarvis" in word.lower():
                speak("Yes?")
                try:
                    with sr.Microphone() as source:
                        print("Listening for your command...")
                        audio_command = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        
                        command = recognizer.recognize_google(audio_command)
                        print(f"User command: {command}")
                        
                        process_command(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that. Could you please repeat your command?")
                except sr.WaitTimeoutError:
                    speak("I'm waiting for your command.")

        except sr.UnknownValueError:
            print("INFO: Could not understand audio for wake word.")
        except sr.WaitTimeoutError:
            print("INFO: No speech detected for wake word.")
        except Exception as e:
            print("An unexpected error occurred in the main loop:")
            traceback.print_exc()