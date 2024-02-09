from re import compile
from typing import Iterator


# intervals in semitones:
U, m2, M2, m3, M3, P4, A4, P5, m6, M6, m7, M7 = range(12)


chord_suffix_meanings = {
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


class ChromaticScale:
    def __init__(self):
        self._notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    def __getitem__(self, i):
        return self._notes[i % 12]
    def index(self, note):
        return self._notes.index(note)


chromatic_scale = ChromaticScale()


class Chord:
    _chord_regex = compile(r"([A-G]#?)(.*)$")

    def __init__(self, name: str):
        self.name, self.notes = name, []
        if match := self._chord_regex.match(name):
            root, suffix = match.groups()
        else:
            raise ValueError(f"Can't parse {name}")
        root_index = chromatic_scale.index(root)
        for component_index in chord_suffix_meanings[suffix]:
            self.notes.append(chromatic_scale[root_index + component_index])

    def __repr__(self):
        return f"{self.name} = <{' '.join(self.notes)}>"


class Tuning:
    def __init__(self, description: str):
        notes = description.split()
        self.open_strings = [chromatic_scale.index(n) for n in notes]

    def _fretted_strings(self, chord: Chord) -> Iterator[list[str]]:
        for open_string in self.open_strings:
            fretted_string = []
            for fret in range(13):  # after an octave it just repeats anyway
                note = chromatic_scale[open_string + fret]
                if note in chord.notes:
                    fretted_string.append(note)
                else:
                    fretted_string.append('.')
            yield fretted_string

    def __call__(self, chord_name: str) -> None:
        """
        Print the fret diagram.
        # TODO: document the language it accepts.
        """
        chord = Chord(chord_name)
        print(f" {chord} ".center(13 * 3, '-'))
        format_row = lambda notes: ' '.join(f"{n:2}" for n in notes)
        rows = [format_row(notes) for notes in self._fretted_strings(chord)]
        for row in reversed(rows):
            print(row)
        print("-" * 13 * 3)


ukulele = Tuning('G C E A')
charango = Tuning('G C E A E')
rajao = Tuning('D G C E A')
timple = Tuning('G C E A D')


if __name__ == '__main__':
    for s in 'A', 'Am7', 'G':
        print(Chord(s))
    print("Ukulele:")
    ukulele('A')
    ukulele('Am7')
    print("Rajão:")
    rajao('A')
    rajao('Am7')
