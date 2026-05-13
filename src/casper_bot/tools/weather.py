"""Weather tool — fetches weather information for a location."""

from langchain_core.tools import tool


@tool
def get_weather(location: str) -> str:
    """Fetch the current weather for a specific location (city, country).
    Use this when the user asks about the weather or temperature."""
    import os
    import httpx

    # Using OpenWeatherMap or similar as a placeholder for the logic
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    
    if not api_key:
        return (
            f"I'd love to check the weather in {location}, but the weather service is not connected. "
            "Please set OPENWEATHER_API_KEY to enable this feature."
        )

    try:
        # Example API call logic
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            city = data["name"]
            
            return f"The current weather in {city} is {temp}°C with {desc}."
    except Exception as e:
        return f"Failed to fetch weather for {location}: {e}"
