import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day16.txt")) as f:
    puzzle_input = f.readline()

# puzzle_input = 'A0016C880162017C3686B18A3D4780'

binary = bin(int(puzzle_input, 16))[2:].zfill(len(puzzle_input) * 4)

version_num_sum = 0
def read_packet(binary):
    global version_num_sum

    length = 0

    packet_version = int(binary[:3], 2)
    version_num_sum += packet_version
    binary = binary[3:]
    packet_type = int(binary[:3], 2)
    binary = binary[3:]
    length += 6

    if packet_type == 4:
        bin_num = ''
        keep_reading = True
        while keep_reading:
            if binary[0] == '0':
                keep_reading = False
            binary = binary[1:]
            bin_num += binary[:4]
            binary = binary[4:]
            length += 5
    else:
        length_type_id = binary[0]
        binary = binary[1:]
        length += 1
        if length_type_id == '0':
            sub_packets_length = int(binary[:15], 2)
            binary = binary[15:]
            length += 15
            sub_packets = binary[:sub_packets_length]
            while len(sub_packets) > 0 and int(sub_packets, 2) > 2:
                sub_packet_length = read_packet(sub_packets)
                sub_packets = sub_packets[sub_packet_length:]
            binary = binary[sub_packets_length:]
            length += sub_packets_length
        else:
            num_sub_packets = int(binary[:11], 2)
            binary = binary[11:]
            length += 11
            for _ in range(num_sub_packets):
                sub_packet_length = read_packet(binary)
                binary = binary[sub_packet_length:]
                length += sub_packet_length

    return length

while len(binary) > 0 and int(binary, 2) > 2:
    binary = binary[read_packet(binary):]
print(version_num_sum)