import customtkinter as ctk
import requests
import subprocess
import threading
import os
import sys
import time
import urllib.request

# --- 1. SETUP & UI ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EasyLocalAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("EasyLocalAI - Free Local ChatGPT")
        self.geometry("700x550")
        
        # UI Elements
        self.chat_display = ctk.CTkTextbox(self, width=680, height=400, state="disabled")
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0))
        
        self.input_box = ctk.CTkEntry(self, width=550, placeholder_text="Ask anything...")
        self.input_box.grid(row=1, column=0, padx=10, pady=10)
        
        self.send_btn = ctk.CTkButton(self, text="Send", width=100, command=self.send_message)
        self.send_btn.grid(row=1, column=1, padx=(0, 10), pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="Checking system...")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Run the environment check in the background so the UI doesn't freeze
        threading.Thread(target=self.setup_environment, daemon=True).start()

    # --- 2. OLLAMA INSTALLATION LOGIC ---
    def setup_environment(self):
        self.update_status("Checking if Ollama is installed...")
        
        try:
            # Ping Ollama to see if it's running
            requests.get("http://localhost:11434", timeout=2)
            self.update_status("Ollama is ready. Make sure you have the model downloaded!")
        except requests.exceptions.ConnectionError:
            self.update_status("Ollama not found. Downloading...")
            self.install_ollama()
            self.update_status("Installing Ollama (this may take a minute)...")
            self.run_silent_installer()
            time.sleep(5) # Wait for background service to start
            self.update_status("Downloading AI model (llama3.2)...")
            subprocess.run(["ollama", "pull", "llama3.2"], capture_output=True)
            self.update_status("Setup complete! You can chat.")

    def install_ollama(self):
        url = "https://ollama.com/download/OllamaSetup.exe"
        urllib.request.urlretrieve(url, "OllamaSetup.exe")

    def run_silent_installer(self):
        subprocess.run(["OllamaSetup.exe", "/S"], check=True)
        os.remove("OllamaSetup.exe")

    # --- 3. THE AI CHAT LOGIC (FIXED) ---
    def send_message(self):
        user_text = self.input_box.get()
        if not user_text.strip():
            return
        
        self.input_box.delete(0, "end")
        self.append_chat(f"You: {user_text}\n")
        self.send_btn.configure(state="disabled")
        self.update_status("AI is thinking...")

        # Send the API request in the background so the app doesn't freeze
        threading.Thread(target=self.get_ai_response, args=(user_text,), daemon=True).start()

    def get_ai_response(self, prompt):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2", # The model we want to use
            "prompt": prompt,
            "stream": False      # Wait for the full response before showing it
        }
        
        try:
            response = requests.post(url, json=payload)
            data = response.json()
            
            # THE FIX: Check if Ollama sent an error instead of a response
            if "error" in data:
                ai_text = f"OLLAMA ERROR: {data['error']}"
            else:
                # If no error, get the response text. If somehow missing, show raw data.
                ai_text = data.get("response", f"Raw data: {data}")
                
            self.append_chat(f"AI: {ai_text}\n\n")
        except Exception as e:
            self.append_chat(f"Connection Error: Could not reach Ollama. {e}\n")
        
        self.send_btn.configure(state="normal")
        self.update_status("Ready.")

    # --- 4. HELPER FUNCTIONS ---
    def append_chat(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def update_status(self, text):
        self.status_label.configure(text=text)

if __name__ == "__main__":
    app = EasyLocalAI()
    app.mainloop()