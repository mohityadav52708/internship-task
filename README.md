# Voice System Assistant (Prototype)

A modular Python assistant that accepts voice/text commands, plans actions, and executes tools on the local system (web, system, and code operations). Designed with a security gate for sensitive actions and a CLI for quick testing.

## Features
- Voice or text command input (voice placeholder; text commands ready)
- Planner (rule-based; optional LLM via OpenAI API)
- Tools: web (open/search), system (run commands), code (create/write files)
- Permission gate via YAML policy
- CLI (`say` for single command; `repl` for continuous loop)
- Tests for core planning logic

## Requirements
- Python 3.10+
- Optional: `OPENAI_API_KEY` environment variable for LLM planning

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure (optional)
Create `agent.config.yaml` (optional). Example:
```yaml
permissions:
  default_allow: false
  allowed_actions:
    - web.open_url
    - web.search_web
    - code.create_file
    - code.write_file
    - code.append_to_file
  # Dangerous operations should be added explicitly by you:
  # - system.run_shell_command

openai:
  model: gpt-4o-mini
```

## Usage
- One-off command:
```bash
python -m voice_agent say "open https://example.com"
```
- REPL mode:
```bash
python -m voice_agent repl
```
- Help:
```bash
python -m voice_agent --help
```

## Notes
- Voice capture is stubbed; enable your preferred STT/TTS stack in `voice_agent/tts.py` and a STT backend (not included by default).
- Some web/system operations are platform-specific. Review `agent.config.yaml` permissions before enabling sensitive actions.
- This is a prototype to be extended with richer tools (e.g., Playwright automation) and stronger auth/confirmation flows.