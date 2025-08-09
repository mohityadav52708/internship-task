from __future__ import annotations

from typing import Any

from rich.console import Console

from .config import AppConfig
from .planner import Planner, Plan
from .security import PermissionManager
from .tools import web as web_tools
from .tools import system as system_tools
from .tools import code as code_tools
from .tts import Speaker


class VoiceAgent:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig.load()
        self.permissions = PermissionManager(self.config)
        self.planner = Planner(openai_model=self.config.openai.model)
        self.speaker = Speaker()
        self.console = Console()

    def handle_text(self, text: str) -> str:
        plan: Plan = self.planner.plan(text)
        action_name = plan.tool
        if not self.permissions.is_action_allowed(action_name, plan.args):
            msg = f"Not allowed by policy: {action_name}"
            self.speaker.say(msg)
            return msg

        result = self._dispatch(action_name, plan.args)
        self.speaker.say(result)
        return result

    def _dispatch(self, tool: str, args: dict[str, Any]) -> str:
        try:
            if tool == "web.open_url":
                return web_tools.open_url(**args)
            if tool == "web.search_web":
                return web_tools.search_web(**args)
            if tool == "system.run_shell_command":
                return system_tools.run_shell_command(**args)
            if tool == "system.open_application":
                return system_tools.open_application(**args)
            if tool == "system.list_directory":
                return system_tools.list_directory(**args)
            if tool == "code.create_file":
                return code_tools.create_file(**args)
            if tool == "code.write_file":
                return code_tools.write_file(**args)
            if tool == "code.append_to_file":
                return code_tools.append_to_file(**args)
        except TypeError as exc:  # wrong args
            return f"Invalid arguments for {tool}: {exc}"
        except Exception as exc:  # noqa: BLE001
            return f"Error executing {tool}: {exc}"
        return f"Unknown tool: {tool}"