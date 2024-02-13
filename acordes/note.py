from __future__ import annotations


class _Multituple:
    def __init__(self, *values: str|tuple[str, ...]):
        self._values = []
        for v in values:
            self._values.append(v if isinstance(v, tuple) else (v,))

    def index(self, value: str) -> int:
        for i, e in enumerate(self._values):
            if value in e:
                return i
        raise ValueError(f"{value:r} not in multituple")

    def __getitem__(self, i: int) -> str:
        return self._values[i][0]


_note_names = _Multituple('C', ('C#', 'Db'), 'D', ('D#', 'Eb'), 'E',
                          'F', ('F#', 'Gb'), 'G', ('G#', 'Ab'), 'A',
                          ('A#', 'Bb'), 'B')


note_regex = "[A-G][#b]?"


class Note:
    def __init__(self, note_name: str):
        self.value = _note_names.index(note_name)

    @staticmethod
    def _from_int(value: int) -> Note:
        note = Note.__new__(Note)
        note.value = value % 12
        return note

    def __repr__(self) -> str:
        return _note_names[self.value]

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __add__(self, interval: int) -> Note:
        return Note._from_int(self.value + interval)
