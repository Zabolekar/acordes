from dataclasses import dataclass
from .note import Note


@dataclass
class Fret:
    index: int
    note: Note|None=None
    group: int|None=None


