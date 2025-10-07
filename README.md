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
- `r_app.py`: Main Flask application and route definitions
- `celery_worker.py`: Celery configuration and task definitions
- `algorithms/sorting.py`: Sorting algorithm classes (Bubble sort, Merge sort, Quick sort)
- `algorithms/search.py`: Search algorithm classes (Binary Search, DFS, BFS)
- `unit_tests`: Unit tests for verifying the functionality of the application

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
gunicorn==20.1.0
Werkzeug>=2.1,<3.0
pytest==6.2.4
```

# Docker Setup

The application is containerized using Docker. This ensures that the app runs consistently across different environments.

## Steps to run the application:

### Clone the repository:

```bash
git clone <repository_url>
cd <project_directory>
```

### Build the Docker image:

Build the Docker image from the Dockerfile:

```bash
docker build -t flask-rest-api .
```

### Run Redis container:

Celery requires a message broker like Redis. You can run Redis in a container using Docker:

```bash
docker run --name redis -p 6379:6379 -d redis:alpine
```

### Run the Flask app with Docker Compose:

You can run both the Flask app and Redis using Docker Compose, which simplifies the setup by running multiple services in containers.

Create a docker-compose.yml file:

```yaml
version: '3.8'
services:
  app:
    build: .
    command: gunicorn -b 0.0.0.0:5000 r_app:app
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
  celery:
    build: .
    command: celery -A celery_worker.celery_worker.celery worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
```

Then, use the following command to start both services (Flask app and Redis):

```bash
docker-compose up --build
```

### Access the API:

Once the containers are up and running, the Flask app will be accessible at `http://localhost:5000`. You can now make requests to the API using tools like Postman or cURL.

It should also be possible to deploy this API in platforms like Render by creating an Background Worker for the celery worker (because this is what will allow the asynchronous handle of tasks) and a Web Service for the program itself. This will allow to make request through the internet anywhere but be aware of possible costs of deployment in the platform of your choosing.

### Running Unit Tests:

Unit tests are located in the `tests/` folder. You can run the tests using `unittest`:

```bash
python -m unittest discover -s tests
```

This will run all the unit tests in the tests directory.

### Example Requests:

1. Sort an array (POST /sort):

```json
{
    "data": [5, 3, 8, 1],
    "algorithm": "merge",
    "ascending": true
}
```

Response:

```json
{
    "sorted_data": [1, 3, 5, 8]
}
```

2. Binary Search on sorted array (POST /binary_search):

```json
{
    "data": [1, 3, 5, 8],
    "target": 5
}
```

Response:

```json
{
    "found": true
}
```

3. Check if an array is sorted (POST /is_sorted):

```json
{
    "data": [1, 3, 5, 8],
    "ascending": true
}
```

Response:

```json
{
    "is_sorted": true
}
```

4. Graph Search (POST /search):

```json
{
    "graph": { "1": [2, 3], "2": [4], "3": [4], "4": [] },
    "start": 1,
    "algorithm": "DFS"
}
```

Response:

```json
{
    "visited": [1, 2, 4, 3]
}
```

### Additional Notes

- **Celery**: The project uses Celery to handle sorting, searching, and other tasks asynchronously. Make sure you have Redis running as the Celery message broker.

- **Caching**: The results of sorting and search operations are cached to improve performance for repeated requests with the same inputs.

- **Error Handling**: The app includes extensive error handling for invalid inputs, ensuring that meaningful error messages are returned to users.
