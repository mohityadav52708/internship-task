from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pydantic import BaseModel


class Plan(BaseModel):
    tool: str
    args: Dict[str, Any] = {}


@dataclass
class Planner:
    openai_model: str = "gpt-4o-mini"

    def plan(self, text: str) -> Plan:
        t = text.strip().lower()

        # URLs or open
        url_match = re.search(r"\b(open)\s+(https?://\S+|\S+\.\w{2,})", t)
        if url_match:
            return Plan(tool="web.open_url", args={"url": url_match.group(2)})

        # search
        search_match = re.search(r"\b(search|google|look up)\s+(for\s+)?(.+)$", t)
        if search_match:
            query = search_match.group(3).strip()
            return Plan(tool="web.search_web", args={"query": query})

        # run command
        run_match = re.search(r"\b(run|execute)\s+(.+)$", t)
        if run_match:
            command = run_match.group(2).strip()
            return Plan(tool="system.run_shell_command", args={"command": command})

        # create/write/append file
        create_match = re.search(r"\b(create)\s+file\s+(.+)$", t)
        if create_match:
            path = create_match.group(2).strip()
            return Plan(tool="code.create_file", args={"path": path})

        write_match = re.search(r"\b(write)\s+file\s+(\S+)\s+with\s+(.+)$", t)
        if write_match:
            path = write_match.group(2)
            content = write_match.group(3)
            return Plan(tool="code.write_file", args={"path": path, "content": content})

        append_match = re.search(r"\b(append)\s+to\s+file\s+(\S+)\s+(.+)$", t)
        if append_match:
            path = append_match.group(2)
            content = append_match.group(3)
            return Plan(tool="code.append_to_file", args={"path": path, "content": content})

        # fallback: use LLM if available
        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI

                client = OpenAI()
                system_prompt = (
                    "You convert user requests into a single tool call. Output strictly JSON with 'tool' and 'args'.\n"
                    "Tools: web.open_url(url), web.search_web(query), system.run_shell_command(command), "
                    "code.create_file(path), code.write_file(path, content), code.append_to_file(path, content)."
                )
                user_prompt = f"User request: {text}"
                response = client.chat.completions.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                )
                content = response.choices[0].message.content or "{}"
                import json

                data = json.loads(content)
                if isinstance(data, dict) and "tool" in data:
                    return Plan(**data)
            except Exception:
                pass

        # default safe fallback
        return Plan(tool="web.search_web", args={"query": text})