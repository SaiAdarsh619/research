from flask import Blueprint, request, jsonify
from utils import fetch_kaggle_datasets, summarize_text

search_blueprint = Blueprint('search', __name__)
@search_blueprint.route("/", methods=["GET"])
def search():
    query = request.args.get("query")  # Retrieve search query from GET request
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Fetch datasets from Kaggle
        datasets = fetch_kaggle_datasets(query)

        # Summarize descriptions
        for dataset in datasets:
            dataset["summary"] = summarize_text(dataset["description"])

        return jsonify({"query": query, "datasets": datasets})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process request"}), 500
