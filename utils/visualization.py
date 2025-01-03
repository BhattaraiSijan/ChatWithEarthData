import matplotlib.pyplot as plt
import io
import base64
import geopandas as gpd
import rasterio
from rasterio.plot import show
from utils.global_config import SUPPORTED_INTENTS


def draw_line_chart(data, variables, years):
    """
    Draw a line chart for the given data and variables over specified years.
    
    Args:
        data (list): List of dictionaries containing year-wise data.
        variables (list): List of variables to visualize.
        years (list): List of years to include in the visualization.
    
    Returns:
        str: Base64-encoded image of the line chart.
    """
    # Extract values for each variable and year
    extracted_data = {var: [] for var in variables}
    
    for year in years:
        # Find the data entry for the current year
        year_data = next((entry for entry in data if entry["year"] == year), None)
        if not year_data:
            continue
        for var in variables:
            extracted_data[var].append(year_data.get(var, 0))

    # Plot the line chart
    fig, ax = plt.subplots(figsize=(8, 6))
    for var, values in extracted_data.items():
        ax.plot(years, values, label=var)

    ax.set_title("Trend Analysis")
    ax.set_xlabel("Years")
    ax.set_ylabel("Values")
    ax.legend()
    plt.grid(True)

    # Save chart to Base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.read()).decode("utf-8")
    plt.close(fig)

    return img_b64

def draw_stacked_area_chart(data, variables, years):
    """
    Draw a stacked area chart showing proportions of multiple variables over time.

    Args:
        data (dict): Processed data with proportions for variables over years.
        variables (list): Variables to visualize.
        years (list): List of years for the x-axis.

    Returns:
        str: File path of the saved chart image.
    """
    values = {var: [data[year].get(var, 0) for year in years] for var in variables}

    plt.figure(figsize=(10, 6))
    plt.stackplot(years, *values.values(), labels=variables)
    plt.title("Proportions of Variables Over Time")
    plt.xlabel("Year")
    plt.ylabel("Proportion")
    plt.legend(loc="upper left")
    plt.grid(True)
    
    file_path = "outputs/stacked_area_chart.png"
    plt.savefig(file_path)
    plt.close()
    
    return file_path

def draw_choropleth_map(raster_file, year, variable):
    """
    Draw a choropleth map showing the spatial distribution of a variable.

    Args:
        raster_file (str): Path to the raster file.
        year (int): Year of the data.
        variable (str): Variable to visualize.

    Returns:
        str: File path of the saved map image.
    """
    with rasterio.open(raster_file) as src:
        data = src.read(1)  # Read the first band
        plt.figure(figsize=(12, 8))
        show(data, transform=src.transform, cmap="viridis")
        plt.title(f"{variable} Distribution for {year}")
        
        file_path = f"outputs/{variable}_{year}_choropleth_map.png"
        plt.savefig(file_path)
        plt.close()
    
    return file_path

def draw_change_map(raster_file1, raster_file2, year1, year2, variable):
    """
    Draw a change map showing differences in variable values between two years.

    Args:
        raster_file1 (str): Path to the raster file for year1.
        raster_file2 (str): Path to the raster file for year2.
        year1 (int): First year.
        year2 (int): Second year.
        variable (str): Variable to visualize.

    Returns:
        str: File path of the saved map image.
    """
    with rasterio.open(raster_file1) as src1, rasterio.open(raster_file2) as src2:
        data1 = src1.read(1)
        data2 = src2.read(1)
        change = data2 - data1

        plt.figure(figsize=(12, 8))
        plt.imshow(change, cmap="coolwarm", extent=src1.bounds)
        plt.colorbar(label="Change")
        plt.title(f"Change in {variable} Between {year1} and {year2}")
        
        file_path = f"outputs/{variable}_change_map_{year1}_{year2}.png"
        plt.savefig(file_path)
        plt.close()
    
    return file_path

def fetch_relevant_data_for_line_chart(data):
    # Extract and preprocess data for line chart
    return data

def fetch_relevant_data_for_stacked_area_chart(data):
    # Extract and preprocess data for stacked area chart
    return data

def fetch_relevant_data_for_choropleth(data):
    # Extract and preprocess data for choropleth map
    return data

def fetch_relevant_data_for_change_map(data):
    # Extract and preprocess data for change map
    return data
