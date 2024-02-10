from __future__ import annotations
from re import compile


class Note:
    def __init__(self, value: int):
        self.value = value % 12

    def __repr__(self) -> str:
        return _note_names[self.value]

    def __eq__(self, other: Note) -> bool:
        return self.value == other.value

    def apply_interval(self, interval: int) -> Note:
        return Note(self.value + interval)


def parse_note(note_name: str) -> Note:
    return Note(_note_names.index(note_name))


def parse_notes(note_names: str) -> list[Note]:
    return [parse_note(name) for name in _note_finder.findall(note_names)]


_note_names = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'


_note_finder = compile(r"([A-G]#?)")
