import tkinter as tk
from tkinter import messagebox, ttk
import keyboard
import threading
import time
import win32gui
import win32api
import win32con

# Variáveis globais
running = False
target_window_title = "Idle Slayer"
interval = 0.1
hold_time = 0.15
between_clicks = 0.05

default_box_witdh = 20

def find_window(title):
    """Encontra o handle da janela pelo título."""
    return win32gui.FindWindow(None, title)

def send_click_to_window(hwnd):
    """Envia cliques (esquerdo e direito) para posições específicas na janela."""
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)

        # Clique esquerdo
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0x0001)
        time.sleep(hold_time)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0x0000)

        # Pequeno atraso entre os cliques
        time.sleep(between_clicks)

        # Clique direito
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 0x0002)
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0x0000)

def autoclick():
    """Função principal do autoclicker."""
    global running, interval
    hwnd = find_window(target_window_title)
    if not hwnd:
        messagebox.showerror("Erro", f"Janela '{target_window_title}' não encontrada!")
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
        messagebox.showinfo("Atualizado", "Configurações atualizadas com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

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
root = tk.Tk()
root.title("Autoclicker")

# Lista de janelas abertas
windows_list = list_open_windows()

# Labels e entradas
tk.Label(root, text="Título da Janela:").grid(row=0, column=0, sticky="w")

# ComboBox das janelas abertas
window_combobox = ttk.Combobox(root, values=windows_list, width=default_box_witdh-2)
window_combobox.set(target_window_title)  # valor padrão
window_combobox.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Intervalo (segundos):").grid(row=1, column=0, sticky="w")
entry_interval = tk.Entry(root, width=default_box_witdh)
entry_interval.insert(0, str(interval))
entry_interval.grid(row=1, column=1)

tk.Label(root, text="Tempo de clique (segundos):").grid(row=2, column=0, sticky="w")
entry_hold_time = tk.Entry(root, width=default_box_witdh)
entry_hold_time.insert(0, str(hold_time))
entry_hold_time.grid(row=2, column=1)

tk.Label(root, text="Intervalo entre os botões (segundos):").grid(row=3, column=0, sticky="w")
entry_between_clicks = tk.Entry(root, width=default_box_witdh)
entry_between_clicks.insert(0, str(between_clicks))
entry_between_clicks.grid(row=3, column=1)

tk.Label(root, text="Clique no botão ao lado para ").grid(row=4, column=0, sticky="w")

# Botões
tk.Button(root, text="Atualizar Configurações", command=update_variables, width=default_box_witdh).grid(row=4, column=1, pady=5)
tk.Button(root, text="Iniciar (F1)", command=start_autoclicker).grid(row=5, column=0, pady=5)
tk.Button(root, text="Parar (F2)", command=stop_autoclicker).grid(row=5, column=1, columnspan=2, pady=5)

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
        print("Autoclicker iniciado via hotkey global (F1)")

    def hotkey_stop():
        stop_autoclicker()
        print("Autoclicker parado via hotkey global (F2)")

    # Teclas globais
    keyboard.add_hotkey('F1', hotkey_start)
    keyboard.add_hotkey('F2', hotkey_stop)

    print("Hotkeys globais F1 e F2 registrados com sucesso.")
    print("Se não funcionarem no jogo, tente executar o script como administrador ou o jogo pode estar bloqueando.")
except ImportError:
    print("Biblioteca 'keyboard' não instalada. Rode 'pip install keyboard' para ter hotkeys globais.")

# Iniciar interface
root.mainloop()
