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
    def __init__(self, name: str):
        if match := note_regex.match(name):
            note_name, octave_name = match.groups()
            note_index = _note_names.index(note_name)
            octave = int(octave_name) if octave_name is not None else 4
            # MIDI-compatible pitch value
            self.pitch = (1 + octave) * 12 + note_index
        else:
            raise ValueError(f"Can't parse note {name}")

    @property
    def note_index(self) -> int:
        return self.pitch % 12

    @property
    def note_name(self) -> str:
        return _note_names[self.note_index]

    @property
    def octave(self) -> int:
        return self.pitch // 12 - 1

    @staticmethod
    def _from_pitch(pitch: int) -> Note:
        note = Note.__new__(Note)
        note.pitch = pitch
        return note

    def __repr__(self) -> str:
        return f'{self.note_name}{self.octave}'
    
    def is_octave_equivalent_to(self, other) -> bool:
        return self.note_index == other.note_index

    def __eq__(self, other) -> bool:
        return self.pitch == other.pitch

    def __add__(self, interval: int) -> Note:
        return Note._from_pitch(self.pitch + interval)
    
    def __sub__(self, other: Note) -> int:
        return self.pitch - other.pitch
