from curl_cffi import requests
from lxml import html
from parser import fetch_url, convert_to_tree
import json
from db import insert_multiple_category

def get_category_links(tree):
    script=tree.cssselect("script[id='__PRELOADED_STATE__']")
    data=json.loads(script[0].text)

    landingpage=data.get("landingpage", {}).get("landingpageData", [])
    category_links = []
    children=[]
    for item in landingpage:
        if item.get("inventoryName")=="categories-leadins-sale":
            children=item.get("widgetData", {}).get("children", [])

    for link in children:
        category_links.append({"category_name": link.get('params', {}).get('trackingParameters'), "main_url": link.get('params', {}).get('url')})

    return category_links


def extract_and_insert_categories(url):
    responce=fetch_url(url)
    if responce is None:
        print(f"Failed to fetch URL: {url}")
        return None
    
    tree=convert_to_tree(responce)

    category_links=get_category_links(tree)
    print(f"Category Links: {len(category_links)}")
    
    insert_multiple_category(category_links)
    print(f"Inserted {len(category_links)} categories.")


def parse_sub_category_products(url, category_name):
    products_links=[]

    responce=fetch_url(url)
    if responce is None:
        print(f"Failed to fetch URL: {url}")
        return []
    
    tree=convert_to_tree(responce)
    script=tree.cssselect("script[id='__PRELOADED_STATE__']")

    categories_json=json.loads(script[0].text)
    
    #landingpage.landingpageData[1].widgetData.children
    landingpage=categories_json["landingpage"]['landingpageData']
    category_links = []
    
    for item in landingpage:
        children=item.get("widgetData", {}).get("children", [])
        if  children:
            for child in children:
                url=child.get('params', {}).get('url')
                if url and ('lp' not in url ) :
                    category_links.append(url)
            break
    # print("Product Links: ",children_list)       
    print(f"Found {len(category_links)} product links in category {category_name}.")
    return category_links


def parse_products_links(url, category_name):
    children_list=[]
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': 'bcookie=60476f24-5483-4664-81ad-148fd1d7bd5d; EXP_login-experience=login-experience-a; EXP_new-relic-client=variant1; EXP_rating-review-v2=rating-review-v2-a; EXP_fe-api-migration-ab=fe-api-migration-a; EXP_mweb-vector-search=mweb-vector-search-b; EXP_mweb-new-user-ranking=sept_popularity_variant1; EXP_UPDATED_AT=1775547331516; EXP_SSR_CACHE=07ef6141d581b99cacac8db6c0608bff; tm_stmp=1776058030131; rum_abMwebSort=46; EXP_add-to-cart-nudge=atc-a; EXP_prod=prod-a; EXP_search_dn_widgets=search_dn_widgets-a; PHPSESSID=d0d906ee2a354d0cb2c4943a2aba9ab9; EXP_checkout-ssr-mweb=variant-pci; EXP_checkout-ssr-dweb=variant-pci; EXP_login-nudge-plp=Variant1; EXP_speculation-rule-cart-ab=speculation-rule-cart-a; EXP_postorder_variant_ab=postorder_default_A; EXP_gamification-nudge=gamification-nudge-b; EXP_account_order_carousel=account_order_carousel-a; EXP_image-search=image-search-a; _gcl_au=1.1.1133687320.1776058031; _ga=GA1.1.234517355.1776058032; _cs_c=0; _fbp=fb.1.1776058032303.259837650718476676; _clck=ffl33j%5E2%5Eg56%5E0%5E2294; WZRK_G=8143bfdd82ff4e5790eb516b290b0635; _hp5_event_props.2101732631=%7B%7D; NF_LN=true; bm_ss=ab8e18ef4e; NYK_PCOUNTER=2; NYK_ECOUNTER=4; _hp5_let.2101732631=1776075276430; _hp5_meta.2101732631=%7B%22setPath%22%3A%7B%7D%2C%22userId%22%3A%221296054012500774%22%2C%22sessionId%22%3A%22412664248174771%22%2C%22sessionProperties%22%3A%7B%22time%22%3A1776075256636%2C%22id%22%3A%22412664248174771%22%2C%22initial_pageview_info%22%3A%7B%22time%22%3A1776075256636%2C%22id%22%3A%222668349417407023%22%2C%22title%22%3A%22Buy%20Miakee%20Cadence%20Red%20Maxi%20Dress%20(S)%20Online%22%2C%22url%22%3A%7B%22domain%22%3A%22www.nykaafashion.com%22%2C%22path%22%3A%22%2Fmiakee-cadence-red-maxi-dress%2Fp%2F24588232%22%2C%22query%22%3A%22%22%2C%22hash%22%3A%22%22%7D%7D%2C%22search_keyword%22%3A%22%22%2C%22referrer%22%3A%22%22%2C%22utm%22%3A%7B%22source%22%3A%22%22%2C%22medium%22%3A%22%22%2C%22term%22%3A%22%22%2C%22content%22%3A%22%22%2C%22campaign%22%3A%22%22%7D%7D%7D; _cs_id=f0cac99b-bc81-a347-acb2-fd90f239a765.1776058032.2.1776075276.1776075253.1768794831.1810222032605.1.x; _clsk=1qhgibh%5E1776075276663%5E5%5E0%5El.clarity.ms%2Fcollect; _ga_DZ4MXZBLKH=GS2.1.s1776075256$o2$g1$t1776075325$j60$l0$h0; bm_so=1538BA138177E760361BE419CC9E0B94A42637676AABC67DF82FF537C16E0B4A~YAAQmB4SAugDJGmdAQAADlyLhgfb5oYTmcV6eVX83tvbrOrvsx3PpS057w338QPFUHXywl1fOJotpRpyXe9O9wXmB3tGvwAKTY/OcmGzFKtWVfoYsU2P8zKGWPh9amlCKBrBiJoDJXu0HuZlUdwHWUWU6ACnW1zhumvKKIDxQVbZN31wB0nMhpitTmQsQY/ByAgMIIpMBaGWs/vtjUtrFCW8ei5x9hSb5m7193NWvNhTQhJLi/wn/ERmz/q025+eW+7lVG9yXPNZSxcQeuoy8Y/PPHaz8DmPskXRxxGdgpt53q6V4UQOYNECnIIxhKKlTD9cumKSg4JDLKqCwB9gWR+2TWQcWpn8xQZOt9gS3CIaRJdqZhotVG/AnP0kSCSyUh9mjoHA3zTN6lekIYnms8eoxa2LLAQbXNZb8DHwLRWGTRHT3Ipamd3nKlY42GVlolczDXQ66y47g4qjxrd5LJ6LEQv0TnRlnF43iA==; bm_lso=1538BA138177E760361BE419CC9E0B94A42637676AABC67DF82FF537C16E0B4A~YAAQmB4SAugDJGmdAQAADlyLhgfb5oYTmcV6eVX83tvbrOrvsx3PpS057w338QPFUHXywl1fOJotpRpyXe9O9wXmB3tGvwAKTY/OcmGzFKtWVfoYsU2P8zKGWPh9amlCKBrBiJoDJXu0HuZlUdwHWUWU6ACnW1zhumvKKIDxQVbZN31wB0nMhpitTmQsQY/ByAgMIIpMBaGWs/vtjUtrFCW8ei5x9hSb5m7193NWvNhTQhJLi/wn/ERmz/q025+eW+7lVG9yXPNZSxcQeuoy8Y/PPHaz8DmPskXRxxGdgpt53q6V4UQOYNECnIIxhKKlTD9cumKSg4JDLKqCwB9gWR+2TWQcWpn8xQZOt9gS3CIaRJdqZhotVG/AnP0kSCSyUh9mjoHA3zTN6lekIYnms8eoxa2LLAQbXNZb8DHwLRWGTRHT3Ipamd3nKlY42GVlolczDXQ66y47g4qjxrd5LJ6LEQv0TnRlnF43iA==~1776078774429; bm_sz=EA4C31F5218D22E4F7EB298EF7718B40~YAAQmB4SAlEGJGmdAQAA12iLhh9KsYA93B7fd9yucLt/MMNo15tQXHcakkYyUNnmhLXJFyW4inojFlZAw+oOGaOQG88OwwWmRASk5gFJ4z46EwuaozDJllEbFoP0Go/d5T1XisYNVx/h6SsuIJ5lqzie2v+bV03Oc3hpgZvJprL1Psk1GsV03EGXsG2RviBy3UHlz5b+fiiotW1K2jf19ypXgucHW2mDmPQqZw/u0fLi8HWhedxIgGMpcvxXDDP2qR6GE4LM4i03+3mA5a0glwyxzdWf8L4i+AQTbojvvJfJaFxPRvg5M5HYXezesCvJSpTRlPhRNLcGTQh2aDmuBLJk3fdJpOtYG7qKWZQExBPdaG6H5aY2hh6MpeM/mZ8KvJ0nZLeI8dBckXvzwcXLOx6xo88u6i0VflsLES/rBHWul0JAHiQNLMx7CNtCZ+Hpz+/GZF7vWm9wztH48tiLuIz9LmeKBBCaM3dBh7YjZLoZRllvt4th4Q==~3355202~4536133; _abck=3B4A608BE5E34ED85A78DF66114D0BBD~0~YAAQmB4SAtsGJGmdAQAA0GuLhg+b0tZtt0XIg0wgf5JZPWU845Nf70vTEW/aUU4ylfeQzO5DxG1KMu0JvTf7ww518Fau1cw8tpck1/V4mDpIPps50xKlQbb9Ws6o/iWpKGqs4Ea5jHShumFFtAin88VSYB+0U16xJmRVlCYHs6Eyet1ocIDOuyMpVlQaMhk4iFqAmvwhO7Kew4Ye88N6HGUB7Rf1IxK0XryX/Kiqhf44b94u2kLXDJUwN457ISBTC5DrHC0gYvF94yeZgee4qp6Z90YyNsLRprNmkSv/yU5JRs7GDa8zIy7AF+anhy43jja4h4eNfjnDr9q3IdEh3sdOKkbpDVl307j0ipcumMeuBRVikpzjbjOXaeWr42K8Pyg3LJTxnr7zWSZ4kpK3gmsrE4d3Z/dCD8QEFRN2hPw+Wdew148ncaWOIQkrG/ubQLxaQZsdGunG9LdEIR8H6lZtIREydfrLDbDcsR5g/ot2wgq0RQEqkJWRf3L1ntKbe9hC39GOBoGonPsWnqSXH3u6dfFNhM5RTrgQQQoPB2PpNV0fbjQVVeICbfI4KZhCRVX7FwjX0XnSSspRg5UUuzzxxfeuLWO9z5sYupTDOdYAy2Q0Ti61LXoRmR6BU2NzHZF5UTKB6jh7iqzlb6escmEEEsrNiaeH8PTzgo7hBt9zSlTn8wFLW2NIVnXJ10qvZzG089Aw4yVEiUiwJTjBaaB0+yqJqaBi9kmLt+0OsiXQgXJ1WXDI4v4T8HrKJRSG57AFRSEmSCFgnT7P5NA5+XYOUPboe82P716elKyoj9W7lkB20zT+En4k+1o=~-1~-1~1776078867~AAQAAAAF%2f%2f%2f%2f%2fxPRjHH0jgfAdlIw6yOVO0ovOcwfF+OR%2fGfCrD4A8QuKm0CsByJSfxCHP5DbHsaq%2f87v3GKsK4fsPThnVPlV%2flG6rrY2lyOOnfFHud%2fmyq5Wo7dhxmE264i02V8uE1IiRCoaE7%2f%2fFNmoBNDwBuqZjxCDVPQ2qYYKU5kFCnRsBIZZG2lNEQX%2fryVs245+AAod+eFneUSgZIDBw%2f84HrbgGfHMQK1pnNbs+gV1fWDY8LPl14w%3d~-1; bm_s=YAAQmB4SAnMIJGmdAQAABnWLhgXRKuxwWmBPk5/5NCnqMY2QNOUMIL9P9eorapQEi+Fc4tL4aCuqddfmm7BxGU4lGJho0XzrZkxpYElUD/5T2PZahl97IDkg5aAeJzapS+3PPGFxayQIE6dPDxAdBrYyVPAf/gPVciDiOzFJlRlVupWUSPAtj7gylUEqgxcbX5ooAD6EsnR0CDWyllRR6q97lw2rZR2NvcUp1TETGCsl2HceADHfRoHKU6a0ejTNjbHBSbt5nF59QG0d3kO5+duf6/ZFJOOj55sgx06ZJ7CVvO+yeg0G95wPb/JeoFqw1WMIU2CoqmLwcF/LQG6t3nVwIrm6NOv7KQbBHUFSJqc2Om8DmTAUw5YKrMmez3eZHEqWmNQWXoscXH+AWuMGygIBQgkHgSerNiBMQPjk3u71ALtU523fquwt25hqoamd3zm8Ol5r8Tn9/dXOV108EACGfdsSz85Z1IGxFucXxbmO8Mgk+2E7eo8FxqzpQXTmRXXxEzacgru2BGEZunEG8Clm0wKjSuisa9DwUC/y/f3vLG0R1c/61aZvXyukePkYleHJWE10cgx0lk8taP9KNUwVRTYOK3dZGM+CKlM4KG0T/vQXc3mvL7IlydCCpINN5UWGFhPlZhvp35vNSQXWYOrCArv8aSsNkz97FdmKhgDKGs2vO1u8I0JskSc/kVb6LAm8Vrhe0jG+kJHfK9ztj1NIGIpyNAxyUBy1Bw3BZl7qXzAPUvqbokLIYHvRWX7oWlpBjGwN54jXH8fyphjliXKv1rJ/j3QQ6RkQK9hg2wok7nv/iDqpPg8dQ/G6v45T5Wl65R5+jqmDkJ0S0i+xu2pXavwZPtZGSdANcnK7YiftN/imEtVXSeSnQvhz3w==',
}
    cookies = {
    'bcookie': '60476f24-5483-4664-81ad-148fd1d7bd5d',
    'EXP_login-experience': 'login-experience-a',
    'EXP_new-relic-client': 'variant1',
    'EXP_rating-review-v2': 'rating-review-v2-a',
    'EXP_fe-api-migration-ab': 'fe-api-migration-a',
    'EXP_mweb-vector-search': 'mweb-vector-search-b',
    'EXP_mweb-new-user-ranking': 'sept_popularity_variant1',
    'EXP_UPDATED_AT': '1775547331516',
    'EXP_SSR_CACHE': '07ef6141d581b99cacac8db6c0608bff',
    'tm_stmp': '1776058030131',
    'rum_abMwebSort': '46',
    'EXP_add-to-cart-nudge': 'atc-a',
    'EXP_prod': 'prod-a',
    'EXP_search_dn_widgets': 'search_dn_widgets-a',
    'PHPSESSID': 'd0d906ee2a354d0cb2c4943a2aba9ab9',
    'EXP_checkout-ssr-mweb': 'variant-pci',
    'EXP_checkout-ssr-dweb': 'variant-pci',
    'EXP_login-nudge-plp': 'Variant1',
    'EXP_speculation-rule-cart-ab': 'speculation-rule-cart-a',
    'EXP_postorder_variant_ab': 'postorder_default_A',
    'EXP_gamification-nudge': 'gamification-nudge-b',
    'EXP_account_order_carousel': 'account_order_carousel-a',
    'EXP_image-search': 'image-search-a',
    '_gcl_au': '1.1.1133687320.1776058031',
    '_ga': 'GA1.1.234517355.1776058032',
    '_cs_c': '0',
    '_fbp': 'fb.1.1776058032303.259837650718476676',
    '_clck': 'ffl33j%5E2%5Eg56%5E0%5E2294',
    'WZRK_G': '8143bfdd82ff4e5790eb516b290b0635',
    '_hp5_event_props.2101732631': '%7B%7D',
    'NF_LN': 'true',
    'bm_ss': 'ab8e18ef4e',
    'NYK_PCOUNTER': '2',
    'NYK_ECOUNTER': '4',
    '_hp5_let.2101732631': '1776075276430',
    '_hp5_meta.2101732631': '%7B%22setPath%22%3A%7B%7D%2C%22userId%22%3A%221296054012500774%22%2C%22sessionId%22%3A%22412664248174771%22%2C%22sessionProperties%22%3A%7B%22time%22%3A1776075256636%2C%22id%22%3A%22412664248174771%22%2C%22initial_pageview_info%22%3A%7B%22time%22%3A1776075256636%2C%22id%22%3A%222668349417407023%22%2C%22title%22%3A%22Buy%20Miakee%20Cadence%20Red%20Maxi%20Dress%20(S)%20Online%22%2C%22url%22%3A%7B%22domain%22%3A%22www.nykaafashion.com%22%2C%22path%22%3A%22%2Fmiakee-cadence-red-maxi-dress%2Fp%2F24588232%22%2C%22query%22%3A%22%22%2C%22hash%22%3A%22%22%7D%7D%2C%22search_keyword%22%3A%22%22%2C%22referrer%22%3A%22%22%2C%22utm%22%3A%7B%22source%22%3A%22%22%2C%22medium%22%3A%22%22%2C%22term%22%3A%22%22%2C%22content%22%3A%22%22%2C%22campaign%22%3A%22%22%7D%7D%7D',
    '_cs_id': 'f0cac99b-bc81-a347-acb2-fd90f239a765.1776058032.2.1776075276.1776075253.1768794831.1810222032605.1.x',
    '_clsk': '1qhgibh%5E1776075276663%5E5%5E0%5El.clarity.ms%2Fcollect',
    '_ga_DZ4MXZBLKH': 'GS2.1.s1776075256$o2$g1$t1776075325$j60$l0$h0',
    'bm_so': '1538BA138177E760361BE419CC9E0B94A42637676AABC67DF82FF537C16E0B4A~YAAQmB4SAugDJGmdAQAADlyLhgfb5oYTmcV6eVX83tvbrOrvsx3PpS057w338QPFUHXywl1fOJotpRpyXe9O9wXmB3tGvwAKTY/OcmGzFKtWVfoYsU2P8zKGWPh9amlCKBrBiJoDJXu0HuZlUdwHWUWU6ACnW1zhumvKKIDxQVbZN31wB0nMhpitTmQsQY/ByAgMIIpMBaGWs/vtjUtrFCW8ei5x9hSb5m7193NWvNhTQhJLi/wn/ERmz/q025+eW+7lVG9yXPNZSxcQeuoy8Y/PPHaz8DmPskXRxxGdgpt53q6V4UQOYNECnIIxhKKlTD9cumKSg4JDLKqCwB9gWR+2TWQcWpn8xQZOt9gS3CIaRJdqZhotVG/AnP0kSCSyUh9mjoHA3zTN6lekIYnms8eoxa2LLAQbXNZb8DHwLRWGTRHT3Ipamd3nKlY42GVlolczDXQ66y47g4qjxrd5LJ6LEQv0TnRlnF43iA==',
    'bm_lso': '1538BA138177E760361BE419CC9E0B94A42637676AABC67DF82FF537C16E0B4A~YAAQmB4SAugDJGmdAQAADlyLhgfb5oYTmcV6eVX83tvbrOrvsx3PpS057w338QPFUHXywl1fOJotpRpyXe9O9wXmB3tGvwAKTY/OcmGzFKtWVfoYsU2P8zKGWPh9amlCKBrBiJoDJXu0HuZlUdwHWUWU6ACnW1zhumvKKIDxQVbZN31wB0nMhpitTmQsQY/ByAgMIIpMBaGWs/vtjUtrFCW8ei5x9hSb5m7193NWvNhTQhJLi/wn/ERmz/q025+eW+7lVG9yXPNZSxcQeuoy8Y/PPHaz8DmPskXRxxGdgpt53q6V4UQOYNECnIIxhKKlTD9cumKSg4JDLKqCwB9gWR+2TWQcWpn8xQZOt9gS3CIaRJdqZhotVG/AnP0kSCSyUh9mjoHA3zTN6lekIYnms8eoxa2LLAQbXNZb8DHwLRWGTRHT3Ipamd3nKlY42GVlolczDXQ66y47g4qjxrd5LJ6LEQv0TnRlnF43iA==~1776078774429',
    'bm_sz': 'EA4C31F5218D22E4F7EB298EF7718B40~YAAQmB4SAlEGJGmdAQAA12iLhh9KsYA93B7fd9yucLt/MMNo15tQXHcakkYyUNnmhLXJFyW4inojFlZAw+oOGaOQG88OwwWmRASk5gFJ4z46EwuaozDJllEbFoP0Go/d5T1XisYNVx/h6SsuIJ5lqzie2v+bV03Oc3hpgZvJprL1Psk1GsV03EGXsG2RviBy3UHlz5b+fiiotW1K2jf19ypXgucHW2mDmPQqZw/u0fLi8HWhedxIgGMpcvxXDDP2qR6GE4LM4i03+3mA5a0glwyxzdWf8L4i+AQTbojvvJfJaFxPRvg5M5HYXezesCvJSpTRlPhRNLcGTQh2aDmuBLJk3fdJpOtYG7qKWZQExBPdaG6H5aY2hh6MpeM/mZ8KvJ0nZLeI8dBckXvzwcXLOx6xo88u6i0VflsLES/rBHWul0JAHiQNLMx7CNtCZ+Hpz+/GZF7vWm9wztH48tiLuIz9LmeKBBCaM3dBh7YjZLoZRllvt4th4Q==~3355202~4536133',
    '_abck': '3B4A608BE5E34ED85A78DF66114D0BBD~0~YAAQmB4SAtsGJGmdAQAA0GuLhg+b0tZtt0XIg0wgf5JZPWU845Nf70vTEW/aUU4ylfeQzO5DxG1KMu0JvTf7ww518Fau1cw8tpck1/V4mDpIPps50xKlQbb9Ws6o/iWpKGqs4Ea5jHShumFFtAin88VSYB+0U16xJmRVlCYHs6Eyet1ocIDOuyMpVlQaMhk4iFqAmvwhO7Kew4Ye88N6HGUB7Rf1IxK0XryX/Kiqhf44b94u2kLXDJUwN457ISBTC5DrHC0gYvF94yeZgee4qp6Z90YyNsLRprNmkSv/yU5JRs7GDa8zIy7AF+anhy43jja4h4eNfjnDr9q3IdEh3sdOKkbpDVl307j0ipcumMeuBRVikpzjbjOXaeWr42K8Pyg3LJTxnr7zWSZ4kpK3gmsrE4d3Z/dCD8QEFRN2hPw+Wdew148ncaWOIQkrG/ubQLxaQZsdGunG9LdEIR8H6lZtIREydfrLDbDcsR5g/ot2wgq0RQEqkJWRf3L1ntKbe9hC39GOBoGonPsWnqSXH3u6dfFNhM5RTrgQQQoPB2PpNV0fbjQVVeICbfI4KZhCRVX7FwjX0XnSSspRg5UUuzzxxfeuLWO9z5sYupTDOdYAy2Q0Ti61LXoRmR6BU2NzHZF5UTKB6jh7iqzlb6escmEEEsrNiaeH8PTzgo7hBt9zSlTn8wFLW2NIVnXJ10qvZzG089Aw4yVEiUiwJTjBaaB0+yqJqaBi9kmLt+0OsiXQgXJ1WXDI4v4T8HrKJRSG57AFRSEmSCFgnT7P5NA5+XYOUPboe82P716elKyoj9W7lkB20zT+En4k+1o=~-1~-1~1776078867~AAQAAAAF%2f%2f%2f%2f%2fxPRjHH0jgfAdlIw6yOVO0ovOcwfF+OR%2fGfCrD4A8QuKm0CsByJSfxCHP5DbHsaq%2f87v3GKsK4fsPThnVPlV%2flG6rrY2lyOOnfFHud%2fmyq5Wo7dhxmE264i02V8uE1IiRCoaE7%2f%2fFNmoBNDwBuqZjxCDVPQ2qYYKU5kFCnRsBIZZG2lNEQX%2fryVs245+AAod+eFneUSgZIDBw%2f84HrbgGfHMQK1pnNbs+gV1fWDY8LPl14w%3d~-1',
    'bm_s': 'YAAQmB4SAnMIJGmdAQAABnWLhgXRKuxwWmBPk5/5NCnqMY2QNOUMIL9P9eorapQEi+Fc4tL4aCuqddfmm7BxGU4lGJho0XzrZkxpYElUD/5T2PZahl97IDkg5aAeJzapS+3PPGFxayQIE6dPDxAdBrYyVPAf/gPVciDiOzFJlRlVupWUSPAtj7gylUEqgxcbX5ooAD6EsnR0CDWyllRR6q97lw2rZR2NvcUp1TETGCsl2HceADHfRoHKU6a0ejTNjbHBSbt5nF59QG0d3kO5+duf6/ZFJOOj55sgx06ZJ7CVvO+yeg0G95wPb/JeoFqw1WMIU2CoqmLwcF/LQG6t3nVwIrm6NOv7KQbBHUFSJqc2Om8DmTAUw5YKrMmez3eZHEqWmNQWXoscXH+AWuMGygIBQgkHgSerNiBMQPjk3u71ALtU523fquwt25hqoamd3zm8Ol5r8Tn9/dXOV108EACGfdsSz85Z1IGxFucXxbmO8Mgk+2E7eo8FxqzpQXTmRXXxEzacgru2BGEZunEG8Clm0wKjSuisa9DwUC/y/f3vLG0R1c/61aZvXyukePkYleHJWE10cgx0lk8taP9KNUwVRTYOK3dZGM+CKlM4KG0T/vQXc3mvL7IlydCCpINN5UWGFhPlZhvp35vNSQXWYOrCArv8aSsNkz97FdmKhgDKGs2vO1u8I0JskSc/kVb6LAm8Vrhe0jG+kJHfK9ztj1NIGIpyNAxyUBy1Bw3BZl7qXzAPUvqbokLIYHvRWX7oWlpBjGwN54jXH8fyphjliXKv1rJ/j3QQ6RkQK9hg2wok7nv/iDqpPg8dQ/G6v45T5Wl65R5+jqmDkJ0S0i+xu2pXavwZPtZGSdANcnK7YiftN/imEtVXSeSnQvhz3w==',
}

    if url:
        base_url = url
        i=1
        while True:
            page_url = f"{base_url}&p={i}"
            print(page_url)
            responce=requests.get(page_url,impersonate="chrome",headers=headers,cookies=cookies)
            if responce.status_code!=200:
                break
            if responce is None:
                print(f"Failed to fetch URL: {page_url}")
                return []
        
            tree=convert_to_tree(responce.text)
            script=tree.cssselect('script[id="__PRELOADED_STATE__"]')
            data=json.loads(script[0].text)

            if not data:
                print(f"No data found for category {category_name}.")
                return []    


            # listingV2.products
            for pro in data.get('listingV2', {}).get('products', []):
                if pro["actionUrl"].startswith("https"):
                    continue
                children_list.append("https://www.nykaafashion.com"+pro["actionUrl"])

            # print("Product Links: ",children_list)       
            
           
            
            i += 1
    print(f"Found {len(children_list)} product links in category {category_name}.")
    return children_list


    