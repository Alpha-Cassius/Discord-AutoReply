import json
import re
import time
import threading
import requests
import websocket
import google.generativeai as genai
import keyboard
from playsound import playsound
from plyer import notification

# ================== CONFIG ==================
USER_TOKEN = 'your_discord_token_here'
CHANNEL_IDS = ['your_channel_id_1', 'your_channel_id_2']
USER_NAME = 'your_discord_username'
GOOGLE_API_KEY = 'your_google_api_key_here'
ALARM_ENABLED = True
ALARM_PLAYING = False
SYS_PROMPT = """
You are Cassius (18 years old guy)...
[ADD YOUR HUMAN PERSONALITY]
"""

# =============== INIT SETUP ================
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-2.0-flash-exp', system_instruction=SYS_PROMPT)
chat = model.start_chat()
stop_event = threading.Event()
heartbeat_interval = None


# =============== UTILITY FUNCTIONS ===============
def send_notification(title: str, body: str):
    notification.notify(app_name="Discord", ticker="Discord Bot", title=title, message=body, timeout=6)


def get_gateway_url():
    headers = {'Authorization': USER_TOKEN}
    response = requests.get('https://discord.com/api/v9/gateway', headers=headers)
    response.raise_for_status()
    data = response.json()
    return f"{data['url']}?v=9&encoding=json"


def split_into_sentences(text: str):
    return re.split(r'(?<=[.!?])\s+', text.strip())


def play_audio_threaded(file_path="hey_listen.mp3", num_times=10):
    def _play_audio():
        global ALARM_PLAYING
        try:
            for _ in range(num_times):
                if keyboard.is_pressed('esc'):
                    print("Escape key pressed. Stopping audio playback.")
                    break
                playsound(file_path, block=True)
        except Exception as e:
            print(f"Audio playback error: {e}")
        finally:
            ALARM_PLAYING = False

    threading.Thread(target=_play_audio, daemon=True).start()


# ============== CHAT FUNCTION ===============
def generate_reply(user_input: str):
    safety_settings = {
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL': 'BLOCK_NONE',
        'DANGEROUS': 'BLOCK_NONE'
    }
    response = chat.send_message(user_input, safety_settings=safety_settings)
    return response.text


def send_message(channel_id: str, message: str):
    headers = {'Authorization': USER_TOKEN}
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    typing_url = f"https://discord.com/api/v9/channels/{channel_id}/typing"

    reply = generate_reply(message)
    sentences = split_into_sentences(reply)

    # Chunking response into manageable pieces
    chunks = []
    buffer = ""
    for sentence in sentences:
        buffer = sentence if not buffer else f"{buffer} {sentence}"
        chunks.append(buffer.strip())
        buffer = ""
    if buffer:
        chunks.append(buffer.strip())

    for chunk in chunks:
        requests.post(typing_url, headers=headers)
        print(f"Typing in {channel_id}: {chunk}")
        payload = {'content': chunk}
        response = requests.post(url, json=payload, headers=headers)
        print(f"Sent ({response.status_code}): {response.text}")
        time.sleep(1.5)


# ============= DISCORD GATEWAY EVENTS =============
def heartbeat(ws):
    while not stop_event.is_set():
        ws.send(json.dumps({"op": 1, "d": None}))
        time.sleep(heartbeat_interval / 1000)


def on_message(ws, message):
    global heartbeat_interval, ALARM_ENABLED, ALARM_PLAYING

    try:
        data = json.loads(message)
        op_code = data.get('op')
        event_name = data.get('t')
        event_data = data.get('d')

        if op_code == 10:
            heartbeat_interval = event_data['heartbeat_interval']
            threading.Thread(target=heartbeat, args=(ws,), daemon=True).start()

        elif op_code == 0 and event_name == 'MESSAGE_CREATE':
            channel_id = event_data.get('channel_id')
            if channel_id in CHANNEL_IDS:
                author = event_data.get('author', {})
                username = author.get('username')
                if username != USER_NAME:
                    content = event_data.get('content')
                    send_notification(title=f"{username} in #{channel_id}", body=content)
                    send_message(channel_id, content)

                    if ALARM_ENABLED and not ALARM_PLAYING:
                        ALARM_PLAYING = True
                        play_audio_threaded()
                        ALARM_ENABLED = False

    except Exception as e:
        print("Error in on_message:", e)


def on_open(ws):
    print("Connected to Discord Gateway")
    payload = {
        "op": 2,
        "d": {
            "token": USER_TOKEN,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": "pc"
            },
            "compress": False,
            "large_threshold": 250,
            "presence": {
                "status": "online",
                "afk": False
            }
        }
    }
    ws.send(json.dumps(payload))


def on_error(ws, error):
    print("WebSocket error:", error)


def on_close(ws, *_):
    print("WebSocket closed")


# ============== MAIN BOT LOOP ==============
def start_bot():
    try:
        ws = websocket.WebSocketApp(
            get_gateway_url(),
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        threading.Thread(target=ws.run_forever, daemon=True).start()

        print(f"Bot running. Watching channels: {CHANNEL_IDS}. Press Ctrl + Shift + S to stop.")
        while not stop_event.is_set():
            if keyboard.is_pressed("ctrl+shift+s"):
                print("Shutdown command received.")
                stop_event.set()
            time.sleep(0.5)

    except Exception as e:
        print("Bot encountered an error:", e)


if __name__ == "__main__":
    start_bot()
