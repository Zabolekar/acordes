from acordes import Tuning


ukulele = Tuning('G4 C4 E4 A4')
charango = Tuning('G4 C5 E A4 E5')
rajao = Tuning('DGCEA')
timple = Tuning('G4 C5 E4 A4 D5')
guitar = Tuning('E2 A2 D3 G3 B3 E4')


if __name__ == '__main__':
    print("Ukulele:")
    ukulele('A')
    ukulele('Am7')
    ukulele('G#')
    ukulele('Ab')
    print("Rajão:")
    rajao('A')
    rajao('Am7')
    print("Charango:")
    charango('Bb')
    print("Guitar:")
    guitar('E')
