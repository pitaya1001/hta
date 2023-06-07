import bisect
from .bitstream import *

english_character_frequencies = [ # 16x16
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0, 722,   0,    0,    2,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
11084,   58,   63,    1,    0,   31,   0,  317,   64,   64,  44,   0,  695,   62,  980,  266,
   69,   67,   56,    7,   73,    3,  14,    2,   69,    1, 167,   9,    1,    2,   25,   94,
    0,  195,  139,   34,   96,   48, 103,   56,  125,  653,  21,   5,   23,   64,   85,   44,
   34,    7,   92,   76,  147,   12,  14,   57,   15,   39,  15,   1,    1,    1,    2,    3,
    0, 3611,  845, 1077, 1884, 5870, 841, 1057, 2501, 3212, 164, 531, 2019, 1330, 3056, 4037,
  848,   47, 2586, 2919, 4771, 1707, 535, 1106,  152, 1243, 100,   0,    2,    0,   10,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   0,    0,    0,    0,   0,   0,    0,    0,    0,    0,
]

class HuffmanNode:
    def __init__(self, value, weight, left=None, right=None, parent=None):
        self.value = value
        self.weight = weight
        self.left = left
        self.right = right
        self.parent = parent

class HuffmanTree:
    def __init__(self, frequency_table):
        assert len(frequency_table) == 256

        # sort table
        leaf_nodes = [None] * 256 # used to generate the encoding table
        sorted_nodes = []
        for i, frequency in enumerate(frequency_table):
            node = HuffmanNode(value=i, weight=max(1, frequency))
            leaf_nodes[i] = node
            bisect.insort_left(sorted_nodes, node, key=lambda e: e.weight)

        # generate binary tree
        while True:
            lesser = sorted_nodes.pop(0)
            greater = sorted_nodes.pop(0)
            node = HuffmanNode(value=None, weight=lesser.weight+greater.weight, left=lesser, right=greater)
            lesser.parent = greater.parent = node

            if len(sorted_nodes) == 0:
                self.root_node = node
                break

            # insertion sort
            bisect.insort_left(sorted_nodes, node, key=lambda e:e.weight)

        # generate encoding table
        self.encoding_table = [None] * 256
        path = bytearray(256)
        for i, node in enumerate(leaf_nodes):
            # calculate sequence
            path_length = 0
            while node != self.root_node:
                path[path_length] = int(node.parent.left != node)
                path_length += 1
                node = node.parent

            # write sequence in reverse order
            bs = Bitstream(capacity=path_length)
            for j in range(path_length-1, 0-1, -1):
                bs.write_bit(path[j] == 1)
            self.encoding_table[i] = bs

default_huffman_tree = HuffmanTree(english_character_frequencies)
