from typing import Iterator
import re
from .chord import Chord
from .note import Note, note_regex
from .formatting import print_fretboard

_tuning_regex = re.compile(fr"\s*({note_regex.pattern}\s*)*$")


def _parse_tuning(description: str) -> list[Note]:
    if _tuning_regex.match(description) is None:
        raise ValueError(f"can't parse tuning {description}")
    open_strings = [Note(match.group()) for match in note_regex.finditer(description)]
    if not open_strings:
        raise ValueError("at least one open string required")
    return open_strings


class Tuning:
    def __init__(self, description: str):
        self._repr = f'Tuning("{description}")'
        self.open_strings = _parse_tuning(description)

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
