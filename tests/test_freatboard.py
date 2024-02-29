import pytest
from io import StringIO
from contextlib import redirect_stdout
import re
from acordes import Tuning
from acordes.chord import Chord
from acordes.instruments import ukulele, charango

"""
ONLY PERFORMS THE MOST BASIC CHECKS!
(i.e. "call doesn't raise Exception" or "output has correct length")
"""


_color_code_regex = re.compile(r"\033\[\d+m")


def test_color():
    with StringIO() as s, redirect_stdout(s):
        ukulele.low_g("A")
        output = s.getvalue()
        assert len(output.split("\n")) == 8

def test_no_color():
    rajao = Tuning("DGCEA")  # without octaves for testing purposes
    with StringIO() as s, redirect_stdout(s):
        rajao("Am7")
        output = s.getvalue()
        assert len(output.split("\n")) == 9

def test_mixed_color():
    reference = ""
    with StringIO() as s, redirect_stdout(s):
        charango("Am7")
        output = s.getvalue()
        assert len(output.split("\n")) == 9

def test_less_frets():
    with StringIO() as s, redirect_stdout(s):
        charango("Am7", 8)
        output = s.getvalue()

    with StringIO() as s, redirect_stdout(s):
        charango("Am7", fret_count=8)
        assert s.getvalue() == output

def test_header():
    with StringIO() as s, redirect_stdout(s):
        charango("Am7")
        lines = s.getvalue().split("\n")
    match = re.fullmatch("-+ (.*) -+", lines[0])
    assert match
    assert match.group(1) == repr(Chord("Am7"))

def test_footer():
    with StringIO() as s, redirect_stdout(s):
        charango("Am7")
        lines = s.getvalue().split("\n")
    assert re.fullmatch("-+", lines[-2])
    assert lines[-1] == ""

def test_fret_numbers():
    with StringIO() as s, redirect_stdout(s):
        charango("Am7")
        lines = s.getvalue().split("\n")
    actual_fret_numbers = lines[1].split()
    expected_fret_numbers = [str(i) for i in range(13)]
    assert actual_fret_numbers == expected_fret_numbers

@pytest.mark.parametrize("fret_count", [1, 3, 12, 24])
def test_fret_numbers_with_fret_count(fret_count: int):
    with StringIO() as s, redirect_stdout(s):
        charango("Am7", fret_count)
        lines = s.getvalue().split("\n")
    actual_fret_numbers = lines[1].split()
    expected_fret_numbers = [str(i) for i in range(fret_count + 1)]
    assert actual_fret_numbers == expected_fret_numbers

def test_line_widths():
    with StringIO() as s, redirect_stdout(s):
        charango("Am7")
        lines = s.getvalue().split("\n")
    colorless_lines = [_color_code_regex.sub("", l) for l in lines]
    first_line_width = len(colorless_lines[0])
    for line in colorless_lines[1:-1]:
        assert len(line) == first_line_width

@pytest.mark.parametrize("tuning", [charango, ukulele.low_g, Tuning("C4")])
def test_string_count(tuning: Tuning):
    with StringIO() as s, redirect_stdout(s):
        tuning("Am7")
        lines = s.getvalue().split("\n")
    strings = lines[2:-2]
    assert len(strings) == len(tuning.open_strings)

def test_fret_notes():
    with StringIO() as s, redirect_stdout(s):
        Tuning("C4")("Cm7")
        lines = s.getvalue().split("\n")
    colorless_lines = [_color_code_regex.sub("", l) for l in lines]
    string = colorless_lines[2]
    fret_notes = string.split()
    assert fret_notes == ['C₄', '.', '.', 'D#₄', '.', '.', '.', 'G₄', '.', '.', 'A#₄', '.', 'C₅']
