from typing import Iterator
import re
from .note import Note
from .formatting import print_fretboard


_split_regex = re.compile(r"\s+|(?=[A-Z])")  # split by whitespace or before uppercase letters


def _parse_tuning(description: str) -> Iterator[Note]:    
    for token in _split_regex.split(description):
        if token != "":
            yield Note(token)


class Tuning:
    def __init__(self, description: str):
        self.open_strings = list(_parse_tuning(description))
        if not self.open_strings:
            raise ValueError("at least one open string required")
        normalized_description = " ".join(repr(note) for note in self.open_strings)
        self._repr = f'Tuning("{normalized_description}")'

    def __repr__(self) -> str:
        return self._repr

    def __call__(self, chord_name: str, fret_count: int=12) -> None:
        """
        Print the fret diagram.
        """
        print_fretboard(self.open_strings, chord_name, fret_count)
