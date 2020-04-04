from random import random

#random() generates numbers from [0,1) (doesn't include 1). 
#Setting these to -1 will disable errors from occuring and 1 will cause errors 100% of the time
NETWORK_DELAY = 0.33
NETWORK_LOSS = 0.5
CORRUPT_CHECKSUM = 0.5

#All the functions return true or false so they can easily be integrated into the server code
def Network_Delay():
    if random() <= NETWORK_DELAY: #Default is 33% packets are delayed
        return True
    else:
        return False

def Network_Loss():
    if random() <= NETWORK_LOSS: #Default is 50% packets are lost
        return True
    else:
        return False

def Packet_Checksum_Corrupter():
    if random() <= CORRUPT_CHECKSUM: #Default is 50% packets are corrupt
        return True
    else:
        return False
