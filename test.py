from acordes import Tuning


ukulele = Tuning('GCEA')
charango = Tuning('GCEAE')
rajao = Tuning('DGCEA')
timple = Tuning('GCEAD')


if __name__ == '__main__':
    print("Ukulele:")
    ukulele('A')
    ukulele('Am7')
    print("Rajão:")
    rajao('A')
    rajao('Am7')
