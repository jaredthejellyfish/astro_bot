from time import sleep

def ello(bruv):
    i = 0
    while True:
        print(bruv)
        i +=1
        sleep(1)
        if i == 10:
            return True


if ello('bruv'):
    print(' Funk')