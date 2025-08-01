# Jarvis Project

Jarvis is a voice-activated personal assistant built using Python. It can perform various tasks such as opening websites, playing music, fetching news, and more.
and the best part of this project is it runs completely locally that is private and requires no API keys 

## Features
- Voice recognition using `speech_recognition`.
- Text-to-speech functionality using `gTTS` and `playsound`.
- Open popular websites like Google, Facebook, LinkedIn, and YouTube.
- Play songs from a predefined music library.
- Fetch and read out the latest news headlines.

## Requirements
Make sure you have installed ollama and downloaded 'llama3' model locally, Although you can use any other models if you have.

Install the required Python libraries using the following command:
```bash
pip install -r requirements.txt
```

## How to Run
1. Ensure you have a working microphone connected to your system.
2. Run the `main.py` file:

```bash
python main.py
```

3. Say "Jarvis" to activate the assistant and give commands like:
   - "Open Google"
   - "Play [song name]"
   - "News"

## Note
- Ensure you have an active internet connection for voice recognition and fetching news.
- Update the `musicLibrary.py` file with your own music links.

## License
This project is licensed under the MIT License.
