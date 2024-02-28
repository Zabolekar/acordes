import pytest
from acordes import Tuning
from acordes.note import Note

@pytest.mark.parametrize("input", ["", "\n \t"])
def test_empty(input):
    with pytest.raises(ValueError, match="at least one open string required"):
        Tuning(input)

def test_no_spaces_no_octaves():
    tuning = Tuning("CE")
    assert tuning.open_strings == [Note(note) for note in ("C", "E")]
    assert repr(tuning) == 'Tuning("C E")'

def test_no_octaves():
    tuning = Tuning("C# F")
    assert tuning.open_strings == [Note(note) for note in ("C#", "F")]
    assert repr(tuning) == 'Tuning("C# F")'

def test_no_spaces():
    tuning = Tuning("D4F#4")
    assert tuning.open_strings == [Note(note) for note in ("D4", "F#4")]
    assert repr(tuning) == 'Tuning("D4 F#4")'

def test_octaves():
    tuning = Tuning("D#4 G4")
    assert tuning.open_strings == [Note(note) for note in ("D#4", "G4")]
    assert repr(tuning) == 'Tuning("D#4 G4")'

def test_mixed():
    tuning = Tuning("E G#4")
    assert tuning.open_strings == [Note(note) for note in ("E", "G#4")]
    assert repr(tuning) == 'Tuning("E G#4")'

def test_mixed_no_spaces():
    tuning = Tuning("FA4")
    assert tuning.open_strings == [Note(note) for note in ("F", "A4")]
    assert repr(tuning) == 'Tuning("F A4")'

@pytest.mark.parametrize("input", ["?", "O", "A-B"])
def test_invalid(input):
    with pytest.raises(ValueError, match="can't parse note .+"):
        Tuning(input)
