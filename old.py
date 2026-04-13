import socket
import struct
import sys

IP:str="192.168.50.224";
MAC:str="d8:b1:ee:36:ca:7b"
PORT:int=2398;

RECV_IP:str="192.168.50.150";
RECV_MAC:str="b8:27:eb:74:f2:6c";
"""
class arpPacket:
    \"""
    # create an arp packet

    \"""
    def __init__(self, 
        hardwareType:bytes,
        protocolType:bytes,

        hardwareLength:bytes, #8bytes
        protocolLength:bytes,
        opporation:bytes,

        senderMacAddress:bytes,

        senderIP:bytes,

        targerMacAddress:bytes,

        targetIP:bytes
    )->None:
        self.htype=hardwareType;
        self.ptype=protocolType;

        self.hlen=hardwareLength;
        self.plen=protocolLength;
        self.oper=opporation;

        self.sha=senderMacAddress;
        
        self.spa=senderIP;

        self.tha=targerMacAddress;

        self.tpa=targetIP;

        pass;
"""

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW);
def main(argc:int, argv:list[str]) -> None:
    sock.bind((IP,PORT));
    print(socket.inet_aton(RECV_IP));
    print(RECV_IP);
    myArp=struct.pack(
        "!16s H 8s 8s 16s 32s 32s 32s 32s",

        b"\x01",0x0800,
        b"\x06",b"\x04",b"\x01",
        bytes.fromhex(MAC.replace(":","")),
        socket.inet_aton(IP),
        bytes.fromhex(RECV_MAC.replace(":","")),
        bytes(map(int, RECV_IP.split('.')))
    );



    sock.sendto(myArp,(RECV_IP,0));

if(__name__=="__main__") : main(len(sys.argv),sys.argv);