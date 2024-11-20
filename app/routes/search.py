from flask import Blueprint, request, jsonify
from utils import fetch_papers

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route("/", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    papers = fetch_papers(query)
    return jsonify({"query": query, "papers": papers})
