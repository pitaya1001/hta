'''
The client encrypts datagrams before sending them to the server
The server decrypts datagrams received from the client before processing them

Note: the server does not encrypt datagrams
'''

encryption_table = bytes.fromhex('''
27 69 FD 87 60 7D 83 02 F2 3F 71 99 A3 7C 1B 9D
76 30 23 25 C5 82 9B EB 1E FA 46 4F 98 C9 37 88
18 A2 68 D6 D7 22 D1 74 7A 79 2E D2 6D 48 0F B1
62 97 BC 8B 59 7F 29 B6 B9 61 BE C8 C1 C6 40 EF
11 6A A5 C7 3A F4 4C 13 6C 2B 1C 54 56 55 53 A8
DC 9C 9A 16 DD B0 F5 2D FF DE 8A 90 FC 95 EC 31
85 C2 01 06 DB 28 D8 EA A0 DA 10 0E F0 2A 6B 21
F1 86 FB 65 E1 6F F6 26 33 39 AE BF D4 E4 E9 44
75 3D 63 BD C0 7B 9E A6 5C 1F B2 A4 C4 8D B3 FE
8F 19 8C 4D 5E 34 CC F9 B5 F3 F8 A1 50 04 93 73
E0 BA CB 45 35 1A 49 47 6E 2F 51 12 E2 4A 72 05
66 70 B8 CD 00 E5 BB 24 58 EE B4 80 81 36 A9 67
5A 4B E8 CA CF 9F E3 AC AA 14 5B 5F 0A 3B 77 92
09 15 4E 94 AD 17 64 52 D3 38 43 0D 0C 07 3C 1D
AF ED E7 08 B7 03 E6 8E AB 91 89 3E 2C 96 42 D9
78 DF D0 57 5D 84 41 7E CE F7 32 C3 D5 20 0B A7
''')

def encrypt_buffer(buffer, server_port):
    encryption_byte = (server_port & 0xff) ^ 0xcc

    buffer = bytearray(buffer) # make sure it is mutable

    # calculate checksum
    checksum = 0
    for byte in buffer:
        checksum ^= byte & 0xaa

    # encrypt buffer
    for i in range(len(buffer)):
        buffer[i] = encryption_table[buffer[i]]
        if i % 2 == 1: # if i is odd
            buffer[i] ^= encryption_byte

    return checksum.to_bytes(1, 'little') + buffer

decryption_table = bytes.fromhex('''
B4 62 07 E5 9D AF 63 DD E3 D0 CC FE DC DB 6B 2E
6A 40 AB 47 C9 D1 53 D5 20 91 A5 0E 4A DF 18 89
FD 6F 25 12 B7 13 77 00 65 36 6D 49 EC 57 2A A9
11 5F FA 78 95 A4 BD 1E D9 79 44 CD DE 81 EB 09
3E F6 EE DA 7F A3 1A A7 2D A6 AD C1 46 93 D2 1B
9C AA D7 4E 4B 4D 4C F3 B8 34 C0 CA 88 F4 94 CB
04 39 30 82 D6 73 B0 BF 22 01 41 6E 48 2C A8 75
B1 0A AE 9F 27 80 10 CE F0 29 28 85 0D 05 F7 35
BB BC 15 06 F5 60 71 03 1F EA 5A 33 92 8D E7 90
5B E9 CF 9E D3 5D ED 31 1C 0B 52 16 51 0F 86 C5
68 9B 21 0C 8B 42 87 FF 4F BE C8 E8 C7 D4 7A E0
55 2F 8A 8E BA 98 37 E4 B2 38 A1 B6 32 83 3A 7B
84 3C 61 FB 8C 14 3D 43 3B 1D C3 A2 96 B3 F8 C4
F2 26 2B D8 7C FC 23 24 66 EF 69 64 50 54 59 F1
A0 74 AC C6 7D B5 E6 E2 C2 7E 67 17 5E E1 B9 3F
6C 70 08 99 45 56 76 F9 9A 97 19 72 5C 02 8F 58
''')

def decrypt_buffer(buffer, server_port):
    decryption_byte = (server_port & 0xff) ^ 0xcc

    packet_checksum = buffer[0] # save checksum to compare later

    buffer = bytearray(buffer[1:]) # make sure it is mutable

    # decrypt buffer
    for i in range(len(buffer)):
        if i % 2 == 1: # if i is odd
            buffer[i] ^= decryption_byte
        buffer[i] = decryption_table[buffer[i]]

    # calculate checksum
    #checksum = 0
    #for byte in buffer:
    #    checksum ^= byte & 0xaa
    #if checksum != packet_checksum:
    #    print('bad checksum')

    return buffer
