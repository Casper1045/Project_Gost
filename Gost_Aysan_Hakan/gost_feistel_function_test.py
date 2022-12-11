import unittest

from gost_feistel_function import *


class TestSBOX(unittest.TestCase):

    def test_s_box_1(self):
        expected = 12
        value = S_BOX_BANK[1][0b11]
        assert expected == value

    def test_s_box_8(self):
        expected = 1
        value = S_BOX_BANK[7][0b0]
        assert expected == value

    def test_s_box_enum_RFC(self):
        data_ind = 0
        for i in range(len(S_BOX_RFC[0])):
            data_in = data_ind
            for x in range(7):
                data_in <<= 4
                data_in |= data_ind
            data_out = apply_sbox(data_in, S_BOX_RFC)
            expected = 0
            for x in range(len(S_BOX_RFC)):
                expected |= S_BOX_RFC[x][data_ind]
                expected <<= 4
            expected >>= 4
            assert expected == data_out
            data_ind = (data_ind + 1) % 16

    def test_s_box_enum_BANK(self):
        data_ind = 0
        for i in range(len(S_BOX_BANK[0])):
            data_in = data_ind
            for x in range(7):
                data_in <<= 4
                data_in |= data_ind
            data_out = apply_sbox(data_in, S_BOX_BANK)
            expected = 0
            for x in range(len(S_BOX_BANK)):
                expected |= S_BOX_BANK[x][data_ind]
                expected <<= 4
            expected >>= 4
            assert expected == data_out
            data_ind = (data_ind + 1) % 16
