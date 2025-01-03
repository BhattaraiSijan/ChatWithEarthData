import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import rasterio
from rasterio.plot import show

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


def draw_choropleth_map(raster_file, year, variable):
    """
    Generate a choropleth map for a specific year and variable.

    Args:
        raster_file (str): Path to the raster file.
        year (int): Year of the data.
        variable (str): Selected variable.

    Returns:
        str: Base64-encoded string of the generated map.
    """
    with rasterio.open(raster_file) as src:
        data = src.read(1)  # Read the first band
        mask = data == int(variable)  # Filter by the variable

        plt.figure(figsize=(12, 8))
        show(mask, transform=src.transform, cmap="Greens")
        plt.title(f"Choropleth Map for {variable} in {year}", fontsize=16)
        plt.figtext(0.5, -0.1, 
                    f"This map visualizes the spatial distribution of '{variable}' in the year {year}.",
                    wrap=True, horizontalalignment='center', fontsize=12)

        # Save the map to a base64 string
        img_io = io.BytesIO()
        plt.savefig(img_io, format="png", bbox_inches="tight")
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.read()).decode("utf-8")
        plt.close()

        return img_base64


def generate_visualizations(data, visualizations):
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
            visualization_results["line_chart"] = draw_line_chart(data)
        elif viz == "bar_chart":
            visualization_results["bar_chart"] = draw_bar_chart(data)
        elif viz == "choropleth_map":
            for entry in data:
                raster_file = entry.get("raster_file")
                year = entry.get("year")
                variable = entry.get("variable")
                if raster_file and variable:
                    visualization_results[f"choropleth_map_{year}"] = draw_choropleth_map(raster_file, year, variable)

    return visualization_results
