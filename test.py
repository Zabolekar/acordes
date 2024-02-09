from chord import Chord
from tuning import Tuning


ukulele = Tuning('G C E A')
charango = Tuning('G C E A E')
rajao = Tuning('D G C E A')
timple = Tuning('G C E A D')


if __name__ == '__main__':
    for s in 'A', 'Am7', 'G':
        print(Chord(s))
    print("Ukulele:")
    ukulele('A')
    ukulele('Am7')
    print("Rajão:")
    rajao('A')
    rajao('Am7')
