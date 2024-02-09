from acordes import Chord, Tuning


ukulele = Tuning('GCEA')
charango = Tuning('GCEAE')
rajao = Tuning('DGCEA')
timple = Tuning('GCEAD')


if __name__ == '__main__':
    for s in 'A', 'Am7', 'G':
        print(Chord(s))
    print("Ukulele:")
    ukulele('A')
    ukulele('Am7')
    print("Rajão:")
    rajao('A')
    rajao('Am7')
