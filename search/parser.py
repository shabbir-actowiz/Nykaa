from params import *
import requests
import json




def get_first_suggestion(keyword):
    params={}

    url = f"https://www.nykaafashion.com/rest/appapi/V2/search/suggestion"
    
    response = requests.get(
                            url,
                            params={**params, 'searchTerm': keyword},
                            cookies=cookies,
                            headers=headers,
                        )
    
    if response.status_code != 200:

        return {"message": f"Failed to fetch suggestions. Status code: {response.status_code}"}
    
    else:

        data=response.json()
        suggestion=data['response']['suggestions']

        if not suggestion:
            return {"message": "No suggestions found for the given keyword."}
        
        first_suggestion_name=data['response']['suggestions'][0]['suggestionWord']
        
    return get_products(first_suggestion_name)

def get_products(suggestion):

    params = {
    'PageSize': '36',
    'filter_format': 'v2',
    'apiVersion': '6',
    'currency': 'INR',
    'country_code': 'IN',
    'deviceType': 'WEBSITE',
    'sort': 'popularity',
    'device_os': 'desktop',
    'currentPage': '1',
    'sort_algo': 'ltr_pinning',
    }   

    response = requests.get('https://www.nykaafashion.com/rest/appapi/V2/categories/products', params={**params, 'searchTerm': suggestion }, headers=headers)

    if response.status_code == 200:

        data=response.json()
        products=data.get('response', {}).get('products', [])
        
        if not products:
            return {"message": "No products found for the given suggestion."}
        
        cleaned_products = [
                clean_listing_product(product)
                for product in products
            ]
        
        return {'first_suggestion': suggestion, "products": cleaned_products}

    else:

        return {"message": f"Failed to fetch products. Status code: {response.status_code}"}
    
def clean_listing_product(product):
    tag_titles = [tag.get("title") for tag in product.get("tag", []) if tag.get("title")]
    color_codes = product.get("sibling_colour_codes") or []

    return {
        "id": product.get("id"),
        "sku": product.get("sku"),
        "brand": product.get("title"),
        "name": product.get("subTitle"),
        "price": product.get("price"),
        "discounted_price": product.get("discountedPrice"),
        "discount_percent": product.get("discount"),
        "image_url": product.get("imageUrl"),
        "action_url": f"https://www.nykaafashion.com{product.get('actionUrl')}",
        "offer_message": product.get("offer_message"),
        "primary_tag": tag_titles[0] if tag_titles else None,
        "tags": tag_titles,
        "color_codes": color_codes,
        "color_count": len(color_codes),
        "is_out_of_stock": bool(product.get("isOutOfStock")),
    }

