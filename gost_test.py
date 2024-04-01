import unittest

from gost import *

key = 65652878985187006891393172765452250063435691895418812924645842034576172192371


class TestGOST(unittest.TestCase):

    def test_encrypt_feistel_function(self):
        cypher = 0xC0B7A8D05F3A829C
        print("cypher_perm", format(cypher, "#018x"))
        keys = gost_key_generator(key)
        expected = [6861940590458943933, 7215815249716206166, 1454199056723880982, 6970494799317957702,
                    13118418667765815482, 2524505886888099779, 10185171773433876557, 13536853240770503342,
                    1781352523866417378, 13028254986213478395, 2339426473590336638, 11565011290379240172,
                    11128327524025929438, 3874378665558303534, 8499527446016725278, 180866496441087797,
                    14421642240273102797, 6430920147742173377, 5265597199025497075, 1311924026534134540,
                    9646150805471086302, 15128654230275860195, 958605790518872617, 3999911330724706024,
                    12747428750834956092, 18239146642442836762, 8435342272049771785, 11843610541953611476,
                    12337460358830403680, 7389475017605844261, 11314464094520767240, 7859688746324751112]

        for i, key_round in enumerate(keys[:-1]):
            cypher = feistel(cypher, key_round)
            assert cypher == expected[i]
        last_round = feistel(cypher, keys[-1], False)
        assert last_round == expected[-1]

    def test_des_ecb_encrypt(self):
        plain_text = 0xe18624e8f674b145
        keys = gost_key_generator(key)
        cypher = encrypt([plain_text], keys)
        assert cypher[0] == 5391480007939838273

    def test_decrypt_feistel_function(self):
        cypher = 0xD9562F48B97EF543
        print("cypher_perm", format(cypher, "#018x"))
        keys = gost_key_generator(key)
        expected = [13366390414517889833, 9981783450075015033, 9122084445913225966, 127819251667249633,
                    11751344850059919218, 4391009031018438760, 18114287389621863063, 4737719290526876155,
                    15951400217261578541, 14120782838119799603, 1769944563357045908, 16935738657355488360,
                    6378887525711337119, 7508018034801779312, 11211186190819109119, 17188455267106303627,
                    4724327184764924544, 4801526047724082967, 3918438542004911601, 15737545160891071438,
                    6310805106474069907, 16869269879350467736, 18077902558108193336, 9523444394271467215,
                    2214758158431231171, 10426146238070009365, 8102026400852609789, 14963221845284508011,
                    6884967453371362488, 12993848889941421838, 10813124075368939411, 9364019414121774995]

        for i, key_round in enumerate(keys[:-1]):
            cypher = feistel(cypher, key_round)
            assert cypher == expected[i]
        last_round = feistel(cypher, keys[-1], False)
        assert last_round == expected[-1]

    def test_des_ecb_decrypt(self):
        cypher = 5391480007939838273
        keys = gost_key_generator(key)
        plain_text = decrypt([cypher], keys)
        assert plain_text[0] == 0xe18624e8f674b145

    def test_des_ecb_encrypt_decrypt(self):
        plain_text = 0x123456ABCD132536
        keys = gost_key_generator(key)
        cypher = encrypt([plain_text], keys)
        plain_text2 = decrypt(cypher, keys)
        assert plain_text2[0] == plain_text

    def test_des_cbc_encrypt_decrypt(self):
        plain_text = 0x123456ABCD132536
        keys = gost_key_generator(key)
        cypher = encrypt([plain_text], keys, "CBC")
        plain_text2 = decrypt(cypher, keys, "CBC")
        assert plain_text2[0] == plain_text

    def test_des_ctr_encrypt_decrypt(self):
        plain_text = 0x123456ABCD132536
        keys = gost_key_generator(key)
        cypher = encrypt([plain_text], keys, "CTR")
        plain_text2 = decrypt(cypher, keys, "CTR")
        assert plain_text2[0] == plain_text
