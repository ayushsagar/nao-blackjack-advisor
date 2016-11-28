import sys
import time
from naoqi import ALProxy

IP = '192.168.86.176'
try:
    aup = ALProxy("ALAudioPlayer", IP, 9559)
    
except Exception,e:
    print "fail"
    sys.exit(1)

fileId = aup.loadFile("/home/nao/naoqi/laugh.wav")
time.sleep(5)
aup.play(fileId)
fileId = aup.loadFile("/home/nao/naoqi/cry.wav")
time.sleep(5)
aup.play(fileId)
