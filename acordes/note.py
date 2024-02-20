from __future__ import annotations
import re


class _NoteNames:
    def __init__(self, *values: str|tuple[str, ...]):
        self._names: list[str] = []
        self._indices: dict[str, int] = {}
        for i, value in enumerate(values):
            if isinstance(value, tuple):
                self._names.append(value[0])  # empty tuples not allowed here
                self._indices |= {name: i for name in value}
            else:
                self._names.append(value)
                self._indices[value] = i

    def index(self, value: str) -> int:
        try:
            return self._indices[value]
        except KeyError as e:
            raise ValueError(f"{value!r} not in multituple") from e

    def __getitem__(self, i: int) -> str:
        return self._names[i]


_note_names = _NoteNames('C', ('C#', 'Db'), 'D', ('D#', 'Eb'), 'E',
                         'F', ('F#', 'Gb'), 'G', ('G#', 'Ab'), 'A',
                         ('A#', 'Bb'), 'B')


note_name_regex = r"[A-G][#b]?"

note_regex = re.compile(fr"({note_name_regex})(-?\d+)?")


class Note:
    """
    Represents either an absolute-pitched note or an octave-invariant note.
    `pitch_class` is the index of the note inside an octave (C = 0, C# = 1, ..., B = 11).
    `octave` is the octave number for an absolute note or `None` for an octave-invariant note.
    """
    def __init__(self, name: str):
        if match := note_regex.match(name):
            note_name, octave_name = match.groups()
            self.pitch_class = _note_names.index(note_name)
            self.octave = int(octave_name) if octave_name is not None else None
        else:
            raise ValueError(f"Can't parse note {name}")

    @staticmethod
    def _from_pitch_class_and_octave(pitch_class: int, octave: int|None) -> Note:
        note = Note.__new__(Note)
        note.pitch_class = pitch_class
        note.octave = octave
        return note

    def to_octave_invariant(self) -> Note:
        return Note._from_pitch_class_and_octave(self.pitch_class, None)

    def __repr__(self) -> str:
        if self.octave is not None:
            return f'{_note_names[self.pitch_class]}{self.octave}'
        else:
            return _note_names[self.pitch_class]

    def __eq__(self, other) -> bool:
        return self.octave == other.octave and self.pitch_class == other.pitch_class

    def __add__(self, interval: int) -> Note:
        pitch = self.pitch_class + interval
        if self.octave is not None:
            return Note._from_pitch_class_and_octave(pitch % 12, self.octave + pitch // 12)
        else:
            return Note._from_pitch_class_and_octave(pitch % 12, None)
