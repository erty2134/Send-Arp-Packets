class Commands:
    def __init__(self):
        self.commandsList:list[str]=[];
    
    def command(func):
        def wrapper(self,name:str):
            self.command.append(name)
            func()
        return wrapper


parse=Commands();

@parse.command("help")
def help():
    print("help: help, print");

print(parse.commandsList)