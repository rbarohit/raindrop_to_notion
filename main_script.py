import requests
from datetime import datetime, timedelta

# Raindrop API details
raindrop_token = '639ad458-6c0a-4a52-9cf2-ddc13f072546'
collections_url = 'https://api.raindrop.io/rest/v1/collections'

# Notion API details
notion_token = 'secret_DA4TPtsfyPqyzIwciKXDdc9VHPl4LIu9tAflFegaVdD'
notion_database_id = '9bb469ff93f94d67b1f2cb8662cd0d3b'
notion_headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# File to store the last checked date
last_date_file = 'last_checked_date.txt'

# Fetch all collection IDs and their names
def fetch_collections():
    headers = {'Authorization': f'Bearer {raindrop_token}'}
    response = requests.get(collections_url, headers=headers)
    if response.status_code == 200:
        collections = response.json()['items']
        return {collection['_id']: collection['title'] for collection in collections}
    else:
        print('Failed to fetch collections:', response.text)
        return {}

# Fetch new articles from a specific collection
def fetch_new_articles(collection_id, last_checked):
    url = f'https://api.raindrop.io/rest/v1/raindrops/{collection_id}'
    headers = {'Authorization': f'Bearer {raindrop_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        articles = response.json()['items']
        return [article for article in articles if datetime.strptime(article['created'], '%Y-%m-%dT%H:%M:%S.%fZ') > last_checked]
    else:
        print(f'Failed to fetch articles from collection {collection_id}:', response.text)
        return []

# Add an article to Notion with highlights
def add_article_to_notion(article, collection_name):
    # Create a page in the Notion database
    properties = {
        "Article Title": {"title": [{"text": {"content": article['title']}}]},
        "Article Link": {"url": article['link']},
        "Collection Name": {"rich_text": [{"text": {"content": collection_name}}]}  # Adjusted to rich_text
    }
    
    # Define the content (blocks) for the page with highlights
    content = []
    for highlight in article.get('highlights', []):
        content.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": highlight['text']}}]}})

    # Assemble the payload for the Notion API call
    data = {
        "parent": {"database_id": notion_database_id},
        "properties": properties,
        "children": content  # This part adds the highlights as content blocks
    }
    
    response = requests.post('https://api.notion.com/v1/pages', headers=notion_headers, json=data)
    if response.status_code == 200:
        print(f"Successfully added {article['title']} to Notion.")
    else:
        print('Failed to add to Notion:', response.text)

# Function to save the current date as the last checked date
def save_last_checked_date():
    with open(last_date_file, 'w') as file:
        file.write(datetime.now().isoformat())

# Function to read the last checked date
def read_last_checked_date():
    try:
        with open(last_date_file, 'r') as file:
            last_date = datetime.fromisoformat(file.read().strip())
    except (FileNotFoundError, ValueError):
        last_date = datetime.now() - timedelta(days=1)  # Default to 1 day ago if no file
    return last_date

# Main script logic
if __name__ == '__main__':
    collections = fetch_collections()
    last_checked_date = read_last_checked_date()

    for collection_id, collection_name in collections.items():
        new_articles = fetch_new_articles(collection_id, last_checked_date)
        for article in new_articles:
            add_article_to_notion(article, collection_name)

    save_last_checked_date()
