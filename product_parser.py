from curl_cffi import requests

from curl_cffi import requests
base_url='https://www.nykaafashion.com'
def parse_product_links(url):
    links=[]
    try:
        page = 1
        new_url = url.replace("currentPage=1", "currentPage={}")
        print(f"Starting to fetch product links from: {url}")
        headers = {
                'domain': 'NYKAA_FASHION',
                'sec-ch-ua-platform': '"Windows"',
                'x-csrf-token': 'K2zAZtcvYyAywhdt',
                'Referer': 'https://www.nykaafashion.com/women/westernwear/c/3?f=new_tags_filter%3Dlatestseason_new_&transaction_id=643cdec843c4973bb7a115efd685f8bb&intcmp=nykaa%3Aother%3Anf-westernwear%3Adefault%3Acategories%3ASLIDING_WIDGET_V2%3A2%3Anew%3A-1%3A643cdec843c4973bb7a115efd685f8bb&p=2',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
                'sec-ch-ua-mobile': '?0',
                'Cookie': '_abck=3B4A608BE5E34ED85A78DF66114D0BBD~-1~YAAQKBzFF20rxWadAQAAFmktiw9gJXrN/NSOtZf6ZLmHaavpraQMSgR4o2f1c5BWEFLD8/pDkcxg5h4eT+ZaRBhrfWPXOCMENe0cMBqvDUlXSDHkKRq0P26w4FmGV5EjbMfx8CzShCQ1EvrbNA9zOOFagNb5LeogfEiCLiyeTzoYPDkgtRlT0alMOGFHVHa6Fz1J+pUOSCcAsFcuR0VoUglEpV+LHeakPBf7vxMFM2Q33zx58yXU6mJ/BvQp96UkIjz9EMKRGEN8OvK30+hDW6Z1QsRZ9NVsDvbFFo8W0LSYg/KYABJIPONnCEytJxvfSW1ccyI7S11YJM9GyqP8C8DhU6H+hgzZLVuXfyKiifaGgrtmDFoQs0J/5G6mrAOAJuHp/96L5VODeDneVtqivX4Ne88oani7t7N3VqrKSU0jEgSGySP74tPPT+rwKaCMZNzpojlmpgSAbtVI9IehUbIcUtImLl9vpp5lukodF2/NXVrRT/Nt2kCstY3yozA1b+jjY/x/rO+iU5JpayhWH7DLEwTaJQlHBeqq6siB3vRk2A/ZkNBbTpZ4dcol+Yo8LDksQZCFCuz/eAXNzWMvcIE6FcFvtvFvs/vhz81bryKay5Hd4aq5sNzh9H4Sn3e4CCLfIL2Bjduw69+49gr6DV1ER4tDZXKBM0C7iGbh+ZDbhfVuK5D/zfyIJZEpocTsP4A6F3q5n+SfHenjstONz2QFofIdk0FMFxRteArFJEa86+oUl99uvgeX1ihQMXWYfU1JvGjuIp97J7huQB/Kn9nloXemEHYwD0Xk2/qnc54YQEcktGKlpCji3TmX~-1~-1~1776086027~AAQAAAAF%2f%2f%2f%2f%2f+5Ljw9f49H25V5iO3TImQurjWgf47PVpuYVIPi2E+o+3ZnceaAD8GltLFa2IT0tKRSxo5zz6bi21utvXUjR7coA4BZvVM3tGnlZGeBnmjlgLJjbIaS9g2S0BefeuY1eiNMGXCqFLRdm9KF9JQ4BN%2ffO%2fj+rRPrGL5MiP%2fDRY%2fB3HrnFrYFUHs0DZwPMfUjfEmk5ld%2f56i0lBhlGwTzAHRmxidoKjl%2fHug7%2fg8VmIxMZ4no%3d~-1; bm_s=YAAQKBzFF24rxWadAQAAFmktiwX2e2wfOCsWSkQHcdd3KKoVAF7QRudtR0o2SsUhcSgccOkzWYJiOhP3Ji/MHHdrcwgqk2t1WcILaITxIgGZxZdVpwjCmnV2ciJAqYzJwJb13XwvdRgF50XGJ7VwvfkuFeLmHydicoaZqXpQJAuEAfaod7nLlDQhhSHWT0+pYyNwolo3A2MXXBM3HcCFpcCRkEF59OWvKydM0tt3MD6co/3etnqdqQTWUYR5i2dg2BoBSHno/SJ55DL8qqoT4vCQsE3Etg8N/4h2o/YGp4pq1ntDWHigeU4YwHNWZeY4z9MQr37IrL7cKPEjWusmM+ZPEe1F9KWHUuuCBiCecctOqQIbzI2TbuvaSF//p0VBLUftvzwAEyAj7ZdH4fMPuq+IRTmhfcgyzF60wPRaoE7t5wmu+Rn7DNBITqkzmqnRzm6wa+J/2MqqOb2nkgO8g7Dj5zafXdt8mxLYFtT2Cknhk7uhQxhnw34USGM46VEAI1GnaI/7oVdKINtUCMlBj3FWaVUzOfwcSqQiKatjdC2w1bZKs4L2DU/+xu7t5b/gW8ZehFxvlL59KaDL2Y5wLjOmz/LCaYndn1RNW98GQUyt2b9P5qK7QH2x9sg7tHNsUmFrc55CdmXtRdhz00VaW8nfJ6yRc4vgmF4=; bm_so=4EF420EB20E17CA7AAC5A000373485629488D90EDCE988647471EFDF7C61A678~YAAQmB4SAos6KGmdAQAAQ4uihgd3sNcgUjJ28gkPU4/o0Np6rv/U4EwaCiN/cL3nCgxar4H/nQlCZahKugMZEwVkGDHpAC+qBOspsBM8u4Nxb9FrYFDiGz+zZC9/eB4qEDHwB60Gmbz60DUNnipWKXKUzrgKObYmT+5iGGPvn/e5Pfyw2J20Kg7gaulQjk12yr90kgW5mtwEByBkKSjO0/Z4rgHASxtQGSFZpTwSbp/3wW1cH4lXQw4nT5Yiu2hmPon/I8dh73tbG7REkFisD40S0EmWPlZF5QPJ3UA7GfaSS86jV6DqopXQSX40ZQcS8PCLZw6m+fGYEkslZNWk+oYpAMMDvdLHRbEArDS4rJig0qyT357Cl/bwy7i6hYubBcFiQDXUrwym401HDTbp296KUH+vbrUvXjxcjEs2gbLdsmTU34oVuM4alzPpN88GFy1hs1AlLlsCbuwwgcl+HRk92VVGaP0a8gVo9w==; bm_ss=ab8e18ef4e; bm_sz=05CAF5E24CBA0BC141ABF7514A287D24~YAAQKBzFF28rxWadAQAAF2ktix90gru8qFTSRDhUjPPH/eYTSgrrixL0VPvVtuCvBQ3H0aPvJMl4BTxt2fIvk7fKmYcMDEXxD7syHEW9UMkChz10KA2DwUUXug6C8xlEZUlpzy1vYenlQq0JgLyuR5zqGYPa4Uj1TAnKKm7elSHk/rQoCp0TUYwFTyX6TBhv7tt7pscwVtWfYpUR+BWPH42YV3WBwLPHPu9ODl5CnhT2ibVEh6n8Xi4mOa4tPnxKwodxc61E/eoNyo2EfqVX2klcUzEVZFqHUNuZDTagGVRjZAunbZLQ5dkNW+p2asIZ2Ws5XVjKbpL0hWwQE6y6KGoiji+drkZ2diknRvXP9yu7ric3W5Ybf2Q=~3553330~4407602'
                }
        while True:
            changed_url = new_url.format(page)
            response = requests.get(changed_url, impersonate="chrome",headers=headers)
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
