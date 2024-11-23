from flask import Blueprint, request, jsonify
from utils import fetch_papers_details, build_search_query

from flask import Blueprint, request, render_template
import requests


search_blueprint = Blueprint('search', __name__)

@search_blueprint.route("/", methods=["POST"])
def search():
    query = request.form.get("query")
    search_type = request.form.get("search_type")
    
    if not query:
        return render_template("results.html", message="No query provided.")

    # Construct the arXiv API query based on the selected search type
    search_query = f"{search_type}:{query}" if search_type != "all" else f"all:{query}"
    
    # Build the arXiv API URL
    arxiv_url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results=5"

    try:
        # Fetch the search results
        response = requests.get(arxiv_url)
        response.raise_for_status()
        
        if response.status_code == 200:
            papers = parse_arxiv_response(response.text)
            return render_template("results.html", papers=papers)
        else:
            return render_template("results.html", message="No results found.")
    except requests.exceptions.RequestException as e:
        return render_template("results.html", message=f"An error occurred: {e}")


def parse_arxiv_response(response_text):
    from xml.etree import ElementTree

    root = ElementTree.fromstring(response_text)
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        author_elems = entry.findall("{http://www.w3.org/2005/Atom}author")
        authors = ", ".join(a.find("{http://www.w3.org/2005/Atom}name").text for a in author_elems if a.find("{http://www.w3.org/2005/Atom}name") is not None)
        organization = entry.find("{http://www.w3.org/2005/Atom}arxiv:affiliation", namespaces={"arxiv": "http://arxiv.org/schemas/atom"})
        organization = organization.text if organization is not None else "Unknown Organization"

        papers.append({
            "title": title,
            "summary": summary,
            "authors": authors,
            "published": published,
            "organization": organization
        })

    return papers