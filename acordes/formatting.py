from dataclasses import dataclass
from enum import Enum, auto
from typing import Final
import re

from .chord import Chord
from .fret import Fret


class OctaveNumbers(Enum):
    NONE = auto()
    ASCII = auto()
    SUBSCRIPT = auto()

class Colorization(Enum):
    NONE = auto()
    DARK_RAINBOW = auto()
    DARK_CONTRAST = auto()
    LIGHT_RAINBOW = auto()
    LIGHT_CONTRAST = auto()


@dataclass
class FormattingOptions:
    fret_count: int=12
    """How many frets to show (not including the nut). Default: 12"""

    fret_width: int=4
    """Number of characters per fret. Values below 3 can cause issues. Default: 4"""

    octave_numbers: OctaveNumbers=OctaveNumbers.SUBSCRIPT
    """How to show octave numbers near the notes. Default: `SUBSCRIPT`"""

    colorization: Colorization=Colorization.DARK_CONTRAST
    """Which color set to use in the output. Default: `DARK_CONTRAST`"""

    fret_placeholder: str='·'  # U+0087 Middle Dot
    """Character(s) marking empty frets. Default: `·` (Middle Dot)"""

    frame_character: str='─'  # U+2500 Box Drawings Light Horizontal
    """Character used to draw the frame. Default: `─` (Box Drawings Light Horizontal)"""


default_formatting_options: Final[FormattingOptions] = FormattingOptions()

compatibility_formatting_options: Final[FormattingOptions] = FormattingOptions(
    octave_numbers=OctaveNumbers.ASCII,
    colorization=Colorization.NONE,
    fret_placeholder='.',  # ASCII Period
    frame_character='-'    # ASCII Hyphen-Minus
)


_rainbow_colors = (
    1,  # red
    3,  # yellow
    2,  # green
    6,  # cyan
    4,  # blue
    5,  # magenta
)

_contrast_colors = (
    1,  # red
    2,  # green
    4,  # blue
    3,  # yellow
    5,  # magenta
    6,  # cyan
)

_color_codes = {
    Colorization.DARK_RAINBOW:   [f'\033[3{c}m' for c in _rainbow_colors],
    Colorization.DARK_CONTRAST:  [f'\033[3{c}m' for c in _contrast_colors],
    Colorization.LIGHT_RAINBOW:  [f'\033[9{c}m' for c in _rainbow_colors],
    Colorization.LIGHT_CONTRAST: [f'\033[9{c}m' for c in _contrast_colors],
}

_color_end = '\033[0m'

_subscript = str.maketrans(
    '0123456789',
    '₀₁₂₃₄₅₆₇₈₉')


def _colored(text: str, color_index: int|None, colorization: Colorization) -> str:
    if colorization == Colorization.NONE or color_index is None:
        return text
    palette = _color_codes[colorization]
    color_code = palette[color_index % len(palette)]
    return color_code + text + _color_end


def _fixed_width(text: str, width: int) -> str:
    return format(text, f'{width}.{width}')


def _format_fret(fret: Fret, options: FormattingOptions) -> str:
    if fret.note is not None:
        text = f'{fret.note}'
        match options.octave_numbers:
            case OctaveNumbers.NONE:
                text = re.sub('[0-9]', text, '')
            case OctaveNumbers.SUBSCRIPT:
                text = text.translate(_subscript)
        text = _fixed_width(text, options.fret_width)
        return _colored(text, fret.group, options.colorization)
    else:
        return _fixed_width(options.fret_placeholder, options.fret_width)


def _format_row(frets: list[Fret], options: FormattingOptions) -> str:
    return ''.join(_format_fret(fret, options) for fret in frets)


def format_fretboard(chord: Chord, fretboard: list[list[Fret]], options: FormattingOptions) -> str:
    width = (1 + options.fret_count) * options.fret_width
    header = f' {chord} '.center(width, options.frame_character)
    fret_numbers = ''.join(format(i, f'<{options.fret_width}') for i in range(1 + options.fret_count))
    rows = '\n'.join(_format_row(row, options) for row in reversed(fretboard))
    footer = options.frame_character * width
    return f'{header}\n{fret_numbers}\n{rows}\n{footer}'
