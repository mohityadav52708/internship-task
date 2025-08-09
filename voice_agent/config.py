from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field


class OpenAIConfig(BaseModel):
    model: str = Field(default="gpt-4o-mini")


class PermissionConfig(BaseModel):
    default_allow: bool = Field(default=True)
    allowed_actions: list[str] = Field(default_factory=list)


class AppConfig(BaseModel):
    permissions: PermissionConfig = Field(default_factory=PermissionConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)

    @staticmethod
    def load(path: Optional[Path] = None) -> "AppConfig":
        if path is None:
            path = Path("agent.config.yaml")
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data: Dict[str, Any] = yaml.safe_load(f) or {}
            return AppConfig(**data)
        return AppConfig()