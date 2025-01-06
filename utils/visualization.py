import matplotlib.pyplot as plt
import numpy as np
import io
import os
import base64
import rasterio
import rioxarray
from rasterio.plot import show
from utils.global_config import VARIABLE_CODE_MAPPING

def draw_line_chart(data):
    """
    Create a line chart to show trends over years.

    Args:
        data (list): Processed data containing area information for each year.

    Returns:
        str: Base64-encoded string of the generated line chart.
    """
    years = list(data.keys())
    areas = [entry["area_km2"] for entry in data.values()]


    plt.figure(figsize=(10, 7))
    plt.plot(years, areas, marker="o", linestyle="-", label="Area (km²)", color="blue")
    plt.title("Trend Analysis: Area Over Time", fontsize=16)
    plt.xlabel("Years", fontsize=14)
    plt.ylabel("Area (km²)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=12)

    plt.figtext(0.5, -0.1, "This visualization shows the trend of area coverage over selected years.", 
                wrap=True, horizontalalignment='center', fontsize=12)

    # Save the chart to a base64 string
    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode("utf-8")
    plt.close()

    return img_base64


def draw_bar_chart(data):
    """
    Create a bar chart for comparison between two years.

    Args:
        data (list): Processed data containing area information for each year.

    Returns:
        str: Base64-encoded string of the generated bar chart.
    """
    years = list(data.keys())
    areas = [entry["area_km2"] for entry in data]

    plt.figure(figsize=(10, 7))
    plt.bar(years, areas, color="orange", label="Area (km²)")
    plt.title("Comparison Analysis: Area for Selected Years", fontsize=16)
    plt.xlabel("Years", fontsize=14)
    plt.ylabel("Area (km²)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y")
    plt.legend(fontsize=12)

    plt.figtext(0.5, -0.1, "This bar chart compares the area coverage for the selected years.", 
                wrap=True, horizontalalignment='center', fontsize=12)

    # Save the chart to a base64 string
    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode("utf-8")
    plt.close()

    return img_base64


def draw_choropleth_map(variable, year, data_dir):
    print(f"Variable: {variable}, Year: {year}")
    """
    Generate a choropleth map for the selected variable and year.

    Args:
        variable (str): The land cover type selected by the user.
        year (str): The year selected by the user.
        data_dir (str): Path to the directory containing raster files.

    Returns:
        str: Base64-encoded string of the generated choropleth map.
    """
    # Map the variable to its numeric code
    variable_code = VARIABLE_CODE_MAPPING[variable]
    # File path for the raster file
    file_path = os.path.join(data_dir, f"LC_Type1_{year[0]}.tif")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raster file not found for year {year[0]}: {file_path}")

    # Read the raster file
    with rioxarray.open_rasterio(file_path) as raster:
        raster_data = raster.squeeze()
        bounds = raster.rio.bounds()

        # Apply the mask for the selected variable
        variable_mask = raster_data == variable_code

        # Generate the plot
        plt.figure(figsize=(8, 6))
        plt.imshow(variable_mask, extent=[bounds[0], bounds[2], bounds[1], bounds[3]], cmap="YlGn")
        plt.colorbar(label="Land Cover Presence")
        plt.title(f"Spatial Distribution of {variable} in {year}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(False)

        # Save the plot to a base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
        plt.close()

        return img_base64


def generate_visualizations(query, data_dir, data, visualizations):
    """
    Generate visualizations based on the provided visualization types.

    Args:
        data (list): Processed raster data.
        visualizations (list): List of visualization types.

    Returns:
        dict: A dictionary of base64-encoded visualization images.
    """
    visualization_results = {}
    for viz in visualizations:
        if viz == "line_chart":
            visualization_results = draw_line_chart(data)
        elif viz == "bar_chart":
            visualization_results = draw_bar_chart(data)
        elif viz == "choropleth_map":
            visualization_results = draw_choropleth_map(query["variables"], query["years"], data_dir)

    return visualization_results
