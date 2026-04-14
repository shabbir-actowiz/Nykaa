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
            if  response.status_code == 204:
                print(response.status_code, f"No content found for page {page}. Stopping pagination.")
                break

            data = response.json()
            if data.get("status", "").lower() == "fail" :
                print(f"Failed to fetch page {page} or no products found. Stopping pagination.")
                break
            products = data.get("response", {}).get("products", [])
            links.extend(extract_links(products))
            page += 1


    except Exception as e:
        print(f"An error occurred: {e}")
        return links

    return links 
def extract_links(products):   
    links = []

    for product in products:
        link = product.get("actionUrl")
        if link:
            links.append(base_url+link)

    return links
