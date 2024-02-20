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

    def _fretted_strings(self, chord_note_indices: set[int]) -> Iterator[list[Note|None]]:
        for open_string in self.open_strings:
            fretted_string: list[Note|None] = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = open_string + fret
                if note.note_index in chord_note_indices:
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
        chord_note_indices = set(n.note_index for n in chord.notes)
        fretted_strings = self._fretted_strings(chord_note_indices)
        rows = [_format_row(notes, root_note) for notes in fretted_strings]
        for row in reversed(rows):
            print(row)
        print("-" * (13 * 4 - 1))


_color_end = '\033[0m'

_colors = [
    '\033[91m',  # bright red
    '\033[93m',  # bright yellow
    '\033[92m',  # bright green
    '\033[96m',  # bright cyan
    '\033[94m',  # bright blue
    '\033[95m',  # bright magenta
]

_subscript = str.maketrans(
    '-0123456789',
    '₋₀₁₂₃₄₅₆₇₈₉')


def _colored(string: str, color: int) -> str:
    return f'{_colors[color % len(_colors)]}{string}{_color_end}'


def _format_fret(note: Note|None, root_note: Note) -> str:
    if note is not None:
        text = f'{note}'.translate(_subscript)
        color = (note - root_note) // 12
        return _colored(f"{text:4}", color)
    else:
        return '.   '


def _format_row(notes: list[Note|None], root_note: Note) -> str:
    return ''.join(_format_fret(note, root_note) for note in notes)
