from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List
import json
import os


def resource_path(relative_path: str) -> str:
    try:
        base_path = os.sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


@dataclass
class Settings:
    target_window_title: str = "Idle Slayer"
    interval: float = 0.001
    hold_time: float = 0.02
    between_clicks: float = 0.001
    enable_left_click: bool = True
    enable_right_click: bool = True
    extra_keys: List[str] = field(default_factory=list)
    key_delay: float = 0.01          # atraso entre pressionar/soltar a tecla base
    modifier_delay: float = 0.005    # atraso ao pressionar/soltar modificadores
    extra_key_gap: float = 0.01      # intervalo entre teclas/combos sucessivos
    language: str = "pt"

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Settings":
        defaults = cls()
        merged = {**defaults.to_dict(), **(data or {})}
        keys = merged.get("extra_keys", []) or []
        merged["extra_keys"] = [str(k).strip() for k in keys if str(k).strip()]
        return cls(**merged)

    def update_from(self, other: "Settings") -> None:
        for field_name in self.__dataclass_fields__.keys():
            setattr(self, field_name, getattr(other, field_name))
