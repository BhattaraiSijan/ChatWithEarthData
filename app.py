from flask import Flask, request, jsonify, render_template
from utils.query_parser import parse_query
from utils.analysis import read_raster_data, generate_visualizations,generate_text_response
from utils.global_config import SUPPORTED_INTENTS
import os
import logging

app = Flask(__name__)

# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/get_intents", methods=["GET"])
def get_intents():
    """Return SUPPORTED_INTENTS as JSON."""
    return jsonify(SUPPORTED_INTENTS)

@app.route("/chat", methods=["POST"])
def chat():
    # Parse the incoming JSON data
    data = request.json
    intent = data.get("intent", "").lower()
    variables = data.get("variables", [])
    years = data.get("years", [])
    comments = data.get("comments", "")

    # Validation
    if not intent:
        return jsonify({"text": "Please select an analysis type."})
    if not variables:
        return jsonify({"text": "Please select at least one variable."})
    if not years or len(years) > 2:
        return jsonify({"text": "Please select one or two years."})

    
    # Analyze the data
    parsed_query = {
        "intent": intent,
        "variables": variables,
        "years": years,
        "comments": comments,
    }

    data = read_raster_data(parsed_query['years'], DATA_DIR)

    text_analysis = generate_text_response(data, parsed_query)
    visualization = generate_visualizations(data, parsed_query)

    return jsonify({"text": text_analysis, "image_base64": visualization})

if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(debug=True, port=5000)
