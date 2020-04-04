import socket
import time
import signal

#Define constants for IP and PORT of server
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
INSTRUCTION = 'what is the current date and time?'

#Closes any open connection and the socket if interrupted (Ctrl-c)
def cleanup(sig, frame):
    print("\nServer was interuppted... Cleaning up socket")
    if conn: 
        print("Server is closing the open connection...")
        conn.close()
    sock.close()
    exit(0)

#Create stream socket (TCP) and bind on IP and PORT constants
conn = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
print("Created server on {}:{}".format(TCP_IP, TCP_PORT))

#set up signal handler to properly close sockets when interrupted
signal.signal(signal.SIGINT, cleanup)

#Loop indefinitely waiting for a connection
while True:
    #Max of 1 connection allowed on socket
    sock.listen(1)
    print("Server is waiting for a connection...")
    #Blocks until a client connects
    conn, addr = sock.accept()
    print("Client connected from: ", addr)
    #Loops while the connection is still open
    while conn:
        print("Server waiting to receive data...")
        #Blocks until the client submits some data, reads it and decodes it
        data = conn.recv(len(INSTRUCTION)).decode('utf-8')
        #Connection was closed, cleans up the socket that was handling the client
        if not data:
            conn.close()
            break

        print("Server received '{}' from client".format(data))
        #Creates response variable and sets the value based on the user request
        msg = ""
        if data.lower() == INSTRUCTION:
            msg = "Current Date and Time - " + time.strftime("%m/%d/%Y %H:%M:%S")
        else:
            msg = "Error: invalid instruction..."
        print("Server responding with '{}'".format(msg))
        #Sends entire message to client connection
        conn.sendall(msg.encode())
    print("Client has disconnected and their socket has been closed...")

