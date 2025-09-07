from __future__ import annotations
from dataclasses import asdict
from typing import Dict, Tuple
import json
import os

from .settings import Settings, resource_path


class ProfilesStore:
    """
    Armazena múltiplos perfis de Settings em um único JSON.
    Arquivo: profiles.json (ao lado do executável / settings.json)

    Estrutura:
    {
      "active_profile": "Default",
      "profiles": {
         "Default": { ... Settings ... },
         "Jogo X": { ... }
      }
    }

    Compatibilidade: se existir apenas settings.json (legado), migra para
    profiles.json com um perfil "Default".
    """

    def __init__(self, filename: str = "profiles.json", legacy_settings_filename: str = "settings.json"):
        self.filename = filename
        self.legacy_settings_filename = legacy_settings_filename
        self.active_profile: str = "Default"
        self.profiles: Dict[str, Settings] = {"Default": Settings()}

    # ---------- Persistência ----------
    def load(self) -> Tuple[str, Dict[str, Settings]]:
        # 1) Tenta carregar profiles.json
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.active_profile = data.get("active_profile") or "Default"
                raw_profiles = data.get("profiles") or {}
                if not raw_profiles:
                    raise ValueError("profiles vazio")
                self.profiles = {name: Settings.from_dict(cfg) for name, cfg in raw_profiles.items()}
                if self.active_profile not in self.profiles:
                    # Garante que o ativo existe
                    self.active_profile = next(iter(self.profiles.keys()))
                return self.active_profile, self.profiles
            except Exception:
                pass

        # 2) Migração: se existir settings.json legado, cria profiles.json
        if os.path.exists(self.legacy_settings_filename):
            try:
                with open(self.legacy_settings_filename, "r", encoding="utf-8") as f:
                    legacy = json.load(f)
                default_settings = Settings.from_dict(legacy)
                self.profiles = {"Default": default_settings}
                self.active_profile = "Default"
                self.save()  # cria profiles.json
                return self.active_profile, self.profiles
            except Exception:
                pass

        # 3) Sem nada: usa defaults
        self.active_profile = "Default"
        self.profiles = {"Default": Settings()}
        self.save()
        return self.active_profile, self.profiles

    def save(self) -> None:
        data = {
            "active_profile": self.active_profile,
            "profiles": {name: s.to_dict() for name, s in self.profiles.items()},
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- Operações de Perfil ----------
    def list_names(self):
        return list(self.profiles.keys())

    def get_active(self) -> Settings:
        return self.profiles[self.active_profile]

    def set_active(self, name: str) -> None:
        if name not in self.profiles:
            raise ValueError(f"Perfil '{name}' não encontrado")
        self.active_profile = name
        self.save()

    def upsert(self, name: str, settings: Settings) -> None:
        self.profiles[name] = Settings.from_dict(settings.to_dict())
        self.save()

    def delete(self, name: str) -> None:
        if name not in self.profiles:
            return
        if len(self.profiles) == 1:
            raise ValueError("Não é possível remover o único perfil existente.")
        del self.profiles[name]
        # Ajusta ativo
        if self.active_profile == name:
            self.active_profile = next(iter(self.profiles.keys()))
        self.save()

    def rename(self, old: str, new: str) -> None:
        if old not in self.profiles:
            raise ValueError("Perfil inexistente")
        if new in self.profiles:
            raise ValueError("Já existe perfil com esse nome")
        self.profiles[new] = self.profiles.pop(old)
        if self.active_profile == old:
            self.active_profile = new
        self.save()

    # ---------- Exportação/Importação ----------
    def export_profile(self, name: str, path: str) -> None:
        if name not in self.profiles:
            raise ValueError("Perfil inexistente")
        payload = {
            "name": name,
            "settings": self.profiles[name].to_dict(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def export_all(self, path: str) -> None:
        payload = {
            "active_profile": self.active_profile,
            "profiles": {n: s.to_dict() for n, s in self.profiles.items()},
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def import_file(self, path: str) -> None:
        """
        Importa tanto um único perfil {name, settings} quanto um pacote {profiles}.
        Em caso de conflito de nome, cria sufixos " (2)", " (3)", ...
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "profiles" in data:  # pacote
            for name, cfg in (data.get("profiles") or {}).items():
                safe = self._unique_name(name)
                self.profiles[safe] = Settings.from_dict(cfg)
        elif "name" in data and "settings" in data:  # único
            name = str(data["name"]) or "Imported"
            safe = self._unique_name(name)
            self.profiles[safe] = Settings.from_dict(data["settings"])
        else:
            raise ValueError("Formato de import inválido.")

        self.save()

    def _unique_name(self, base: str) -> str:
        name = base
        i = 2
        while name in self.profiles:
            name = f"{base} ({i})"
            i += 1
        return name
