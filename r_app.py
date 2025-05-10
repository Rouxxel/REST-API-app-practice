from flask import Flask, request, jsonify
from algorithms.sorting import Bub_sort, Merge_sort, Quick_sort, Sorted_checker
from algorithms.search import Bin_search, DFS, BFS

app = Flask(__name__)

@app.route('/sort', methods=['POST'])
def sort_numbers():
    data = request.json.get('data')
    algorithm = request.json.get('algorithm')
    ascending = request.json.get('ascending', True)

    if not data or not algorithm:
        return jsonify({"error": "Invalid input"}), 400

    # Map algorithm names to classes
    algorithms = {
        "bubble": Bub_sort(),
        "merge": Merge_sort(),
        "quick": Quick_sort(),
    }

    sorter = algorithms.get(algorithm.lower())
    if not sorter:
        return jsonify({"error": "Unknown algorithm"}), 400

    if algorithm.lower() in ["quick", "merge"]:
        sorted_data = sorter.sort(ascending, data, 0, len(data) - 1)
    else:
        sorted_data = sorter.sort(ascending, data)

    return jsonify({"sorted_data": sorted_data})

@app.route('/binary_search', methods=['POST'])
def binary_search():
    data = request.json.get('data')
    target = request.json.get('target')

    if data is None or target is None:
        return jsonify({"error": "Invalid input"}), 400

    if not Sorted_checker().is_sorted_asc(True, data):
        return jsonify({"error": "Input data must be sorted in ascending order"}), 400

    searcher = Bin_search()
    found = searcher.search(data, target)
    return jsonify({"found": found})

@app.route('/is_sorted', methods=['POST'])
def is_sorted():
    data = request.json.get('data')
    ascending = request.json.get('ascending')

    if data is None or ascending is None:
        return jsonify({"error": "Invalid input"}), 400

    checker = Sorted_checker()
    result = checker.is_sorted_asc(ascending, data)
    return jsonify({"is_sorted": result})

@app.route('/search', methods=['POST'])
def graph_search():
    graph = request.json.get('graph')
    start = request.json.get('start')
    algorithm = request.json.get('algorithm')

    if graph is None or start is None or algorithm is None:
        return jsonify({"error": "Invalid input"}), 400

    if algorithm.lower() == "dfs":
        dfs = DFS()
        visited = dfs.search(graph, start)
        return jsonify({"visited": visited})

    elif algorithm.lower() == "bfs":
        bfs = BFS()
        visited = bfs.search(graph, start)
        return jsonify({"visited": visited})

    else:
        return jsonify({"error": "Unknown algorithm"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
