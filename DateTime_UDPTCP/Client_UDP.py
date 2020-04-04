import socket

#Define constants for IP and PORT of the server
UDP_IP = "127.0.0.1"
UDP_PORT = 5004

#Create the datagram socket (UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    #Get message from user to send to server
    msg = str(input("Enter a message to send to the server (quit to exit): "))
    if msg == "quit" or msg == '': break
    print("Client sending {} to server".format(msg))
    #Send message to server
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    #Wait until the server responds
    data, addr = sock.recvfrom(1024)
    #Decode data as utf-8
    data = data.decode('utf-8')
    print("Client got response: ", data)

sock.close()