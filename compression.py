import sys
import unittest

import test_data
import tests
import time


class Node:
    def __init__(self, left=None, right=None, freq=None, value=None, code=''):
        self.left = left
        self.right = right
        self.freq = freq
        self.value = value
        self.code = code


def validate_input(data: bytes):
    # check if data exists, is valid, and contains more than one element
    try:
        if data is not None and data.decode() and len(data) > 1:
            return True
        else:
            return False
    except(UnicodeDecodeError, AttributeError):
        return False


# source: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
def print_tree(node, level=0):
    if node is not None:
        print_tree(node.left, level + 1)
        if node.value is not None:
            print(' ' * 4 * level + '-> ' + str(node.value) + ": " + str(node.freq))
        else:
            print(' ' * 4 * level + '-> ' + str(node.freq))
        print_tree(node.right, level + 1)


def get_frequency_table(data: bytes) -> dict:
    frequencies = {}
    unique_values = list(set(data))
    for u in unique_values:
        num_occurrences = data.count(u)
        frequencies[u] = num_occurrences
    return frequencies


def create_tree(frequencies: dict):
    # create a leaf node for each of the unique values in the dataset
    nodes = []
    for key, val in frequencies.items():
        nodes.append(Node(value=key, freq=val))
    # iterate until one node exists (i.e. root node)
    while len(nodes) > 1:
        # sort the nodes in ascending order by frequency
        sorted_nodes = sorted(nodes, key=lambda x: x.freq)
        # find the 2 nodes with minimum frequency
        left_child = sorted_nodes[0]
        right_child = sorted_nodes[1]
        freq = left_child.freq + right_child.freq
        # assign binary codes to the branches
        left_child.code = 0
        right_child.code = 1
        # create new node
        new_node = Node(left=left_child, right=right_child, freq=freq)
        # remove the used nodes & replace with new node
        nodes.remove(left_child)
        nodes.remove(right_child)
        nodes.append(new_node)
    return nodes[0]


def get_code(tree_node, value='', code_values={}):
    current_code = value + str(tree_node.code)
    if tree_node.left:
        get_code(tree_node.left, current_code)
    if tree_node.right:
        get_code(tree_node.right, current_code)
    if not tree_node.left and not tree_node.right:
        code_values[tree_node.value] = current_code
    return code_values


def encode(data: bytes, codes: dict):
    encoded_value = ''
    for d in data:
        encoded_value = ''.join([encoded_value, codes[d]])
    return encoded_value


def decode(encoded_value: str, codes: dict):
    data_buffer = []

    while encoded_value:
        for key, val in codes.items():
            if encoded_value.startswith(val):
                data_buffer.append(key)
                encoded_value = encoded_value[len(val):]
    return bytes(data_buffer)


def calc_compression_ratio(encoded_data: str, raw_data_size: int):
    num_bytes_encoded = len(encoded_data) / 8
    # calculate compression ratio: # bytes from raw data / # bytes from encoded data
    comp_ratio = num_bytes_encoded / raw_data_size
    return comp_ratio


def byte_compress(data: bytes):
    # start timer for run time of encoding
    start = time.time()

    # check if input is an array of bytes > 1
    if not validate_input(data):
        sys.exit("Invalid input. Data must be an array of bytes and have length > 1.")

    # generate frequency table
    frequencies = get_frequency_table(data)

    # create binary tree
    root_node = create_tree(frequencies)

    # calculate codes for each leaf node
    codes = get_code(root_node)

    # encode the byte array
    encoded_value = encode(data, codes)

    # stop timer, encoding complete
    end = time.time()

    # print binary tree (if leaf node --> value: frequency)
    # print_tree(root_node)

    # decode
    decoded_buffer = decode(encoded_value, codes)

    # check if encoding was lossless
    if data != decoded_buffer:
        print("Lossless Algorithm: FALSE")

    # calculate compression ratio -> # of encoded bytes per 1 raw byte
    compression_ratio = calc_compression_ratio(encoded_value, len(data))

    # print results
    print("Size of raw data: " + str(len(data)) + " bytes")
    print('Size of encoded data: ' + str(len(encoded_value)/8) + " bytes")
    print('Compression ratio: ' + str(compression_ratio))
    print('Run time: ' + str(round((end - start) * 1000, 5)) + ' ms')

    return encoded_value


if __name__ == "__main__":
    # run tests
    # test_suite = unittest.TestLoader().loadTestsFromModule(tests)
    # unittest.TextTestRunner(verbosity=2).run(test_suite)

    # run algorithm
    compressed_bytes = byte_compress(test_data.example_data)

