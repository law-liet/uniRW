from __future__ import absolute_import
import unittest

import os
from shutil import rmtree

from uniRW.File import OutputLine
from uniRW.File import OutputFile
from uniRW.Value import Value
from uniRW import HWriter


class TestWriter(unittest.TestCase):

    def setUp(self):
        output = os.path.join(os.path.dirname(__file__), 'output')
        os.mkdir(output)

    def tearDown(self):
        output = os.path.join(os.path.dirname(__file__), 'output')
        rmtree(output)

    def test_write(self):
        name = Value('Name')
        course = Value('Course')
        rank = Value('Rank')
        grade1 = Value("Grade")
        grade2 = Value("Grade", to_string=lambda x: str(max(x)))
        grade3 = Value("Grade", to_string=lambda x: str(x[0]) + ',' + str(x[1]))

        hierarchy1 = {name: {course: [rank, grade1]}}
        hierarchy2 = {name: {course: [rank, grade2]}}
        hierarchy3 = {name: {course: [grade3]}}

        output_file1 = os.path.join(os.path.dirname(__file__), 'output/output1.csv')
        output_file2 = os.path.join(os.path.dirname(__file__), 'output/output2.csv')
        output_file3 = os.path.join(os.path.dirname(__file__), 'output/output3.csv')

        value_line1 = [name, course, rank, grade1]
        value_line2 = [name, course, rank, grade2]
        value_line3 = [name, course, grade3]

        output1 = OutputFile(output_file1, OutputLine(','), epilogue=['# Test output', '# uniRW HWriter'])
        output2 = OutputFile(output_file2, OutputLine(','), foreword=['# Test output', '# uniRW HWriter'])
        output3 = OutputFile(
            output_file3,
            OutputLine(','),
            header=['Name', 'Course', 'Rank', 'Grade']
        )

        value_dict1 = {'Alice': {'Math': {'Rank': 1, 'Grade': 100.0}, 'CS': {'Rank': 2, 'Grade': 95.0}},
                       'Bobby': {'Math': {'Rank': 2, 'Grade': 90.0}, 'CS': {'Rank': 1, 'Grade': 98.0}}}
        value_dict2 = {'Alice': {'Math': {'Rank': 1, 'Grade': [100.0, 90.0, 95.0]},
                                 'CS': {'Rank': 2, 'Grade': [80.0, 90.0, 75.0]}},
                       'Bobby': {'Math': {'Rank': 2, 'Grade': [60.0, 70.0, 80.0]},
                                 'CS': {'Rank': 1, 'Grade': [90.0, 95.0]}}}
        value_dict3 = {'Alice': {'Math': {'Grade': (1, 100.0)}, 'CS': {'Grade': (2, 95.0)}},
                       'Bobby': {'Math': {'Grade': (2, 90.0)}, 'CS': {'Grade': (1, 95.0)}}}

        HWriter(hierarchy1, value_line1).write(output1, value_dict1, sort_by='Grade')
        HWriter(hierarchy2, value_line2).write(output2, value_dict2, sort_by='Grade')
        HWriter(hierarchy3, value_line3).write(output3, value_dict3, sort_by='Grade')

        ref_file1 = os.path.join(os.path.dirname(__file__), 'data/output1.csv')
        ref_file2 = os.path.join(os.path.dirname(__file__), 'data/output2.csv')
        ref_file3 = os.path.join(os.path.dirname(__file__), 'data/output3.csv')

        ref1 = open(ref_file1, 'r')
        ref2 = open(ref_file2, 'r')
        ref3 = open(ref_file3, 'r')

        out1 = open(output_file1, 'r')
        out2 = open(output_file2, 'r')
        out3 = open(output_file3, 'r')

        self.assertEqual(ref1.read(), out1.read())
        self.assertEqual(ref2.read(), out2.read())
        self.assertEqual(ref3.read(), out3.read())

        ref1.close()
        ref2.close()
        ref3.close()
        out1.close()
        out2.close()
        out3.close()


if __name__ == '__main__':
    unittest.main()
