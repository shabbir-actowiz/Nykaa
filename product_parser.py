from curl_cffi import requests

from curl_cffi import requests
base_url='https://www.nykaafashion.com'
def parse_product_links(url):
    links=[]
    try:
        page = 1
        new_url = url.replace("currentPage=1", "currentPage={}")
        print(f"Starting to fetch product links from: {url}")
        while True:
            changed_url = new_url.format(page)
            response = requests.get(changed_url, impersonate="chrome")       
            data = response.json()
            
            products = data.get("response", {}).get("products", [])
            if response.status_code != 200 or data.get("status", "").lower() == "fail" or not products:
                print(f"Failed to fetch page {page} or no products found. Stopping pagination.")
                break

            links.extend(extract_links(products))
            page += 1
            
        return links    

    except Exception as e:
        print(f"An error occurred: {e}")
        return links


def extract_links(products):   
    links = []

    for product in products:
        link = product.get("actionUrl")
        if link:
            links.append(base_url+link)

    return links
