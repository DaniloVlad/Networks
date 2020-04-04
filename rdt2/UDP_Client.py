import socket
from util import *

#IP/Port configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

#Prepare socket data to be transmitted, also could have been done using btyes() function
packet_data = [b"NCC-1701", b"NCC-1422", b"NCC-1017"]

#Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

#Set the timeout duration for the blocking ops on the socket to 9ms
sock.settimeout(0.009)

#Stores the clients current seq number
seq = 0

#Stores the current packet data to send
count = 0

#Stores the last acked packet to detect duplicate acks
lastACK = None

while count < len(packet_data):

    #Create the packet with the current sequence number and data
    values = (0, seq, packet_data[count])
    checksum = mk_csum(*values)
    UDP_Packet = mk_pkt(0, seq, packet_data[count], checksum)

    #Send the packet to the server
    sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

    #Loop will continue until the proper ack is recieved
    while True:
        try:
            #Recieve and unpack data
            data, addr = sock.recvfrom(1024)
            pkt = unpacker.unpack(data)

            #If the packet isn't corrupt and the proper ack is recieved we can exit and send next data
            if not isCorrupt(pkt) and isACK(pkt, seq):
                #Increment count for next iteration
                count += 1

                #print the data we recieved
                print_packet(addr, pkt)

                #update the last acked packet to this one
                lastACK = pkt
                print_success("Client :: Server repsonse is correct") 

                #Switch the sequence number   
                seq = 1^seq
                break

            #If theres an error with the response we continue listening until a timeout happens
            else:

                #Duplicate ack, ignore it and wait for next response
                if pkt == lastACK:
                    print_warning("Client :: Duplicate ACK... Doing nothing...")
                    continue
                
                if isCorrupt(pkt):
                    print_error("Client :: Server response has corrupt CHECKSUM!")

                if not isACK(pkt, seq):
                    print_error("Client :: Server response has incorrect ACK!")
                
                continue

        #A timeout occured we must resend the packet!
        except socket.timeout:
            sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
            print_error("Client :: Socket timed out, retransmitting!")
    