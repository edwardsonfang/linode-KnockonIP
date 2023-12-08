from ping3 import ping, verbose_ping

TARGET_IP = '{Your IP}' 

if __name__ == '__main__':
    success = 0
    fail = 0
    for count in range(0,5):
        second = ping(TARGET_IP, unit='ms')
        if second == None:
            fail += 1
            print('This is a None')
        elif second == False:
            fail += 1
            print('This is a False')
        else:
            success += 1
            print('it took {} miliseconds'.format(second))
    if fail == 5:
        print('Success =  {}'.format(success))
        print('Fail =  {}'.format(fail))
        print('This one is totally unaccessable!')
    elif fail > success:
        print('Success =  {}'.format(success))
        print('Fail =  {}'.format(fail))
        print('This one is nearly unaccessable!')
    elif fail == 0 and success == 5:
        print('Fail =  {}'.format(fail))
        print('Success =  {}'.format(success))
        print('This one is totally accessable!')
    else:
        print('Success =  {}'.format(success))
        print('Fail =  {}'.format(fail))
        print('This one is nearly accessable!')


