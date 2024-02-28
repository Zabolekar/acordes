from acordes.instruments import cavaquinho, mandolin

def test_cavaquinho():
    assert repr(cavaquinho.ggbd) == 'Tuning("G4 G4 B4 D5")'

def test_mandolin():
    assert repr(mandolin) == 'Tuning("G3 D4 A4 E5")'
