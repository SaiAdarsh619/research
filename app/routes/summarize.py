from flask import Blueprint, request, jsonify
from utils import summarize_text

summarize_blueprint = Blueprint('summarize', __name__)

@summarize_blueprint.route("/", methods=["POST"])
def summarize():
    # Expecting JSON input with a list of texts to summarize
    data = request.get_json()
    if "texts" not in data or not isinstance(data["texts"], list):
        return jsonify({"error": "Invalid input. Provide a list of texts to summarize."}), 400

    texts = data["texts"]
    try:
        summaries = summarize_text(texts)  # Summarize the list of texts
        return jsonify({"summaries": summaries})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
