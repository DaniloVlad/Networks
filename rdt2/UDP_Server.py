import socket
import time
from util import *
from errors import *

#IP/Port configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("Starting server on {}:{}".format(UDP_IP, UDP_PORT))

#Create the socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#Stores the current seq number the server is expecting
seq = 0

#Stores the last acked packet, used for checking duplicates
lastAcked = None

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    #Convert data to tuple according to the format of unpacker
    UDP_Packet = unpacker.unpack(data)
    
    #To simulate network delays we put the server to sleep for longer than the clients socket timeout
    if Network_Delay():
        print_error("Server :: Packet Delayed!")
        time.sleep(0.01)

    #To simulate network loss we wont send any sort of response
    elif Network_Loss():
        print_error("Server :: Packet Lost!")
        continue

    #To simulate corrupt checksums I make a fake packet with an incorrect checksum
    elif Packet_Checksum_Corrupter():
        print_error("Server :: Corrupt Checksum!")
        UDP_Packet = (UDP_Packet[0], UDP_Packet[1], UDP_Packet[2], b'Corrupt!')
    
    #Duplicate Packet, resend ACK and continue onto next iteration
    if UDP_Packet == lastAcked:
        print_warning("Server :: Duplicate Packet!  Resending ACK...")
        rep_csum = mk_csum(1, lastAcked[1], b'')
        resp_pkt = mk_pkt(1, lastAcked[1], b'', rep_csum)
        sock.sendto(resp_pkt, addr)
        continue

    #Packet has correct checksum and sequence number
    if not isCorrupt(UDP_Packet) and seq == UDP_Packet[1]:
        print_success("Server :: Client Packet Checksum and Sequence number are correct!")
        print_packet(addr, UDP_Packet)

        #Set last acked packet to be able to reACK if a duplicate comes in
        lastAcked = UDP_Packet

        #Create the checksum for the servers response
        checksum = mk_csum(1, seq, b'')        

        #Create the packet
        resp_pkt = mk_pkt(1, seq, b'', checksum)

        #Send the packet to the client
        sock.sendto(resp_pkt, addr)
        print_success("Server has responded!")

        #Switch SEQ between 1 and 0
        seq = 1^seq

    else:
        #Print errors for both corruption and incorrect seq number
        if isCorrupt(UDP_Packet):
            print_error("Server :: Client Packet Checksum is corrupt!")

        #Client and Server SEQ numbers are not matching
        if seq != UDP_Packet[1]:
            print_error("Server :: Client Packet SEQ is incorrect!")

        #We ack the inverse of the current packets sequence number to notify the client an error occured
        checksum = mk_csum(1, 1^UDP_Packet[1], b'')
        resp_pkt = mk_pkt(1, 1^UDP_Packet[1], b'', checksum)
        sock.sendto(resp_pkt, addr)