from __future__ import annotations
from re import compile

chord_regex = compile(r"([A-G]#?)(.*)$")

# intervals in semitones:
U, m2, M2, m3, M3, P4, A4, P5, m6, M6, m7, M7 = range(12)


# abstract chords
X5 = (U, P5) 
Xno5 = (U, M3)
Xmno5 = (U, m3)
X = (U, M3, P5)
Xm = (U, m3, P5)
X7 = (U, M3, P5, m7)
XM7 = (U, M3, P5, M7)
Xm7 = (U, m3, P5, m7)
XmM7 = (U, m3, P5, M7)


chord_kinds = {"5": X5, "(no5)": Xno5, "m(no5)": Xmno5, "": X, "m": Xm, "7": X7, "M7": XM7, "m7": Xm7, "mM7": XmM7 }


class ChromaticScale:
    def __init__(self):
        self._notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    def __getitem__(self, i):
        return self._notes[i % 12]
    def index(self, note):
        return self._notes.index(note)


chromatic_scale = ChromaticScale()


class Chord:
    @staticmethod
    def parse(s: str) -> Chord:
        root, kind = chord_regex.match(s).groups()
        component_indices = chord_kinds[kind]
        return Chord(root, component_indices)

    def __init__(self, root: str, component_indices: tuple[int, ...]):
        self.notes = []
        root_index = chromatic_scale.index(root)  
        for i in component_indices:
            self.notes.append(chromatic_scale[root_index + i])
    def __repr__(self):
        return ' '.join(self.notes)


class Tuning:
    def __init__(self, description: str):
        notes = description.split()
        self.open_strings = [chromatic_scale.index(n) for n in notes]

    def _fretted_strings(self, chord: Chord) -> list[list[str]]:
        strings = []
        for open_string in self.open_strings:
            fretted_string = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = chromatic_scale[open_string + fret]
                if note in chord.notes:
                    fretted_string.append(note)
                else:
                    fretted_string.append('.')
            strings.append(fretted_string)
        return strings

    def __call__(self, chord: str) -> str:
        """
        Print the fret diagram.
        # TODO: document the language it accepts.
        """
        chord = Chord.parse(chord)
        format_row = lambda notes: ' '.join(f"{n:2}" for n in notes)
        rows = [format_row(notes) for notes in self._fretted_strings(chord)]
        for row in reversed(rows):
            print(row)


ukulele = Tuning('G C E A')
charango = Tuning('G C E A E')
rajao = Tuning('D G C E A')
timple = Tuning('G C E A D')


if __name__ == '__main__':
    A = Chord('A', X)
    Am7 = Chord('A', Xm7)
    G = Chord('G', X)
    print(A)
    print(Am7)
    print(G)
    print("-" * 50)
    for chord in "A", "Am7":
        for tuning in ukulele, rajao:
            tuning(chord)
            print("-" * 50)
