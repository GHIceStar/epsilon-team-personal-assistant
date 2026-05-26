"""Persistence layer for saving and loading the address book with pickle."""
import pickle
from pathlib import Path

from models import AddressBook


DEFAULT_STORAGE_FILE = ".addressbook.pkl"

class AddressBookStorage:
    """Manage address book persistence on disk using pickle serialization."""

    def __init__(self, filename: str = DEFAULT_STORAGE_FILE) -> None:
        self.filename = filename
        self._data = AddressBook()

    @property
    def path(self) -> Path:
        """Return the absolute path to the storage file."""
        return Path(__file__).resolve().parent / self.filename

    def load(self) -> AddressBook:
        """Load the address book from disk or return a new empty one."""
        try:
            with self.path.open("rb") as file:
                data = pickle.load(file)

            if not isinstance(data, AddressBook):
                data = AddressBook()
        except (
            FileNotFoundError,
            EOFError,
            pickle.PickleError,
            AttributeError,
            ImportError
        ):
            data = AddressBook()

        self._data = data
        return data

    def save(self) -> None:
        """Save the current address book state to disk."""
        with self.path.open("wb") as file:
            pickle.dump(self._data, file)

    def __enter__(self) -> AddressBook:
        """Load data when entering the storage context."""
        return self.load()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Save data when leaving the storage context."""
        self.save()
