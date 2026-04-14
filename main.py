from db import *
from parser_link import *
import time
from curl_cffi import requests
home_url = "https://www.nykaafashion.com/"

if __name__ == "__main__":
    res=requests.get(home_url, impersonate='chrome', timeout=30)
    print(res.status_code)
    if res.status_code!=200:
        print("Error fetching URL")

    root=html.fromstring(res.text)
    script=root.xpath("//script[@id='__PRELOADED_STATE__']/text()")
    json_data=json.loads(script[0])