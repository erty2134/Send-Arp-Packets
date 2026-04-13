import threading
import time
import copy
# custom command parser trial

def findSubString(string:str, start:str, end:str)->str:
    return string[string.find(start):string.find(end)];

class Command:
    def __init__(self, inputCopy, newThread=True):
        self.myList=[]
        self.__newThread=newThread
        self._inputCopy=copy.deepcopy(inputCopy)
        print(type(self.myList))
        
    def _update(self, fn=None)->None:
        print("function name "+fn.__name__)
        print("input "+self._inputCopy[0:len(fn.__name__)])
        while self.__newThread:
            if fn.__name__ == self._inputCopy[0:len(fn.__name__)]:
                fn();
        
        if fn: return
        

        for function in self.myList:
            # check some stuff
            pass;
        if fn.__name__ == self._inputCopy[0:len(fn.__name__)]:
                fn();
    
    def addToList(self, data):
        def wrapper(fn):
            self.myList.append(fn)

            threading.Thread(target=self._update, args=[fn]).start()
            #print (self.myList)
            #fn()
            #print(fn,self)
        return wrapper

inputs:str="help"
command=Command(inputs)   

@command.addToList(inputs)
def help():
    print("help: command")


@command.addToList(inputs)
def targetIP(prefix="set ")->None:
    print(f"input is {command._inputCopy}!") # i know i am refrencing a varible that shouldnt be

    
inputs="help"
inputs="showInput"
print()
print()

time.sleep(5)
#print(type(command.myList))

#while True:
#    command.update(input("enter command: "))