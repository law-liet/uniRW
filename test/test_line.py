from __future__ import absolute_import

import unittest

from uniRW.Line import Line, OutputLine


class TestLine(unittest.TestCase):

    def setUp(self):
        self.comma_line = Line(',')
        self.space_line = Line('\s+')
        self.data_comma_line1 = 'A,B,C,D'
        self.data_comma_line2 = '1,2,3,4'
        self.data_space_line1 = 'A  B C   D'
        self.data_space_line2 = '1  2 3   4'

    def test_header(self):
        self.comma_line.store(self.data_comma_line1)
        self.comma_line.set_header()
        self.assertEqual(self.comma_line.name_col_dict, {'A': 0, 'B': 1, 'C': 2, 'D': 3})
        self.comma_line.clear()
        self.assertEqual(self.comma_line.name_col_dict, {})

        self.comma_line.store(self.data_comma_line2)
        self.comma_line.set_header()
        self.assertEqual(self.comma_line.name_col_dict, {'1': 0, '2': 1, '3': 2, '4': 3})
        self.comma_line.clear()
        self.assertEqual(self.comma_line.name_col_dict, {})

        self.space_line.store(self.data_space_line1)
        self.space_line.set_header()
        self.assertEqual(self.space_line.name_col_dict, {'A': 0, 'B': 1, 'C': 2, 'D': 3})
        self.space_line.clear()
        self.assertEqual(self.space_line.name_col_dict, {})

        self.space_line.store(self.data_space_line2)
        self.space_line.set_header()
        self.assertEqual(self.space_line.name_col_dict, {'1': 0, '2': 1, '3': 2, '4': 3})
        self.space_line.clear()
        self.assertEqual(self.space_line.name_col_dict, {})

    def test_get(self):
        self.comma_line.store(self.data_comma_line1)
        self.comma_line.set_header()
        self.comma_line.store(self.data_comma_line2)

        self.assertEqual(self.comma_line['A'], '1')
        self.assertEqual(self.comma_line['B'], '2')
        self.assertEqual(self.comma_line['C'], '3')
        self.assertEqual(self.comma_line['D'], '4')
        with self.assertRaises(KeyError):
            print(self.comma_line['E'])

        self.assertEqual(self.comma_line[0], '1')
        self.assertEqual(self.comma_line[1], '2')
        self.assertEqual(self.comma_line[2], '3')
        self.assertEqual(self.comma_line[3], '4')
        self.assertEqual(self.comma_line[-4], '1')
        self.assertEqual(self.comma_line[-3], '2')
        self.assertEqual(self.comma_line[-2], '3')
        self.assertEqual(self.comma_line[-1], '4')
        with self.assertRaises(IndexError):
            print(self.comma_line[4])

        self.comma_line.clear()

        self.comma_line.store(self.data_comma_line2)
        self.comma_line.set_header()
        self.comma_line.store(self.data_comma_line1)

        self.assertEqual(self.comma_line['1'], 'A')
        self.assertEqual(self.comma_line['2'], 'B')
        self.assertEqual(self.comma_line['3'], 'C')
        self.assertEqual(self.comma_line['4'], 'D')
        with self.assertRaises(KeyError):
            print(self.comma_line['5'])

        self.assertEqual(self.comma_line[0], 'A')
        self.assertEqual(self.comma_line[1], 'B')
        self.assertEqual(self.comma_line[2], 'C')
        self.assertEqual(self.comma_line[3], 'D')
        self.assertEqual(self.comma_line[-4], 'A')
        self.assertEqual(self.comma_line[-3], 'B')
        self.assertEqual(self.comma_line[-2], 'C')
        self.assertEqual(self.comma_line[-1], 'D')
        with self.assertRaises(IndexError):
            print(self.comma_line[4])
        with self.assertRaises(IndexError):
            print(self.comma_line[-5])

        self.comma_line.clear()

        self.space_line.store(self.data_space_line1)
        self.space_line.set_header()
        self.space_line.store(self.data_space_line2)

        self.assertEqual(self.space_line['A'], '1')
        self.assertEqual(self.space_line['B'], '2')
        self.assertEqual(self.space_line['C'], '3')
        self.assertEqual(self.space_line['D'], '4')
        with self.assertRaises(KeyError):
            print(self.space_line['E'])

        self.assertEqual(self.space_line[0], '1')
        self.assertEqual(self.space_line[1], '2')
        self.assertEqual(self.space_line[2], '3')
        self.assertEqual(self.space_line[3], '4')
        self.assertEqual(self.space_line[-4], '1')
        self.assertEqual(self.space_line[-3], '2')
        self.assertEqual(self.space_line[-2], '3')
        self.assertEqual(self.space_line[-1], '4')
        with self.assertRaises(IndexError):
            print(self.space_line[4])
        with self.assertRaises(IndexError):
            print(self.space_line[-5])

        self.space_line.clear()

        self.space_line.store(self.data_space_line2)
        self.space_line.set_header()
        self.space_line.store(self.data_space_line1)

        self.assertEqual(self.space_line['1'], 'A')
        self.assertEqual(self.space_line['2'], 'B')
        self.assertEqual(self.space_line['3'], 'C')
        self.assertEqual(self.space_line['4'], 'D')
        with self.assertRaises(KeyError):
            print(self.space_line['5'])

        self.assertEqual(self.space_line[0], 'A')
        self.assertEqual(self.space_line[1], 'B')
        self.assertEqual(self.space_line[2], 'C')
        self.assertEqual(self.space_line[3], 'D')
        self.assertEqual(self.space_line[-4], 'A')
        self.assertEqual(self.space_line[-3], 'B')
        self.assertEqual(self.space_line[-2], 'C')
        self.assertEqual(self.space_line[-1], 'D')
        with self.assertRaises(IndexError):
            print(self.space_line[4])
        with self.assertRaises(IndexError):
            print(self.space_line[-5])

        self.space_line.clear()

    def test_output_line(self):
        comma_line = OutputLine(',', 'a,', ',d')
        space_line = OutputLine(' ', 'd ', ' a')

        self.assertEqual(comma_line.get_line(['b', 'c']), 'a,b,c,d')
        self.assertEqual(comma_line.get_line(['1', '2', '3']), 'a,1,2,3,d')
        self.assertEqual(space_line.get_line(['b', 'c']), 'd b c a')
        self.assertEqual(space_line.get_line(['1', '2', '3']), 'd 1 2 3 a')

if __name__ == '__main__':
    unittest.main()
