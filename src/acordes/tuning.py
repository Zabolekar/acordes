from typing import Iterator
import re
from .chord import Chord
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

    def _fretted_strings(self, allowed_pitches: set[int], fret_count: int) -> Iterator[list[Note|None]]:
        for open_string in self.open_strings:
            fretted_string: list[Note|None] = []
            for fret in range(fret_count + 1):
                note = open_string + fret
                if note.pitch_class in allowed_pitches:
                    fretted_string.append(note)
                else:
                    fretted_string.append(None)
            yield fretted_string

    def __call__(self, chord_name: str, fret_count: int=12) -> None:
        """
        Print the fret diagram.
        """
        chord = Chord(chord_name)
        allowed_pitches = set(n.pitch_class for n in chord.notes)
        fretted_strings = list(self._fretted_strings(allowed_pitches, fret_count))
        print_fretboard(chord, fretted_strings)
