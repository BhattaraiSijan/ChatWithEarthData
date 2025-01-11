from flask import Flask, request, jsonify, render_template
from utils.query_parser import parse_query
from utils.analysis import analyze_query, suggest_visualizations
from utils.global_config import VARIABLES, ANALYSIS_TYPES, YEARS, VISUALIZATION_CAPTIONS
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


@app.route("/get_config", methods=["GET"])
def get_config():
    """API to fetch configuration for the form."""
    return jsonify({
        "variables": VARIABLES,
        "analysis_types": ANALYSIS_TYPES,
        "years": YEARS
    })


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat queries and return analysis results."""
    data = request.json
    # Extract form data
    intent = data.get("analysisType", "").lower()
    variables = data.get("variable", [])
    years = data.get("years", [])
    comments = data.get("comments", "")

    # Validation
    if not intent:
        return jsonify({"text": "Please select an analysis type."})
    if not variables:
        return jsonify({"text": "Please select at least one variable."})
    if not years or len(years) > 2:
        return jsonify({"text": "Please select a year"})

     # Prepare metadata
    metadata = {
        "description": "Land cover classification data",
        "source": "MODIS Terra/Aqua satellite imagery",
        "processing_steps": [
            "Data downloaded from NASA EarthData",
            "Reprojected to WGS84 EPSG:4326",
            "Processed to extract land cover type"
        ],
    }


    # Parse the query
    parsed_query = {
        "intent": intent,
        "variables": variables,
        "years": years,
        "comments": comments
    }
    
    result = analyze_query(parsed_query, DATA_DIR, metadata)

    # Prepare response
    response = {
        "text": result['summary'],
        "image": result['visualizations'],
    }

    return jsonify(response)

if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(debug=True, port=5000)
