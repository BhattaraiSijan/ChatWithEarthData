# global_config.py

SUPPORTED_INTENTS = {
    "trend_analysis": {
        "required_variables": ["land_cover_type", "time_range"],
        "visualizations": ["line_chart", "stacked_area_chart"]
    },
    "spatial_distribution": {
        "required_variables": ["land_cover_type", "region", "year"],
        "visualizations": ["choropleth_map"]
    },
    "change_detection": {
        "required_variables": ["land_cover_type", "time_points"],
        "visualizations": ["change_map"]
    },
    "compare": {
        "required_variables": ["land_cover_types", "regions", "time_points"],
        "visualizations": ["bar_chart", "side_by_side_maps"]
    },
    "statistical_summary": {
        "required_variables": ["land_cover_type", "year"],
        "visualizations": ["pie_chart"]
    },
    "correlation_analysis": {
        "required_variables": ["land_cover_type", "correlating_factors"],
        "visualizations": ["scatter_plot", "heatmap"]
    }
}
