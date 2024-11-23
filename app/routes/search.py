from flask import Blueprint, request, render_template
from utils import fetch_papers

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/", methods=["POST"])
def search():
    search_field = request.form.get("search_field", "all").lower()
    query = request.form.get("query", "").strip()

    if not query:
        return render_template("results.html", papers=[], error="No query provided.")

    try:
        papers = fetch_papers(query, search_field)
        return render_template("results.html", papers=papers)
    except Exception as e:
        return render_template("results.html", papers=[], error=f"An error occurred: {e}")
