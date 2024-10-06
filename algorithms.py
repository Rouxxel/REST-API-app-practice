from collections import deque

class Bub_sort:
    def sort(self, ascending:bool, data: list[int]) -> list[int]:
        arr_len=len(data)
        
        if ascending:
            for i in range(0,arr_len):
                stop_early=True
                for j in range(0,arr_len-1-i):
                    if data[j] > data[j+1]:
                        data[j],data[j+1] = data[j+1],data[j]
                        #middle=data[j]
                        #data[j]=data[j+1]
                        #data[j+1]=middle
                        stop_early=False
                if stop_early:
                    break
        else:
            for i in range(0,arr_len):
                stop_early=True
                for j in range(0,arr_len-1-i):
                    if data[j] < data[j+1]:
                        data[j],data[j+1] = data[j+1],data[j]
                        #middle=data[j]
                        #data[j]=data[j+1]
                        #data[j+1]=middle
                        stop_early=False
                if stop_early:
                    break
        
        return data

class Quick_sort:
    
    def swap(self,data: list[int],i:int,j:int):
        data[i], data[j] = data[j], data[i]
        
    def partition(self,ascending:bool,data:list[int],low:int,high:int) -> int: #low=0,high=last index
        
        pivot=data[high]
        i=low-1
        
        if ascending:
            for j in range(low,high):
                if data[j] < pivot:
                    i=i+1
                    self.swap(data,i,j)
        else:
            for j in range(low,high):
                if data[j] > pivot:
                    i=i+1
                    self.swap(data,i,j)
                
        self.swap(data,i+1,high)
        return i+1
    
    def sort(self,ascending:bool,data:list[int], low:int, high:int) -> list[int]:
        if low<high:
            part_ind=self.partition(ascending,data,low,high)
            
            self.sort(ascending,data, low, part_ind - 1)
            self.sort(ascending,data, part_ind + 1, high)
            
        return data
            
class Merge_sort:
    def merge(self, data: list[int], left: int, middle: int, right: int, ascending: bool):
        n1 = middle - left + 1
        n2 = right - middle

        # Create temp arrays
        leftar = [0] * n1
        rightar = [0] * n2

        # Copy data to temp arrays L[] and R[]
        for i in range(n1):
            leftar[i] = data[left + i]

        for j in range(n2):
            rightar[j] = data[middle + 1 + j]

        # Merge the temp arrays back into data[left..r]
        i = 0  # Initial index of first subarray L[]
        j = 0  # Initial index of second subarray R[]
        k = left  # Initial index of merged subarray data[]

        if ascending:
            # Merging for ascending order
            while i < n1 and j < n2:
                if leftar[i] <= rightar[j]:
                    data[k] = leftar[i]
                    i += 1
                else:
                    data[k] = rightar[j]
                    j += 1
                k += 1
        else:
            # Merging for descending order
            while i < n1 and j < n2:
                if leftar[i] >= rightar[j]:
                    data[k] = leftar[i]
                    i += 1
                else:
                    data[k] = rightar[j]
                    j += 1
                k += 1

        # Copy the remaining elements of L[], if there are any
        while i < n1:
            data[k] = leftar[i]
            i += 1
            k += 1

        # Copy the remaining elements of R[], if there are any
        while j < n2:
            data[k] = rightar[j]
            j += 1
            k += 1

    def sort(self, ascending: bool, data: list[int], left: int, right: int) -> list[int]:
        if left < right:
            # Find the middle point
            middle = left + (right - left) // 2

            # Sort first and second halves
            self.sort(ascending, data, left, middle)
            self.sort(ascending, data, middle + 1, right)

            # Merge the sorted halves
            self.merge(data, left, middle, right, ascending)
        return data

#----------------------------------------------------------------
class Bin_search:
    def search(self,data: list[int],target:int) -> bool:
        left=0
        right=len(data)-1
        
        while left < right:
            mid = left + (right - left) // 2
            
            if data[mid] == target:
                return True
            elif data[mid] < target:
                left = mid +1
            else:
                right = mid -1
        
        return False
    
#----------------------------------------------------------------
class Sorted_list:
    def is_sorted_asc(self,ascending:bool,data:list[int]) -> bool:
        
        if ascending:
            for i in range(0,len(data) - 1):
                if data[i] > data[i + 1]:
                    return False
            return True
        else:
            for i in range(0,len(data) - 1):
                if data[i] < data[i + 1]:
                    return False
            return True

#----------------------------------------------------------------
class DFS:
    def __init__(self):
        self.visited = set()

    def search(self, graph: dict, start: int):
        if start not in self.visited:
            print(start)  # Process the node (print, add to list, etc.)
            self.visited.add(start)
            for neighbor in graph[start]:
                self.search(graph, neighbor)

class BFS:
    def search(self, graph: dict, start: int):
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            print(node)  # Process the node (print, add to list, etc.)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


