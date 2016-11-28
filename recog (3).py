from naoqi import *
import time


IP = '192.168.86.176'

class SpeechRecoModule(ALModule):
    """ A module to use speech recognition """
    def __init__(self, name):
        ALModule.__init__(self, name)
        try:
            self._recognizedWord=[]
            self._recognized_words_list=[]
            self.asr = ALProxy("ALSpeechRecognition")
            self._voc_dict=[]
        except Exception as e:
            self.asr = None
        self.memory = ALProxy("ALMemory")
        #print self.getName()

    def onLoad(self):
        from threading import Lock
        self.bIsRunning = False
        self.mutex = Lock()
        self.hasPushed = False
        self.hasSubscribed = False
        self.BIND_PYTHON(self.getName(), "onWordRecognized")

    def onUnload(self):
        from threading import Lock
        self.asr.pause(True)
        self.mutex.acquire()
        try:
            if (self.bIsRunning):
                if (self.hasSubscribed):
                    self.memory.unsubscribeToEvent("WordRecognized", self.getName())
                    #self.asr.pause(True)
                if (self.hasPushed and self.asr):
                    self.asr.popContexts()
        except RuntimeError, e:
            self.mutex.release()
            raise e
        self.bIsRunning = False;
        self.mutex.release()

    def onInput_onStart(self):
        from threading import Lock
        self.mutex.acquire()
        if(self.bIsRunning):
            self.mutex.release()
            return
        self.bIsRunning = True
        try:
            if self.asr:
                self.asr.setVisualExpression(True)
                self.asr.pushContexts()
            self.hasPushed = True
            if self.asr:
                self.asr.setVocabulary( self._voc_dict, True )
            self.memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognized")
            self.hasSubscribed = True
        except RuntimeError, e:
            self.mutex.release()
            self.onUnload()
            raise e
        self.mutex.release()

    def onWordRecognized(self, key, value, message):
        #print 'word recognized'
        #print key,'key'
        #print value,'value'
        #print message,'message'

        if(len(value) > 1 and value[1] >= 0.45):
            print 'recognized the word :', value[0]
            self._recognizedWord=value
            self._recognized_words_list.append(value[0])
        else:
            print 'unsifficient threshold'
    def getWord(self):
        if self._recognizedWord == []:
            return ""
        return self._recognizedWord[0]
    def getLastWord(self):
        size=len(self._recognized_words_list)
        return self._recognized_words_list[size-2]
    def SetVocDict(self,voc):
        self._voc_dict=voc





global broker; broker = ALBroker("pythonBroker","0.0.0.0", 0, IP, 9559)
global pythonSpeechModule;
pythonSpeechModule = SpeechRecoModule('pythonSpeechModule')
vocabulary=['yes','no','game','next']
pythonSpeechModule.SetVocDict(vocabulary)
pythonSpeechModule.onLoad()
#pythonSpeechModule.onUnload()
pythonSpeechModule.onInput_onStart()
#pythonSpeechModule.sleep(10)
time.sleep(10)
pythonSpeechModule.onUnload()
word=pythonSpeechModule.getWord()
print type(word)
print type(vocabulary[0])
print vocabulary[0]
print word
if word.find(vocabulary[0]):
    print 'found'