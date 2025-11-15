# 🔐 Local Password Manager (Python)

A simple, secure, and fully local password manager built in Python.  
It uses **AES-256 encryption (Fernet)** and a **master password** derived from PBKDF2-HMAC with SHA-256 to protect all stored credentials.

No cloud. No telemetry. 100% offline.

---

## ✨ Features

- 🔑 **Master password protection**
- 🔐 **PBKDF2-HMAC (SHA-256) key derivation**
- 🔒 **AES-256 encryption** (via Fernet)
- 📁 Secure vault
- ➕ Add new credentials  
- 🔍 Retrieve saved credentials  
- 📃 List all stored sites  
- ❌ Delete saved entries

---

## 🗂 Folder Structure
project/
│── manager.py
│── README.md

When the application runs (or when packaged as EXE), it automatically creates:
├── vault.json
├── salt.bin

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/bichiouyahya/Local-Password-Manager.git
cd Local-Password-Manager
```

### 2. Install required dependencies
pip install cryptography

### 3. Running the App (Python)
python manager.py

📄 License
This project is released under the MIT License.
You are free to use, modify, and distribute it.

🤝 Contributing
Pull requests are welcome.
Open an issue for feature requests or bugs.
