from flask import Blueprint, render_template
from utils import fetch_full_article

view_article_blueprint = Blueprint("view_article", __name__)

@view_article_blueprint.route("/<article_id>", methods=["GET"])
def view_article(article_id):
    try:
        article_content = fetch_full_article(article_id)
        return render_template("article.html", content=article_content)
    except Exception as e:
        return render_template("article.html", error=f"An error occurred: {e}")
