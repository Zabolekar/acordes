from types import SimpleNamespace
from .tuning import Tuning

# balalaika prima
balalaika = SimpleNamespace(
    academic = Tuning("E4 E4 A4"),
    folk = Tuning("C4 E4 G4"))

banjo = Tuning("G4 D3 G3 B3 D4")

bass = Tuning("E1 A1 D2 G2")

braguinha = Tuning("D4 G4 B4 D5")

charango = Tuning("G4 C5 E A4 E5")

cavaquinho = SimpleNamespace(
    ggbd = Tuning("G4 G4 B4 D5"),  # Portugal
    dabe = Tuning("D5 A4 B4 E5"),  # Portugal
    dgbd = braguinha,              # Brazil, tuning is the same as that of Madeiran braguinha
    dgbe = Tuning("D4 G4 B4 E5"))  # Brazil

dala_faendyr = Tuning("E4 A4 E5")  # Ossetian lute

dechig_pondar = Tuning("C4 D4 G4") # Chechen lute, see https://www.youtube.com/watch?v=PU5Ki7tIldA

guitalele = Tuning("A2 D3 G3 C4 E4 A4")

guitar = Tuning("E2 A2 D3 G3 B3 E4")

guitarron = Tuning("A1 D2 G2 C3 E3 A2")  # Mexican guitarrón

jarana_jarocha = Tuning("G3 C4 E A3 G3")

jarana_huasteca = Tuning("G3 B3 D4 F#4 A4")

mandolin = Tuning("G3 D4 A4 E5")

rajao = Tuning("D4 G4 C4 E4 A4")

requinto = guitalele

semistrunka = Tuning("D2 G2 B2 D3 G3 B3 D4")  # "Russian guitar"

tenor_guitar = Tuning("C3 G3 D4 A4")

timple = Tuning("G4 C5 E4 A4 D5")

ukulele = SimpleNamespace(
    high_g = Tuning("G4 C4 E4 A4"),
    low_g = Tuning("G3 C4 E4 A4"),
    baritone = Tuning("D3 G3 B3 E4"))

vihuela = Tuning("A3 D4 G4 B3 E4")  # modern mexican vihuela

viola = tenor_guitar

violin = mandolin
