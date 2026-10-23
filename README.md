# EasyLocalAI 🧠💻

A simple, 1-click local AI chat application for Windows. 

Millions of people want to try local AI, but get stuck trying to install Python, configure environments, and download models. **EasyLocalAI** solves this. It is a lightweight desktop app that automatically installs Ollama, downloads the `llama3.2` model, and gives you a beautiful, dark-mode chat interface. 

No subscriptions. No API keys. Your data never leaves your computer.

## ✨ Features

- **1-Click Setup:** Automatically detects if Ollama is installed. If not, it downloads and installs it silently in the background.
- **Auto-Downloads Models:** Automatically pulls the `llama3.2` model so you can chat immediately.
- **Modern UI:** Built with `customtkinter` for a sleek, dark-mode chat experience.
- **100% Private:** All processing is done on your local GPU. No data is sent to OpenAI, Google, or anyone else.
- **Standalone App:** Can be compiled into a single `.exe` that doesn't require Python to be installed.

## 🚀 How to Download & Use

1. Go to the **Releases** tab on the right side of this GitHub page.
2. Download the latest `EasyLocalAI.exe` file.
3. Double-click the `.exe` to open the app.
4. *Note: If you don't have Ollama installed, the app will download and install it automatically. This may take a few minutes depending on your internet speed.*
5. Start chatting!

## 🛠️ How to Run from Source (For Developers)

If you want to run the Python script directly:

1. Clone this repository:
   ```bash
   git clone https://github.com/Qrdz0/EasyLocalAI.git
