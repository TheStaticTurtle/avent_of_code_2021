import enum
import io
import os
import time
from dataclasses import dataclass
from typing import List

input_data = open("input.txt", "r").read().replace("\n", "")

def prod(iterable):
    p = 1
    for n in iterable:
        p *= n
    return p


class PacketType(enum.Enum):
    TYPE_SUM = 0
    TYPE_PRODUCT = 1
    TYPE_MIN = 2
    TYPE_MAX = 3
    TYPE_GRT = 5
    TYPE_LST = 6
    TYPE_EQL = 7
    TYPE_LITERAL = 4


class Packet:
    LEN_TYPE_ID_BITS = 15
    LEN_TYPE_ID_COUNT = 11

    def __init__(self, version, type: PacketType, raw_value, value):
        self.version = version
        self.type = type
        self.raw_value = raw_value
        self._value = value

    def __repr__(self):
        if self.type != PacketType.TYPE_LITERAL:
            return f"<Packet version={self.version} type={self.type} childs={self._value}>"
        else:
            return f"<Packet version={self.version} type={self.type} value={self.value}>"

    def pprint(self, tab=0):
        tab_string = "    "*tab
        if self.type != PacketType.TYPE_LITERAL:
            out = tab_string + f"<Packet version={self.version} type={self.type} value={self.value} childs=[\n"
            for child in self._value:
                out += child.pprint(tab=tab+1) + "\n"
            out += tab_string + f"]>"
            return out
        else:
            return tab_string+f"<Packet version={self.version} type={self.type} value={self.value}>"

    @property
    def version_sum(self):
        version_sum = self.version
        if isinstance(self._value, list):
            for child in self._value:
                version_sum += child.version_sum
        return version_sum

    @property
    def value(self):
        if self.type == PacketType.TYPE_LITERAL:
            return self._value

        if self.type == PacketType.TYPE_SUM:
            return sum(c.value for c in self._value)
        if self.type == PacketType.TYPE_PRODUCT:
            return prod(c.value for c in self._value)
        if self.type == PacketType.TYPE_MIN:
            return min(c.value for c in self._value)
        if self.type == PacketType.TYPE_MAX:
            return max(c.value for c in self._value)
        if self.type == PacketType.TYPE_GRT:
            assert len(self._value) == 2
            return 1 if self._value[0].value > self._value[1].value else 0
        if self.type == PacketType.TYPE_LST:
            assert len(self._value) == 2
            return 1 if self._value[0].value < self._value[1].value else 0
        if self.type == PacketType.TYPE_EQL:
            assert len(self._value) == 2
            return 1 if self._value[0].value == self._value[1].value else 0


    @classmethod
    def from_bitstream(cls, stream: io):
        version = eval(f"0b{stream.read(3)}")
        type_id = PacketType(eval(f"0b{stream.read(3)}"))

        if type_id != PacketType.TYPE_LITERAL:
            length_type_id = cls.LEN_TYPE_ID_BITS if stream.read(1) == '0' else cls.LEN_TYPE_ID_COUNT
            length = eval(f"0b{stream.read( length_type_id )}")

            packets = []

            if length_type_id == cls.LEN_TYPE_ID_COUNT:
                for i in range(length):
                    packets.append(Packet.from_bitstream(stream))

            if length_type_id == cls.LEN_TYPE_ID_BITS:
                pos = stream.tell()
                data = stream.read(length)
                stream.seek(pos+length)

                tmp_stream = io.StringIO(data)
                while True:
                    try:
                        packet = Packet.from_bitstream(tmp_stream)
                        packets.append(packet)
                    except Exception as e:
                        break

            return Packet(version, type_id, None, packets)

        else:
            value = ""
            while stream.read(1) == "1":
                value += stream.read(4)
            value += stream.read(4)

        return Packet(version, type_id, value, eval(f"0b{value}"))


bit_string = ''.join([f"{byte:08b}" for byte in bytes.fromhex(input_data)])
bitstream = io.StringIO(bit_string)

packet = Packet.from_bitstream(bitstream)
print(packet.pprint())
print(f"Version sum: {packet.version_sum}")
print(f"Value: {packet.value}")