import os
import rasterio
import numpy as np
from utils.global_config import SUPPORTED_INTENTS
from utils.visualization import *

# Define forest classes and pixel area for calculation
FOREST_CLASSES = [1, 2, 3, 4, 5]  # Example forest classes
PIXEL_AREA_KM2 = 0.25  # Assuming 500m x 500m pixel size

def generate_visualizations(data, parsed_query):
    """Generate visualizations based on parsed query."""
    visualizations = []
    visualizations_list = suggest_visualizations(parsed_query)

    for viz in visualizations_list:
        if viz == "line_chart":
            visualizations.append(draw_line_chart(data, parsed_query["variables"], parsed_query["years"]))
        elif viz == "choropleth_map":
            for entry in data:
                raster_file = entry.get("raster_file")
                if raster_file:
                    year = entry.get("year")
                    variable = parsed_query["variables"][0]  # Assume one variable for simplicity
                    visualizations.append(draw_choropleth_map(raster_file, year, variable))

    return visualizations


def generate_text_response(data,parsed_query):
    """
    Generate textual analysis response based on the query and data.
    """
    # Use third-party API like GPT to process text response (to be implemented later)
    response = f"Analyzed data for query: {parsed_query.get('intent')} with years {parsed_query.get('years')}"
    return response

def suggest_visualizations(parsed_query):
    """
    Suggest visualizations based on the parsed query.
    """
    intent = parsed_query.get("intent")
    variables = parsed_query.get("variables", {})

    visualizations = []

    if intent in SUPPORTED_INTENTS:
        # Fetch recommended visualizations from global config
        visualizations = SUPPORTED_INTENTS[intent]["visualizations"]

    return visualizations

import os
import rasterio

def read_raster_data(years, data_dir):
    """
    Reads raster files for the specified years and extracts relevant data.
    
    Args:
        years (list): List of years for which data should be read.
        data_dir (str): Path to the directory containing the raster files.
    
    Returns:
        list: A list of dictionaries containing data and metadata for each year.
    """
    results = []
    for year in years:
        file_path = os.path.join(data_dir, f"LC_Type1_{year}.tif")
        print(f"Checking file: {file_path}")  # Debugging

        if os.path.isfile(file_path):
            with rasterio.open(file_path) as src:
                raster_data = src.read(1)  # Read the first band
                results.append({
                    "year": year,
                    "raster_file": file_path,
                    "raster_data": raster_data,  # Store the raster array
                    "metadata": src.meta,  # Store raster metadata
                })
        else:
            print(f"File not found for year {year}: {file_path}")  # Debugging
            results.append({
                "year": year,
                "raster_file": None,
                "raster_data": None,
                "metadata": None,
            })
    return results
