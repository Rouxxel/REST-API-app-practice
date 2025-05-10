# REST-API-app-practice

This project is a **REST API** built using **Flask**, **Docker**, and **Celery**, providing a set of endpoints for various algorithms like sorting arrays, performing binary search, checking if an array is sorted, and running search algorithms on graphs (DFS and BFS). 

The API accepts **JSON payloads** and returns computed results such as:
- Sorted arrays
- Search results (binary search)
- Traversal paths (DFS/BFS for graph search)

The project uses a **modular structure** for better maintainability and scalability. The key functionalities are separated into distinct modules:
- **Sorting algorithms**: Bubble sort, Merge sort, Quick sort
- **Search algorithms**: Binary search, DFS (Depth-First Search), BFS (Breadth-First Search)
- **Error handling**: Ensures smooth responses even when something goes wrong

Additionally, this project includes:
- **Celery**: For asynchronous background task processing (sorting and search tasks)
- **Flask-Caching**: For caching responses to improve performance
- **Unit Testing**: To ensure the reliability of the codebase

## Features

### Endpoints:
- **`/sort`** (POST): Sort an array using the specified algorithm (Bubble, Merge, Quick).
- **`/binary_search`** (POST): Perform a binary search on a sorted array.
- **`/is_sorted`** (POST): Check if an array is sorted in ascending or descending order.
- **`/search`** (POST): Perform graph search using DFS or BFS.

### Background Tasks (Celery):
- Sorting algorithms are executed asynchronously using **Celery**, allowing users to perform other tasks while waiting for the result.
- Celery tasks include sorting arrays, performing binary search, and checking if the array is sorted.

### Caching:
- Results for sorting, binary search, and sorted-checking are cached using **Flask-Caching**, ensuring that repeated requests with the same input don't have to be reprocessed.

### Error Handling:
- Comprehensive error handling is implemented, providing clear and informative error messages in case of invalid inputs or unexpected issues.

### Unit Tests:
- The project includes **unit tests** for core functionalities like sorting, searching, and checking if an array is sorted.

## Project Structure

The project has been refactored into modules to keep the code clean and maintainable:
- `app.py`: Main Flask application and route definitions
- `celery_worker.py`: Celery configuration and task definitions
- `algorithms/sorting.py`: Sorting algorithm classes (Bubble sort, Merge sort, Quick sort)
- `algorithms/search.py`: Search algorithm classes (Binary Search, DFS, BFS)
- `tests`: Unit tests for verifying the functionality of the application

## Requirements

Make sure you have the following installed:
- **Docker**
- **Docker Compose**
- **Redis** (for Celery to work as a message broker)

### Python dependencies:
The following dependencies are required for the project to run:

```txt
Flask==2.2.2
Flask-Caching==2.3.1
celery==5.5.2
redis==6.0.0
