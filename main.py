from lxml import html
from db import *
from category_link_parser import *
from product_parser import *
import json


def get_category_json():
    try:
        response = requests.get("https://www.nykaafashion.com", impersonate="chrome")
        tree = html.fromstring(response.text)
        script=tree.cssselect("script[id='__PRELOADED_STATE__']")
        data=json.loads(script[0].text)

        with open("category_links.json","w",encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

        return data
    
    except Exception as e:
        print(f"Error fetching category JSON: {e}")
        return {}



if __name__ == "__main__":
    print('-' * 50)
    print("Starting Nykaa Scraper")
    print('-' * 50)
    create_schema()

    if not has_categories():
        source_file = get_category_json()
        parsed = parse_category_file(source_file)
        with open("parsed_categories.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=4)

        count=insert_category_link(parsed)
        print(f"Inserted/Updated {count} category links.")
        print()
        print('-' * 50)
    else:
        print("Categories already exist in database. Skipping all operations.")
        print('-' * 50)
    while True:
        pending_links=get_pending_category_links()
        if not pending_links:
            print('-' * 50)
            print("No pending category links found. Exiting.")
            print('-' * 50)
            break
        for link in pending_links:
            category_id=link['sub_id']
            api_url=link['product_api_url']
            print('-' * 50)
            print(f"Processing category ID {category_id} with API URL: {api_url}")
            print('-' * 50)
            product_links=parse_product_links(api_url)
            if product_links:
                insert_product_links(category_id, product_links)
                update_category_status(category_id, 'done')
            else:
                print(f"No product links found for category ID {category_id}. Marking as failed.")
                update_category_status(category_id, 'failed')