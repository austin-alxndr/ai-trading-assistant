import os
import requests
from dotenv import load_dotenv
load_dotenv()

### First Three Signals ###

def get_signals_status(status):
    # Fixed desired keys with their new names
    key_mappings = {
        'kode': 'ticker',
        'plantp1': 'take-profit-1',
        'plantp2': 'take-profit-2',
        'plancl': 'cut-loss-1',
        'plancl2': 'cut-loss-2',
        'planskenario': 'scenario'
    }
    
    url = "https://sucor.sahamology.id/signal"
    payload = {
        'id': os.getenv('API_ID'),
        'key': os.getenv('API_KEY'),
        'short': 'volume',
        'status': status
    }
    headers = {}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            json_response = response.json()
            signals = json_response.get("signal", [])
            if signals:
                # Get up to the first three signals from the list
                first_three_signals = signals[:3]
                # Process each of the first three signals
                processed_signals = [
                    {new_key: signal.get(old_key, None) for old_key, new_key in key_mappings.items()}
                    for signal in first_three_signals
                ]
                return processed_signals
            else:
                return "No signals found"
        except ValueError:  # JSONDecodeError in Python 3.5+
            return "Error decoding JSON response"
    else:
        return f"API request failed with status code: {response.status_code}"
    

print(get_signals_status("fresh buy"))

### First Signal ###

def get_first_signal_for_status(status):
    # Fixed desired keys with their new names
    key_mappings = {
        'kode': 'ticker',
        'plantp1': 'take-profit-1',
        'plantp2': 'take-profit-2',
        'plancl': 'cut-loss-1',
        'plancl2': 'cut-loss-2',
        'planskenario': 'scenario'
    }
    
    url = "https://sucor.sahamology.id/signal"
    payload = {
        'id': '846765',
        'key': 'SUCOR-z2m5d23a-r1h6-r3o3-gw0k-wetuibdjhkjah',
        'short': 'volume',
        'status': status
    }
    headers = {}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            json_response = response.json()
            signals = json_response.get("signal", [])
            if signals:
                first_signal = signals[0]
                # Filter and rename the keys in the first signal as specified
                filtered_and_renamed_signal = {new_key: first_signal.get(old_key, None) for old_key, new_key in key_mappings.items()}
                return filtered_and_renamed_signal
            else:
                return "No signals found"
        except ValueError:  # JSONDecodeError in Python 3.5+
            return "Error decoding JSON response"
    else:
        return f"API request failed with status code: {response.status_code}"