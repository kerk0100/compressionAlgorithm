from compression import *


class Test(unittest.TestCase):
    def test_valid_input(self):
        invalid_data_0 = "Not a data buffer of bytes."
        self.assertFalse(validate_input(invalid_data_0))

        invalid_data_1 = [0x03, 0x74, 0x04]
        self.assertFalse(validate_input(invalid_data_1))

        invalid_data_2 = None
        self.assertFalse(validate_input(invalid_data_2))

        invalid_data_3 = []
        self.assertFalse(validate_input(invalid_data_3))

        invalid_data_4 = bytes([])
        self.assertFalse(validate_input(invalid_data_4))

        invalid_data_5 = bytes([0x04])
        self.assertFalse(validate_input(invalid_data_5))

        valid_data_0 = bytes([0x03, 0x74, 0x04])
        self.assertTrue(validate_input(valid_data_0))

    def test_frequency(self):
        data_for_freq = bytes([0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64,
                               0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09])
        expected_freq = {0: 5, 3: 1, 100: 4, 4: 3, 69: 1, 9: 3, 116: 1, 53: 2, 86: 4}
        self.assertEqual(get_frequency_table(data_for_freq), expected_freq, "FAILED.")

        self.assertEqual(get_frequency_table(bytes([0x1, 0x2, 0x2])), {1: 1, 2: 2}, "FAILED.")

    def test_create_tree(self):
        frequencies_0 = {0: 5, 3: 1, 100: 4, 4: 3, 69: 1, 9: 3, 116: 1, 53: 2, 86: 4}
        self.assertEqual(create_tree(frequencies_0).freq, 24, "FAILED.")
        self.assertEqual(create_tree(frequencies_0).left.freq, 10, "FAILED.")
        self.assertEqual(create_tree(frequencies_0).right.freq, 14, "FAILED.")
        self.assertEqual(create_tree(frequencies_0).value, None, "FAILED.")

        frequencies_1 = {0: 5, 2: 3, 3: 1}
        self.assertEqual(create_tree(frequencies_1).freq, 9, "FAILED.")
        self.assertEqual(create_tree(frequencies_1).left.freq, 4, "FAILED.")
        self.assertEqual(create_tree(frequencies_1).right.freq, 5, "FAILED.")
        self.assertEqual(create_tree(frequencies_1).value, None, "FAILED.")

    def test_get_code(self):
        frequencies_0 = {0: 5, 3: 1, 100: 4, 4: 3, 69: 1, 9: 3, 116: 1, 53: 2, 86: 4}
        node_0 = create_tree(frequencies_0)
        expected_codes_0 = {0: '00', 3: '0100', 69: '0101', 4: '011', 9: '100', 116: '1010',
                            53: '1011', 100: '110', 86: '111'}
        output_0 = get_code(node_0)
        self.assertEqual(output_0, expected_codes_0, "FAILED.")

    def test_encode(self):
        data_to_encode = bytes([0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64,
                                0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09])
        codes_for_encoding = {0: '00', 3: '0100', 69: '0101', 4: '011', 9: '100', 116: '1010',
                              53: '1011', 100: '110', 86: '111'}
        expected_code = '010010100110110111011101111011011011000000000001110101111111111100100100'
        self.assertEqual(encode(data_to_encode, codes_for_encoding), expected_code, "FAILED.")

    def test_decode(self):
        data_to_decode = '010010100110110111011101111011011011000000000001110101111111111100100100'
        codes_for_decoding = {0: '00', 3: '0100', 69: '0101', 4: '011', 9: '100', 116: '1010',
                              53: '1011', 100: '110', 86: '111'}
        expected_data = bytes([0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64,
                               0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09])
        self.assertEqual(decode(data_to_decode, codes_for_decoding), expected_data, 'FAILED.')


