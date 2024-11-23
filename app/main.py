import os
import requests
from flask import Flask, request, render_template
from routes.search import search_blueprint
from routes.summarize import summarize_blueprint
from utils import build_search_query, fetch_papers, parse_arxiv_response


# Set the full path for templates
template_folder = os.path.join(os.getcwd(), 'templates')

app = Flask(__name__, template_folder=template_folder)

# Register Blueprints
app.register_blueprint(search_blueprint, url_prefix="/search")
app.register_blueprint(summarize_blueprint, url_prefix="/summarize")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Extract form data
    form_data = {
        "query": request.form.get("query"),
        "author": request.form.get("author"),
        "organization": request.form.get("organization"),
        "published_from": request.form.get("published_from"),
        "published_to": request.form.get("published_to"),
        "keywords": request.form.get("keywords"),
    }
    
    # Build the search query
    search_query = build_search_query(form_data)
    arxiv_url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results=5"
    
    # Fetch results from arXiv
    try:
        response = requests.get(arxiv_url)
        response.raise_for_status()
        papers = parse_arxiv_response(response.text)
        return render_template("results.html", papers=papers)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)