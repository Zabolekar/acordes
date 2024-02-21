from typing import Iterator
from .chord import Chord
from .note import Note, note_regex
from .fret import Fret
from .formatting import FormattingOptions, format_fretboard


def _parse_tuning(description: str) -> list[Note]:
    return [Note(match.group()) for match in note_regex.finditer(description)]


class Tuning:
    def __init__(self, description: str):
        self._repr = f'Tuning("{description}")'
        self.open_strings = _parse_tuning(description)

    def __repr__(self) -> str:
        return self._repr

    def _fretted_strings(self, chord_pitch_classes: set[int], fret_count: int) -> Iterator[list[Note|None]]:
        for open_string in self.open_strings:
            fretted_string: list[Note|None] = []
            for fret in range(1 + fret_count):
                note = open_string + fret
                if note.pitch_class in chord_pitch_classes:
                    fretted_string.append(note)
                else:
                    fretted_string.append(None)
            yield fretted_string

    def get_fretboard(self, chord: Chord, fret_count: int=12) -> list[list[Fret]]:
        # TODO: Concider a dedicated class for fretboards
        root_note = chord.notes[0]
        chord_pitch_classes = set(n.pitch_class for n in chord.notes)
        fretted_strings = self._fretted_strings(chord_pitch_classes, fret_count)

        fretboard: list[list[Fret]]  = []
        for fretted_string in fretted_strings:
            row: list[Fret] = []
            for fret_index, note in enumerate(fretted_string):
                if note is not None and note.octave is not None:
                    # notes inside a single group form a non-inverted chord
                    group = (note.octave * 12 + note.pitch_class - root_note.pitch_class) // 12
                else:
                    group = None
                row.append(Fret(fret_index, note, group))
            fretboard.append(row)

        return fretboard

    def __call__(self, chord_name: str, options: FormattingOptions|None=None) -> None:
        """
        Print the fret diagram.
        """
        if options is None:
            options = FormattingOptions()
        chord = Chord(chord_name)
        fretboard = self.get_fretboard(chord, options.fret_count)
        formatted = format_fretboard(chord, fretboard, options)
        print(formatted)
