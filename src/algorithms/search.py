from collections import deque

class Bin_search:
    def search(self, data: list[int], target: int) -> bool:
        """
        Perform binary search on a sorted array to find a target value.
        
        Args:
            data: Sorted list of numbers to search in
            target: Value to search for
            
        Returns:
            True if target is found, False otherwise
            
        Note:
            The input data must be sorted in ascending order for binary search to work correctly.
        """
        if not data:  # Handle empty array
            return False
            
        left = 0
        right = len(data) - 1
        
        while left <= right:
            mid = left + (right - left) // 2

            if data[mid] == target:
                return True
            elif data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return False

class DFS:
    def search(self, graph: dict, start: int) -> list[int]:
        """
        Perform Depth-First Search on a graph starting from the given node.
        
        Args:
            graph: Dictionary where keys are nodes and values are lists of neighbors
            start: Starting node for the search
            
        Returns:
            List of visited nodes in DFS order
        """
        if start not in graph:
            return [start]  # Return just the start node if it's not in the graph
            
        visited = []
        self._dfs_helper(graph, start, visited)
        return visited
    
    def _dfs_helper(self, graph: dict, node: int, visited: list):
        """Helper method for recursive DFS traversal"""
        if node not in visited:
            visited.append(node)
            # Get neighbors, defaulting to empty list if node not in graph
            neighbors = graph.get(node, [])
            for neighbor in neighbors:
                self._dfs_helper(graph, neighbor, visited)

class BFS:
    def search(self, graph: dict, start: int) -> list[int]:
        """
        Perform Breadth-First Search on a graph starting from the given node.
        
        Args:
            graph: Dictionary where keys are nodes and values are lists of neighbors
            start: Starting node for the search
            
        Returns:
            List of visited nodes in BFS order
        """
        if start not in graph:
            return [start]  # Return just the start node if it's not in the graph
            
        visited = []
        queue = deque([start])
        seen = set([start])

        while queue:
            node = queue.popleft()
            visited.append(node)
            # Get neighbors, defaulting to empty list if node not in graph
            neighbors = graph.get(node, [])
            for neighbor in neighbors:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        return visited
