import requests

token = '639ad458-6c0a-4a52-9cf2-ddc13f072546'
url = 'https://api.raindrop.io/rest/v1/collections'

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

# Checking the response from the server
if response.status_code == 200:
    # If the response is successful, print the data
    print('Success:')
    print(response.json())
else:
    # If the response is an error, print the status code and message
    print('Failed:')
    print('Status code:', response.status_code)
    print('Message:', response.text)


collections_url = 'https://api.raindrop.io/rest/v1/collections'

# Headers with authentication
headers = {
    'Authorization': f'Bearer {token}'
}

# Making the GET request to fetch collections
collections_response = requests.get(collections_url, headers=headers)

# Checking the response from the server
if collections_response.status_code == 200:
    # Parse the JSON response
    collections_data = collections_response.json()
    
    # Assuming there is at least one collection and we are taking the first one
    if collections_data['items']:
        collection_id = collections_data['items'][0]['_id']
        print('Collection ID:', collection_id)

        # URL for the specific collection's raindrops
        raindrops_url = f'https://api.raindrop.io/rest/v1/raindrops/{collection_id}'

        # Making the GET request to fetch raindrops from the specific collection
        raindrops_response = requests.get(raindrops_url, headers=headers)

        # Checking the response for raindrops
        if raindrops_response.status_code == 200:
            print('Raindrops Data:')
            print(raindrops_response.json())
        else:
            print('Failed to get raindrops:')
            print('Status code:', raindrops_response.status_code)
            print('Message:', raindrops_response.text)
    else:
        print('No collections found.')
else:
    print('Failed to get collections:')
    print('Status code:', collections_response.status_code)
    print('Message:', collections_response.text)


    base_url = 'https://api.raindrop.io/rest/v1/raindrop/'

# Headers with authentication
headers = {
    'Authorization': f'Bearer {token}'
}

# Example response data, substitute with your actual response
response_data = {
    'result': True,
    'items': [
        {'_id': 794814410},
        {'_id': 794816468}
    ]
}

# Iterate over each item in the response
for item in response_data['items']:
    raindrop_id = item['_id']
    raindrop_url = f"{base_url}{raindrop_id}"

    # Making the GET request to fetch details for each raindrop
    raindrop_response = requests.get(raindrop_url, headers=headers)

    # Checking the response from the server
    if raindrop_response.status_code == 200:
        print(f'Details for Raindrop ID {raindrop_id}:')
        print(raindrop_response.json())
    else:
        print(f'Failed to get details for Raindrop ID {raindrop_id}:')
        print('Status code:', raindrop_response.status_code)
        print('Message:', raindrop_response.text)