from io import StringIO
from contextlib import redirect_stdout
from acordes import Tuning
from acordes.instruments import ukulele, charango

"""
ONLY PERFORMS THE MOST BASIC CHECKS!
(i.e. "call doesn't raise Exception" or "output has correct length")
"""

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
