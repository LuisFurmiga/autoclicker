import threading
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

from models.settings import Settings
from models.auto_clicker import AutoClicker
from models.profiles import ProfilesStore
from views.main_window import MainWindow


class AppController:
    def __init__(self):
        # Store de perfis (migra settings.json -> profiles.json automaticamente)
        self.store = ProfilesStore()
        active_name, profiles = self.store.load()
        self.settings = self.store.get_active()

        # Service
        self.autoclicker = AutoClicker(self.settings)

        # View
        self.root = tk.Tk()
        self.view = MainWindow(self.root, self.settings, self, profiles_names=self.store.list_names(), active_profile=active_name)

        # Estado
        self._run_lock = threading.Lock()
        self._running = False

    # ============== Ciclo de vida ==============
    def run(self):
        self.view.init_widgets()
        self.view.bind_hotkeys(self.start, self.stop)
        self.view.update_texts()  # i18n
        self.root.mainloop()

    # ============== Ações disparadas pela View ==============
    def start(self, *_):
        with self._run_lock:
            if self._running:
                return
            self._running = True
        self.autoclicker.start(on_error=self._on_error)
        self.view.set_running(True)

    def stop(self, *_):
        with self._run_lock:
            if not self._running:
                return
            self._running = False
        self.autoclicker.stop()
        self.view.set_running(False)

    def update_settings_from_view(self):
        try:
            new_settings = self.view.read_settings()
            # Atualiza o objeto vivo usado pela thread
            self.settings.update_from(new_settings)
            # Salva no perfil ativo
            active = self.view.get_selected_profile_name()
            self.store.upsert(active, self.settings)
            messagebox.showinfo(self.view.t("title_update"), self.view.t("message_update"))
        except ValueError:
            messagebox.showerror(self.view.t("title_error"), self.view.t("message_value_error"))

    def switch_language(self, lang_code: str):
        self.view.set_language(lang_code)
        self.view.update_texts()

    # ---- Perfis ----
    def create_profile(self):
        name = simpledialog.askstring(self.view.t("profile_new_title"), self.view.t("profile_new_prompt"))
        if not name:
            return
        if name in self.store.profiles:
            messagebox.showerror(self.view.t("title_error"), self.view.t("profile_exists"))
            return
        # Baseado no formulário atual
        try:
            base = self.view.read_settings()
        except ValueError:
            base = self.settings
        self.store.upsert(name, base)
        self.view.refresh_profiles(self.store.list_names(), active=name)
        self.switch_profile(name)

    def delete_profile(self):
        name = self.view.get_selected_profile_name()
        try:
            self.store.delete(name)
        except ValueError as e:
            messagebox.showerror(self.view.t("title_error"), str(e))
            return
        self.view.refresh_profiles(self.store.list_names(), active=self.store.active_profile)
        self.switch_profile(self.store.active_profile)

    def rename_profile(self):
        old = self.view.get_selected_profile_name()
        new = simpledialog.askstring(self.view.t("profile_rename_title"), self.view.t("profile_rename_prompt").format(old=old))
        if not new or new == old:
            return
        try:
            self.store.rename(old, new)
        except ValueError as e:
            messagebox.showerror(self.view.t("title_error"), str(e))
            return
        self.view.refresh_profiles(self.store.list_names(), active=new)
        self.switch_profile(new)

    def switch_profile(self, name: str):
        self.store.set_active(name)
        # Atualiza referência de settings usada pelo AutoClicker
        self.settings = self.store.get_active()
        self.autoclicker.settings = self.settings
        # Repreenche formulário
        self.view.fill_from_settings(self.settings)

    def export_profile(self):
        name = self.view.get_selected_profile_name()
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[["JSON", ".json"]], initialfile=f"{name}.json")
        if not path:
            return
        try:
            self.store.export_profile(name, path)
            messagebox.showinfo(self.view.t("export_title"), self.view.t("export_ok"))
        except Exception as e:
            messagebox.showerror(self.view.t("title_error"), str(e))

    def export_all(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[["JSON", ".json"]], initialfile="profiles_export.json")
        if not path:
            return
        try:
            self.store.export_all(path)
            messagebox.showinfo(self.view.t("export_title"), self.view.t("export_ok"))
        except Exception as e:
            messagebox.showerror(self.view.t("title_error"), str(e))

    def import_profiles(self):
        path = filedialog.askopenfilename(filetypes=[["JSON", ".json"]])
        if not path:
            return
        try:
            self.store.import_file(path)
            self.view.refresh_profiles(self.store.list_names(), active=self.store.active_profile)
            messagebox.showinfo(self.view.t("import_title"), self.view.t("import_ok"))
        except Exception as e:
            messagebox.showerror(self.view.t("title_error"), str(e))

    # ============== Callbacks ==============
    def _on_error(self, title: str, msg: str):
        messagebox.showerror(title, msg)
