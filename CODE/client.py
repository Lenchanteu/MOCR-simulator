import socket
import struct
import time
import zlib

HOST = 'localhost'
PORT = 8841
packet_format = '>B4sBBIdHI102sB'

def read_MRSTP_packet(data, sock):
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
    if time.time() >= time_of_send + 0.5:
        print(Warning("Network is congested, slowing down the packet transmission."))
        network_latency = "bad"
    
    #dispatch
    if info_type == 0x01:
        #hello_message(sock, message)
        pass
    elif info_type == 0x02:
        pass
client_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)