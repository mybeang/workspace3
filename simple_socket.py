####
# Send the packet some interface using udp
###
import socket


data = b'\xa0\xce\xc8\x06c\x95\xa0\xce\xc8\x05e\x87\x08\x00E\x00\x00\x14\x00\x01\x00\x00@\x00yd\xc0\xc0\xc0\x01\xc0\xc0\xc0\x020000000000'
sock1 = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)

sock1.bind(("192.192.192.2", 0))
sock1.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)
sock1.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
sock1.settimeout(5)
#sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#while True:
 #   sock1.sendto(data, ("192.192.192.2", 0))
buf = list()
rev_data = ""
while True:
    try:
        rev_data = sock1.recvfrom(1024)
    except socket.timeout:
        break
    else:
        if rev_data:
            buf.append(rev_data[0])

print(len(buf))
sock1.recvfrom(1024)