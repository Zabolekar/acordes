from __future__ import annotations
import re


_note_names = [
    ['C'], ['C#', 'Db'],
    ['D'], ['D#', 'Eb'],
    ['E'],
    ['F'], ['F#', 'Gb'],
    ['G'], ['G#', 'Ab'],
    ['A'], ['A#', 'Bb'],
    ['B'],
]

# our code is key-agnostic, so supporting notation like Cb wouldn't be useful anyway
_unsupported = { 'Cb' : 'B', 'B#' : 'C', 'Fb' : 'E', 'E#' : 'F' }

_note_index_by_name = {name: i for i, names in enumerate(_note_names) for name in names}

note_name_regex = r"[A-G][#b]?"  # used by chord.py

_note_regex = re.compile(fr"({note_name_regex})(\d)?")  # note name, then octave number


class Note:
    """
    Represents either an absolute-pitched note or an octave-invariant note.
    `pitch_class` is the index of the note inside an octave (C = 0, C# = 1, ..., B = 11).
    `octave` is the octave number (from 0 to 9) for an absolute note or `None` for an octave-invariant note.
    """
    def __init__(self, name: str):
        if match := _note_regex.fullmatch(name):
            note_name, octave_name = match.groups()
            if note_name in _unsupported:
                suggestion = _unsupported[note_name]
                raise ValueError(f"use {suggestion} instead of {note_name}")
            self.pitch_class = _note_index_by_name[note_name]
            self.octave = int(octave_name) if octave_name is not None else None
        else:
            raise ValueError(f"can't parse note {name}")

    @staticmethod
    def _from_pitch_class_and_octave(pitch_class: int, octave: int|None) -> Note:
        note = Note.__new__(Note)
        note.pitch_class = pitch_class
        note.octave = octave
        return note

    def __repr__(self) -> str:
        note_name = _note_names[self.pitch_class][0]
        if self.octave is not None:
            return f'{note_name}{self.octave}'
        else:
            return note_name

    def __eq__(self, other) -> bool:
        return self.octave == other.octave and self.pitch_class == other.pitch_class

    def __add__(self, interval: int) -> Note:
        pitch = self.pitch_class + interval
        if self.octave is not None:
            return Note._from_pitch_class_and_octave(pitch % 12, self.octave + pitch // 12)
        else:
            return Note._from_pitch_class_and_octave(pitch % 12, None)
