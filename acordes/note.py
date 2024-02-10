from __future__ import annotations


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


_note_names = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
