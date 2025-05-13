import os
import requests
import json
from dotenv import load_dotenv
from functools import lru_cache



load_dotenv()

def get_location_id(city: str, country_code: str, file_path: str = "JSON\\locations.json") -> str:
    '''
    returns the location id of a given city and country code.
    '''
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            locations = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    for location in locations:
        if location["name"].lower() == city.lower() and location["country_code"].lower() == country_code.lower():
            location_id = location["id"]
            return location_id
    
    return f"Location not found for {city}, {country_code}"


@lru_cache(maxsize=100)
def search_competitors(query: str, city:str, country_code:str) -> str:
    """
    using google to find the competitors of a given Startup idea and returns a short list.
    """
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the SERPAPI_API_KEY environment variable.")
    
    location_id = get_location_id(city, country_code)
    if isinstance(location_id, str) and "Location not found" in location_id:
        return location_id
    
    params = {
        "engine": "google",
        "q": query + "startup competitors",
        "num": 5,
        "api_key": api_key,
        "location": location_id
    }
    
    try:
        res = requests.get("https://serpapi.com/search", params=params)
        results = res.json().get("organic_results", [])
        if not results:
            return "No competitors found."

        output =  "Top competitors:\n"
        for result in results:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                output += f"- {title}: {link}\n"
        return output
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching data from SerpAPI: {e}"
    


