import tkinter as tk
from tkinter import messagebox, ttk
import json
import keyboard
import threading
import time
import win32gui
import win32api
import win32con

# Inicializa a janela principal do Tkinter
root = tk.Tk()

# Variáveis globais
running = False
target_window_title = "Idle Slayer"
interval = 0.1
hold_time = 0.15
between_clicks = 0.05
translations = {}
current_language = "pt"
default_box_witdh = 20 # Largura padrão das caixas de texto
enable_left_click = tk.BooleanVar(value=True)  # Ativado por padrão
enable_right_click = tk.BooleanVar(value=True)  # Ativado por padrão

def load_translations():
    """Carrega as traduções do arquivo JSON."""
    global translations
    try:
        import sys
        import os

        def resource_path(relative_path):
            """Obter o caminho do recurso, seja no modo desenvolvimento ou empacotado."""
            try:
                # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        # Caminho do JSON ajustado
        with open(resource_path("languages/translations.json"), "r", encoding="utf-8") as file:
            translations = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de tradução 'translations.json' não encontrado!")
        root.quit()

def translate(key):
    """Obtém a tradução para a chave no idioma atual."""
    return translations.get(current_language, {}).get(key, key)

def switch_language(lang):
    """Muda o idioma e atualiza a interface."""
    global current_language
    current_language = lang
    update_labels()

def update_labels():
    """Atualiza os textos das labels, botões e menus na interface."""
    root.title(translate("window_title"))
    label_target_window.config(text=translate("target_window"))
    label_interval.config(text=translate("interval"))
    label_hold_time.config(text=translate("hold_time"))
    label_between_clicks.config(text=translate("between_clicks"))
    label_update.config(text=translate("label_update"))
    button_update.config(text=translate("update"))
    button_start.config(text=translate("start"))
    button_stop.config(text=translate("stop"))
    check_left_click.config(text=translate("left_click"))
    check_right_click.config(text=translate("right_click"))

    # Remove todos os itens do menu antes de recriar
    menu.delete(0, tk.END)  # Limpa completamente o menu principal

    # Recria o menu de idiomas
    new_language_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label=translate("menu_language"), menu=new_language_menu)
    new_language_menu.add_command(label="English", command=lambda: switch_language("en"))
    new_language_menu.add_command(label="Español", command=lambda: switch_language("es"))
    new_language_menu.add_command(label="Português", command=lambda: switch_language("pt"))


def find_window(title):
    """Encontra o handle da janela pelo título."""
    return win32gui.FindWindow(None, title)

def send_click_to_window(hwnd):
    """Envia cliques (esquerdo e direito) para posições específicas na janela."""
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)

        # Clique esquerdo (verifica se está habilitado)
        if enable_left_click.get():
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0x0001)
            time.sleep(hold_time)
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0x0000)

        # Pequeno atraso entre os cliques
        time.sleep(between_clicks)

        # Clique direito (verifica se está habilitado)
        if enable_right_click.get():
            win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 0x0002)
            win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0x0000)

def autoclick():
    """Função principal do autoclicker."""
    global running, interval
    hwnd = find_window(target_window_title)
    if not hwnd:
        messagebox.showerror(translate("title_error"), f"Janela '{target_window_title}' não encontrada!")
        running = False
        return

    while running:
        send_click_to_window(hwnd)
        time.sleep(interval)

def start_autoclicker(event=None):
    """Inicia o autoclicker em uma thread separada."""
    global running
    if not running:
        running = True
        threading.Thread(target=autoclick, daemon=True).start()

def stop_autoclicker(event=None):
    """Para o autoclicker."""
    global running
    running = False

def update_variables():
    """Atualiza as variáveis com os valores da interface."""
    global interval, hold_time, between_clicks, target_window_title
    try:
        interval = float(entry_interval.get())
        hold_time = float(entry_hold_time.get())
        between_clicks = float(entry_between_clicks.get())
        target_window_title = window_combobox.get()  # Pega o texto selecionado no ComboBox
        messagebox.showinfo(translate("title_update"), translate("message_update") + "!")
    except ValueError:
        messagebox.showerror(translate("title_error"), translate("message_value_error"))

def list_open_windows():
    """Retorna a lista de títulos de janelas abertas e visíveis."""
    def enum_windows(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            text = win32gui.GetWindowText(hwnd)
            if text:
                result.append(text)
    results = []
    win32gui.EnumWindows(enum_windows, results)
    return results

########################
# PARTE DA INTERFACE   #
########################
load_translations()

# Lista de janelas abertas
windows_list = list_open_windows()

# Labels e entradas
label_target_window = tk.Label(root, text=translate("target_window"))
label_target_window.grid(row=0, column=0, sticky="w")

# ComboBox das janelas abertas
window_combobox = ttk.Combobox(root, values=windows_list, width=default_box_witdh-2)
window_combobox.set(target_window_title)  # valor padrão
window_combobox.grid(row=0, column=1, padx=5, pady=5)

label_interval = tk.Label(root, text=translate("interval"))
label_interval.grid(row=1, column=0, sticky="w")
entry_interval = tk.Entry(root, width=default_box_witdh)
entry_interval.insert(0, str(interval))
entry_interval.grid(row=1, column=1)

label_hold_time = tk.Label(root, text=translate("hold_time"))
label_hold_time.grid(row=2, column=0, sticky="w")
entry_hold_time = tk.Entry(root, width=default_box_witdh)
entry_hold_time.insert(0, str(hold_time))
entry_hold_time.grid(row=2, column=1)

label_between_clicks = tk.Label(root, text=translate("between_clicks"))
label_between_clicks.grid(row=3, column=0, sticky="w")
entry_between_clicks = tk.Entry(root, width=default_box_witdh)
entry_between_clicks.insert(0, str(between_clicks))
entry_between_clicks.grid(row=3, column=1)

# Caixas de seleção para habilitar/desabilitar botões do mouse
check_left_click = tk.Checkbutton(root, text=translate("left_click"), variable=enable_left_click)
check_left_click.grid(row=4, column=0, sticky="w", padx=5, pady=5)

check_right_click = tk.Checkbutton(root, text=translate("right_click"), variable=enable_right_click)
check_right_click.grid(row=4, column=1, sticky="w", padx=5, pady=5)

label_update = tk.Label(root, text=translate("label_update"))
label_update.grid(row=5, column=0, sticky="w")

# Botões
button_update = tk.Button(root, text=translate("update"), command=update_variables, width=default_box_witdh)
button_update.grid(row=5, column=1, pady=5)

button_start = tk.Button(root, text=translate("start"), command=start_autoclicker)
button_start.grid(row=6, column=0, pady=5)

button_stop = tk.Button(root, text=translate("stop"), command=stop_autoclicker)
button_stop.grid(row=6, column=1, columnspan=2, pady=5)

# Menu de idiomas
menu = tk.Menu(root)
root.config(menu=menu)

# Atalhos de teclado dentro da janela Tkinter
root.bind("<F1>", start_autoclicker)
root.bind("<F2>", stop_autoclicker)

########################
# PARTE DOS HOTKEYS    #
########################
# Esses hotkeys funcionam GLOBALMENTE, independente de foco
try:
    import keyboard
    
    def hotkey_start():
        start_autoclicker()

    def hotkey_stop():
        stop_autoclicker()

    # Teclas globais
    keyboard.add_hotkey('F1', hotkey_start)
    keyboard.add_hotkey('F2', hotkey_stop)

    print(translate("important"))
except ImportError:
    print(translate("import_error_keyboard"))

# Atualiza os textos da interface
update_labels()

# Iniciar interface
root.mainloop()
