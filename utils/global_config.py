# Variables for Analysis
VARIABLES = [
    {"value": "evergreen_needleleaf_forest", "label": "Evergreen Needleleaf Forest"},
    {"value": "evergreen_broadleaf_forest", "label": "Evergreen Broadleaf Forest"},
    {"value": "deciduous_needleleaf_forest", "label": "Deciduous Needleleaf Forest"},
    {"value": "deciduous_broadleaf_forest", "label": "Deciduous Broadleaf Forest"},
    {"value": "mixed_forests", "label": "Mixed Forests"},
    {"value": "closed_shrublands", "label": "Closed Shrublands"},
    {"value": "open_shrublands", "label": "Open Shrublands"},
    {"value": "woody_savannas", "label": "Woody Savannas"},
    {"value": "savannas", "label": "Savannas"},
    {"value": "grasslands", "label": "Grasslands"},
    {"value": "permanent_wetlands", "label": "Permanent Wetlands"},
    {"value": "croplands", "label": "Croplands"},
    {"value": "urban_and_built_up_lands", "label": "Urban and Built-up Lands"},
    {"value": "cropland_natural_vegetation", "label": "Cropland/Natural Vegetation"},
    {"value": "snow_and_ice", "label": "Snow and Ice"},
    {"value": "barren_or_sparsely_vegetated", "label": "Barren or Sparsely Vegetated"},
    {"value": "no_data", "label": "No Data"},
]

# Variable to Numeric Code Mapping
VARIABLE_CODE_MAPPING = {
    "evergreen_needleleaf_forest": 1,
    "evergreen_broadleaf_forest": 2,
    "deciduous_needleleaf_forest": 3,
    "deciduous_broadleaf_forest": 4,
    "mixed_forests": 5,
    "closed_shrublands": 6,
    "open_shrublands": 7,
    "woody_savannas": 8,
    "savannas": 9,
    "grasslands": 10,
    "permanent_wetlands": 11,
    "croplands": 12,
    "urban_and_built_up_lands": 13,
    "cropland_natural_vegetation": 14,
    "snow_and_ice": 15,
    "barren_or_sparsely_vegetated": 16,
    "no_data": 255,
}

# Supported Analysis Types and Their Expected Visualizations
ANALYSIS_TYPES = [
    # {"value": "trend_analysis", "label": "Trend Analysis"},
    {"value": "spatial_distribution", "label": "Spatial Distribution"},
    # {"value": "change_detection", "label": "Change Detection"},
    # {"value": "comparison", "label": "Comparison"},
    # {"value": "statistical_summary", "label": "Statistical Summary"},
]

# Available Years
YEARS = list(range(2011, 2021))  # 2011 to 2020

# Default Visualization Mapping for Each Analysis Type
ANALYSIS_VISUALIZATIONS = {
    "trend_analysis": ["line_chart"],
    "spatial_distribution": ["choropleth_map","map"],
    "change_detection": ["change_map", "bar_chart"],
    "comparison": ["side_by_side_maps", "bar_chart"],
    "statistical_summary": ["pie_chart"],
}

# Captions for Visualizations
VISUALIZATION_CAPTIONS = {
    "line_chart": "Trend of {variable} over the selected years.",
    "choropleth_map": "Spatial distribution of {variable} in the selected region and year.",
    "change_map": "Change detection map showing differences in {variable} between selected years.",
    "bar_chart": "Comparison of {variable} across selected years or regions.",
    "side_by_side_maps": "Side-by-side maps comparing spatial distribution of {variable} for the selected years.",
    "pie_chart": "Statistical summary of {variable} for the selected year.",
}

OPENAI_API_KEY = "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"