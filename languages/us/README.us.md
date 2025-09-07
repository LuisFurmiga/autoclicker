# AutoClicker 2.0

## Multilingual README
Você fala português? Acesse: [![pt](https://img.shields.io/badge/lang-pt-green.svg)](https://github.com/LuisFurmiga/Autoclicker/blob/main/README.md)

¿Hablas español? Accede: [![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/es/README.es.md)

---

## 🚀 Overview
**AutoClicker 2.0** is an advanced tool for automating mouse clicks and keystrokes in specific windows.  
It has been completely rewritten from version 1.0, bringing **multi-profile support, multilingual interface, and new customization options**.

Perfect for games, software testing, and any repetitive task requiring fast and constant interactions with the mouse or keyboard.

---

## ✨ What's New in 2.0
- ✅ **Multiple profiles** stored in `profiles.json`
  - Create, rename, delete, import, and export (single or all profiles).
  - Automatic migration from `settings.json` (legacy) to `profiles.json`.
- ✅ **Reorganized interface (Tkinter)**
  - **Language menu** (Portuguese, English, Spanish).
  - **Profiles menu** (with radiobutton selection and management options).
- ✅ **Full automation**
  - Independent left and right clicks.
  - Send **extra keys**, including combos (`ctrl+c`, `ctrl+shift+tab`, etc.).
- ✅ **Global hotkeys**
  - `F1` → start
  - `F2` → stop
- ✅ **Target window selection**
  - Dropdown shows all currently open windows.
- ✅ **Messages and errors translated** into three languages (i18n).

---

## 📂 Project Structure
```
autoclicker/
│── app.py                 # Entry point
│── controllers/
│   └── app_controller.py  # Main logic
│── models/
│   ├── settings.py        # Profile configuration
│   ├── auto_clicker.py    # Autoclicker implementation
│   └── profiles.py        # Multiple profiles storage
│── views/
│   └── main_window.py     # Tkinter interface
│── profiles.json          # User profiles
│── translations.json      # Translations (pt, en, es)
│── requirements.py        # Automatically installs dependencies
│── README.md              # Main document (PT-BR)
```

---

## ⚙️ Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/LuisFurmiga/autoclicker.git
    ```
2. Access the directory:
    ```sh
    cd autoclicker
    ```
3. If you don’t have Python installed yet, check the guide [Python for Windows](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/us/python_windows.us.md).
4. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
   or use the automatic installer:
    ```sh
    python requirements.py
    ```

---

## 🎮 Usage
1. Run the program:
    ```sh
    python app.py
    ```
2. Choose the **target window** from the dropdown list.
3. Adjust click intervals, hold time, and extra keys.
4. Save your settings into a **profile**.
5. Use:
   - `F1` → **Start**
   - `F2` → **Stop**

---

## 🌐 Supported Languages
- 🇧🇷 Portuguese  
- 🇺🇸 English  
- 🇪🇸 Spanish  

Language can be changed directly in the **menu interface**.

---

## 📤 Profiles
- Create as many as you want.
- Export/import individual profiles or all at once.
- Profiles are saved in `profiles.json`.

---

## 🛠️ Dependencies
- [keyboard](https://pypi.org/project/keyboard/) → global hotkeys  
- [pywin32](https://pypi.org/project/pywin32/) → Windows window & event handling  

---

## ⚠️ Important Notes
- Run as **Administrator** if global hotkeys don’t work inside the game.  
- This program is **Windows-only** because it depends on `pywin32`.  

---

## 📜 License
This project is open-source under the [MIT](https://opensource.org/licenses/MIT) license.
