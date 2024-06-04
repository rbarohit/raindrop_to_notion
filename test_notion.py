import requests

token = 'secret_DA4TPtsfyPqyzIwciKXDdc9VHPl4LIu9tAflFegaVdD'
database_id = '9bb469ff93f94d67b1f2cb8662cd0d3b'


headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # Make sure this is the latest version available
}

# The data for the new database entry
data = {
    "parent": {"database_id": database_id},
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "New Entry"
                    }
                }
            ]
        }
    }
}

# Make the HTTP request to create a new entry in the Notion database
response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
print(response.text)  # This prints the response from the Notion API