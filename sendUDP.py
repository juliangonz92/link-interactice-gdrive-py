import socket

UDP_IP = "192.168.0.43"
UDP_PORT = 5000
MESSAGE = 'take photo'
#MESSAGE = 'hello'
bufferSize = 1024

bytestosend = MESSAGE.encode('utf-8')

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytestosend, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(bufferSize)

print('Data from server: ', data)