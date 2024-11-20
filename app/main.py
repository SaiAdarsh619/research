import os
from utils import fetch_kaggle_datasets  # Assuming you have a utility to fetch papers
from flask import Flask, request, render_template
from routes.search import search_blueprint
from routes.summarize import summarize_blueprint

template_folder = os.path.join(os.getcwd(), 'templates')

app = Flask(__name__, template_folder=template_folder)

# Register blueprints
app.register_blueprint(search_blueprint, url_prefix="/search")

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("query") if request.method == "GET" else request.form.get("query")
    datasets = []

    if query:
        response = app.test_client().get(f"/search?query={query}")
        print(response.status_code)  # Log the status code
        print(response.data)         # Log the raw data response

        if response.is_json:         # Check if the response is valid JSON
            datasets = response.json.get("datasets", [])
        else:
            print("Error: Response is not JSON")  # Debug if response isn't JSON

    return render_template("index.html", query=query, datasets=datasets)

if __name__ == "__main__":
    app.run(debug=True)