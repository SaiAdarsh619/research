import os
from flask import Flask, request, render_template
from routes.search import search_blueprint
from routes.summarize import summarize_blueprint

# Set the full path for templates
template_folder = os.path.join(os.getcwd(), 'templates')

app = Flask(__name__, template_folder=template_folder)

# Register Blueprints
app.register_blueprint(search_blueprint, url_prefix="/search")
app.register_blueprint(summarize_blueprint, url_prefix="/summarize")

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query") if request.method == "POST" else None
    papers = []

    if query:
        # Importing fetch_papers dynamically
        from utils import fetch_papers  
        papers = fetch_papers(query)

    return render_template("index.html", query=query, papers=papers)

if __name__ == "__main__":
    app.run(debug=True)
