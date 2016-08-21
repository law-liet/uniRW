from __future__ import absolute_import

import unittest

from uniRW.State import State


class TestState(unittest.TestCase):

    def test_get(self):
        for i in range(100):
            state = State({'count': i, 'count+1': i + 1, 'count*2': i * 2})
            self.assertEqual(state['count'], i)
            self.assertEqual(state['count+1'], i + 1)
            self.assertEqual(state['count*2'], i * 2)
            with self.assertRaises(KeyError):
                print(state['count' + str(i)])

    def test_set(self):
        state = State({'count': 0, 'count+1': 0, 'count*2': 0})
        with self.assertRaises(KeyError):
            state['count'] = 1
        state.release()
        for i in range(100):
            state['count'] = i
            state['count+1'] = i + 1
            state['count*2'] = i * 2
            self.assertEqual(state['count'], i)
            self.assertEqual(state['count+1'], i + 1)
            self.assertEqual(state['count*2'], i * 2)
        state.lock()
        with self.assertRaises(KeyError):
            state['count'] = 0

    def test_update(self):
        state = State({'count1': 0, 'count2': 0, 'count3': 0})
        count1 = 0
        count2 = 0

        def update1(state, _):
            state['count1'] += 1

        def update2(state, _):
            state['count2'] += 2

        def update3(state, val):
            state['count3'] = val

        state.update_func = update1
        with self.assertRaises(KeyError):
            state.update(0)

        state.release()
        for i in range(100):
            count1 += 1
            state.update(0)
            self.assertEqual(state['count1'], count1)
        state.lock()

        state.update_func = update2
        with self.assertRaises(KeyError):
            state.update(0)

        state.release()
        for i in range(100):
            count2 += 2
            state.update(0)
            self.assertEqual(state['count2'], count2)
        state.lock()

        state.update_func = update3
        with self.assertRaises(KeyError):
            state.update(0)

        state.release()
        for i in range(100):
            state.update(0)
            self.assertEqual(state['count3'], 0)
        state.lock()


if __name__ == '__main__':
    unittest.main()
