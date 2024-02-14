from __future__ import annotations
from functools import lru_cache


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


note_regex = "[A-G][#b]?"


class Note:
    def __init__(self, note_name: str):
        self._index = _note_names.index(note_name)

    @staticmethod
    def _from_int(index: int) -> Note:
        note = Note.__new__(Note)
        note._index = index % 12
        return note

    def __repr__(self) -> str:
        return _note_names[self._index]

    def __eq__(self, other) -> bool:
        return self._index == other._index

    def __add__(self, interval: int) -> Note:
        return Note._from_int(self._index + interval)
