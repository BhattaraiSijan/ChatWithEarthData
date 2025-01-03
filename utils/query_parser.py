# utils/query_parser.py
import re
from utils.global_config import SUPPORTED_INTENTS

def parse_query(user_query):
    """
    Parse the user query to identify intent and variables.
    """
    parsed_query = {
        "intent": None,
        "variables": {}
    }

    # Step 1: Identify intent
    for intent, config in SUPPORTED_INTENTS.items():
        if intent in user_query.lower():
            parsed_query["intent"] = intent
            break

    if not parsed_query["intent"]:
        # If no intent is identified, return as is
        return parsed_query

    # Step 2: Extract variables based on intent
    required_vars = SUPPORTED_INTENTS[parsed_query["intent"]]["required_variables"]
    for var in required_vars:
        # Basic example using regex (improve as needed)
        if var == "land_cover_type":
            match = re.search(r"(forest|grassland|urban|water)", user_query.lower())
            parsed_query["variables"][var] = match.group(0) if match else None
        elif var == "time_range":
            match = re.search(r"\b\d{4}\b to \b\d{4}\b", user_query.lower())
            parsed_query["variables"][var] = match.group(0) if match else None
        elif var == "time_points":
            match = re.findall(r"\b\d{4}\b", user_query.lower())
            parsed_query["variables"][var] = match if match else None
        elif var == "region":
            match = re.search(r"(north|south|east|west|central)", user_query.lower())
            parsed_query["variables"][var] = match.group(0) if match else None

    # Step 3: Validate variables
    parsed_query["variables"] = {k: v for k, v in parsed_query["variables"].items() if v is not None}

    return parsed_query
