import socket
import time
import signal

#Define constants for IP and PORT of the server
UDP_IP = '127.0.0.1'
UDP_PORT = 5004
INSTRUCTION = 'what is the current date and time?'

#Closes socket if interupted
def cleanup(sig, frame):
    print("\nServer was interuppted, closing the socket")
    sock.close()
    exit(0)

#Create and bind a datagram socket (UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Created socket on {}:{}".format(UDP_IP, UDP_PORT))

#set up signal handler for interupts
signal.signal(signal.SIGINT, cleanup)

#Loop indefinitely waiting for packets
while True:
    #recv() blocks until data is availible
    data, addr = sock.recvfrom(len(INSTRUCTION))
    #Data is returned as bytes array and must be decoded
    data = data.decode('utf-8')
    print("Client sent data from: ", addr)
    print("Server Received '{}' from client".format(data))
    msg = ""
    #Set return message based on what was received
    if data.lower() == INSTRUCTION:
        msg = "Current Date and Time - " + time.strftime("%m/%d/%Y %H:%M:%S")
    else:
        msg = "Error: invalid instruction...."
    #Send return message to the address data was received from
    sock.sendto(msg.encode(), addr)
    print("Server has sent back: ", msg)