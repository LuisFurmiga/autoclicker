from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import win32gui

from models.settings import Settings, resource_path


class MainWindow:
    def __init__(self, root: tk.Tk, settings: Settings, controller, profiles_names=None, active_profile: str | None = None):
        self.root = root
        self.settings = settings
        self.controller = controller

        self.root.title("AutoClicker")

        # i18n
        self.translations = {}
        self.current_language = settings.language or "pt"
        self._load_translations()

        # Perfis (agora via MENU, não mais via combobox na tela)
        self.profile_var = tk.StringVar(value=active_profile or "Default")
        self.profile_names = profiles_names or ["Default"]

        # widgets (somente os de configuração principal)
        self.window_combobox: ttk.Combobox | None = None
        self.entry_interval: tk.Entry | None = None
        self.entry_hold_time: tk.Entry | None = None
        self.entry_between_clicks: tk.Entry | None = None
        self.var_left = tk.BooleanVar(value=self.settings.enable_left_click)
        self.var_right = tk.BooleanVar(value=self.settings.enable_right_click)
        self.entry_keys: tk.Entry | None = None
        self.btn_update: tk.Button | None = None
        self.btn_start: tk.Button | None = None
        self.btn_stop: tk.Button | None = None
        self.menu_bar: tk.Menu | None = None
        self.menu_profiles: tk.Menu | None = None

    # ============== Infra ==============
    def _load_translations(self):
        path = resource_path("languages/translations.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de tradução 'translations.json' não encontrado!")
            self.root.quit()

    def t(self, key: str) -> str:
        return self.translations.get(self.current_language, {}).get(key, key)

    def set_language(self, lang: str):
        self.current_language = lang

    # ============== Construção da UI ==============
    def init_widgets(self):
        pad = {"padx": 6, "pady": 6}

        # ---- Campos principais (sem seção de perfis) ----
        tk.Label(self.root, text=self.t("target_window")).grid(row=0, column=0, sticky="w", **pad)
        self.window_combobox = ttk.Combobox(self.root, values=self._list_open_windows(), width=28)
        self.window_combobox.set(self.settings.target_window_title)
        self.window_combobox.grid(row=0, column=1, sticky="we", **pad)

        tk.Label(self.root, text=self.t("interval")).grid(row=1, column=0, sticky="w", **pad)
        self.entry_interval = tk.Entry(self.root, width=30)
        self.entry_interval.insert(0, str(self.settings.interval))
        self.entry_interval.grid(row=1, column=1, **pad)

        tk.Label(self.root, text=self.t("hold_time")).grid(row=2, column=0, sticky="w", **pad)
        self.entry_hold_time = tk.Entry(self.root, width=30)
        self.entry_hold_time.insert(0, str(self.settings.hold_time))
        self.entry_hold_time.grid(row=2, column=1, **pad)

        tk.Label(self.root, text=self.t("between_clicks")).grid(row=3, column=0, sticky="w", **pad)
        self.entry_between_clicks = tk.Entry(self.root, width=30)
        self.entry_between_clicks.insert(0, str(self.settings.between_clicks))
        self.entry_between_clicks.grid(row=3, column=1, **pad)

        tk.Checkbutton(self.root, text=self.t("left_click"), variable=self.var_left).grid(row=4, column=0, sticky="w", **pad)
        tk.Checkbutton(self.root, text=self.t("right_click"), variable=self.var_right).grid(row=4, column=1, sticky="w", **pad)

        tk.Label(self.root, text=self.t("additional_keys")).grid(row=5, column=0, sticky="w", **pad)
        self.entry_keys = tk.Entry(self.root, width=30)
        self.entry_keys.insert(0, ", ".join(self.settings.extra_keys))
        self.entry_keys.grid(row=5, column=1, **pad)
        tk.Label(self.root, text=self.t("keys_hint")).grid(row=6, column=0, columnspan=2, sticky="w", **pad)

        self.btn_update = tk.Button(self.root, text=self.t("update"), command=self.controller.update_settings_from_view, width=30)
        self.btn_update.grid(row=7, column=0, **pad)
        self.btn_start = tk.Button(self.root, text=self.t("start"), command=self.controller.start, width=30)
        self.btn_start.grid(row=7, column=1, **pad)
        self.btn_stop = tk.Button(self.root, text=self.t("stop"), command=self.controller.stop, width=30)
        self.btn_stop.grid(row=8, column=0, columnspan=2, **pad)

        # ---- Menu (Idioma + Perfil) ----
        self.menu_bar = tk.Menu(self.root)

        # Menu Idioma
        lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        lang_menu.add_command(label="English", command=lambda: self.controller.switch_language("en"))
        lang_menu.add_command(label="Español", command=lambda: self.controller.switch_language("es"))
        lang_menu.add_command(label="Português", command=lambda: self.controller.switch_language("pt"))
        self.menu_bar.add_cascade(label=self.t("menu_language"), menu=lang_menu)

        # Menu Perfil (com submenu de seleção por radiobutton)
        self.menu_profiles = tk.Menu(self.menu_bar, tearoff=0)
        self._rebuild_profile_menu()
        self.menu_bar.add_cascade(label=self.t("menu_profile"), menu=self.menu_profiles)

        self.root.config(menu=self.menu_bar)
        self.root.title(self.t("window_title"))

    def _rebuild_profile_menu(self):
        # Limpa e recria opções do menu de perfis
        self.menu_profiles.delete(0, tk.END) if self.menu_profiles.index("end") is not None else None

        # Seletor (submenu com radiobuttons)
        select_menu = tk.Menu(self.menu_profiles, tearoff=0)
        for name in self.profile_names:
            select_menu.add_radiobutton(
                label=name,
                variable=self.profile_var,
                value=name,
                command=lambda n=name: self.controller.switch_profile(n)
            )
        self.menu_profiles.add_cascade(label=self.t("profile_select"), menu=select_menu)
        self.menu_profiles.add_separator()

        # Ações
        self.menu_profiles.add_command(label=self.t("profile_new"), command=self.controller.create_profile)
        self.menu_profiles.add_command(label=self.t("profile_rename"), command=self.controller.rename_profile)
        self.menu_profiles.add_command(label=self.t("profile_delete"), command=self.controller.delete_profile)
        self.menu_profiles.add_separator()
        self.menu_profiles.add_command(label=self.t("export_one"), command=self.controller.export_profile)
        self.menu_profiles.add_command(label=self.t("export_all"), command=self.controller.export_all)
        self.menu_profiles.add_command(label=self.t("import_any"), command=self.controller.import_profiles)

    def update_texts(self):
        # Atualiza rótulos principais
        self.root.title(self.t("window_title"))
        widgets = {
            (0, 0): self.t("target_window"),
            (1, 0): self.t("interval"),
            (2, 0): self.t("hold_time"),
            (3, 0): self.t("between_clicks"),
            (4, 0): self.t("left_click"),
            (4, 1): self.t("right_click"),
            (5, 0): self.t("additional_keys"),
            (6, 0): self.t("keys_hint"),
        }
        for (row, col), text in widgets.items():
            w = self._get_label_at(row, col)
            if isinstance(w, tk.Label):
                w.config(text=text)
        if self.btn_update:
            self.btn_update.config(text=self.t("update"))
        if self.btn_start:
            self.btn_start.config(text=self.t("start"))
        if self.btn_stop:
            self.btn_stop.config(text=self.t("stop"))

        # Atualiza labels dos menus
        self.init_menu_only()

    def init_menu_only(self):
        # Recria toda a barra para refrescar traduções
        self.menu_bar = tk.Menu(self.root)
        # Idioma
        lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        lang_menu.add_command(label="English", command=lambda: self.controller.switch_language("en"))
        lang_menu.add_command(label="Español", command=lambda: self.controller.switch_language("es"))
        lang_menu.add_command(label="Português", command=lambda: self.controller.switch_language("pt"))
        self.menu_bar.add_cascade(label=self.t("menu_language"), menu=lang_menu)
        # Perfil
        self.menu_profiles = tk.Menu(self.menu_bar, tearoff=0)
        self._rebuild_profile_menu()
        self.menu_bar.add_cascade(label=self.t("menu_profile"), menu=self.menu_profiles)
        self.root.config(menu=self.menu_bar)

    def _get_label_at(self, row, col):
        for w in self.root.grid_slaves(row=row, column=col):
            return w
        return None

    def set_running(self, is_running: bool):
        state = tk.DISABLED if is_running else tk.NORMAL
        for w in [self.window_combobox, self.entry_interval, self.entry_hold_time, self.entry_between_clicks, self.entry_keys, self.btn_update]:
            if w is not None:
                w.config(state=state)
        if self.btn_start:
            self.btn_start.config(state=tk.DISABLED if is_running else tk.NORMAL)
        if self.btn_stop:
            self.btn_stop.config(state=tk.NORMAL if is_running else tk.DISABLED)

    def read_settings(self) -> Settings:
        interval = float(self.entry_interval.get())
        hold_time = float(self.entry_hold_time.get())
        between = float(self.entry_between_clicks.get())
        title = self.window_combobox.get()
        keys_raw = self.entry_keys.get() or ""
        keys = [k.strip() for k in keys_raw.split(",") if k.strip()]
        s = Settings(
            target_window_title=title,
            interval=interval,
            hold_time=hold_time,
            between_clicks=between,
            enable_left_click=self.var_left.get(),
            enable_right_click=self.var_right.get(),
            extra_keys=keys,
            language=self.current_language,
        )
        return s

    def bind_hotkeys(self, start_cb, stop_cb):
        self.root.bind("<F1>", start_cb)
        self.root.bind("<F2>", stop_cb)
        try:
            import keyboard
            keyboard.add_hotkey('F1', lambda: start_cb(None))
            keyboard.add_hotkey('F2', lambda: stop_cb(None))
            print(self.t("important"))
        except Exception:
            print(self.t("import_error_keyboard"))

    def _list_open_windows(self):
        results = []
        def enum_windows(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                text = win32gui.GetWindowText(hwnd)
                if text:
                    results.append(text)
        win32gui.EnumWindows(enum_windows, None)
        return results

    # ---- Perfis (helpers) ----
    def get_selected_profile_name(self) -> str:
        return self.profile_var.get() or "Default"

    def refresh_profiles(self, names, active: str | None = None):
        self.profile_names = names
        if active:
            self.profile_var.set(active)
        self._rebuild_profile_menu()

    def fill_from_settings(self, s: Settings):
        self.window_combobox.set(s.target_window_title)
        self.entry_interval.delete(0, tk.END)
        self.entry_interval.insert(0, str(s.interval))
        self.entry_hold_time.delete(0, tk.END)
        self.entry_hold_time.insert(0, str(s.hold_time))
        self.entry_between_clicks.delete(0, tk.END)
        self.entry_between_clicks.insert(0, str(s.between_clicks))
        self.var_left.set(s.enable_left_click)
        self.var_right.set(s.enable_right_click)
        self.entry_keys.delete(0, tk.END)
        self.entry_keys.insert(0, ", ".join(s.extra_keys))
