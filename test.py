import unittest
import prove
class TEST_PROVE(unittest.TestCase):
    def test_match(self):
        r = "เราเดินทางไปทุกที่"
        h = "เราเดินทางไปทุกที่"
        threshold =5
        chunkSize = 13     
        result = prove.measureByWER(r, h,threshold,chunkSize)
        assum = ([('เราเดินทางไปท', 'เราเดินทางไปท'), ('ุกที่', 'ุกที่')], 18, 18)
        self.assertEqual(result,assum)

    def test_delet(self):
        r = "123456789123456789"
        h = "12345678923456789"
        threshold =5
        chunkSize = 12     
        result = prove.measureByWER(r, h,threshold,chunkSize)
        assum = ([('123456789', '123456789'), ('123456789', '23456789')], 18, 17)
        self.assertEqual(result,assum)

    def test_insert(self):
        r = "123456789123456789"
        h = "123456789135135123456789"
        threshold =5
        chunkSize = 20     
        result = prove.measureByWER(r, h,threshold,chunkSize)
        assum = ([('1234567891', '1234567891'), ('23456789', '35135123456789')], 18, 24)
        self.assertEqual(result,assum)

    def test_sub(self):
        r = "123456789123456789"
        h = "123456789341256789"
        threshold =5
        chunkSize = 12     
        result = prove.measureByWER(r, h,threshold,chunkSize)
        assum = ([('123456789', '123456789'), ('123456789', '341256789')], 18, 18)
        self.assertEqual(result,assum)
    

if __name__ == '__main__':
    unittest.main()