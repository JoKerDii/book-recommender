from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from main import search_and_recommend_books

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    query = request.form["query"]
    recommendations = search_and_recommend_books(query=query)
    return jsonify(
        {
            "recommendation1": recommendations.get('Recommendation0', ''),
            "recommendation2": recommendations.get('Recommendation1', ''),
            "recommendation3": recommendations.get('Recommendation2', ''),
        }
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True, port=8001)
