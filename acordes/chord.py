import re
from .note import Note


# intervals in semitones:
U, m2, M2, m3, M3, P4, A4, P5, m6, M6, m7, M7 = range(12)


suffix_meanings = {
    "5": (U, P5),
    "(no5)": (U, M3),
    "m(no5)": (U, m3),
    "": (U, M3, P5),
    "m": (U, m3, P5),
    "7": (U, M3, P5, m7),
    "M7": (U, M3, P5, M7),
    "m7": (U, m3, P5, m7),
    "mM7": (U, m3, P5, M7)
}


chord_validator = re.compile(r"([A-G]#?)(.*)$")


class Chord:
    def __init__(self, name: str):
        self.name, self.notes = name, []

        if match := chord_validator.match(name):
            root_name, suffix = match.groups()
        else:
            raise ValueError(f"Can't parse {name}")

        root = Note(root_name)
        for interval in suffix_meanings[suffix]:
            self.notes.append(root + interval)

    def __repr__(self) -> str:
        return f"{self.name} = <{' '.join(f'{n}' for n in self.notes)}>"
