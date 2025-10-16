from flask import Flask, request, jsonify
from flask_caching import Cache
from celery_worker.celery_worker import create_celery
from algorithms.sorting import Bub_sort, Merge_sort, Quick_sort, Sorted_checker
from algorithms.search import Bin_search, DFS, BFS
import logging
import os
import hashlib
import json

"""Logging"""
#Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
#Create a log_handler for the application
log_handler = logging.getLogger(__name__)
logging.debug("log_handler set up and initialized")

"""Flask app"""
app = Flask(__name__)

"""app config"""
app.config.update(
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

"""Caching"""
#Initialize the Flask-Caching extension
app.config['CACHE_TYPE'] = 'SimpleCache'  # Using simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds (5 minutes)
cache = Cache(app)

"""Celery asynchronous"""
app.config.update(
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"), #Redis as broker
    CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"), #Redis for storing task results
)
celery = create_celery(app)

"""Helper Functions"""
def generate_cache_key(prefix: str, **kwargs) -> str:
    """Generate a unique cache key based on request parameters"""
    # Sort the kwargs to ensure consistent key generation
    sorted_params = json.dumps(kwargs, sort_keys=True, default=str)
    hash_object = hashlib.md5(sorted_params.encode())
    return f"{prefix}_{hash_object.hexdigest()}"

def validate_request_json():
    """Validate that request contains valid JSON"""
    if not request.is_json:
        return {"error": "Request must contain valid JSON"}, 400
    if not request.json:
        return {"error": "Request body cannot be empty"}, 400
    return None

def validate_data_list(data, field_name="data", allow_empty=False):
    """Validate that data is a proper list"""
    if data is None:
        return {"error": f"'{field_name}' is required"}, 400
    if not isinstance(data, list):
        return {"error": f"'{field_name}' must be a list"}, 400
    if not allow_empty and len(data) == 0:
        return {"error": f"'{field_name}' cannot be empty"}, 400
    if not all(isinstance(x, (int, float)) for x in data):
        return {"error": f"'{field_name}' must contain only numbers"}, 400
    return None

def validate_algorithm(algorithm, valid_algorithms):
    """Validate algorithm parameter"""
    if algorithm is None:
        return {"error": "'algorithm' is required"}, 400
    if not isinstance(algorithm, str):
        return {"error": "'algorithm' must be a string"}, 400
    if algorithm.lower() not in valid_algorithms:
        return {"error": f"'algorithm' must be one of: {', '.join(valid_algorithms)}"}, 400
    return None

def validate_graph(graph, start):
    """Validate graph structure and start node"""
    if graph is None:
        return {"error": "'graph' is required"}, 400
    if not isinstance(graph, dict):
        return {"error": "'graph' must be a dictionary"}, 400
    if len(graph) == 0:
        return {"error": "'graph' cannot be empty"}, 400
    
    # Convert string keys to integers if needed and validate structure
    try:
        normalized_graph = {}
        for key, neighbors in graph.items():
            # Convert key to int if it's a string representation of an int
            if isinstance(key, str) and key.isdigit():
                int_key = int(key)
            elif isinstance(key, int):
                int_key = key
            else:
                return {"error": f"Graph key '{key}' must be an integer or string representation of integer"}, 400
            
            if not isinstance(neighbors, list):
                return {"error": f"Neighbors of node {int_key} must be a list"}, 400
            
            # Validate neighbors are integers
            for neighbor in neighbors:
                if not isinstance(neighbor, int):
                    return {"error": f"All neighbors must be integers, found {type(neighbor).__name__}: {neighbor}"}, 400
            
            normalized_graph[int_key] = neighbors
        
        # Check if start node exists in graph
        if start not in normalized_graph:
            return {"error": f"Start node {start} not found in graph"}, 400
            
        return normalized_graph
    except (ValueError, TypeError) as e:
        return {"error": f"Invalid graph structure: {str(e)}"}, 400

"""Celery related"""
#Celery task definition to sort numbers asynchronously
@celery.task(bind=True)
def async_sort_task(self, data, algorithm, ascending):
    try:
        # Map algorithm names to classes
        algorithms = {
            "bubble": Bub_sort(),
            "merge": Merge_sort(),
            "quick": Quick_sort(),
        }
        sorter = algorithms.get(algorithm.lower())
        if not sorter:
            raise Exception("Unknown algorithm")
        if algorithm.lower() in ["quick", "merge"]:
            return sorter.sort(ascending, data, 0, len(data) - 1)
        else:
            return sorter.sort(ascending, data)
    except Exception as e:
        raise self.retry(exc=e)

#Celery task for binary search asynchronously
@celery.task(bind=True)
def async_binary_search_task(self, data, target):
    try:
        if not Sorted_checker().is_sorted_asc(True, data):
            raise Exception("Input data is not sorted in ascending order")
        searcher = Bin_search()
        found = searcher.search(data, target)
        return found
    except Exception as e:
        raise self.retry(exc=e)

#Celery task for checking if the data is sorted asynchronously
@celery.task(bind=True)
def async_sorted_checker_task(self, data, ascending):
    try:
        checker = Sorted_checker()
        result = checker.is_sorted_asc(ascending, data)
        return result
    except Exception as e:
        raise self.retry(exc=e)

"""Routes"""
@app.route('/sort', methods=['POST'])
def sort_numbers():
    try:
        # Validate JSON request
        json_error = validate_request_json()
        if json_error:
            return jsonify(json_error[0]), json_error[1]

        data = request.json.get('data')
        algorithm = request.json.get('algorithm')
        ascending = request.json.get('ascending', True)
        
        # Log the incoming request data
        log_handler.info(f"Received sorting request: data={data}, "
                        f"algorithm={algorithm}, ascending={ascending}")

        # Enhanced input validation
        data_error = validate_data_list(data)
        if data_error:
            log_handler.error(f'Invalid data input: {data_error[0]}')
            return jsonify(data_error[0]), data_error[1]

        valid_algorithms = ["bubble", "merge", "quick"]
        algorithm_error = validate_algorithm(algorithm, valid_algorithms)
        if algorithm_error:
            log_handler.error(f'Invalid algorithm input: {algorithm_error[0]}')
            return jsonify(algorithm_error[0]), algorithm_error[1]

        if not isinstance(ascending, bool):
            log_handler.error('Invalid input: Invalid ascending flag (expected boolean)')
            return jsonify({"error": "'ascending' must be a boolean"}), 400

        # Additional validation for data size
        if len(data) > 10000:
            log_handler.error('Data size too large')
            return jsonify({"error": "Data size cannot exceed 10,000 elements"}), 400

        # Generate cache key
        cache_key = generate_cache_key("sort", data=data, algorithm=algorithm.lower(), ascending=ascending)
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            log_handler.info("Returning cached result")
            return jsonify({"sorted_data": cached_result})

        # Map algorithm names to classes
        algorithms = {
            "bubble": Bub_sort(),
            "merge": Merge_sort(),
            "quick": Quick_sort(),
        }

        sorter = algorithms.get(algorithm.lower())
        log_handler.info(f"Using algorithm: {algorithm.lower()}")

        # Create a copy of data to avoid modifying the original
        data_copy = data.copy()

        if algorithm.lower() in ["quick", "merge"]:
            log_handler.info(f"Sorting data with {algorithm.lower()} algorithm")
            sorted_data = sorter.sort(ascending, data_copy, 0, len(data_copy) - 1)
        else:
            log_handler.info(f"Sorting data with {algorithm.lower()} algorithm")
            sorted_data = sorter.sort(ascending, data_copy)

        # Cache the result
        cache.set(cache_key, sorted_data)
        
        log_handler.info(f"Sorted data: {sorted_data}")
        return jsonify({"sorted_data": sorted_data})

    except Exception as e:
        log_handler.error(f"Unexpected error in sort_numbers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/binary_search', methods=['POST'])
def binary_search():
    try:
        # Validate JSON request
        json_error = validate_request_json()
        if json_error:
            return jsonify(json_error[0]), json_error[1]

        data = request.json.get('data')
        target = request.json.get('target')
        
        # Log the incoming request
        log_handler.info(f"Received binary search request: data={data}, target={target}")

        # Enhanced input validation
        data_error = validate_data_list(data)
        if data_error:
            log_handler.error(f'Invalid data input: {data_error[0]}')
            return jsonify(data_error[0]), data_error[1]

        if target is None:
            log_handler.error('Invalid input: Missing target')
            return jsonify({"error": "'target' is required"}), 400

        if not isinstance(target, (int, float)):
            log_handler.error('Invalid input: Invalid target (expected number)')
            return jsonify({"error": "'target' must be a number"}), 400

        # Additional validation for data size
        if len(data) > 100000:
            log_handler.error('Data size too large for binary search')
            return jsonify({"error": "Data size cannot exceed 100,000 elements for binary search"}), 400

        # Check if data is sorted
        if not Sorted_checker().is_sorted_asc(True, data):
            log_handler.error('Input data is not sorted in ascending order')
            return jsonify({"error": "Input data must be sorted in ascending order"}), 400

        # Generate cache key
        cache_key = generate_cache_key("binary_search", data=data, target=target)
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            log_handler.info("Returning cached result")
            return jsonify({"found": cached_result})

        searcher = Bin_search()
        found = searcher.search(data, target)
        
        # Cache the result
        cache.set(cache_key, found)
        
        log_handler.info(f"Search result for target {target}: {'Found' if found else 'Not found'}")
        return jsonify({"found": found})

    except Exception as e:
        log_handler.error(f"Unexpected error in binary_search: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/is_sorted', methods=['POST'])
def is_sorted():
    try:
        # Validate JSON request
        json_error = validate_request_json()
        if json_error:
            return jsonify(json_error[0]), json_error[1]

        data = request.json.get('data')
        ascending = request.json.get('ascending')
        
        # Log the incoming request
        log_handler.info(f"Received check for sorted data request: data={data}, ascending={ascending}")

        # Enhanced input validation
        data_error = validate_data_list(data, allow_empty=True)  # Allow empty arrays for is_sorted check
        if data_error:
            log_handler.error(f'Invalid data input: {data_error[0]}')
            return jsonify(data_error[0]), data_error[1]

        if ascending is None:
            log_handler.error('Invalid input: Missing ascending flag')
            return jsonify({"error": "'ascending' is required"}), 400

        if not isinstance(ascending, bool):
            log_handler.error('Invalid input: Invalid ascending flag (expected boolean)')
            return jsonify({"error": "'ascending' must be a boolean"}), 400

        # Additional validation for data size
        if len(data) > 100000:
            log_handler.error('Data size too large')
            return jsonify({"error": "Data size cannot exceed 100,000 elements"}), 400

        # Handle edge case: empty or single element arrays are always sorted
        if len(data) <= 1:
            log_handler.info("Empty or single element array is always sorted")
            return jsonify({"is_sorted": True})

        # Generate cache key
        cache_key = generate_cache_key("is_sorted", data=data, ascending=ascending)
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            log_handler.info("Returning cached result")
            return jsonify({"is_sorted": cached_result})

        checker = Sorted_checker()
        result = checker.is_sorted_asc(ascending, data)
        
        # Cache the result
        cache.set(cache_key, result)
        
        log_handler.info(f"Data is sorted (ascending={ascending}): {result}")
        return jsonify({"is_sorted": result})

    except Exception as e:
        log_handler.error(f"Unexpected error in is_sorted: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/search', methods=['POST'])
def graph_search():
    try:
        # Validate JSON request
        json_error = validate_request_json()
        if json_error:
            return jsonify(json_error[0]), json_error[1]

        graph = request.json.get('graph')
        start = request.json.get('start')
        algorithm = request.json.get('algorithm')
        
        # Log the incoming request
        log_handler.info(f"Received graph search request: graph={graph}, start={start}, algorithm={algorithm}")

        # Enhanced input validation
        if start is None:
            log_handler.error('Invalid input: Missing start node')
            return jsonify({"error": "'start' is required"}), 400

        if not isinstance(start, int):
            log_handler.error('Invalid input: Invalid start node (expected integer)')
            return jsonify({"error": "'start' must be an integer"}), 400

        valid_algorithms = ["dfs", "bfs"]
        algorithm_error = validate_algorithm(algorithm, valid_algorithms)
        if algorithm_error:
            log_handler.error(f'Invalid algorithm input: {algorithm_error[0]}')
            return jsonify(algorithm_error[0]), algorithm_error[1]

        # Validate and normalize graph
        graph_result = validate_graph(graph, start)
        if isinstance(graph_result, tuple):  # Error case
            log_handler.error(f'Invalid graph input: {graph_result[0]}')
            return jsonify(graph_result[0]), graph_result[1]
        
        normalized_graph = graph_result

        # Additional validation for graph size
        total_nodes = len(normalized_graph)
        total_edges = sum(len(neighbors) for neighbors in normalized_graph.values())
        
        if total_nodes > 10000:
            log_handler.error('Graph too large')
            return jsonify({"error": "Graph cannot have more than 10,000 nodes"}), 400
        
        if total_edges > 50000:
            log_handler.error('Graph has too many edges')
            return jsonify({"error": "Graph cannot have more than 50,000 edges"}), 400

        # Generate cache key
        cache_key = generate_cache_key("graph_search", graph=normalized_graph, start=start, algorithm=algorithm.lower())
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            log_handler.info("Returning cached result")
            return jsonify({"visited": cached_result})

        # Perform search based on the algorithm
        if algorithm.lower() == "dfs":
            log_handler.info(f"Using DFS algorithm for graph search")
            dfs = DFS()
            visited = dfs.search(normalized_graph, start)
        elif algorithm.lower() == "bfs":
            log_handler.info(f"Using BFS algorithm for graph search")
            bfs = BFS()
            visited = bfs.search(normalized_graph, start)

        # Cache the result
        cache.set(cache_key, visited)
        
        log_handler.info(f"Graph search completed. Visited nodes: {visited}")
        return jsonify({"visited": visited})

    except Exception as e:
        log_handler.error(f"Unexpected error in graph_search: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
