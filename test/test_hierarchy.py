from __future__ import absolute_import

import unittest

from uniRW.Hierarchy import Hierarchy
from uniRW.Value import Value


class TestHierarchy(unittest.TestCase):

    def setUp(self):
        self.name = Value('Name')
        self.subject = Value('Subject')
        self.grade = Value('Grade')
        self.rank = Value('Rank')

    def test_check(self):
        name = self.name
        subject = self.subject
        grade = self.grade
        rank = self.rank
        s_name = self.name.state_value()
        s_subject = self.subject.state_value()
        s_grade = self.grade.state_value()
        s_rank = self.rank.state_value()

        Hierarchy.check({name: [grade]})
        Hierarchy.check({name: [grade, subject]})
        Hierarchy.check({name: [grade, subject, rank]})
        Hierarchy.check({name: {subject: [grade, rank]}})
        Hierarchy.check({name: {subject: {grade: [rank]}}})
        Hierarchy.check({s_name: [s_grade]})
        Hierarchy.check({s_name: [s_grade, s_subject]})
        Hierarchy.check({s_name: [s_grade, s_subject, s_rank]})
        Hierarchy.check({s_name: {s_subject: [s_grade, s_rank]}})
        Hierarchy.check({s_name: {s_subject: {s_grade: [s_rank]}}})

        with self.assertRaises(Exception):
            Hierarchy.check(name)
        with self.assertRaises(Exception):
            Hierarchy.check({name: grade})
        with self.assertRaises(Exception):
            Hierarchy.check({name: {subject: [grade], rank: [grade]}})
        with self.assertRaises(Exception):
            Hierarchy.check([{name: grade}])
        with self.assertRaises(Exception):
            Hierarchy.check(s_name)
        with self.assertRaises(Exception):
            Hierarchy.check({s_name: s_grade})
        with self.assertRaises(Exception):
            Hierarchy.check({s_name: {s_subject: [s_grade], s_rank: [s_grade]}})
        with self.assertRaises(Exception):
            Hierarchy.check([{s_name: s_grade}])

    def test_apply_post_map(self):
        name = self.name
        subject = self.subject
        grade = self.grade
        rank = self.rank

        grade.post_map_f = lambda _, x: x - 1.0
        rank.post_map_f = lambda _, x: x + 1

        hierarchy1 = {name: [grade]}
        hierarchy2 = {name: {subject: [rank, grade]}}

        value_dict1 = {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 3.0}}
        value_dict2 = {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}},
                       'Bob': {'CS': {'Rank': 2, 'Grade': 3.0}}}

        Hierarchy.apply_post_map(hierarchy1, {}, value_dict1)
        Hierarchy.apply_post_map(hierarchy2, {}, value_dict2)

        self.assertEqual(value_dict1, {'Alice': {'Grade': 3.0}, 'Bob': {'Grade': 2.0}})
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Rank': 2, 'Grade': 3.0}},
                                       'Bob': {'CS': {'Rank': 3, 'Grade': 2.0}}})

    def test_merge(self):
        name = self.name
        subject = self.subject
        grade = self.grade
        rank = self.rank.state_value()

        grade.reduce_f = max
        rank.reduce_f = min
        grade.post_map_f = lambda _, x: x - 1.0
        rank.post_map_f = lambda _, x: x + 1
        grade.post_reduce_f = min
        rank.post_reduce_f = max

        hierarchy1 = {name: [grade]}
        hierarchy2 = {name: {subject: [rank, grade]}}

        value_dict11 = {'Alice': {'Grade': 4.0}}
        value_dict12 = {'Alice': {'Grade': 3.0}}
        value_dict13 = {'Bob': {'Grade': 3.5}}
        value_dict20 = {'Alice': {'Math': {'Rank': 2, 'Grade': 3.0}}}
        value_dict21 = {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}}
        value_dict22 = {'Alice': {'CS': {'Rank': 2, 'Grade': 3.9}}}
        value_dict23 = {'Bob': {'Math': {'Rank': 2, 'Grade': 3.0}}}

        self.assertEqual(Hierarchy.merge(hierarchy1, value_dict11, value_dict12),
                         {'Alice': {'Grade': 4.0}})
        self.assertEqual(Hierarchy.merge(hierarchy1, value_dict11, value_dict12, True),
                         {'Alice': {'Grade': 2.0}})
        self.assertEqual(Hierarchy.merge(hierarchy1, value_dict11, value_dict13),
                         {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 3.5}})
        self.assertEqual(Hierarchy.merge(hierarchy1, value_dict11, value_dict13, True),
                         {'Alice': {'Grade': 3.0}, 'Bob': {'Grade': 2.5}})

        self.assertEqual(Hierarchy.merge(hierarchy2, value_dict20, value_dict21),
                         {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}})
        self.assertEqual(Hierarchy.merge(hierarchy2, value_dict20, value_dict21, True),
                         {'Alice': {'Math': {'Rank': 3, 'Grade': 2.0}}})
        self.assertEqual(Hierarchy.merge(hierarchy2, value_dict21, value_dict22),
                         {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0},
                                    'CS': {'Rank': 2, 'Grade': 3.9}}})
        self.assertEqual(Hierarchy.merge(hierarchy2, value_dict21, value_dict22, True),
                         {'Alice': {'Math': {'Rank': 2, 'Grade': 3.0},
                                    'CS': {'Rank': 3, 'Grade': 2.9}}})
        self.assertEqual(Hierarchy.merge(hierarchy2, value_dict21, value_dict23),
                         {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}},
                          'Bob': {'Math': {'Rank': 2, 'Grade': 3.0}}})
        self.assertEqual(Hierarchy.merge(hierarchy2, value_dict21, value_dict23, True),
                         {'Alice': {'Math': {'Rank': 2, 'Grade': 3.0}},
                          'Bob': {'Math': {'Rank': 3, 'Grade': 2.0}}})

    def test_traverse(self):
        name = self.name
        subject = self.subject
        grade = self.grade
        rank = self.rank.state_value()

        grade.map_f = lambda _, x: float(x)
        grade.reduce_f = max
        rank.map_f = lambda _, x: int(x)
        rank.reduce_f = min

        hierarchy1 = {name: [grade]}
        hierarchy2 = {name: {subject: [rank, grade]}}

        line11 = {'Name': 'Alice', 'Subject': 'Math',  'Grade': '3.0'}
        line12 = {'Name': 'Alice', 'Subject': 'Math',  'Grade': '4.0'}
        line13 = {'Name': 'Alice', 'Subject': 'CS', 'Grade': '3.5'}
        line21 = {'Name': 'Bob', 'Subject': 'CS',  'Grade': '3.5'}
        line22 = {'Name': 'Bob', 'Subject': 'CS', 'Grade': '3.0'}
        line23 = {'Name': 'Bob', 'Subject': 'Math', 'Grade': '4.0'}

        value_dict1 = {}
        Hierarchy.traverse(hierarchy1, line11, {'Rank': '3'}, value_dict1)
        self.assertEqual(value_dict1, {'Alice': {'Grade': 3.0}})
        Hierarchy.traverse(hierarchy1, line12, {'Rank': '1'}, value_dict1)
        self.assertEqual(value_dict1, {'Alice': {'Grade': 4.0}})
        Hierarchy.traverse(hierarchy1, line13, {'Rank': '2'}, value_dict1)
        self.assertEqual(value_dict1, {'Alice': {'Grade': 4.0}})
        Hierarchy.traverse(hierarchy1, line21, {'Rank': '2'}, value_dict1)
        self.assertEqual(value_dict1, {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 3.5}})
        Hierarchy.traverse(hierarchy1, line22, {'Rank': '3'}, value_dict1)
        self.assertEqual(value_dict1, {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 3.5}})
        Hierarchy.traverse(hierarchy1, line23, {'Rank': '1'}, value_dict1)
        self.assertEqual(value_dict1, {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 4.0}})

        value_dict2 = {}
        Hierarchy.traverse(hierarchy2, line11, {'Rank': '3'}, value_dict2)
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Grade': 3.0, 'Rank': 3}}})
        Hierarchy.traverse(hierarchy2, line12, {'Rank': '1'}, value_dict2)
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Grade': 4.0, 'Rank': 1}}})
        Hierarchy.traverse(hierarchy2, line13, {'Rank': '2'}, value_dict2)
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Grade': 4.0, 'Rank': 1},
                                                 'CS': {'Grade': 3.5, 'Rank': 2}}})
        Hierarchy.traverse(hierarchy2, line21, {'Rank': '2'}, value_dict2)
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Grade': 4.0, 'Rank': 1},
                                                 'CS': {'Grade': 3.5, 'Rank': 2}},
                                       'Bob': {'CS': {'Grade': 3.5, 'Rank': 2}}})
        Hierarchy.traverse(hierarchy2, line22, {'Rank': '3'}, value_dict2)
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Grade': 4.0, 'Rank': 1},
                                                 'CS': {'Grade': 3.5, 'Rank': 2}},
                                       'Bob': {'CS': {'Grade': 3.5, 'Rank': 2}}})
        Hierarchy.traverse(hierarchy2, line23, {'Rank': '1'}, value_dict2)
        self.assertEqual(value_dict2, {'Alice': {'Math': {'Grade': 4.0, 'Rank': 1},
                                                 'CS': {'Grade': 3.5, 'Rank': 2}},
                                       'Bob': {'CS': {'Grade': 3.5, 'Rank': 2},
                                               'Math': {'Grade': 4.0, 'Rank': 1}}})


    def test_flatten(self):
        name = self.name
        subject = self.subject
        grade = self.grade
        rank = self.rank.state_value()

        hierarchy1 = {name: [grade]}
        hierarchy2 = {name: {subject: [rank, grade]}}

        value_dict11 = {'Alice': {'Grade': 4.0}}
        value_dict12 = {'Alice': {'Grade': 4.0}, 'Bob': {'Grade': 3.0}}
        value_dict21 = {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}, 'CS': {'Rank': 2, 'Grade': 3.9}}}
        value_dict22 = {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}, 'CS': {'Rank': 2, 'Grade': 3.8}},
                        'Bob': {'Math': {'Rank': 2, 'Grade': 3.0}, 'CS': {'Rank': 1, 'Grade': 3.9}}}

        key = lambda v: v['Grade']

        value_lines = []
        Hierarchy.flatten(hierarchy1, value_dict11, value_lines)
        self.assertEqual(value_lines, [{'Name': 'Alice', 'Grade': 4.0}])

        value_lines = []
        Hierarchy.flatten(hierarchy1, value_dict12, value_lines)
        self.assertEqual(sorted(value_lines, key=key),
                         sorted([{'Name': 'Alice', 'Grade': 4.0}, {'Name': 'Bob', 'Grade': 3.0}], key=key))

        value_lines = []
        Hierarchy.flatten(hierarchy2, value_dict21, value_lines)
        self.assertEqual(sorted(value_lines, key=key),
                         sorted([{'Name': 'Alice', 'Subject': 'Math', 'Rank': 1, 'Grade': 4.0},
                                 {'Name': 'Alice', 'Subject': 'CS', 'Rank': 2, 'Grade': 3.9}], key=key))

        value_lines = []
        Hierarchy.flatten(hierarchy2, value_dict22, value_lines)
        self.assertEqual(sorted(value_lines, key=key),
                         sorted([{'Name': 'Alice', 'Subject': 'Math', 'Rank': 1, 'Grade': 4.0},
                                 {'Name': 'Alice', 'Subject': 'CS', 'Rank': 2, 'Grade': 3.8},
                                 {'Name': 'Bob', 'Subject': 'Math', 'Rank': 2, 'Grade': 3.0},
                                 {'Name': 'Bob', 'Subject': 'CS', 'Rank': 1, 'Grade': 3.9}], key=key))

if __name__ == '__main__':
    unittest.main()
