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


class ChromaticScale:
    def __init__(self):
        self._notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    def __getitem__(self, i):
        return self._notes[i % 12]
    def index(self, note):
        return self._notes.index(note)


chromatic_scale = ChromaticScale()


class Chord:
    #@staticmethod
    #def parse(cls, s: str) -> Chord:
    #    ...
    #    return Chord(root, component_indices)

    def __init__(self, root: str, component_indices: list[int]):
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

    def fretboard(self, chord: Chord) -> str:
        format_row = lambda notes: ' '.join(f"{n:2}" for n in notes)
        rows = [format_row(notes) for notes in self._fretted_strings(chord)]
        rows.reverse()
        return '\n'.join(rows)  # TODO: multiline repr does NOT actually work like this


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
    for chord in A, Am7:  # TODO: make it accept strings like Am or A(no5) instead. I just want an interface like ukulele("Am7") and it prints
        for tuning in ukulele, rajao:
            print(tuning.fretboard(chord))
            print("-" * 50)
