import socket

#Define constants for IP and PORT of the server
TCP_IP = '127.0.0.1'
TCP_PORT = 5005

print("Client attempting to connect to {}:{}".format(TCP_IP, TCP_PORT))
#Create socket object and connect to the constant IP and PORT
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

while True:
    #Get message from user to submit to server
    msg = str(input("Enter a message to send to server (quit to exit): "))
    if msg == "quit" or msg == '': break
    print("Sending '{}' to server".format(msg))
    #Send data to server
    sock.sendall(msg.encode())
    #Wait for servers response and decode the data
    data = sock.recv(1024).decode('utf-8')
    if not data: 
        print("Socket was closed by server...")
        break
    print("Client got response: ", data)

#Close the socket
sock.close()