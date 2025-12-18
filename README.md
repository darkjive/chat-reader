# WhatsApp Chat Exporter

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python script to export the chat history of a specific contact or group from WhatsApp Web using Selenium.

---

### ⚠️ Disclaimer & Important Warnings

*   **For Educational & Personal Use Only:** This script is intended for personal use to back up your own chat data. Do not use it for any other purpose.
*   **Requires Debug Mode:** This script works by remotely controlling your browser. This requires you to start Chrome in a special "remote debugging" mode, which grants the script significant control over your browser session.
*   **Brittle by Nature:** The script relies on the internal HTML structure of WhatsApp Web. WhatsApp can (and does) update its website frequently, which will likely break this script. Future updates will be required to keep it working.
*   **Use a Temporary Profile:** The instructions below use a temporary browser profile to avoid interfering with your main browser data and for better security.

---

### ✨ Features

*   Connects to an existing Chrome session.
*   Searches for a specified contact or group.
*   Automatically scrolls up to the beginning of the chat to load the entire history.
*   Extracts all messages and prints them to the console.
*   Saves a full copy of the chat to `exported_chat.txt`.

---

### ⚙️ Prerequisites

*   Python 3.7+
*   Google Chrome browser

---

### 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd chat-reader
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS & Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

###  kullanım

1.  **Edit the Script:**
    Open the `whatsapp_reader.py` file and change the `CONTACT_NAME` variable to the exact name of the contact or group you want to export.

    ```python
    # whatsapp_reader.py
    CONTACT_NAME = "John Doe" # <-- Change this
    ```

2.  **Close All Chrome Instances:**
    This is crucial for the next step to work correctly.

3.  **Start Chrome in Debug Mode:**
    Open a terminal and run the appropriate command for your operating system. This will open a new, temporary Chrome window.

    *   **On Linux:**
        ```bash
        google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-dev-session"
        ```
    *   **On macOS:**
        ```bash
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-dev-session"
        ```
    *   **On Windows:**
        ```cmd
        "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-dev-session"
        ```

4.  **Log into WhatsApp Web:**
    In the new Chrome window that just opened, navigate to `web.whatsapp.com` and log in by scanning the QR code with your phone. Wait for your chats to load completely.

5.  **Run the Script:**
    Go back to your terminal (where the virtual environment is activated) and run the script:
    ```bash
    python whatsapp_reader.py
    ```

The script will now take over, find the chat, scroll through its history, and print all messages to the console. A file named `exported_chat.txt` will be created with the full chat log.

---

### 🤝 Contributing

Contributions are welcome! If you want to improve the script, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Some ideas for improvement:
*   Make XPaths more robust.
*   Add error handling for more edge cases.
*   Export to different formats (JSON, CSV).
*   Add a simple GUI.

---

### 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
