"""Contact record model."""
from typing import Optional

from models.fields import Birthday, Name, Phone
from exceptions import ContactError


class Record:
    """Represents a contact record in the address book."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        """
        Add a phone number to the record.
        :param phone: the phone number to add
        :return: None
        """
        found_phone_obj = self.find_phone(phone)

        if found_phone_obj is not None:
            raise ContactError(f"Phone {phone} is already added to the contact")

        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Edit an existing phone number.
        :param old_phone: the phone number to be replaced
        :param new_phone: the new phone number to replace with
        :return: None
        """
        found_phone_obj = self.find_phone(old_phone)

        if found_phone_obj is None:
            raise ContactError("Phone number not found")

        found_phone_obj.value = Phone(new_phone).value

    def remove_phone(self, phone: str) -> None:
        """
        Remove a phone number from the record.
        :param phone: the phone number to remove
        :return: None
        """
        found_phone_obj = self.find_phone(phone)

        if not found_phone_obj:
            raise ContactError("Phone number not found")

        self.phones.remove(found_phone_obj)

    def find_phone(self, phone: str) -> Optional[Phone]:
        """
        Find a phone number in the record.
        :param phone: the phone number to find
        :return: Phone object if found, else None
        """
        clean_phone = Phone.normalize(phone)

        for p in self.phones:
            if p.value == clean_phone:
                return p

        return None

    def add_birthday(self, birthday: str) -> None:
        """
        Add a birthday to the record.
        :param birthday: the birthday to add in format DD.MM.YYYY
        :return: None
        """
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones = "; ".join(str(phone) for phone in self.phones) or "-"
        birthday = str(self.birthday.format()) if self.birthday else "-"
        return (
            f"Contact name: {self.name.value}, "
            f"Birthday: {birthday}, "
            f"Phones: {phones}"
        )
