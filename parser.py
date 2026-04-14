from logging import info
from curl_cffi import requests
from lxml import html




def fetch_url(url):
    try:
        response = requests.get(url, impersonate='chrome', timeout=30)
        if response.status_code != 200:
            print(f"Error fetching URL: {url} | Status Code: {response.status_code}")
            return None
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

def convert_to_tree(text):
    try:
        tree = html.fromstring(text)
        return tree 
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None


