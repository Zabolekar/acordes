from typing import Iterator
import re
from .chord import Chord
from .note import Note, note_regex


_note_finder = re.compile(note_regex)


def _parse_tuning(description: str) -> list[Note]:
    return [Note(name) for name in _note_finder.findall(description)]


class Tuning:
    def __init__(self, description: str):
        self._repr = f'Tuning("{description}")'
        self.open_strings = _parse_tuning(description)

    def __repr__(self) -> str:
        return self._repr

    def _fretted_strings(self, chord: Chord) -> Iterator[list[Note|None]]:
        for open_string in self.open_strings:
            fretted_string: list[Note|None] = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = open_string + fret
                if note in chord.notes:
                    fretted_string.append(note)
                else:
                    fretted_string.append(None)
            yield fretted_string

    def __call__(self, chord_name: str) -> None:
        """
        Print the fret diagram.
        """
        chord = Chord(chord_name)
        print(f" {chord} ".center(13 * 3, '-'))
        print(' '.join(f"{i:<2}" for i in range(13)))
        rows = [_format_row(notes) for notes in self._fretted_strings(chord)]
        for row in reversed(rows):
            print(row)
        print("-" * 13 * 3)


def _format_row(notes: list[Note|None]) -> str:
    frets = (f'{n}' if n is not None else '.' for n in notes)
    return ' '.join(f"{f:2}" for f in frets)
