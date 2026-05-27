"""Contact record model."""
from typing import Optional

from models.fields import Birthday, Name, Phone, Email
from exceptions import ContactError


class Record:
    """Represents a contact record in the address book."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.emails = []
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

    def add_email(self, email: str) -> None:
        """
        Add an email to the record.
        :param email: the email address to add
        :return: None
        """
        found_email_obj = self.find_email(email)

        if found_email_obj is not None:
            raise ContactError(
                f"Email {email} is already added to the contact"
            )

        self.emails.append(Email(email))

    def edit_email(self, old_email: str, new_email: str) -> None:
        """
        Edit an existing email address.
        :param old_email: the email address to be replaced
        :param new_email: the new email address to replace with
        :return: None
        """
        found_email_obj = self.find_email(old_email)
        existing_email = self.find_email(new_email)

        if found_email_obj is None:
            raise ContactError("Email address not found")
        
        if existing_email and existing_email is not found_email_obj:
            raise ContactError(
                f"New email {new_email} already exists in the contact"
            )

        found_email_obj.value = Email(new_email).value

    def remove_email(self, email: str) -> None:
        """
        Remove an email address from the record.
        :param email: the email address to remove
        :return: None
        """
        found_email_obj = self.find_email(email)

        if not found_email_obj:
            raise ContactError("Email address not found")

        self.emails.remove(found_email_obj)

    def find_email(self, email: str) -> Optional[Email]:
        """
        Find an email address in the record.
        :param email: the email address to find
        :return: Email object if found, else None
        """
        clean_email = Email.normalize(email)

        for email_obj in self.emails:
            if email_obj.value == clean_email:
                return email_obj

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
        emails = "; ".join(str(email) for email in self.emails) or "-"
        birthday = str(self.birthday.format()) if self.birthday else "-"
        return (
            f"Contact name: {self.name.value}, "
            f"Birthday: {birthday}, "
            f"Phones: {phones}, "
            f"Emails: {emails}"
        )
