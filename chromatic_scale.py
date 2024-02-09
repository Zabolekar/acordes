_notes = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'

def get(index: int) -> str:
    return _notes[index % 12]

def index(note: str) -> int:
    return _notes.index(note)
