import unittest
from algorithms.sorting import Bub_sort, Quick_sort, Merge_sort

class TestSortingAlgorithms(unittest.TestCase):
    
    def test_bubble_sort_ascending(self):
        sorter = Bub_sort()
        data = [5, 1, 3, 7, 2]
        sorted_data = sorter.sort(True, data)
        self.assertEqual(sorted_data, [1, 2, 3, 5, 7])

    def test_bubble_sort_descending(self):
        sorter = Bub_sort()
        data = [5, 1, 3, 7, 2]
        sorted_data = sorter.sort(False, data)
        self.assertEqual(sorted_data, [7, 5, 3, 2, 1])

    def test_quick_sort_ascending(self):
        sorter = Quick_sort()
        data = [5, 1, 3, 7, 2]
        sorted_data = sorter.sort(True, data, 0, len(data)-1)
        self.assertEqual(sorted_data, [1, 2, 3, 5, 7])

    def test_quick_sort_descending(self):
        sorter = Quick_sort()
        data = [5, 1, 3, 7, 2]
        sorted_data = sorter.sort(False, data, 0, len(data)-1)
        self.assertEqual(sorted_data, [7, 5, 3, 2, 1])

    def test_merge_sort_ascending(self):
        sorter = Merge_sort()
        data = [5, 1, 3, 7, 2]
        sorted_data = sorter.sort(True, data, 0, len(data)-1)
        self.assertEqual(sorted_data, [1, 2, 3, 5, 7])

    def test_merge_sort_descending(self):
        sorter = Merge_sort()
        data = [5, 1, 3, 7, 2]
        sorted_data = sorter.sort(False, data, 0, len(data)-1)
        self.assertEqual(sorted_data, [7, 5, 3, 2, 1])

if __name__ == '__main__':
    unittest.main()
