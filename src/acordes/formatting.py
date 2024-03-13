from typing import Iterator
from .chord import Chord
from .note import Note

from colorama import just_fix_windows_console, Fore, Style


just_fix_windows_console()


_colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.BLUE,  # blue before yellow for better contrast between adjacent colors
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.CYAN
]


_color_end = Style.RESET_ALL


_subscript = str.maketrans(
    '0123456789',
    '₀₁₂₃₄₅₆₇₈₉')


def _colored(text: str, color: str) -> str:
    return color + text + _color_end


def _format_fret(note: Note|None, root_note: Note) -> str:
    if note is None:
        return ".   "

    text = repr(note).translate(_subscript)
    text = f"{text:<4}"
    if note.octave is None:
        return text

    # notes inside a single group form a non-inverted chord
    group = (note.octave * 12 + note.pitch_class - root_note.pitch_class) // 12
    color = _colors[group % len(_colors)]
    return _colored(text, color)


def _format_row(row: list[Note|None], root_note: Note) -> str:
    return ''.join(_format_fret(note, root_note) for note in row)


def _fretted_strings(open_strings: list[Note], allowed_pitches: set[int], column_count: int) -> Iterator[list[Note|None]]:
    for open_string in open_strings:
        fretted_string: list[Note|None] = []
        for fret in range(column_count):
            note = open_string + fret
            if note.pitch_class in allowed_pitches:
                fretted_string.append(note)
            else:
                fretted_string.append(None)
        yield fretted_string


def print_fretboard(open_strings: list[Note], chord_name: str, fret_count: int) -> None:
    chord = Chord(chord_name)
    allowed_pitches = set(n.pitch_class for n in chord.notes)
    column_count = fret_count + 1
    fretboard = list(_fretted_strings(open_strings, allowed_pitches, column_count))

    width = column_count * 4
    print(f' {chord} '.center(width, '-'))
    print(''.join(f'{i:<4}' for i in range(column_count)))  # fret numbers
    root_note = chord.notes[0]
    for row in reversed(fretboard):  # each row corresponds to one string
        print(_format_row(row, root_note))
    print('-' * width)
