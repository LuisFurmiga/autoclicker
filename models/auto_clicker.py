# models/auto_clicker.py
import threading
import time
from typing import Callable, Optional

import win32api
import win32con
import win32gui

from .settings import Settings

_VK_BY_NAME = {
    "enter": win32con.VK_RETURN,
    "return": win32con.VK_RETURN,
    "tab": win32con.VK_TAB,
    "space": win32con.VK_SPACE,
    "esc": win32con.VK_ESCAPE,
    "escape": win32con.VK_ESCAPE,
    "backspace": win32con.VK_BACK,
    "up": win32con.VK_UP,
    "down": win32con.VK_DOWN,
    "left": win32con.VK_LEFT,
    "right": win32con.VK_RIGHT,
    "delete": win32con.VK_DELETE,
    "home": win32con.VK_HOME,
    "end": win32con.VK_END,
    "pageup": win32con.VK_PRIOR,
    "pagedown": win32con.VK_NEXT,
    "lshift": win32con.VK_LSHIFT, "rshift": win32con.VK_RSHIFT,
    "lctrl":  win32con.VK_LCONTROL, "rctrl":  win32con.VK_RCONTROL,
    "lalt":   win32con.VK_LMENU,    "ralt":   win32con.VK_RMENU,
}

_MOD_VK = {
    "shift": win32con.VK_SHIFT,  "lshift": win32con.VK_LSHIFT, "rshift": win32con.VK_RSHIFT,
    "ctrl":  win32con.VK_CONTROL,"lctrl":  win32con.VK_LCONTROL,"rctrl":  win32con.VK_RCONTROL,
    "alt":   win32con.VK_MENU,   "lalt":   win32con.VK_LMENU,   "ralt":   win32con.VK_RMENU,
}

_RIGHT_EXTENDED = {"rctrl", "ralt"}  # precisam do bit "extended" no lParam

def _vk_from_token(token: str) -> Optional[int]:
    t = token.strip().lower()
    if t in _VK_BY_NAME:
        return _VK_BY_NAME[t]
    if len(t) == 1:  # letras/dígitos
        return ord(t.upper())
    if t.startswith("f") and t[1:].isdigit():  # F1..F24
        n = int(t[1:])
        if 1 <= n <= 24:
            return getattr(win32con, f"VK_F{n}")
    return None

def _post_key(hwnd, vk, down: bool, is_sys: bool = False, extended: bool = False):
    scan = win32api.MapVirtualKey(vk, 0)
    lparam = 1 | (scan << 16)
    if extended:
        lparam |= (1 << 24)
    if not down:
        lparam |= (1 << 30) | (1 << 31)
    msg = (win32con.WM_SYSKEYDOWN if down else win32con.WM_SYSKEYUP) if is_sys else \
          (win32con.WM_KEYDOWN if down else win32con.WM_KEYUP)
    win32api.PostMessage(hwnd, msg, vk, lparam)

def _send_combo(hwnd, tokens: list[str], settings: Settings):
    # Suporta "lctrl+rshift+tab", "ralt+f4", etc.
    mods = [t for t in tokens[:-1] if t in _MOD_VK]
    base_vk = _vk_from_token(tokens[-1])
    if base_vk is None:
        return

    # Alt (inclui lalt/ralt) => usa mensagens SYSKEY
    is_sys = any(m in ("alt", "lalt", "ralt") for m in mods)

    # pressiona modificadores
    for m in mods:
        ext = m in _RIGHT_EXTENDED
        _post_key(hwnd, _MOD_VK[m], True, is_sys=is_sys, extended=ext)
        time.sleep(settings.modifier_delay)

    # tecla base
    _post_key(hwnd, base_vk, True, is_sys=is_sys)
    time.sleep(settings.key_delay)
    _post_key(hwnd, base_vk, False, is_sys=is_sys)

    # solta modificadores (ordem inversa)
    for m in reversed(mods):
        time.sleep(settings.modifier_delay)
        ext = m in _RIGHT_EXTENDED
        _post_key(hwnd, _MOD_VK[m], False, is_sys=is_sys, extended=ext)

class AutoClicker:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(self, on_error: Optional[Callable[[str, str], None]] = None) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, args=(on_error,), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _run(self, on_error: Optional[Callable[[str, str], None]]):
        hwnd = win32gui.FindWindow(None, self.settings.target_window_title)
        if not hwnd:
            if on_error:
                on_error("Erro", f"Janela '{self.settings.target_window_title}' não encontrada!")
            return
        while not self._stop_event.is_set():
            self._send_clicks(hwnd)
            self._send_extra_keys(hwnd)  # <-- agora direcionado à janela alvo
            time.sleep(self.settings.interval)

    def _send_clicks(self, hwnd):
        if self.settings.enable_left_click:
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0x0001, 0)
            time.sleep(self.settings.hold_time)
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0x0000, 0)

        time.sleep(self.settings.between_clicks)

        if self.settings.enable_right_click:
            win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 0x0002, 0)
            win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0x0000, 0)

    def _send_extra_keys(self, hwnd):
        if not self.settings.extra_keys:
            return
        for spec in self.settings.extra_keys:
            tokens = [t.strip().lower() for t in spec.split("+") if t.strip()]
            if not tokens:
                continue

            # Modificador sozinho (shift/ctrl/alt e variantes L/R)
            if len(tokens) == 1 and tokens[0] in _MOD_VK:
                name = tokens[0]
                vk = _MOD_VK[name]
                is_sys = name in ("alt", "lalt", "ralt")
                ext = name in _RIGHT_EXTENDED
                _post_key(hwnd, vk, True, is_sys=is_sys, extended=ext)
                time.sleep(self.settings.key_delay)
                _post_key(hwnd, vk, False, is_sys=is_sys, extended=ext)
                time.sleep(self.settings.extra_key_gap)
                continue

            # Combinações tipo ctrl+shift+tab
            if len(tokens) >= 2 and all(t in _MOD_VK or _vk_from_token(t) for t in tokens):
                _send_combo(hwnd, tokens, self.settings)
            else:
                vk = _vk_from_token(tokens[0])
                if vk is None:
                    continue
                _post_key(hwnd, vk, True)
                time.sleep(self.settings.key_delay)
                _post_key(hwnd, vk, False)

            time.sleep(self.settings.extra_key_gap)  # intervalo entre teclas/combos
