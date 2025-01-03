# query_parser.py
from utils.global_config import VARIABLES, ANALYSIS_TYPES, YEARS

def parse_query(query):
    """
    Parse the incoming query to extract variable, analysis type, and years.
    
    Args:
        query (dict): The user's input data, including variable, analysis type, years, and comments.
    
    Returns:
        dict: Parsed query with structured information.
    """
    # Extract inputs
    variable = query.get("variable", "").lower()
    analysis_type = query.get("analysisType", "").lower()
    years = query.get("years", [])
    comments = query.get("comments", "")

    # Validate the variable
    valid_variables = [v["value"] for v in VARIABLES]
    if variable not in valid_variables:
        raise ValueError(f"Invalid variable: {variable}. Must be one of: {', '.join(valid_variables)}")

    # Validate the analysis type
    valid_analysis_types = [a["value"] for a in ANALYSIS_TYPES]
    if analysis_type not in valid_analysis_types:
        raise ValueError(f"Invalid analysis type: {analysis_type}. Must be one of: {', '.join(valid_analysis_types)}")

    # Validate the years
    valid_years = [str(year) for year in YEARS]
    for year in years:
        if year not in valid_years:
            raise ValueError(f"Invalid year: {year}. Must be one of: {', '.join(valid_years)}")
    if len(years) > 2 and analysis_type in ["change_detection", "comparison"]:
        raise ValueError("Only two years can be selected for change detection or comparison.")

    # Return structured data
    return {
        "variable": variable,
        "analysis_type": analysis_type,
        "years": years,
        "comments": comments,
    }
