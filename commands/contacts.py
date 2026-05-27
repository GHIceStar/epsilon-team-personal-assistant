"""
Module for the base contacts commands:
- add
- change
- phone
- all
"""
from registry import register_command
from commands.utils import input_error, validate_command_args
from exceptions import ContactError
from dto import CommandResult, CommandContext
from models import Record


@register_command(
    "add",
    usage='add [name] [phone]',
    description="Add a contact or append a phone to an existing contact",
    category="contacts",
)
@input_error
def add_contact(context: CommandContext) -> CommandResult:
    """Add a new contact with name and phone number to contacts."""
    validate_command_args(context.command, context.args, 2)

    name, phone, *_ = context.args
    record = context.book.find(name)
    result_message = "Contact updated"

    if record is None:
        record = Record(name)
        context.book.add_record(record)
        result_message = "Contact added"

    record.add_phone(phone)

    return CommandResult(message=result_message)

@register_command(
    "add-email",
    usage='add-email [name] [email]',
    description="Add an email to existing contact",
    category="contacts",
)
@input_error
def add_email(context: CommandContext) -> CommandResult:
    """Add a new email to existing contact."""
    validate_command_args(context.command, context.args, 2)

    name, email, *_ = context.args
    record = context.book.find(name)
    result_message = "Contact updated"

    if record is None:
        raise ContactError("Contact not found")

    if email is not None:
        record.add_email(email)

    return CommandResult(message=result_message)

@register_command(
    "change",
    usage="change [name] [old phone] [new phone]",
    description="Change an existing phone number for a contact",
    category="contacts",
)
@input_error
def change_contact(context: CommandContext) -> CommandResult:
    """Change the phone number of an existing contact."""
    validate_command_args(
        context.command,
        context.args,
        3,
    )

    name, old_phone, new_phone, *_ = context.args
    record = context.book.find(name)

    if record is None:
        raise ContactError("Contact not found")

    record.edit_phone(old_phone, new_phone)
    return CommandResult(message="Contact updated")

@register_command(
    "change-email",
    usage="change-email [name] [old email] [new email]",
    description="Change an existing email for a contact",
    category="contacts",
)
@input_error
def change_email(context: CommandContext) -> CommandResult:
    """Change the email of an existing contact."""
    validate_command_args(
        context.command,
        context.args,
        3,
    )

    name, old_email, new_email, *_ = context.args
    record = context.book.find(name)

    if record is None:
        raise ContactError("Contact not found")

    record.edit_email(old_email, new_email)
    return CommandResult(message="Contact updated")

@register_command(
    "delete",
    usage="delete [name]",
    description="Delete a contact by name",
    category="contacts",
)
@input_error
def delete_contact(context: CommandContext) -> CommandResult:
    """Delete a contact by name from contacts."""
    validate_command_args(
        context.command,
        context.args,
        1,
    )

    name, *_ = context.args
    context.book.delete(name)
    return CommandResult(message="Contact deleted")

@register_command(
    "remove-email",
    usage="remove-email [name] [email]",
    description="Remove one email from a contact",
    category="contacts",
)
@input_error
def remove_email(context: CommandContext) -> CommandResult:
    """Delete an email from contact."""
    validate_command_args(
        context.command,
        context.args,
        2,
    )

    name, email, *_ = context.args
    record = context.book.find(name)

    if record is None:
        raise ContactError("Contact not found")

    record.remove_email(email)
    return CommandResult(message="Email removed")

@register_command(
    "remove-phone",
    usage="remove-phone [name] [phone]",
    description="Remove one phone number from a contact",
    category="contacts",
)
@input_error
def remove_phone(context: CommandContext) -> CommandResult:
    """Delete a phone number from contact."""
    validate_command_args(
        context.command,
        context.args,
        2,
    )

    name, phone, *_ = context.args
    record = context.book.find(name)

    if record is None:
        raise ContactError("Contact not found")

    record.remove_phone(phone)
    return CommandResult(message="Phone removed")

@register_command(
    "contact",
    usage="contact [name]",
    description="Show the full contact card by name",
    category="contacts",
)
@input_error
def show_contact(context: CommandContext) -> CommandResult:
    """Show the contact info by name."""
    validate_command_args(context.command, context.args, 1)

    name, *_ = context.args
    record = context.book.find(name)

    if record is None:
        raise ContactError("Contact not found")

    return CommandResult(message=str(record))

@register_command(
    "all",
    usage="all",
    description="Show all contacts",
    category="contacts",
)
@input_error
def show_all(context: CommandContext) -> CommandResult:
    """Show all contacts in the format: {name}: {phone}."""
    if not context.book:
        return CommandResult(message="No contacts found")

    result = "\n".join(
        str(record)
        for record in context.book.values()
    )
    return CommandResult(message=result)
