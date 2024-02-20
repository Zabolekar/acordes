from acordes import Tuning


ukulele = Tuning('GCEA')
charango = Tuning('G4C5E4A4E5')
rajao = Tuning('DGCEA')
timple = Tuning('G4C5E4A4D5')
guitar = Tuning('E2A2D3G3B3E4')


if __name__ == '__main__':
    print("Ukulele:")
    ukulele('A')
    ukulele('Am7')
    ukulele('G#')
    ukulele('Ab')
    print("Rajão:")
    rajao('A')
    rajao('Am7')
    print("Guitar:")
    guitar('E')
