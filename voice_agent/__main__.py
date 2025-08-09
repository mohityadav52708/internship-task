from __future__ import annotations

import sys

import click

from .agent import VoiceAgent
from .config import AppConfig


@click.group()
def cli() -> None:
    """Voice System Assistant CLI"""


@cli.command()
@click.argument("text", nargs=-1)
def say(text: tuple[str, ...]) -> None:
    agent = VoiceAgent(AppConfig.load())
    input_text = " ".join(text).strip()
    if not input_text:
        click.echo("Provide text, e.g., python -m voice_agent say 'open example.com'")
        sys.exit(1)
    result = agent.handle_text(input_text)
    click.echo(result)


@cli.command()
def repl() -> None:
    agent = VoiceAgent(AppConfig.load())
    click.echo("Assistant REPL. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            click.echo()
            break
        if line.lower() in {"exit", "quit"}:
            break
        if not line:
            continue
        result = agent.handle_text(line)
        click.echo(result)


if __name__ == "__main__":
    cli()