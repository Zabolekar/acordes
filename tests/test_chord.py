import pytest
from acordes.note import Note
from acordes.chord import Chord

def test_valid():
    assert Chord("C").notes == [Note(s) for s in ("C", "E", "G")]
    assert Chord("Cm").notes == [Note(s) for s in ("C", "Eb", "G")]
    assert Chord("CmM7").notes == [Note(s) for s in ("C", "Eb", "G", "B")]
    assert Chord("A").notes == [Note(s) for s in ("A", "C#", "E")]
    assert Chord("Am").notes == [Note(s) for s in ("A", "C", "E")]
    assert Chord("Am7").notes == [Note(s) for s in ("A", "C", "E", "G")]

@pytest.mark.parametrize("input", ["", "5", "H5"])
def test_invalid_root(input):
    with pytest.raises(ValueError, match=f"can't parse chord {input}"):
        Chord(input)

def test_invalid_suffix():
    with pytest.raises(ValueError, match="can't parse chord suffix m5"):
        Chord("Cm5")

def test_repr():
    assert repr(Chord("C(no5)")) == "C(no5) = <C E>"
    assert repr(Chord("C")) == "C = <C E G>"
    assert repr(Chord("Bb5")) == "Bb5 = <A# F>"    
    assert repr(Chord("C6")) == "C6 = <C E G A>"
