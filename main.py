from pathlib import Path
from db import *
from category_link_parser import *
from product_parser import *
import json



def main():
    create_schema()
    source_file = Path(__file__).with_name("category_links.json")
    parsed = parse_category_file(source_file)

    with open("parsed_categories.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)

    count=insert_category_link(parsed)
    print(f"Inserted/Updated {count} category links.")

    while True:
        pending_links=get_pending_category_links()
        if not pending_links:
            print("No pending category links found. Exiting.")
            break

        for link in pending_links:
            category_id=link['sub_id']
            api_url=link['product_api_url']
            print(f"Processing category ID {category_id} with API URL: {api_url}")
            product_links=parse_product_links(api_url)
            insert_product_links(category_id, product_links)

    


if __name__ == "__main__":
    main()
