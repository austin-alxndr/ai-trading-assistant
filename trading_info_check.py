import os
import requests
from dotenv import load_dotenv
load_dotenv()

def get_trading_info(ticker):
    # Check for null pointer references
    if not ticker:
        raise ValueError("Ticker cannot be null or empty")

    url = "https://sucor.sahamology.id/arvita/artificial"
    payload = {
        'id': os.getenv('API_ID'),
        'key': os.getenv('API_KEY'),
        'pesan': '#'+ticker  # Ensure this is the correct key for the ticker
    }
    headers = {}
    
    response = requests.post(url, headers=headers, data=payload)

    # print(f"HTTP Status Code: {response.status_code}")  # Debugging line

    if response.status_code == 200:
        try:
            json_response = response.json()
        except ValueError as e:
            # Log the error and return a generic error message
            print(f"Error decoding JSON: {e}")
            return "Error decoding JSON response"

        # Check for unhandled exceptions
        try:
            result = json_response.get("result", "No signals found")
        except Exception as e:
            # Log the error and return a generic error message
            print(f"Error getting result from JSON: {e}")
            return "Error getting result"

        return result
    else:
        return f"API request failed with status code: {response.status_code}"


# Ensure you print the function's output when calling it
print(get_trading_info('BMRI'))