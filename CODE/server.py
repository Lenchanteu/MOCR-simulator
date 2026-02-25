import socket
import struct
import time
import zlib

HOST = 'localhost'
PORT = 8841
packet_format = '>B4sBBIdHI102sB'

def split_IP(ip):
    a = ip.split('.')
    b = hex(a[0])
    c = hex(a[1])
    d = hex(a[2])
    e = hex(a[3])
    return b , c, d, e

def first_transmission(sock):
    hello = 0x55
    closing = 0xAA
    name = socket.gethostbyname(HOST)
    name = split_IP(name)
    computer_type = 0x01
    computer_number = 0x00
    packet_number = 0x01
    info_type = 0x01
    b = [0xA2]
    for i in range(101):
        b.append(0x00)
    message = b
    sending_time = time.time()
    checksum = zlib.crc32(struct.pack('>B4sBBIdH102sB', hello, name, computer_type, computer_number, packet_number, sending_time, info_type, message, closing))
    transmission = struct.pack(packet_format, hello, name, computer_type, computer_number, packet_number, sending_time, info_type, checksum, message, closing)
    sock.send(transmission)
def recv_exact(sock, size):
    buffer = b''
    while len(buffer) < size:
        chunk = sock.recv(size - len(buffer))
        if not chunk:
            raise ConnectionError("Connection closed")
        buffer += chunk
    return buffer

def read_MRSTP_packet(data):
    packet_state = "good"
    network_latency = "good"
    unpack_data = struct.unpack(packet_format, data)
    #hello message
    hello = unpack_data[0]
    #Sender info
    name = unpack_data[1] #IP address of sender
    ip = socket.inet_ntoa(name)
    computer_type = unpack_data[2] #server or client
    computer_number = unpack_data[3]
    #Packet info
    packet_number = unpack_data[4]
    time_of_send = unpack_data[5]
    info_type = unpack_data[6]
    checksum = unpack_data[7]
    #message
    message = unpack_data[8]
    #closing
    closing = unpack_data[9]

    #checks
    if hello != 0x55:
        print(Warning("The packet was corrupted. Discarding. Reason: the hello message is wrong"))
        packet_state = "wrong"
    if closing != 0xAA:
        print(Warning("The packet was corrupted. Discarding. Reason: the closing message is wrong"))
        packet_state = "wrong"
    if computer_type != 0x00:
        print(Warning("The packet sender is not a client. Discarding. Reason: the info was not directed to the server"))
        packet_state = "wrong"
    check_data = struct.pack('>B4sBBIdH102sB', unpack_data[0], unpack_data[1], unpack_data[2], unpack_data[3], unpack_data[4], unpack_data[5], unpack_data[6], unpack_data[8], unpack_data[9])
    if checksum != zlib.crc32(check_data):
        print(Warning("The packet was corrupted. Discarding. Reason: the checksums did not match."))
        packet_state = "wrong"
    if time.time() > time_of_send + 2:
        print(Warning("Network is congested, slowing down the packet transmission."))
        network_latency = "bad"
    



server_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_co.bind((HOST, PORT))
server_co.listen(1)
conn, addr = server_co.accept()
data = recv_exact(conn, struct.calcsize(packet_format))



