import unittest
from src.algorithms.search import Bin_search, DFS, BFS

class TestSearchAlgorithms(unittest.TestCase):

    def test_binary_search_found(self):
        searcher = Bin_search()
        data = [1, 3, 5, 7, 9]
        result = searcher.search(data, 5)
        self.assertTrue(result)

    def test_binary_search_not_found(self):
        searcher = Bin_search()
        data = [1, 3, 5, 7, 9]
        result = searcher.search(data, 4)
        self.assertFalse(result)

    def test_dfs(self):
        graph = {1: [2, 3], 2: [4], 3: [5], 4: [], 5: []}
        dfs = DFS()
        visited = dfs.search(graph, 1)
        self.assertEqual(visited, [1, 2, 4, 3, 5])

    def test_bfs(self):
        graph = {1: [2, 3], 2: [4], 3: [5], 4: [], 5: []}
        bfs = BFS()
        visited = bfs.search(graph, 1)
        self.assertEqual(visited, [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()
