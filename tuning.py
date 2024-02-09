from typing import Iterator
from chord import Chord
from chromatic_scale import chromatic_scale


class Tuning:
    def __init__(self, description: str):
        notes = description.split()
        self.open_strings = [chromatic_scale.index(n) for n in notes]

    def _fretted_strings(self, chord: Chord) -> Iterator[list[str]]:
        for open_string in self.open_strings:
            fretted_string = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = chromatic_scale[open_string + fret]
                if note in chord.notes:
                    fretted_string.append(note)
                else:
                    fretted_string.append('.')
            yield fretted_string

    def __call__(self, chord_name: str) -> None:
        """
        Print the fret diagram.
        # TODO: document the language it accepts.
        """
        chord = Chord(chord_name)
        print(f" {chord} ".center(13 * 3, '-'))
        format_row = lambda notes: ' '.join(f"{n:2}" for n in notes)
        rows = [format_row(notes) for notes in self._fretted_strings(chord)]
        for row in reversed(rows):
            print(row)
        print("-" * 13 * 3)
