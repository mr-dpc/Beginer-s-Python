import speech_recognition as sr
import pyttsx3
import random
import socket
import subprocess
from datetime import datetime
from database import hay  # Import hay list from the database module
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Constants for commands
COMMAND_JARVIS_SLEEP = 'jarvis sleep'
COMMAND_DATE_TIME = 'date'
COMMAND_IP_ADDRESS = 'ip'
COMMAND_HOW_ARE_YOU = 'how are you'
COMMAND_WIFI = 'wifi'
COMMAND_INC_VOLUME = 'increase volume'
COMMAND_DEC_VOLUME = 'decrease volume'
COMMAND_MUTE_VOLUME = 'mute'
COMMAND_SHUTDOWN = 'shutdown'
COMMAND_RESTART = 'restart'
COMMAND_LOG_OFF = 'log off'
COMMAND_OPEN_NOTEPAD = 'open notepad'
COMMAND_OPEN_CALCULATOR = 'open calculator'
COMMAND_JARVIS_EXIT = 'jarvis exit'

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize text-to-speech and speech recognition
def initialize_text_to_speech():
    try:
        engine.setProperty('rate', 150)
    except pyttsx3.PyTTSError as e:
        logging.error(f"Error initializing pyttsx3: {e}")
        exit()

def initialize_speech_recognition():
    return sr.Recognizer()

def recognize_audio(prompt):
    with sr.Microphone() as source:
        logging.info(prompt)
        engine.say(prompt)
        engine.runAndWait()

        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.UnknownValueError:
            logging.warning("Sorry, could not understand audio.")
            engine.say("Sorry, I couldn't understand that. Can you please repeat?")
            engine.runAndWait()
            return None

        return audio

def recognize_start_word():
    return recognize_audio("Please tell the start word...")

def recognize_speech():
    return recognize_audio("Listening for commands...")

def run_jarvis():
    while True:
        command_audio = recognize_speech()
        if command_audio:
            try:
                command_text = recognizer.recognize_google(command_audio).lower()
            except sr.UnknownValueError:
                logging.warning("Sorry, could not understand audio.")
                engine.say("Sorry, I couldn't understand that. Can you please repeat?")
                engine.runAndWait()
                continue

            if COMMAND_JARVIS_SLEEP in command_text:
                logging.info("Jarvis is sleeping...")
                engine.say("Jarvis is sleeping now. Wake me up when you need assistance.")
                engine.runAndWait()
                break
            elif COMMAND_DATE_TIME in command_text:
                say_date()
            elif COMMAND_IP_ADDRESS in command_text:
                ip_address()
            elif COMMAND_HOW_ARE_YOU in command_text:
                hay_response()
            elif COMMAND_WIFI in command_text:
                get_wifi_networks()
            elif COMMAND_INC_VOLUME in command_text:
                increase_volume()
            elif COMMAND_DEC_VOLUME in command_text:
                decrease_volume()
            elif COMMAND_MUTE_VOLUME in command_text:
                mute_volume()
            elif COMMAND_SHUTDOWN in command_text:
                shutdown_pc()
            elif COMMAND_RESTART in command_text:
                restart_pc()
            elif COMMAND_LOG_OFF in command_text:
                logoff_pc()
            elif COMMAND_OPEN_NOTEPAD in command_text:
                open_app('notepad.exe')
            elif COMMAND_OPEN_CALCULATOR in command_text:
                open_app('calc.exe')
            elif COMMAND_JARVIS_EXIT in command_text:
                logging.info("Exiting Jarvis...")
                engine.say("Exiting Jarvis. Goodbye!")
                engine.runAndWait()
                break

def say_date():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    engine.say(dt)
    engine.runAndWait()

def ip_address():
    local = socket.gethostbyname(socket.gethostname())
    engine.say(local)
    engine.runAndWait()

def hay_response():
    choke = random.choice(hay)
    engine.say(choke)
    engine.runAndWait()

def get_wifi_networks():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'network'], capture_output=True, text=True)
        networks = result.stdout
        logging.info("Available Wi-Fi Networks:")
        logging.info(networks)
        engine.say("Here are the available Wi-Fi networks:")
        engine.say(networks)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error getting Wi-Fi networks: {e}")

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def increase_volume():
    set_volume(1.0)  # Set to 100%
    logging.info("Volume increased")

def decrease_volume():
    set_volume(0.5)  # Set to 50%
    logging.info("Volume decreased")

def mute_volume():
    set_volume(0.0)  # Mute
    logging.info("Volume muted")

def shutdown_pc():
    try:
        subprocess.run(['shutdown', '/s', '/t', '1'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error shutting down the PC: {e}")

def restart_pc():
    try:
        subprocess.run(['shutdown', '/r', '/t', '1'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error restarting the PC: {e}")

def logoff_pc():
    try:
        subprocess.run(['shutdown', '/l'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error logging off the PC: {e}")

def open_app(app_name):
    try:
        subprocess.run([app_name], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error opening the app: {e}")

if __name__ == "__main__":
    initialize_text_to_speech()
    initialize_speech_recognition()

    while True:
        start_word_audio = recognize_start_word()
        if start_word_audio:
            try:
                start_word_text = recognizer.recognize_google(start_word_audio).lower()
            except sr.UnknownValueError:
                logging.warning("Sorry, could not understand audio or the start word was not recognized.")
                engine.say("Sorry, could not recognize the start word. Please try again.")
                engine.runAndWait()
                continue

            if 'jarvis on' in start_word_text:
                logging.info("Jarvis activated!")
                engine.say("Jarvis activated! Please give me commands.")
                engine.runAndWait()
                run_jarvis()
                break
            else:
                logging.warning("Incorrect start word. Please try again.")
                engine.say("Incorrect start word. Please try again.")
                engine.runAndWait()
