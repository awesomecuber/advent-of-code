import functools
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day16.txt")) as f:
    puzzle_input = f.readline()

# puzzle_input = '9C0141080250320F1802104A08'

binary = bin(int(puzzle_input, 16))[2:].zfill(len(puzzle_input) * 4)

version_num_sum = 0


def read_packet(binary):
    global version_num_sum

    value = 0
    length = 0

    packet_version = int(binary[:3], 2)
    version_num_sum += packet_version
    binary = binary[3:]
    packet_type = int(binary[:3], 2)
    binary = binary[3:]
    length += 6

    if packet_type == 4:
        bin_num = ""
        keep_reading = True
        while keep_reading:
            if binary[0] == "0":
                keep_reading = False
            binary = binary[1:]
            bin_num += binary[:4]
            binary = binary[4:]
            length += 5
        value = int(bin_num, 2)
    else:
        length_type_id = binary[0]
        binary = binary[1:]

        values = []
        length += 1
        if length_type_id == "0":
            sub_packets_length = int(binary[:15], 2)
            binary = binary[15:]
            length += 15
            sub_packets = binary[:sub_packets_length]
            while len(sub_packets) > 0 and int(sub_packets, 2) > 2:
                sub_packet_value, sub_packet_length = read_packet(sub_packets)
                values.append(sub_packet_value)
                sub_packets = sub_packets[sub_packet_length:]
            binary = binary[sub_packets_length:]
            length += sub_packets_length
        else:
            num_sub_packets = int(binary[:11], 2)
            binary = binary[11:]
            length += 11
            for _ in range(num_sub_packets):
                sub_packet_value, sub_packet_length = read_packet(binary)
                values.append(sub_packet_value)
                binary = binary[sub_packet_length:]
                length += sub_packet_length
        match packet_type:
            case 0:
                value = sum(values)
            case 1:
                value = functools.reduce(lambda x, y: x * y, values)
            case 2:
                value = min(values)
            case 3:
                value = max(values)
            case 5:
                value = 1 if values[0] > values[1] else 0
            case 6:
                value = 1 if values[0] < values[1] else 0
            case 7:
                value = 1 if values[0] == values[1] else 0

    return value, length


print(read_packet(binary)[0])
