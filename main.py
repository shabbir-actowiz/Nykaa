from db import *
from parser_link import extract_and_insert_categories, parse_products_links, parse_sub_category_products
import time
home_url = "https://www.nykaafashion.com/"


def process_pending_rows(fetch_fn, handler_fn):
    while True:
        rows = fetch_fn()
        if not rows:
            break

        for row in rows:
            handler_fn(row)

def process_category(category):
    sub_id = category["sub_id"]
    main_url = category["main_url"]
    category_name = category["category_name"]

    try:
        product_urls = parse_sub_category_products(main_url, category_name)
        if product_urls is None:
            update_status_fail(sub_id)
            return

        if product_urls:
            insert_sub_category_links(sub_id, product_urls)
            print(f"Inserted {len(product_urls)} sub-category links for category {sub_id}.")
        else:
            print(f"No sub-category links found for category {sub_id}.")

        update_status_done(sub_id)
    except Exception as e:
        print(f"Error processing category {sub_id}: {e}")
        update_status_fail(sub_id)

def process_sub_category(category):
    sub_id = category["sub_id"]
    main_url = category["main_url"]
    category_name = category["category_name"]

    try:
        product_urls = parse_products_links(main_url, category_name)
        if product_urls is None:
            update_sub_category_status_fail(sub_id)
            return

        if product_urls:
            insert_products_links(sub_id, product_urls)
            print(f"Inserted {len(product_urls)} product links for category {sub_id}.")
        else:
            print(f"No product links found for category {sub_id}.")

        update_sub_category_status_done(sub_id)
    except Exception as e:
        print(f"Error processing category {sub_id}: {e}")
        update_sub_category_status_fail(sub_id)

def main():
    start_time = time.time()
    create_database()
    create_table()

    if fetch_category_count() == 0:
        extract_and_insert_categories(home_url)

    process_pending_rows(get_pending_links, process_category)
    process_pending_rows(get_sub_category_links, process_sub_category)

    print(f"Total execution time: {time.time() - start_time} seconds")
    print("Done!")


if __name__ == "__main__":
    main()