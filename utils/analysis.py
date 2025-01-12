import os
import rasterio
import numpy as np
from utils.global_config import VARIABLES, YEARS, VARIABLE_CODE_MAPPING, ANALYSIS_VISUALIZATIONS
from utils.visualization import generate_visualizations
import rioxarray
import openai
from dotenv import load_dotenv
load_dotenv()

def analyze_query(query, data_dir, metadata):
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
    user_comment = query["comments"]
    # print("ANALYSIS TYPE: ", analysis_type)
    # Read and process raster data
    data = read_raster_data(variable, years, data_dir)

    # Suggest visualizations
    suggested_viz = suggest_visualizations(analysis_type)
    # print("Suggested visualizations:", suggested_viz)
    # Generate visualizations
    visualizations = generate_visualizations(query,data_dir, data, suggested_viz)

    # Generate text summary
    text_summary = generate_analysis_summary(data, analysis_type, metadata, variable, user_comment)
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


# Set OpenAI API key
def generate_analysis_summary(data, analysis_type, metadata, variable, user_comment=None):
    """
    Generate a text summary using ChatGPT API based on the analysis type, processed data, and metadata.

    Args:
        data (dict): Processed raster data where each key is a year and the value is a dictionary with analysis details.
        analysis_type (str): Type of analysis requested.
        metadata (dict): Information about the data and processing.
        variable (str): The variable being analyzed.
        user_comment (str, optional): Additional comment or question from the user.

    Returns:
        str: Text summary of the analysis.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY') 
    # Extract summary statistics from the data
    summary_stats = []
    for year, details in data.items():
        summary_stats.append(
            f"Year {year}: "
            f"Variable={details['variable']}, "
            f"Pixel Count={details['pixel_count']}, "
            f"Area={details['area_km2']} km²"
        )

    stats_summary = "\n".join(summary_stats)
    user_comment_text = f"User's comment/question: {user_comment}" if user_comment else "No additional comment provided."

    # Prepare the prompt
    prompt = f"""
    You are a highly knowledgeable data analyst. Based on the following context, generate a detailed yet concise explanation.

    Analysis Context:
    - Variable being analyzed: {variable}
    - Type of analysis: {analysis_type}

    Metadata:
    {metadata}

    Processed Data Summary:
    - Statistics by year:
    {stats_summary}

    {user_comment_text}

    Response:
    """

    # Call ChatGPT API with updated method
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data analyst assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "An error occurred while generating the summary."



def suggest_visualizations(analysis_type):
    """
    Suggest visualizations based on the analysis type using global configuration.

    Args:
        analysis_type (str): Type of analysis requested.

    Returns:
        list: Suggested visualizations.
    """
    return ANALYSIS_VISUALIZATIONS.get(analysis_type, [])
