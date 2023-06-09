import struct
from sa import Vec2, Vec3, Quat
from .common import SAMP_ENCODING

def TO_BYTES(bit_count): return (bit_count + 7) // 8
def TO_BITS(byte_count): return byte_count * 8
def DIV_INT_CEIL(a, b): return (a - 1) // b + 1

# copy n bits from i(at offset io) to o(at offset oo)
# i: input buffer
# o: output buffer (bytearray)
# n: number of bits to copy
# io: input offset in bits
# oo: output offset in bits
def copy_bits(i, o, n, io, oo):
    # determine helper variables
    ibi = io // 8 # index(in bytes) in input of first byte read from
    obi = oo // 8 # index(in bytes) in output first byte written to

    # determine how many bytes will be written to in o
    # n      pattern  write_byte_count
    # 0      P0       0        =   0
    # 1      P1       1        =   1 + 0
    # 2-8    P2       1 or 2   =   1 + 0 + (0 or 1)
    # 9      P1       2        =   1 + 1
    # 10-16  P2       2 or 3   =   1 + 1 + (0 or 1)
    # 17     P1       3        =   1 + 2
    # 18-24  P2       3 or 4   =   1 + 2 + (0 or 1)
    # 25     P1       4        =   1 + 3
    #
    # 3 patterns:
    # PATTERN 0(P0) n = 0     -> write_byte_count = 0
    # PATTERN 1(P1) n % 8 = 1 -> write_byte_count = 1 + ((n-1) // 8)
    # PATTERN 2(P2) else      -> write_byte_count = 1 + ((n-2) // 8) + (0 if (((oo%8)+((n-2)%8)+2)<=8) else 1)
    if n == 0:       write_byte_count = 0
    elif n % 8 == 1: write_byte_count = 1 + ((n-1) // 8)
    else:            write_byte_count = 1 + ((n-2) // 8) + (0 if (((oo % 8)+((n-2) % 8)+2)<=8) else 1)

    k = 0
    bits_written = 0
    bits_just_written = 0
    #print(f'write_byte_count={write_byte_count} ibi={ibi} obi={obi}')

    # iterate each byte written to in output and modify it
    for j in range(write_byte_count):
        #calculate some helper variables; determine if input bits are in one or two bytes
        if j == 0:
            obo = oo % 8
            if obo + n < 8:
                obr = 8 - obo - n
            else:
                obr = 0
            bits_just_written = 8 - obo - obr

            ibo = io % 8
        else:
            ibo = (ibo + bits_just_written) % 8

            obo = 0
            if j != write_byte_count - 1:
                obr = 0
                bits_just_written = 8
            else:
                obr = 8 - (n - bits_written)
                bits_just_written = n - bits_written

        if ibo + bits_just_written <= 8:
            # bits come from ONE byte in input
            ibr = 8 - ibo - bits_just_written
            input_one_byte = True # 1
        else:
            # bits come from TWO byte in input
            ibr = 16 - ibo - bits_just_written
            input_one_byte = False # 2

        bits_written += bits_just_written

        # calculate input bits
        if input_one_byte:
            byte = (i[ibi + k] >> ibr) & (0xff >> (ibo+ibr))
        else:
            bit_count = 16 - ibo - ibr
            hi_bit_count = 8 - ibo
            lo_bit_count = bit_count - hi_bit_count
            hi = (i[ibi + k] & (0xff >> ibo))
            lo = i[ibi + k + 1] >> ibr
            byte = (hi << lo_bit_count) | lo
        if ibo + bits_just_written >= 8:
            k += 1

        # clear bits
        clear_mask = ((0xff >> (obo + obr)) << obr) & 0xff
        o[obi + j] &= ~clear_mask

        # or bits
        o[obi + j] |= (byte << obr)

class Bitstream:
    def __init__(self, data=None, data_len_in_bits=0, capacity=0):
        maximum_data_len_in_bits = len(data) * 8 if data else 0
        if data_len_in_bits == 0:
            self.len = maximum_data_len_in_bits
        else:
            if data_len_in_bits > maximum_data_len_in_bits:
                raise ValueError('bad data_len_in_bits')
            self.len = data_len_in_bits
        self.data = data if data else bytearray(max(capacity, TO_BYTES(self.len)))
        self.read_offset = 0 # read offset in bits
        self.write_offset = 0 # write offset in bits

    def to_bytes(self):
        return self.data[:TO_BYTES(self.len)]

    def reserve(self, size_in_bytes):
        if len(self.data) >= size_in_bytes:
            return
        self.data += bytearray(size_in_bytes - len(self.data))

    def empty(self):
        return self.len == 0

    def capacity(self):
        return len(self.data)

    def skip_bits(self, bit_count):
        self.read_offset += bit_count

    def skip_bytes(self, byte_count):
        self.read_offset += byte_count * 8

    def get_read(self):
        return self.read_offset

    def set_read(self, offset):
        self.read_offset = offset

    def get_write(self):
        return self.write_offset

    def set_write(self, offset):
        self.write_offset = offset

    def align_read_to_byte_boundary(self):
        # if not aligned to byte boundary
        if self.read_offset % 8 != 0:
            # add the number of bits remaining to be aligned
            self.read_offset += 8 - (self.read_offset % 8)

    def align_write_to_byte_boundary(self):
        # if not aligned to byte boundary
        if self.write_offset % 8 != 0:
            # add the number of bits remaining to be aligned
            self.write_offset += 8 - (self.write_offset % 8)

    def reset(self):
        self.read_offset = 0
        self.write_offset = 0
        self.len = 0

    def unread_bits_count(self):
        return self.len - self.read_offset

    def read_bit(self):
        bit = (self.data[self.read_offset // 8] >> (7 - self.read_offset % 8)) & 1
        self.read_offset += 1
        return bit

    # o: bytearray that receives the data
    # n: number of bits to read from the Bitstream
    # oo(in bits) output offset in the dst bytearray to write the data to
    def read_bits(self, o, n, oo=0):
        copy_bits(self.data, o, n, self.read_offset, oo)
        self.read_offset += n

    def read_bits_num(self, n):
        num = 0
        for i in range(n):
            num += self.read_bit() << (n - 1 - i)
        return num

    def read_aligned(self, o, byte_count):
        bit_count = byte_count * 8
        self.align_read_to_byte_boundary()
        for j in range(byte_count):
            o[j] = self.data[(self.read_offset // 8) + j]
        self.read_offset += bit_count

    def read_u8(self):
        return struct.unpack('B', self.read_buffer(8))[0]

    def read_i8(self):
        return struct.unpack('b', self.read_buffer(8))[0]

    def read_u16(self):
        return struct.unpack('H', self.read_buffer(16))[0]

    def read_i16(self):
        return struct.unpack('h', self.read_buffer(16))[0]

    def read_u32(self):
        return struct.unpack('I', self.read_buffer(32))[0]

    def read_i32(self):
        return struct.unpack('i', self.read_buffer(32))[0]

    def read_u64(self):
        return struct.unpack('Q', self.read_buffer(64))[0]

    def read_i64(self):
        return struct.unpack('q', self.read_buffer(64))[0]

    def read_float(self):
        return struct.unpack('f', self.read_buffer(32))[0]

    # 00 00 00 20
    # 1 1 1 + bin(20h)
    # o: bytearray that receives the data
    def read_compressed(self, o, byte_count):
        one_count = 0
        for i in range(byte_count):
            if one_count == byte_count - 1:
                break
            if self.read_bit() == 1:
                one_count += 1
            else: break
        for i in range(one_count): # fill zeros
            o[byte_count - one_count + i] = 0x00
        if one_count < byte_count - 1:
            self.read_bits(o, (byte_count - one_count) * 8)
        else:
            bits_to_read = 4 if self.read_bit() else 8
            self.read_bits(o, bits_to_read, bits_to_read % 8)

    def read_compressed_u16(self):
        b = bytearray(2)
        self.read_compressed(b, 2)
        return struct.unpack('H', b)[0]

    def read_compressed_u32(self):
        b = bytearray(4)
        self.read_compressed(b, 4)
        return struct.unpack('I', b)[0]

    # return [-1, +1]
    def read_compressed_float(self):
        return (self.read_u16() / 32767.5) - 1.0

    # n: bit count
    def read_buffer(self, n):
        buffer = bytearray(TO_BYTES(n))
        self.read_bits(buffer, n)
        return buffer

    def read_dynamic_buf8(self):
        return self.read_buffer(TO_BITS(self.read_u8()))

    def read_dynamic_buf16(self):
        return self.read_buffer(TO_BITS(self.read_u16()))

    def read_dynamic_buf32(self):
        return self.read_buffer(TO_BITS(self.read_u32()))

    def read_dynamic_str8(self):
        return self.read_dynamic_buf8().decode(SAMP_ENCODING)

    def read_dynamic_str16(self):
        return self.read_dynamic_buf16().decode(SAMP_ENCODING)

    def read_dynamic_str32(self):
        return self.read_dynamic_buf32().decode(SAMP_ENCODING)

    def read_huffman_buffer(self, root_node):
        output = bytearray()
        node = root_node
        bit_count = self.read_compressed_u16()
        for _ in range(bit_count):
            node = node.left if (self.read_bit() == 0) else node.right
            if node.left is None and node.right is None:
                output += bytearray([node.value])
                node = root_node
        return output

    def read_vec2(self):
        x = self.read_float()
        y = self.read_float()
        return Vec2(x, y)

    def read_vec3(self):
        x = self.read_float()
        y = self.read_float()
        z = self.read_float()
        return Vec3(x, y, z)

    def read_compressed_vec3(self):
        length = self.read_float()
        if length > 0.00001:
            x = self.read_compressed_float()
            y = self.read_compressed_float()
            z = self.read_compressed_float()
        else:
            x = y = z = 0.0
        return Vec3(x, y, z)

    def read_quat(self):
        w = self.read_float()
        x = self.read_float()
        y = self.read_float()
        z = self.read_float()
        return Quat(w, x, y, z)

    def read_norm_quat(self):
        w_sign = -1 if self.read_bit() else 1
        x_sign = -1 if self.read_bit() else 1
        y_sign = -1 if self.read_bit() else 1
        z_sign = -1 if self.read_bit() else 1
        x = x_sign * (self.read_u16() / 2**16)
        y = y_sign * (self.read_u16() / 2**16)
        z = z_sign * (self.read_u16() / 2**16)
        w = w_sign * min(1 - x*x - y*y - z*z, 0)**0.5
        return Quat(w, x, y, z)

    # WRITE METHODS

    # n: size of bit sequence to be written
    def check_resize(self, n):
        if n + self.len > TO_BITS(len(self.data)): # resize buffer
            self.data = self.data + bytearray(max(TO_BYTES(n*2), len(self.data)))

    def update_len(self):
        self.len = self.write_offset if (self.write_offset > self.len) else self.len

    def write_bit(self, bit):
        self.check_resize(1)
        if bit == 1: # set bit
            self.data[self.write_offset // 8] |= 1 << (7 - (self.write_offset % 8))
        else: # clear bit
            self.data[self.write_offset // 8] &= ~(1 << (7 - (self.write_offset % 8)))
        self.write_offset += 1
        self.update_len()

    def write_bits(self, i, n, io=0):
        self.check_resize(n)
        copy_bits(i, self.data, n, io, self.write_offset)
        self.write_offset += n
        self.update_len()

    def write_bits_num(self, num, n):
        for i in range(n):
            self.write_bit(int(not not (num & (1 << (n - 1 - i)))))

    def write_aligned(self, buffer):
        self.check_resize(len(buffer))
        self.align_write_to_byte_boundary()
        for i in range(len(buffer)):
            self.data[self.write_offset // 8 + i] = buffer[i]
        self.write_offset += len(buffer) * 8
        self.update_len()

    def write_u8(self, n):
        self.write_bits(struct.pack('B', n), 8)

    def write_i8(self, n):
        self.write_bits(struct.pack('b', n), 8)

    def write_u16(self, n):
        self.write_bits(struct.pack('H', n), 16)

    def write_i16(self, n):
        self.write_bits(struct.pack('h', n), 16)

    def write_u32(self, n):
        self.write_bits(struct.pack('I', n), 32)

    def write_i32(self, n):
        self.write_bits(struct.pack('i', n), 32)

    def write_u64(self, n):
        self.write_bits(struct.pack('Q', n), 32)

    def write_i64(self, n):
        self.write_bits(struct.pack('q', n), 32)

    def write_float(self, float):
        self.write_bits(struct.pack('f', float), 32)

    def write_compressed(self, b):
        i = len(b) - 1
        while i > 0:
            if b[i] == 0x00:
                self.write_bit(1)
            else:
                self.write_bit(0)
                self.write_bits(b, (i + 1) * 8)
                return
            i -= 1

        bit = int((b[i] & 0xF0) == 0x00)
        self.write_bit(bit)
        sz = 4 if bit else 8
        self.write_bits(b[i:i+1], sz, sz % 8)

    def write_compressed_u16(self, value):
        self.write_compressed(struct.pack('H', value))

    def write_compressed_u32(self, value):
        self.write_compressed(struct.pack('I', value))

    # value = [-1, +1]
    def write_compressed_float(self, value):
        if value < -1.0: value = -1.0
        elif value > 1.0: value = 1.0
        self.write_u16(int((value + 1.0) * 32767.5))

    def write_buffer(self, buffer, n):
        self.write_bits(buffer, n)

    def write_dynamic_buf8(self, buffer):
        self.write_u8(len(buffer))
        self.write_buffer(buffer, TO_BITS(len(buffer)))

    def write_dynamic_buf16(self, buffer):
        self.write_u16(len(buffer))
        self.write_buffer(buffer, TO_BITS(len(buffer)))

    def write_dynamic_buf32(self, buffer):
        self.write_u32(len(buffer))
        self.write_buffer(buffer, TO_BITS(len(buffer)))
    
    def write_dynamic_str8(self, s):
        self.write_dynamic_buf8(s.encode(SAMP_ENCODING))

    def write_dynamic_str16(self, s):
        self.write_dynamic_buf16(s.encode(SAMP_ENCODING))

    def write_dynamic_str32(self, s):
        self.write_dynamic_buf32(s.encode(SAMP_ENCODING))

    def write_huffman_buffer(self, buffer, encoding_table):
        bit_count = sum(encoding_table[byte].len for byte in buffer)
        self.write_compressed_u16(bit_count)
        for byte in buffer:
            self.write_bits(encoding_table[byte].data, encoding_table[byte].len)

    def write_vec2(self, v):
        self.write_float(v.x)
        self.write_float(v.y)

    def write_vec3(self, v):
        self.write_float(v.x)
        self.write_float(v.y)
        self.write_float(v.z)

    def write_compressed_vec3(self, v):
        length = (v.x**2 + v.y**2 + v.z**2)**0.5 # theorem of pitagoras
        self.write_float(length)
        if length > 0.00001:
            self.write_compressed_float(v.x / length)
            self.write_compressed_float(v.y / length)
            self.write_compressed_float(v.z / length)

    def write_quat(self, q):
        self.write_float(q.w)
        self.write_float(q.x)
        self.write_float(q.y)
        self.write_float(q.z)

    def write_norm_quat(self, q):
        self.write_bit(q.w < 0)
        self.write_bit(q.x < 0)
        self.write_bit(q.y < 0)
        self.write_bit(q.z < 0)
        self.write_u16(int(abs(q.x) * 2**16))
        self.write_u16(int(abs(q.y) * 2**16))
        self.write_u16(int(abs(q.z) * 2**16))
