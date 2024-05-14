import requests

def get_invest_info(ticker):
    url = "https://sucor.sahamology.id/arvita/artificial"
    payload = {
        'id': '846765',
        'key': 'SUCOR-z2m5d23a-r1h6-r3o3-gw0k-wetuibdjhkjah',
        'pesan': 'invest #'+ticker  # Ensure this is the correct key for the ticker
    }
    headers = {}
    
    response = requests.post(url, headers=headers, data=payload)

    # print(f"HTTP Status Code: {response.status_code}")  # Debugging line

    if response.status_code == 200:
        try:
            json_response = response.json()
        #    print(f"JSON Response: {json_response}")  # Debugging line

            result = json_response.get("result", "No signals found")
            return result
        except ValueError as e:  # More specific exception handling
            print(f"Error decoding JSON: {e}")  # Debugging line
            return "Error decoding JSON response"
    else:
        return f"API request failed with status code: {response.status_code}"

# Ensure you print the function's output when calling it
print(get_invest_info('BMRI'))