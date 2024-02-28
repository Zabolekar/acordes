import pytest
from acordes.note import Note

def test_octave():
    assert Note("A0").octave == 0
    assert Note("A4").octave == 4
    assert Note("A9").octave == 9

def test_no_octave():
    assert Note("C").octave is None
    assert Note("C").pitch_class == Note("C4").pitch_class == 0
    assert Note("B").pitch_class == Note("B4").pitch_class == 11

def test_accidentals():
    assert Note("C#") == Note("Db")
    assert Note("F#3") == Note("Gb3")

@pytest.mark.parametrize("input,suggestion", [("B#","C"), ("Cb","B"), ("E#","F"), ("Fb","E")])
def test_unsupported(input, suggestion):
    with pytest.raises(ValueError, match=f"use {suggestion} instead of {input}"):
        Note(input)

@pytest.mark.parametrize("input", ["C10", "D-1", "E4#"])
def test_invalid_octave(input):
    with pytest.raises(ValueError, match=f"can't parse note {input}"):
        Note(input)

@pytest.mark.parametrize("input", ["", "4", " C", "c", "C##", "H"])
def test_invalid_note(input):
    with pytest.raises(ValueError, match=f"can't parse note {input}"):
        Note(input)

def test_repr():
    assert repr(Note("G5")) == "G5"
    assert repr(Note("F")) == "F"
    assert repr(Note("Ab")) == "G#"

def test_equality():
    assert Note("B") == Note("B")
    assert Note("B") != Note("C")
    assert Note("B4") == Note("B4")
    assert Note("B4") != Note("B")
    assert Note("B4") != Note("B5")

def test_addition():
    assert Note("G3") + 1 == Note("G#3")
    assert Note("F3") + 7 == Note("C4")
    assert Note("B") + 1 == Note("C")
