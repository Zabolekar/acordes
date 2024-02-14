import re
from .note import Note, note_regex


# intervals in semitones:
P1, m2, M2, m3, M3, P4, A4, P5, m6, M6, m7, M7 = range(12)


suffix_meanings = {
    "5":      (P1,     P5),
    "m(no5)": (P1, m3),
    "(no5)":  (P1, M3),
    "m":      (P1, m3, P5),
    "":       (P1, M3, P5),
    "m7":     (P1, m3, P5, m7),
    "mM7":    (P1, m3, P5, M7),
    "7":      (P1, M3, P5, m7),
    "M7":     (P1, M3, P5, M7),
    "aug":    (P1, M3, m6),
    "dim":    (P1, m3, A4),
    "dim7":   (P1, m3, A4, M6),
    "m7b5":   (P1, m3, A4, m7),
    "7b5":    (P1, M3, A4, m7),
    "aug7":   (P1, M3, m6, m7),
    "augM7":  (P1, M3, m6, M7),
    "sus2":   (P1, M2, P5),
    "sus4":   (P1, P4, P5),
    "9":      (P1, M3, P5, m7, M2),
    "m9":     (P1, m3, P5, m7, M2),
    "M9":     (P1, M3, P5, M7, M2),
    "mM9":    (P1, m3, P5, M7, M2),
    "7b9":    (P1, M3, P5, m7, m2),
    "aug9":   (P1, M3, m6, m7, M2),
    "augM9":  (P1, M3, m6, M7, M2),
    "dim9":   (P1, m3, A4, M6, M2),
    "dimb9":  (P1, m3, A4, M6, m2),
    "m9b5":   (P1, m3, A4, m7, M2),
    "mb9b5":  (P1, m3, A4, m7, m2),
    "2":      (P1, M3, P5, M2),      # aka add9
    "m2":     (P1, m3, P5, M2),      # aka madd9
    "6":      (P1, M3, P5, M6),      # aka add13
    "m6":     (P1, m3, P5, M2)       # aka madd13
}


chord_regex = re.compile(fr"({note_regex})(.*)$")


class Chord:
    def __init__(self, name: str):
        self.name, self.notes = name, []

        if match := chord_regex.match(name):
            root_name, suffix = match.groups()
        else:
            raise ValueError(f"Can't parse {name}")

        root = Note(root_name)
        for interval in suffix_meanings[suffix]:
            self.notes.append(root + interval)

    def __repr__(self) -> str:
        return f"{self.name} = <{' '.join(f'{n}' for n in self.notes)}>"
