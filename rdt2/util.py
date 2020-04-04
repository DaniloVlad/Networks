import binascii
import struct
import hashlib

#Set to True for coloured output. Will not work on windows.
COLORED_PRINT = False

#Used in both client and server to unpack data
unpacker = struct.Struct('I I 8s 32s')

#checks if the recieved ack is for the correct sequence number
def isACK(rcvpkt, seq):
    return rcvpkt[0] == 1 and rcvpkt[1] == seq

#verifies the checksum, returns true if corrupt and false otherwise
def isCorrupt(rcvpkt):
    chksum = mk_csum(rcvpkt[0], rcvpkt[1], rcvpkt[2])
    pktChkSum = rcvpkt[3]
    return chksum != pktChkSum

#Helper function for create checksums, returns a byte string
def mk_csum(ack, seq, data):
    data_pkt = struct.Struct('I I 8s')
    packed_data = data_pkt.pack(ack, seq, data)
    return bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

#Helper function for creating packets, returns the packet
def mk_pkt(ack, seq, data, csum):
    pkt = unpacker.pack(ack, seq, data, csum)
    return pkt


#Print the packet data
def print_packet(addr, pkt):
    print("Packet received:\n\tFrom: {}\n\tAck: {}\n\tSeq: {}\n\tData: {}\n\tChecksum: {}\n".format(addr, *pkt))

#Helper functions used for printing in colour to more easily identify errors!
def print_error(string): 
    if COLORED_PRINT:
        print('\x1b[6;37;41m' + 'ERROR: ' + string + '\x1b[0m\n')
    else:
        print("ERROR: "+string+'\n')

def print_success(string):
    if COLORED_PRINT:
        print('\x1b[6;37;42m' + 'SUCCESS: ' + string + '\x1b[0m\n')
    else:
        print("SUCCESS: " + string + '\n')

def print_warning(string): 
    if COLORED_PRINT:
        print('\x1b[6;30;43m' + 'WARNING: ' + string + '\x1b[0m\n')
    else:
        print("WARNING: "+string+'\n')