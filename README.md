# REST-API-app-practice

This project is a **production-ready REST API** built using **Flask**, **Docker**, and **Celery**, providing a robust set of endpoints for various algorithms like sorting arrays, performing binary search, checking if an array is sorted, and running search algorithms on graphs (DFS and BFS). 

The API accepts **JSON payloads** with comprehensive input validation and returns computed results such as:
- Sorted arrays with multiple algorithm options
- Binary search results with performance optimization
- Array sorting validation with edge case handling
- Graph traversal paths (DFS/BFS) with intelligent graph normalization

The project uses a **modular structure** for better maintainability and scalability. The key functionalities are separated into distinct modules:
- **Sorting algorithms**: Bubble sort, Merge sort, Quick sort with enhanced error handling
- **Search algorithms**: Binary search, DFS (Depth-First Search), BFS (Breadth-First Search) with improved robustness
- **Input validation**: Comprehensive validation for all endpoints with detailed error messages
- **Smart caching**: Request-specific caching system for optimal performance

## 🚀 Recent Enhancements (v2.0)

This API has been significantly enhanced with:
- **🛡️ Comprehensive Input Validation**: All endpoints now validate JSON structure, data types, required fields, and business logic constraints
- **⚡ Smart Caching System**: Request-specific cache keys prevent false cache hits and improve performance
- **🔧 Algorithm Improvements**: Fixed critical bugs and enhanced robustness of all algorithms
- **📊 Resource Management**: Added reasonable limits to prevent resource exhaustion
- **🎯 Better Error Handling**: Structured error messages with specific field-level feedback
- **📚 Enhanced Documentation**: Comprehensive docstrings and improved code organization

Additionally, this project includes:
- **Celery**: For asynchronous background task processing (sorting and search tasks)
- **Flask-Caching**: Smart caching with request-specific keys for optimal performance
- **Unit Testing**: Comprehensive test suite ensuring reliability of the codebase

## 🎯 Features

### API Endpoints:
- **`/sort`** (POST): Sort arrays using Bubble, Merge, or Quick sort algorithms with comprehensive validation
- **`/binary_search`** (POST): Perform binary search on sorted arrays with automatic sort validation
- **`/is_sorted`** (POST): Check if arrays are sorted in ascending or descending order with edge case handling
- **`/search`** (POST): Perform graph traversal using DFS or BFS with intelligent graph normalization

### 🛡️ Enhanced Input Validation:
- **JSON Structure Validation**: Ensures all requests contain valid JSON
- **Type Safety**: Strict type checking for all parameters (lists, integers, booleans, strings)
- **Required Field Validation**: Clear error messages for missing required parameters
- **Business Logic Validation**: 
  - Binary search requires sorted arrays
  - Graph search validates node existence and structure
  - Algorithm names must be from supported list
- **Resource Limits**: Prevents resource exhaustion with reasonable size limits
- **Data Integrity**: Validates numeric data and proper list structures

### ⚡ Smart Caching System:
- **Request-Specific Keys**: Each unique request gets its own cache entry using MD5 hashing
- **No False Cache Hits**: Different requests never return incorrect cached results
- **Performance Optimization**: Repeated identical requests return instantly from cache
- **Automatic Expiration**: 5-minute default cache timeout with configurable settings
- **Memory Efficient**: Optimized cache key generation and storage

### 🔧 Algorithm Improvements:
- **Binary Search**: Fixed critical bug (missing return statement) and added empty array handling
- **DFS/BFS**: Improved state management, removed persistent variables, enhanced error handling
- **Graph Processing**: Automatic conversion of string keys to integers for flexibility
- **Edge Case Handling**: Proper handling of empty arrays, single elements, and missing nodes
- **Documentation**: Comprehensive docstrings for all algorithm classes and methods

### 🚨 Advanced Error Handling:
- **Structured Error Messages**: Consistent JSON error format across all endpoints
- **Field-Specific Feedback**: Detailed information about which field caused the error
- **HTTP Status Codes**: Proper use of 400 (client errors) and 500 (server errors)
- **Validation Details**: Clear explanations of what went wrong and how to fix it
- **Logging Integration**: Comprehensive logging for debugging and monitoring

### 🧪 Comprehensive Testing:
- **Unit Tests**: Full test coverage for all algorithms and core functionality
- **Validation Tests**: Tests for all input validation scenarios
- **Edge Case Tests**: Coverage of empty arrays, single elements, and boundary conditions
- **Error Condition Tests**: Verification of proper error handling and status codes
- **Performance Tests**: Caching functionality and response time validation

## 📁 Project Structure

The project follows a clean, modular architecture for maintainability and scalability:

```
REST-API-app-practice/
├── r_app.py                    # Main Flask application with enhanced validation and caching
├── src/                        # Source code directory
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── sorting.py          # Sorting algorithm classes (Bubble, Merge, Quick sort)
│   │   └── search.py           # Search algorithm classes (Binary Search, DFS, BFS)
│   ├── celery_worker/
│   │   ├── __init__.py
│   │   └── celery_worker.py    # Celery configuration and task definitions
│   ├── unit_tests/
│   │   ├── __init__.py
│   │   ├── test_sort.py        # Unit tests for sorting algorithms
│   │   └── test_search.py      # Unit tests for search algorithms
│   └── utils/
│       ├── __init__.py
│       └── pycache_n_logs_deleter.py  # Utility for cleaning cache and logs
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker container configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
└── IMPROVEMENTS.md             # Detailed changelog and improvements
```

### Key Components:
- **`r_app.py`**: Enhanced Flask application with comprehensive input validation, smart caching, and improved error handling
- **`src/algorithms/`**: Modular algorithm implementations with improved robustness and documentation
- **`src/unit_tests/`**: Comprehensive test suite ensuring code reliability and correctness
- **`src/celery_worker/`**: Asynchronous task processing configuration for scalable operations
- **`src/utils/`**: Utility functions and helper scripts for project maintenance

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

Unit tests are located in the `src/unit_tests/` folder. You can run the tests using pytest:

```bash
# Run all tests with verbose output
python -m pytest src/unit_tests/ -v

# Run specific test file
python -m pytest src/unit_tests/test_sort.py -v

# Run tests with coverage (if coverage is installed)
python -m pytest src/unit_tests/ --cov=src.algorithms --cov-report=html
```

This will run all unit tests and verify the functionality of sorting and search algorithms.

## 📋 API Usage Examples

### ✅ Valid Requests:

#### 1. Sort an array (POST /sort):

```json
{
    "data": [5, 3, 8, 1],
    "algorithm": "merge",
    "ascending": true
}
```

**Response:**
```json
{
    "sorted_data": [1, 3, 5, 8]
}
```

**Supported algorithms:** `"bubble"`, `"merge"`, `"quick"`

#### 2. Binary Search on sorted array (POST /binary_search):

```json
{
    "data": [1, 3, 5, 8],
    "target": 5
}
```

**Response:**
```json
{
    "found": true
}
```

**Note:** Data must be sorted in ascending order for binary search to work correctly.

#### 3. Check if an array is sorted (POST /is_sorted):

```json
{
    "data": [1, 3, 5, 8],
    "ascending": true
}
```

**Response:**
```json
{
    "is_sorted": true
}
```

**Edge cases:** Empty arrays and single-element arrays always return `true`.

#### 4. Graph Search (POST /search):

```json
{
    "graph": {1: [2, 3], 2: [4], 3: [4], 4: []},
    "start": 1,
    "algorithm": "DFS"
}
```

**Response:**
```json
{
    "visited": [1, 2, 4, 3]
}
```

**Supported algorithms:** `"DFS"`, `"BFS"`  
**Note:** Graph keys can be integers or string representations of integers.

### ❌ Error Examples:

#### Missing Required Field:
```json
{
    "algorithm": "merge",
    "ascending": true
}
```
**Response (400):**
```json
{
    "error": "'data' is required"
}
```

#### Invalid Data Type:
```json
{
    "data": "not a list",
    "algorithm": "merge",
    "ascending": true
}
```
**Response (400):**
```json
{
    "error": "'data' must be a list"
}
```

#### Unknown Algorithm:
```json
{
    "data": [1, 2, 3],
    "algorithm": "invalid",
    "ascending": true
}
```
**Response (400):**
```json
{
    "error": "'algorithm' must be one of: bubble, merge, quick"
}
```

#### Unsorted Data for Binary Search:
```json
{
    "data": [3, 1, 4, 2],
    "target": 2
}
```
**Response (400):**
```json
{
    "error": "Input data must be sorted in ascending order"
}
```

#### Start Node Not in Graph:
```json
{
    "graph": {2: [3], 3: []},
    "start": 1,
    "algorithm": "DFS"
}
```
**Response (400):**
```json
{
    "error": "Start node 1 not found in graph"
}
```

## 🔧 Resource Limits & Performance

### Data Size Limits:
- **Sorting operations**: Maximum 10,000 elements
- **Binary search**: Maximum 100,000 elements  
- **Is sorted check**: Maximum 100,000 elements
- **Graph search**: Maximum 10,000 nodes and 50,000 edges

### Performance Features:
- **Smart Caching**: Identical requests return instantly from cache
- **Memory Management**: Efficient data copying and cleanup
- **Resource Protection**: Prevents system overload with reasonable limits
- **Optimized Algorithms**: Enhanced implementations with better time complexity

## 🚨 Error Handling & Validation

### Input Validation:
- **JSON Structure**: All requests must contain valid JSON
- **Required Fields**: Clear error messages for missing parameters
- **Type Safety**: Strict validation of data types (lists, integers, booleans)
- **Business Logic**: Algorithm-specific validation (e.g., sorted arrays for binary search)
- **Resource Limits**: Prevents requests that could cause system issues

### Error Response Format:
All errors return a consistent JSON structure:
```json
{
    "error": "Descriptive error message explaining what went wrong"
}
```

### HTTP Status Codes:
- **200**: Successful operation
- **400**: Client error (invalid input, validation failure)
- **500**: Server error (unexpected system error)

## 🧪 Testing & Quality Assurance

### Test Coverage:
- ✅ **Algorithm Tests**: All sorting and search algorithms
- ✅ **Validation Tests**: Input validation for all endpoints
- ✅ **Edge Case Tests**: Empty arrays, single elements, boundary conditions
- ✅ **Error Tests**: Proper error handling and status codes
- ✅ **Performance Tests**: Caching functionality verification

### Running Tests:
```bash
# Run all tests with unittest
python -m unittest discover -s src/unit_tests -v

# Or run with pytest (if available and compatible)
python -m pytest src/unit_tests/ -v

# Check test results
# All tests should pass: "10 tests ... OK"
```

## 📚 Additional Notes

- **Celery Integration**: The project uses Celery for asynchronous task processing. Ensure Redis is running as the message broker.

- **Smart Caching**: Results are cached with request-specific keys, preventing false cache hits and improving performance for repeated requests.

- **Production Ready**: Enhanced error handling, input validation, and resource management make this API suitable for production environments.

- **Scalability**: Modular design and Docker containerization support easy scaling and deployment.

- **Monitoring**: Comprehensive logging helps with debugging and performance monitoring.

## 🚀 Deployment Considerations

### Local Development:
```bash
# Start the application
docker-compose up --build

# Access API at: http://localhost:5000
```

### Production Deployment:
- Consider using Redis for caching in production environments
- Implement rate limiting for API protection
- Add authentication and authorization as needed
- Monitor resource usage and adjust limits accordingly
- Use environment variables for configuration management

### Cloud Deployment:
This API can be deployed on platforms like:
- **Render**: Create a Web Service for the Flask app and a Background Worker for Celery
- **Heroku**: Use web and worker dynos
- **AWS/GCP/Azure**: Deploy using container services with Redis instances

**Note**: Be aware of potential costs when deploying to cloud platforms.
