from typing import Iterator
from .chord import Chord
from .note import Note, parse_notes


class Tuning:
    def __init__(self, description: str):
        self.open_strings = parse_notes(description)

    def _fretted_strings(self, chord: Chord) -> Iterator[list[Note]]:
        for open_string in self.open_strings:
            fretted_string: list[Note|None] = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = open_string.apply_interval(fret)
                if note in chord.notes:
                    fretted_string.append(note)
                else:
                    fretted_string.append(None)
            yield fretted_string

    def __call__(self, chord_name: str) -> None:
        """
        Print the fret diagram.
        # TODO: document the language it accepts.
        """
        chord = Chord(chord_name)
        print(f" {chord} ".center(13 * 3, '-'))
        print(' '.join(f"{i:<2}" for i in range(13)))
        rows = [_format_row(notes) for notes in self._fretted_strings(chord)]
        for row in reversed(rows):
            print(row)
        print("-" * 13 * 3)


def _format_row(notes: list[Note]) -> str:
    frets = (f'{n}' if n else '.' for n in notes)
    return ' '.join(f"{f:2}" for f in frets)
