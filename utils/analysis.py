import os
import rasterio
import numpy as np
from utils.global_config import VARIABLES, YEARS, VARIABLE_CODE_MAPPING
from utils.visualization import generate_visualizations
import rioxarray


def analyze_query(query, data_dir):
    """
    Process the entire analysis pipeline.

    Args:
        query (dict): Parsed query from the user input.
        data_dir (str): Path to the data directory.

    Returns:
        dict: Results including text summary and visualizations.
    """
    variable = query["variables"]
    years = query["years"]
    analysis_type = query["intent"]

    # Read and process raster data
    data = read_raster_data(variable, years, data_dir)
    # Generate text summary
    text_summary = generate_analysis_summary(data, analysis_type)

    # Suggest visualizations
    suggested_viz = suggest_visualizations(analysis_type)

    # Generate visualizations
    visualizations = generate_visualizations(data, suggested_viz)

    return {
        "summary": text_summary,
        "visualizations": visualizations,
    }


def read_raster_data(variable, years, data_dir):
    """
    Read raster data for the given variable and years.

    Args:
        variable (str): The variable label (e.g., "classified_land").
        years (list): List of years to analyze.
        data_dir (str): Path to the directory containing raster files.

    Returns:
        dict: Processed raster data for each year.
    """
    variable_code = get_variable_code(variable)
    data = {}

    for year in years:
        file_path = os.path.join(data_dir, f"LC_Type1_{year}.tif")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Raster file not found for year {year}: {file_path}")

        with rioxarray.open_rasterio(file_path) as raster:
            print(f"Processing raster for year {year}")
            print(f"Variable Code: {variable_code}")
            unique_values = np.unique(raster.values)
            print(f"Unique values in raster: {unique_values}")

            # Apply mask for the variable code
            variable_mask = raster.values == variable_code
            pixel_count = variable_mask.sum()
            area_km2 = pixel_count * 0.25  # Assuming 500m x 500m pixels

            print(f"Year {year}: {pixel_count} pixels, {area_km2:.2f} km²")

            # Store results
            data[year] = {
                "variable": variable,
                "pixel_count": int(pixel_count),
                "area_km2": round(area_km2, 2),
                "transform": raster.rio.transform(),
                "crs": raster.rio.crs,
                "year": int(year),
            }

    return data

def get_variable_code(variable):
    """
    Map the variable label to its corresponding numeric code.

    Args:
        variable (str): The variable label (e.g., "evergreen_needleleaf_forest").

    Returns:
        int: The numeric code corresponding to the variable.
    """
    if variable not in VARIABLE_CODE_MAPPING:
        raise ValueError(f"Invalid variable: {variable}")
    return VARIABLE_CODE_MAPPING[variable]


def generate_analysis_summary(data, analysis_type):
    """
    Generate a text summary based on the analysis type and processed data.

    Args:
        data (list): Processed raster data.
        analysis_type (str): Type of analysis requested.

    Returns:
        str: Text summary of the analysis.
    """
    summary = "text summary for {analysis_type} analysis"

    return summary


def suggest_visualizations(analysis_type):
    """
    Suggest visualizations based on the analysis type.

    Args:
        analysis_type (str): Type of analysis requested.

    Returns:
        list: Suggested visualizations.
    """
    if analysis_type == "trend_analysis":
        return ["line_chart", "stacked_area_chart"]
    elif analysis_type == "change_detection":
        return ["bar_chart", "side_by_side_maps"]
    else:
        return []