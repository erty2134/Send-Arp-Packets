#creating an arg parser for my main script

class CommandParser:
    def __init__(self):
        self._functionList:list[function]=[];
        self._dataList:dict[str]={};
        self._dataPrefixList:list[str]=[];
    def update(self,input_:str)->None:
        #if function_ not in self._functionList:
        #    print(f"command, '{function_}' not found");
        for function_ in self._functionList:
            if (function_["prefix"]!=input_[0:len(function_["prefix"])]):
                continue;
            if(function_["command"]!=input_[len(function_["prefix"]):len(function_["prefix"]+function_["command"])]):
                continue;
            inputValue=input_[len(function_["prefix"]+function_["function"].__name__)+1:-1];
            function_["function"](inputValue);
    
    def makeDataPrefix(self,prefix):
        def wrapper(fn):
            self._dataList.append(prefix);
        return wrapper;
    
    def makeData(self,data=""):
        def wrapper(fn):
            self._dataList.append({"function":fn, "data":data});
        return wrapper;

    def makeCommand(self,prefix:str="",command=""):
        def wrapper(fn):
            self._functionList.append({"function":fn,"prefix":prefix,"command":command});
        return wrapper;
    
myCLI=CommandParser();
running:bool=True;


@myCLI.makeCommand(prefix="start ")
def help():
    print("Help, command");
@myCLI.makeCommand(prefix="set ",command="targetip")
def targetip(value):
    print(f"target ip set to '{value}'");
@myCLI.makeCommand(prefix="")
def quit():
    running=False;
    print(running);

myCLI.update("set targetip 123\n");