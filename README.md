# 🤖 Discord AutoReply — AI-Powered Auto Responder

**Discord AutoReply** is a real-time, AI-driven Discord bot that listens to selected channels and auto-replies like a witty, chill human. It's built using Google Gemini's latest model, Discord's WebSocket gateway, and a snappy personality system that makes every response feel human — not robotic.

---

## 🚀 Features

- 🧠 **Gemini AI-Powered Replies**  
  Replies are short, sarcastic, helpful, and totally not robotic. Just like talking to your sharpest friend.

- 🔔 **Smart Notifications + Optional Alarm**  
  Shows a desktop notification and plays an alert sound when someone posts in your watched channels.

- 🧵 **Message Chunking + Typing Indicator**  
  Long replies? Automatically split into clean, natural chunks with typing simulation.

- 🔁 **Live Message Listening (WebSocket)**  
  Monitors messages from specified channels in real-time using Discord’s WebSocket gateway.

- 🛑 **ESC to Cancel Alarm** | **Ctrl+Shift+S to Stop Bot**  
  Escape the audio chaos or gracefully shut down the bot whenever you need to.

---

## 🧩 Tech Stack

- 🐍 Python 3.9+
- 🌐 [Discord Gateway API](https://discord.com/developers/docs/topics/gateway)
- 🧠 [Google Generative AI (Gemini)](https://aistudio.google.com/)
- 🔔 `plyer`, `playsound`, `keyboard` for native desktop interactions

---

## ⚙️ Setup

### 1. Requirements

Install required packages:

```bash
pip install requests websocket-client google-generativeai keyboard plyer playsound
````

### 2. Get Your Tokens

* **Discord User Token** *(⚠️ risky, see warning below)*
* **Google Gemini API Key** – [Get one here](https://aistudio.google.com/app/apikey)

### 3. Configure the Script

Open `main.py` and set:

```python
USER_TOKEN = 'your_discord_token_here'
CHANNEL_IDS = ['your_channel_id_1', 'your_channel_id_2']
GOOGLE_API_KEY = 'your_google_api_key_here'
USER_NAME = 'your_discord_username'
```

You can also change the alert sound (default: `hey_listen.mp3`) and alarm settings.

---

## 🧠 AI Personality

All replies come from a system prompt that makes the AI act like an 18-year-old dev named **Cassius** — chill, witty, sometimes sarcastic, and always human-like.
He answers tech questions, jokes around, gives real advice, and keeps it all super real.

---

## 🚨 Important Warning

> This bot uses a **Discord user token**, which is against [Discord's Terms of Service](https://discord.com/terms).
> Using this may get your account **banned or disabled**. Use it at your own risk and preferably with a throwaway account.

---

## 📌 Hotkeys & Controls

* **ESC** — Stop alarm audio playback
* **Ctrl + Shift + S** — Gracefully shut down the bot

---

## 🛠️ Ideas for Future Features

* [ ] Switch to Discord bot token + OAuth2
* [ ] Web-based control panel
* [ ] Add channel-based AI behavior customization
* [ ] TTS voice replies

---

## 🙏 Credits

* AI model by **Google Gemini**
* Discord API usage via raw WebSocket
* Prompt engineering by the dev (aka you!)
* Audio & UX via `playsound`, `keyboard`, `plyer`

---

## 📄 License

MIT License — free to use, modify, and share.

---

> **Made with ❤️ by Vaibhav Pandey**


