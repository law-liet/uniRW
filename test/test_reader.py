from __future__ import absolute_import

import os
import unittest
from operator import add

from uniRW.File import DataFile
from uniRW.HReader import HReader
from uniRW.Line import Line
from uniRW.State import State
from uniRW.Value import Value, StateValue
from uniRW.util import pureR, pureL


class TestReader(unittest.TestCase):

    def setUp(self):

        def average(num_list):
            return round(sum(num_list) / len(num_list), 2)

        name = Value('Name')
        course = Value('Course')
        number = StateValue('Number')
        grade1 = Value("Grade", map_f=pureR(float), reduce_f=max, post_reduce_f=max)
        grade2 = Value(
            name='Grade',
            map_f=pureR(lambda x: [float(x)]),
            reduce_f=add,
            post_map_f=pureR(average),
            post_reduce_f=max,
        )

        example1 = os.path.join(os.path.dirname(__file__), 'data/example1.csv')
        example2A = os.path.join(os.path.dirname(__file__), 'data/example2A.csv')
        example2B = os.path.join(os.path.dirname(__file__), 'data/example2B.csv')

        self.example1 = DataFile(example1, Line(','), header_lineno=1)
        self.example2A = DataFile(example2A, Line(','), header_lineno=0)
        self.example2B = DataFile(example2B, Line(','), header_lineno=0)

        self.hierarchy11 = {name: [grade1]}
        self.hierarchy12 = {name: [grade2]}
        self.hierarchy13 = {name: [grade1, number]}
        self.hierarchy21 = {name: {course: [grade1]}}
        self.hierarchy22 = {name: {course: [grade2]}}

    def test_read_lines(self):
        value_dict11 = {'Alice': {'Grade': 4.0}}
        value_dict12 = {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 3.0}}
        value_dict21 = {'Alice': {'Math': {'Grade': 4.0}, 'CS': {'Grade': 3.9}}}
        value_dict22 = {'Alice': {'Math': {'Grade': 4.0}, 'CS': {'Grade': 3.8}},
                        'Bob': {'Math': {'Grade': 3.0}, 'CS': {'Grade': 3.9}}}
        value_lines11 = [{'Name': 'Alice', 'Grade': 4.0}]
        value_lines12 = [{'Name': 'Alice', 'Grade': 4.0}, {'Name': 'Bob', 'Grade': 3.0}]
        value_lines21 = [{'Name': 'Alice', 'Course': 'Math', 'Rank': 1, 'Grade': 4.0},
                         {'Name': 'Alice', 'Course': 'CS', 'Rank': 2, 'Grade': 3.9}]
        value_lines22 = [{'Name': 'Alice', 'Course': 'Math', 'Rank': 1, 'Grade': 4.0},
                         {'Name': 'Alice', 'Course': 'CS', 'Rank': 2, 'Grade': 3.8},
                         {'Name': 'Bob', 'Course': 'Math', 'Rank': 2, 'Grade': 3.0},
                         {'Name': 'Bob', 'Course': 'CS', 'Rank': 1, 'Grade': 3.9}]

        grade_dict11, _ = HReader(self.hierarchy11).read_lines(value_lines11)
        grade_dict12, _ = HReader(self.hierarchy11).read_lines(value_lines12)
        grade_dict21, _ = HReader(self.hierarchy21).read_lines(value_lines21)
        grade_dict22, _ = HReader(self.hierarchy21).read_lines(value_lines22)

        self.assertEqual(grade_dict11, value_dict11)
        self.assertEqual(grade_dict12, value_dict12)
        self.assertEqual(grade_dict21, value_dict21)
        self.assertEqual(grade_dict22, value_dict22)

    def test_read(self):
        def skip_first_line(line):
            return not line[0][0] == '#'

        def update(state):
            state['Number'] += 1

        state = State({'Number': 0}, pureL(update))

        grade_dict11, _ = HReader(self.hierarchy11, filter_f=pureR(skip_first_line)).read(self.example1)
        grade_dict12, _ = HReader(self.hierarchy12, filter_f=pureR(skip_first_line)).read(self.example1)
        grade_dict13, final_state = HReader(self.hierarchy13, state, pureR(skip_first_line)).read(self.example1)

        grade_dict21A, _ = HReader(self.hierarchy21).read(self.example2A)
        grade_dict21B, _ = HReader(self.hierarchy21).read(self.example2B)
        grade_dict21C, _ = HReader(self.hierarchy21, state).read(self.example2A, carry_state=True)
        grade_dict22A, _ = HReader(self.hierarchy22).read(self.example2A)
        grade_dict22B, _ = HReader(self.hierarchy22).read(self.example2B)
        grade_dict22AP, _ = HReader(self.hierarchy22).read(self.example2A, apply_post_map=True)
        grade_dict22BP, _ = HReader(self.hierarchy22).read(self.example2B, apply_post_map=True)

        self.assertEqual(grade_dict11, {'Alice': {'Grade': 3.5}, 'Bob': {'Grade': 4.0}})
        self.assertEqual(grade_dict12, {'Alice': {'Grade': [3.5, 3.4]}, 'Bob': {'Grade': [2.6, 4.0]}})
        self.assertEqual(grade_dict13, {'Alice': {'Grade': 3.5, 'Number': 5}, 'Bob': {'Grade': 4.0, 'Number': 4}})
        self.assertEqual(final_state['Number'], 5)

        self.assertEqual(grade_dict21A, {'Alice': {'Math': {'Grade': 100.0}}, 'Bobby': {'Math': {'Grade': 90.0}}})
        self.assertEqual(grade_dict21B, {'Alice': {'CS': {'Grade': 95.0}}, 'Bobby': {'CS': {'Grade': 100.0}}})
        self.assertEqual(state['Number'], 7)
        self.assertEqual(grade_dict22A, {'Alice': {'Math': {'Grade': [100.0, 90.0, 95.0]}},
                                         'Bobby': {'Math': {'Grade': [60.0, 90.0, 70.0, 80.0]}}})
        self.assertEqual(grade_dict22B, {'Alice': {'CS': {'Grade': [80.0, 90.0, 75.0, 95.0]}},
                                         'Bobby': {'CS': {'Grade': [100.0, 90.0, 95.0]}}})
        self.assertEqual(grade_dict22AP, {'Alice': {'Math': {'Grade': 95.0}},
                                          'Bobby': {'Math': {'Grade': 75.0}}})
        self.assertEqual(grade_dict22BP, {'Alice': {'CS': {'Grade': 85.0}},
                                          'Bobby': {'CS': {'Grade': 95.0}}})

    def test_read_all(self):
        grade_dict11 = HReader(self.hierarchy11).read_all([self.example2A, self.example2B])
        grade_dict12 = HReader(self.hierarchy12).read_all([self.example2A, self.example2B])
        grade_dict21 = HReader(self.hierarchy21).read_all([self.example2A, self.example2B])
        grade_dict22 = HReader(self.hierarchy22).read_all([self.example2A, self.example2B])

        self.assertEqual(grade_dict11, {'Alice': {'Grade': 100.0}, 'Bobby': {'Grade': 100.0}})
        self.assertEqual(grade_dict12, {'Alice': {'Grade': 95.0}, 'Bobby': {'Grade': 95.0}})
        self.assertEqual(grade_dict21, {'Alice': {'Math': {'Grade': 100.0}, 'CS': {'Grade': 95.0}},
                                        'Bobby': {'Math': {'Grade': 90.0}, 'CS': {'Grade': 100.0}}})
        self.assertEqual(grade_dict22, {'Alice': {'Math': {'Grade': 95.0}, 'CS': {'Grade': 85.0}},
                                        'Bobby': {'Math': {'Grade': 75.0}, 'CS': {'Grade': 95.0}}})


if __name__ == '__main__':
    unittest.main()
