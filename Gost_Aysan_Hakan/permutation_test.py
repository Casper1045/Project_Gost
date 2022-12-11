import unittest
from permutation import permutation, shift_left

INIT_PERM_TEST = [1, 5, 9, 8, 2, 3, 7, 4, 6]
FINAL_PERM_TEST = [1, 5, 6, 8, 2, 9, 7, 4, 3]


class TestPermutation(unittest.TestCase):

    def test_permutation_init_from_book(self):
        init = 0b100000001
        final = permutation(init, INIT_PERM_TEST, 9)
        expected = 0b101000000
        assert final == expected

    def test_permutation_final_from_book(self):
        expected = 0b100000001
        init = 0b101000000
        final = permutation(init, FINAL_PERM_TEST, 9)
        assert final == expected

    def test_permutation_identity(self):
        init = 0b1010
        pos = [1, 2, 3, 4]
        final = permutation(init, pos, 4)
        assert init == final

    def test_permutation_A(self):
        init = 0b1010
        expected = 0b0011
        pos = [2, 4, 3, 1]
        final = permutation(init, pos, 4)
        assert expected == final

    def test_permutation_inverse(self):
        init = 0b1010
        expected = 0b0101
        pos = [4, 3, 2, 1]
        final = permutation(init, pos, 4)
        assert expected == final

    def test_permutation_B(self):
        init = 0b1010
        expected = 0b1100
        pos = [3, 1, 4, 2]
        final = permutation(init, pos, 4)
        assert expected == final

    def test_shift_left_4bits(self):
        init = 0b1010
        final = shift_left(init, 4, 1)
        expected = 0b0101
        assert expected == final

        final = shift_left(final, 4, 1)
        expected = 0b1010
        assert expected == final

    def test_shift_left_7bits(self):
        init = 0b1010111
        final = shift_left(init, 7, 1)
        expected = 0b0101111
        assert expected == final

        final = shift_left(final, 7, 1)
        expected = 0b1011110
        assert expected == final

    def test_shift_left_7bits_3bits(self):
        init = 0b1010111
        final = shift_left(init, 7, 3)
        expected = 0b0111101
        assert expected == final

    def test_shift_left_32bits_12bits(self):
        init = 0x12345678
        final = shift_left(init, 32, 12)
        expected = 0x45678123
        assert expected == final
