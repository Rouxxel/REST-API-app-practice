from collections import deque

class Bin_search:
    def search(self, data: list[int], target: int) -> bool:
        left = 0
        right = len(data) - 1
        
        while left <= right:  # Fixed: it should be <= not <
            mid = left + (right - left) // 2

            if data[mid] == target:
                return True
            elif data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return False

class DFS:
    def __init__(self):
        self.visited = []

    def search(self, graph: dict, start: int) -> list[int]:
        if start not in self.visited:
            self.visited.append(start)
            for neighbor in graph.get(start, []):
                self.search(graph, neighbor)
        return self.visited

class BFS:
    def search(self, graph: dict, start: int) -> list[int]:
        visited = []
        queue = deque([start])
        seen = set([start])

        while queue:
            node = queue.popleft()
            visited.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        return visited
