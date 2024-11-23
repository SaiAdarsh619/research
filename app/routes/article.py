from flask import Blueprint, render_template, request
from utils import fetch_paper_details

article_blueprint = Blueprint('article', __name__)

@article_blueprint.route("/article/<arxiv_id>", methods=["GET"])
def article(arxiv_id):
    # Get the full paper details from arXiv API
    paper = fetch_paper_details(arxiv_id)
    
    if paper:
        # Get the previous search query from the request arguments
        previous_query = request.args.get('query', '')
        return render_template("article.html", paper=paper, previous_query=previous_query)
    else:
        return "Error fetching paper details", 404
