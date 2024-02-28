import re
from .note import Note, note_name_regex


# intervals in semitones:
P1, m2, M2, m3, M3, P4, A4, P5, m6, M6, m7, M7 = range(12)


suffix_meanings = {
    "m(no5)": (P1, m3),
    "(no5)":  (P1, M3),
    "5":      (P1,     P5),
    "dim":    (P1, m3, A4),
    "sus2":   (P1, M2, P5),
    "m":      (P1, m3, P5),
    "":       (P1, M3, P5),
    "sus4":   (P1, P4, P5),
    "aug":    (P1, M3, m6),
    "m6":     (P1, m3, P5, M6),
    "6":      (P1, M3, P5, M6),
    "m7":     (P1, m3, P5, m7),
    "mM7":    (P1, m3, P5, M7),
    "7":      (P1, M3, P5, m7),
    "M7":     (P1, M3, P5, M7)
}


chord_regex = re.compile(fr"({note_name_regex})(.*)")


class Chord:
    def __init__(self, name: str):
        self.name, self.notes = name, []

        if match := chord_regex.fullmatch(name):
            root_name, suffix = match.groups()
        else:
            raise ValueError(f"can't parse chord {name}")

        root = Note(root_name)
        if suffix not in suffix_meanings:
            raise ValueError(f"can't parse chord suffix {suffix}")
        
        for interval in suffix_meanings[suffix]:
            self.notes.append(root + interval)

    def __repr__(self) -> str:
        return f"{self.name} = <{' '.join(f'{n}' for n in self.notes)}>"
