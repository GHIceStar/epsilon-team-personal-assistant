"""Module for command registry management."""
from dataclasses import dataclass
from typing import Callable

from dto import CommandResult, CommandContext


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Metadata and handler for one CLI command."""

    name: str
    handler: Callable[[CommandContext], CommandResult]
    usage: str
    description: str
    category: str = "general"


_registry: dict[str, Callable[[CommandContext], CommandResult]] = {}
_command_specs: dict[str, CommandSpec] = {}


def register_command(
    name: str,
    *,
    usage: str | None = None,
    description: str | None = None,
    category: str = "general",
):
    """Decorator to register a command and its metadata in the registry."""

    def decorator(func: Callable[[CommandContext], CommandResult]):
        _registry[name] = func
        _command_specs[name] = CommandSpec(
            name=name,
            handler=func,
            usage=usage or name,
            description=description or (func.__doc__ or "").strip() or name,
            category=category,
        )
        return func

    return decorator


def get_registry() -> dict[str, Callable[[CommandContext], CommandResult]]:
    """Get a copy of the handler registry."""
    return _registry.copy()


def get_command_specs() -> dict[str, CommandSpec]:
    """Get a copy of command metadata."""
    return _command_specs.copy()


def get_command_spec(name: str) -> CommandSpec | None:
    """Get metadata for a specific command."""
    return _command_specs.get(name)
