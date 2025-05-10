from flask import Flask, request, jsonify
from algorithms.sorting import Bub_sort, Merge_sort, Quick_sort, Sorted_checker
from algorithms.search import Bin_search, DFS, BFS
import logging

app = Flask(__name__)

#Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

#Create a log_handler for the application
log_handler = logging.getLogger(__name__)
logging.debug("log_handler set up and initialized")

app = Flask(__name__)

@app.route('/sort', methods=['POST'])
def sort_numbers():
    try:
        data = request.json.get('data')
        algorithm = request.json.get('algorithm')
        ascending = request.json.get('ascending', True)
        
        # Log the incoming request data
        log_handler.info(f"Received sorting request: data={data}, "
                        "algorithm={algorithm}, ascending={ascending}")

        # Input validation
        if not data or not isinstance(data, list):
            log_handler.error('Invalid input: Missing or invalid data (expected list)')
            return jsonify({"error": "'data' must be a non-empty list"}), 400

        if not algorithm or not isinstance(algorithm, str):
            log_handler.error('Invalid input: Missing or invalid algorithm (expected string)')
            return jsonify({"error": "'algorithm' must be a non-empty string"}), 400

        if not isinstance(ascending, bool):
            log_handler.error('Invalid input: Invalid ascending flag (expected boolean)')
            return jsonify({"error": "'ascending' must be a boolean"}), 400

        # Map algorithm names to classes
        algorithms = {
            "bubble": Bub_sort(),
            "merge": Merge_sort(),
            "quick": Quick_sort(),
        }

        sorter = algorithms.get(algorithm.lower())
        if not sorter:
            log_handler.error(f"Unknown algorithm: {algorithm}")
            return jsonify({"error": "Unknown algorithm"}), 400
        log_handler.info(f"Using algorithm: {algorithm.lower()}")

        if algorithm.lower() in ["quick", "merge"]:
            log_handler.info(f"Sorting data with {algorithm.lower()} algorithm")
            sorted_data = sorter.sort(ascending, data, 0, len(data) - 1)
        else:
            log_handler.info(f"Sorting data with {algorithm.lower()} algorithm")
            sorted_data = sorter.sort(ascending, data)

        log_handler.info(f"Sorted data: {sorted_data}")
        return jsonify({"sorted_data": sorted_data})

    except Exception as e:
        log_handler.error(f"Unexpected error in sort_numbers: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/binary_search', methods=['POST'])
def binary_search():
    try:
        data = request.json.get('data')
        target = request.json.get('target')
        
        # Log the incoming request
        log_handler.info(f"Received binary search request: data={data}, target={target}")

        # Input validation
        if data is None or not isinstance(data, list):
            log_handler.error('Invalid input: Missing or invalid data (expected list)')
            return jsonify({"error": "'data' must be a non-empty list"}), 400

        if target is None or not isinstance(target, int):
            log_handler.error('Invalid input: Missing or invalid target (expected integer)')
            return jsonify({"error": "'target' must be an integer"}), 400

        # Check if data is sorted
        if not Sorted_checker().is_sorted_asc(True, data):
            log_handler.error('Input data is not sorted in ascending order')
            return jsonify({"error": "Input data must be sorted in ascending order"}), 400

        searcher = Bin_search()
        found = searcher.search(data, target)
        
        log_handler.info(f"Search result for target {target}: {'Found' if found else 'Not found'}")
        return jsonify({"found": found})

    except Exception as e:
        log_handler.error(f"Unexpected error in binary_search: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/is_sorted', methods=['POST'])
def is_sorted():
    try:
        data = request.json.get('data')
        ascending = request.json.get('ascending')
        
        # Log the incoming request
        log_handler.info(f"Received check for sorted data request: data={data}, ascending={ascending}")

        # Input validation
        if data is None or not isinstance(data, list):
            log_handler.error('Invalid input: Missing or invalid data (expected list)')
            return jsonify({"error": "'data' must be a non-empty list"}), 400

        if ascending is None or not isinstance(ascending, bool):
            log_handler.error('Invalid input: Missing or invalid ascending flag (expected boolean)')
            return jsonify({"error": "'ascending' must be a boolean"}), 400

        checker = Sorted_checker()
        result = checker.is_sorted_asc(ascending, data)
        
        log_handler.info(f"Data is sorted (ascending={ascending}): {result}")
        return jsonify({"is_sorted": result})

    except Exception as e:
        log_handler.error(f"Unexpected error in is_sorted: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/search', methods=['POST'])
def graph_search():
    try:
        graph = request.json.get('graph')
        start = request.json.get('start')
        algorithm = request.json.get('algorithm')
        
        # Log the incoming request
        log_handler.info(f"Received graph search request: graph={graph}, start={start}, algorithm={algorithm}")

        # Input validation
        if graph is None or not isinstance(graph, dict):
            log_handler.error('Invalid input: Missing or invalid graph (expected dictionary)')
            return jsonify({"error": "'graph' must be a non-empty dictionary"}), 400

        if start is None or not isinstance(start, int):
            log_handler.error('Invalid input: Missing or invalid start (expected integer)')
            return jsonify({"error": "'start' must be an integer"}), 400

        if algorithm is None or not isinstance(algorithm, str):
            log_handler.error('Invalid input: Missing or invalid algorithm (expected string)')
            return jsonify({"error": "'algorithm' must be a non-empty string"}), 400

        # Perform search based on the algorithm
        if algorithm.lower() == "dfs":
            log_handler.info(f"Using DFS algorithm for graph search")
            dfs = DFS()
            visited = dfs.search(graph, start)
            return jsonify({"visited": visited})

        elif algorithm.lower() == "bfs":
            log_handler.info(f"Using BFS algorithm for graph search")
            bfs = BFS()
            visited = bfs.search(graph, start)
            return jsonify({"visited": visited})

        else:
            log_handler.error(f"Unknown algorithm: {algorithm}")
            return jsonify({"error": "Unknown algorithm"}), 400

    except Exception as e:
        log_handler.error(f"Unexpected error in graph_search: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
