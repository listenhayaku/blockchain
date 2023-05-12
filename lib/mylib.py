import msvcrt
import select
import sys

class myNonBlockingInput():
    def __init__(self):
        self.buffer = str()
        self.ret = str()

    def ReceiveInput(self):
        if(msvcrt.kbhit()):
            char = msvcrt.getch().decode("utf-8")
            self.buffer += char
            print(char,end="")
        if(len(self.buffer) > 0 and self.buffer[-1] == '\r'):
            self.ret = self.buffer[0:-1]
            self.buffer = ""
            print(self.ret)
            return self.ret
        else: return ""


'''
class myNonBlockingInput():
    def __init__(self):
        self.buffer = str()
        self.ret = str()

    def ReceiveInput(self):
        i, o, e = select.select( [sys.stdin], [], [], 1)
        if (i):
            self.buffer.append(sys.stdin.buffer.readline().strip())   #sys.stdin.readline() 可以讀取成str
#sys.stdin.buffer.readline() 讀取成bytes
        else:
            pass
        while len(self.buffer) > 0:
            self.ret = bytes(self.buffer.pop())
            print("(debug)[communicator.py][inputFunc]self.ret:",self.ret)
        return self.ret
        #print("(debug)[communicator.py][[testFunc]dataQueue:",dataQueue)
        #大感謝這個方法使input可以被中斷出來檢查flag是否轉為停止
        #https://stackoverflow.com/questions/1335507/keyboard-input-with-timeout -Pontus
'''
    