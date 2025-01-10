import matplotlib.pyplot as plt
import numpy as np
import folium
import rasterio
import io
import os
import base64
import json
import rasterio
import rioxarray
import geopandas as gpd
from rasterio.plot import show
from rasterio.mask import mask
from utils.global_config import VARIABLE_CODE_MAPPING
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import mapping
from io import BytesIO


def draw_choropleth_map(variable, year, data_dir):
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
    visualization_results = {}  # Initialize an empty dictionary to store visualizations
    for viz in visualizations:
        if viz == "line_chart":
            visualization_results["line_chart"] = draw_line_chart(data)
        elif viz == "bar_chart":
            visualization_results["bar_chart"] = draw_bar_chart(data)
        elif viz == "choropleth_map":
            visualization_results["choropleth_map"] = draw_choropleth_map(query["variables"], query["years"], data_dir)
        elif viz == "map":
            visualization_results["map"] = draw_map(query["variables"], query["years"], data_dir)

    return visualization_results

def draw_map(variable, year, data_dir):
    """
    Generate a map highlighting the selected variable in the given year's GeoTIFF data.

    Args:
        variable (str): Variable name to filter (e.g., "Forest").
        year (str): Year for the data (e.g., "2011").
        data_dir (str): Directory containing GeoTIFF files.

    Returns:
        str: Base64-encoded HTML representation of the map.
    """
    variable_code = VARIABLE_CODE_MAPPING[variable]
    tif_path = os.path.join(data_dir, f"LC_Type1_{year[0]}.tif")

    # Open the raster file
    with rasterio.open(tif_path) as src:
        if src.crs.to_string() != "EPSG:4326":
            transform, width, height = calculate_default_transform(
                src.crs, "EPSG:4326", src.width, src.height, *src.bounds
            )
            kwargs = src.meta.copy()
            kwargs.update({"crs": "EPSG:4326", "transform": transform, "width": width, "height": height})

            # Reproject on-the-fly without saving
            destination = np.zeros((height, width), dtype=np.uint8)
            reproject(
                source=rasterio.band(src, 1),
                destination=destination,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs="EPSG:4326",
                resampling=Resampling.nearest,
            )
        else:
            destination = src.read(1)
            transform = src.transform

        # Mask for the variable
        mask = (destination == variable_code).astype(float)

        # Downscale the mask for reduced memory usage
        scale_factor = 4
        mask_resized = mask[::scale_factor, ::scale_factor]

        # Get the bounding box
        left, bottom, right, top = rasterio.transform.array_bounds(
            mask_resized.shape[0], mask_resized.shape[1], transform
        )

    # Generate the overlay image in memory
    img_buffer = BytesIO()
    plt.imshow(mask_resized, cmap="Oranges", interpolation="nearest")
    plt.axis("off")
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close()
    img_buffer.seek(0)
    image_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    img_buffer.close()

    # Convert base64 image to a Folium-compatible data URL
    image_url = f"data:image/png;base64,{image_base64}"

    # Create the Folium map
    center_lat = (top + bottom) / 2
    center_lon = (left + right) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=3)

    # Overlay the in-memory image
    folium.raster_layers.ImageOverlay(
        image=image_url,
        bounds=[[bottom, left], [top, right]],
        opacity=0.8,
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Convert map to base64 string
    map_html = m._repr_html_()
    map_base64 = base64.b64encode(map_html.encode("utf-8")).decode("utf-8")

    return map_base64



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