from typing import Iterator
from .chord import Chord
from .note import Note, note_regex


def _parse_tuning(description: str) -> list[Note]:
    return [Note(match.group()) for match in note_regex.finditer(description)]


class Tuning:
    def __init__(self, description: str):
        self._repr = f'Tuning("{description}")'
        self.open_strings = _parse_tuning(description)

    def __repr__(self) -> str:
        return self._repr

    def _fretted_strings(self, chord_pitch_classes: set[int]) -> Iterator[list[Note|None]]:
        for open_string in self.open_strings:
            fretted_string: list[Note|None] = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = open_string + fret
                if note.pitch_class in chord_pitch_classes:
                    fretted_string.append(note)
                else:
                    fretted_string.append(None)
            yield fretted_string

    def __call__(self, chord_name: str) -> None:
        """
        Print the fret diagram.
        """
        chord = Chord(chord_name)
        print(f" {chord} ".center(13 * 4 - 1, '-'))
        print(''.join(f"{i:<4}" for i in range(13)))
        root_note = chord.notes[0]
        chord_pitch_classes = set(n.pitch_class for n in chord.notes)
        fretted_strings = self._fretted_strings(chord_pitch_classes)
        rows = [_format_row(notes, root_note) for notes in fretted_strings]
        for row in reversed(rows):
            print(row)
        print("-" * (13 * 4 - 1))


_color_end = '\033[0m'

_colors = [
    '\033[32m',  # green
    '\033[31m',  # red
    '\033[34m',  # blue
    '\033[33m',  # yellow
    '\033[35m',  # magenta
    '\033[36m',  # cyan
]

_subscript = str.maketrans(
    '-0123456789',
    '₋₀₁₂₃₄₅₆₇₈₉')


def _colored(text: str, color: int) -> str:
    color_start = _colors[color % len(_colors)]
    return color_start + text + _color_end


def _format_fret(note: Note|None, root_note: Note) -> str:
    if note is not None:
        text = f'{note}'.translate(_subscript)
        if note.octave is not None:
            color = (note.octave * 12 + note.pitch_class - root_note.pitch_class) // 12
            return _colored(f"{text:4}", color)
        else:
            return f"{text:4}"
    else:
        return '.   '


def _format_row(notes: list[Note|None], root_note: Note) -> str:
    return ''.join(_format_fret(note, root_note) for note in notes)
