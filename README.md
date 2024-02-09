"Acordes" means "chords" in Spanish and Portuguese. It will help you determine how to play a chord on a stringed instrument. There are many sites dedicated to guitar or ukulele chords, but for some other instruments, chord tables are harder to find.

# Usage

```pycon
>>> from acordes import Tuning
>>> charango = Tuning("G C E A E")
>>> charango("C7")
----------- C7 = <C E G A#> -----------
0  1  2  3  4  5  6  7  8  9  10 11 12
E  .  .  G  .  .  A# .  C  .  .  .  E 
.  A# .  C  .  .  .  E  .  .  G  .  . 
E  .  .  G  .  .  A# .  C  .  .  .  E 
C  .  .  .  E  .  .  G  .  .  A# .  C 
G  .  .  A# .  C  .  .  .  E  .  .  G 
---------------------------------------
>>> braguinha = Tuning("D G B D")
>>> braguinha("Em")
------------- Em = <E G B> ------------
0  1  2  3  4  5  6  7  8  9  10 11 12
.  .  E  .  .  G  .  .  .  B  .  .  . 
B  .  .  .  .  E  .  .  G  .  .  .  B 
G  .  .  .  B  .  .  .  .  E  .  .  G 
.  .  E  .  .  G  .  .  .  B  .  .  . 
---------------------------------------
```

Supported chord descriptions are (examples with C as the root note):
- with two notes: C5, C(no5), Cm(no5)
- with three notes: C, Cm
- with four notes: C7, CM7, Cm7, CmM7

# Development

Check types: `mypy acordes`

Run tests: `python test.py`
