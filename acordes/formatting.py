from dataclasses import dataclass

from .chord import Chord
from .fret import Fret


@dataclass
class FormattingOptions:
    note_colors: list[str]|None
    
    @staticmethod
    def _object_hook(object):
        if not isinstance(object, dict):
            raise ValueError('Root object expected')
        note_colors = object.get('note_colors', None)
        if note_colors is not None:
            if not isinstance(note_colors, list):
                raise ValueError('`note_colors` should be a list')
            for color in note_colors:
                if not isinstance(color, str):
                    raise ValueError('`note_colors` should contain string values')
                if color not in _color_codes:
                    raise ValueError(f'Unknown color `{color}`')
            if len(note_colors) == 0:
                note_colors = None
        return FormattingOptions(note_colors)


default_formatting_options = FormattingOptions(
    note_colors=['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
)


_color_codes = {
    'black'         : '\033[30m',
    'red'           : '\033[31m',
    'green'         : '\033[32m',
    'yellow'        : '\033[33m',
    'blue'          : '\033[34m',
    'magenta'       : '\033[35m',
    'cyan'          : '\033[36m',
    'white'         : '\033[37m',
    'bright_black'  : '\033[90m',
    'bright_red'    : '\033[91m',
    'bright_green'  : '\033[92m',
    'bright_yellow' : '\033[93m',
    'bright_blue'   : '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan'   : '\033[96m',
    'bright_white'  : '\033[97m',
}

_color_end = '\033[0m'

_subscript = str.maketrans(
    '0123456789',
    '₀₁₂₃₄₅₆₇₈₉')


FRET_WIDTH = 3

FRET_PLACEHOLDER = '·'  # U+0087 Middle Dot

FRAME_CHARACTER = '─'  # U+2500 Box Drawings Light Horizontal


def _colored(text: str, color: str) -> str:
    return _color_codes[color] + text + _color_end


def _fixed_width(text: str, width: int) -> str:
    return format(text, f'{width}.{width}')


def _format_fret(fret: Fret, options: FormattingOptions) -> str:
    if fret.note is not None:
        text = f'{fret.note}'.translate(_subscript)
        text = _fixed_width(text, FRET_WIDTH)
        if options.note_colors is not None and fret.group is not None:
            color = options.note_colors[fret.group % len(options.note_colors)]
            return _colored(text, color)
        else:
            return text
    else:
        return _fixed_width(FRET_PLACEHOLDER, FRET_WIDTH)


def _format_row(frets: list[Fret], options: FormattingOptions) -> str:
    return ''.join(_format_fret(fret, options) for fret in frets)


def format_fretboard(chord: Chord, fretboard: list[list[Fret]], fret_count: int, options: FormattingOptions) -> str:
    width = (1 + fret_count) * FRET_WIDTH
    header = f' {chord} '.center(width, FRAME_CHARACTER)
    fret_numbers = ''.join(format(i, f'<{FRET_WIDTH}') for i in range(1 + fret_count))
    rows = '\n'.join(_format_row(row, options) for row in reversed(fretboard))
    footer = FRAME_CHARACTER * width
    return f'{header}\n{fret_numbers}\n{rows}\n{footer}'
