import serial
import time
import yaml 

with open('test.yml') as bit:
    stream = yaml.load(bit,Loader=yaml.FullLoader)
ser = serial.Serial('COM4', 115200)
# 통신 시작 전 파이썬 버퍼를 비워주기 위해 아두이노에서 더미 바이트를 받아온다.
# 아두이노에서 setup() 함수에서 더미바이트를 보냄
# 실행할 때 아두이노를 먼저 리셋해주고 파이썬을 실행하면 된다.
if ser.readable():
#    time.sleep(1)
    ser.read()
streamNum = 1
for key in stream.keys():
    datalen = len(stream[key].keys())
    bitStream = bytearray(datalen+1)
    bitStream[0] = datalen
    idx = 1
    #for key in stream.keys():
    for seg in stream[key].values():
        for i in range(0,8):
            bitStream[idx] = bitStream[idx] | (seg[i] << (7-i) )
        idx = idx + 1
        
    readMode = 1
    # readMode == 1 -> checking if python send valid data to arduino
    # readMode == 2 -> arduino send 1 to python after finish spi communication
    ser.write(bitStream)
    while readMode == 1:
        time.sleep(1)
    #    print(ser.in_waiting)
        if ser.in_waiting >= datalen:
            receive = ser.read(datalen)
            print("bitstream", end=' ')
            print(streamNum)
            streamNum = streamNum + 1
            compare = True
            for i in range(0, datalen):
                if bitStream[ i+1 ] != receive[ i ]:
                    compare = False
            if compare:
                print("data transfer to arduino complete")
                ser.write(bytes(bytearray([0x01])))
                for i in range(0, datalen):
                    for j in range(0,8):
                        print((receive[i]>>(7-j))%2,end='')
                    print(" ",end='')     
                print()
                readMode = 2
            else:
                print("error! arduino receive wrong data")
                ser.write(bytes(bytearray([0x02])))
                for i in range(0, datalen):
                    for j in range(0,8):
                        print((receive[i]>>(7-j))%2,end='')
                    print(" ",end='')     
                print()
                exit()
        else:
            print("waiting for checking data")

    while readMode == 2:
        time.sleep(1)
        # print(ser.in_waiting)
        if ser.in_waiting == 1:
            receive = ser.read()
            if receive[0] == 1:
                print("spi communication complete")
                readMode = 0
            else:
                print("error! something wrong between arduino and chip")
                print(receive[0])
                exit()
        else:
            print("waiting for spi communication")
