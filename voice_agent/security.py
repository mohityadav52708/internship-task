from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import AppConfig


@dataclass
class PermissionManager:
    config: AppConfig

    def is_action_allowed(self, action_name: str, action_args: dict[str, Any] | None = None) -> bool:
        if action_name in self.config.permissions.allowed_actions:
            return True
        return self.config.permissions.default_allow