"""Field value objects for address book records."""
import re
from datetime import datetime
from typing import Optional

from exceptions import ContactError


class Field:
    """Base class for fields in the address book."""

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Represents a name field in the address book."""

    def __init__(self, value: str) -> None:
        if not value.strip():
            raise ContactError("Name cannot be empty")

        super().__init__(value.strip())


class Birthday(Field):
    """Represents a birthday field in the address book."""
    date_format: str = "%d.%m.%Y"

    def __init__(self, value: str) -> None:
        try:
            birthday_date = datetime.strptime(str(value).strip(), Birthday.date_format).date()
            super().__init__(birthday_date)
        except ValueError as exc:
            raise ContactError("Invalid date format. Use DD.MM.YYYY") from exc

    def format(self, out_format: Optional[str] = None) -> str:
        """
        Return formatted date value.

        :param out_format: Optional output format override.
        """
        return self.value.strftime(
            out_format
            if out_format is not None
            else Birthday.date_format
        )


class Phone(Field):
    """Represents a phone number field in the address book."""

    def __init__(self, value: str) -> None:
        normalized_value = self.normalize(value)

        if len(normalized_value) != 10:
            raise ContactError("Phone number must contain 10 digits")

        super().__init__(normalized_value)

    @staticmethod
    def normalize(value: str) -> str:
        """Return phone number containing only digits."""
        return re.sub(r"\D", "", value)
