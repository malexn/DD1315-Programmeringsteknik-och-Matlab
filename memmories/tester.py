import unittest
import os
from memory import Memory

class MemoryTest(unittest.TestCase):
    m = Memory(2,2)
    n = Memory(4,4)
    def test_memory(self):

        self.assertEqual(len(self.m.las_fil(2)), 4)
        self.assertEqual(len(self.n.las_fil(4)), 8)
        self.assertEqual(len(self.m.las_fil(6)), 12)
        self.assertEqual(len(self.n.las_fil(8)), 16)
        self.assertEqual(self.m.hamta_cell(1, 1), 0)
        self.assertEqual(self.n.hamta_cell(2, 2), 5)

        self.assertNotEqual(len(self.m.las_fil(2)), 2)
        self.assertNotEqual(len(self.n.las_fil(4)), 4)
        self.assertNotEqual(len(self.m.las_fil(6)), 6)
        self.assertNotEqual(len(self.n.las_fil(8)), 8)
        self.assertNotEqual(self.m.hamta_cell(1, 1), 1)
        self.assertNotEqual(self.n.hamta_cell(2, 2), 2)

        self.assertTrue(os.path.isfile('highscore.txt'))


if __name__ == "__main__":
    unittest.main()
