"""
Module for the system commands:
- hello
- close
- exit
"""
from dto import CommandResult, CommandContext
from registry import register_command

@register_command(
    "hello",
    usage="hello",
    description="Show a greeting from the assistant",
    category="system",
)
def hello_command(context: CommandContext) -> CommandResult:
    """Greet the user command."""
    return CommandResult(message="How can I help you?")

@register_command("exit", usage="exit", description="Close the application", category="system")
@register_command("close", usage="close", description="Close the application", category="system")
def exit_command(context: CommandContext) -> CommandResult:
    """Exit the application."""
    return CommandResult(message="Good bye", exit=True)
