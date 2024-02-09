class ChromaticScale:
    def __init__(self):
        self._notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    def __getitem__(self, i):
        return self._notes[i % 12]
    def index(self, note):
        return self._notes.index(note)


chromatic_scale = ChromaticScale()
