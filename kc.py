import requests

url = "https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2&apiVersion=6&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop&categoryId=6857&currentPage=1&sort_algo=ltr_pinning"

payload = {}
headers = {
  'domain': 'NYKAA_FASHION',
  'sec-ch-ua-platform': '"Windows"',
  'x-csrf-token': 'K2zAZtcvYyAywhdt',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
  'sec-ch-ua-mobile': '?0',
  'Cookie': '_abck=80476E1C47F571BA98D8EC2E6A45978F~-1~YAAQmB4SAok6KGmdAQAAQ4uihg+3FkOyBe7cUSWb4KsEPSfKibpy3AAgFAcUFhV/VWvI6A/Mah3XiBM5vI+t3HshKHcPx1pPxp3zrCWtvXgsifYrETBtHSqMJzs5kpyKakosq8O4qZ4GfMMiDwVLf/DF/nnIqYSBRjz3Kbc/2Gpr4qbp99K/8BcMZRE5WSeggAyevMxABH9yfMO9prmVe1n8EAR0jyG98bnB0PMpwLnkuRHyElMJGBbLSEfzN3ydUgNo9pDgNh5vwuovMy9tjIzt0QfyMP8sYcc1GL2Hx06nI06MPtvViqM/FM0RKQiLqHUH7lmDgYoMLV5V/ld523jW914yF3FEe5xx3XBWruhuuvwfLvoRJqeiiqPZkcWPTJH4NG1tyXKpmE8W6TAEcJq7HvLxYvrPOhCYJj8hsBZwZusdjUbDzTjKdQ+T8xSsgRfWzeCJJ3GCJTEVeVCiMZ6U~-1~-1~-1~-1~-1; bm_s=YAAQmB4SAslqKGmdAQAAma2jhgX2op59/79opSUp54V3IwKtA7QyQP/1xdQlw0eTa9sj9C86gRhA3JGDNiB0GnfDp7PS3wlAf9YK4jb6vFgYrfo56hy6NlM+rnNdWF0SuEiYyF0or2o1W6xG6JWpDu2rX/p0XrwJR7h3Ok7E7SLIdeEWN9A9DlzGddyu6fX0zvk4qDjB3BBz0ANfdHdp3UdbGdtBXth67qESGN7uKjqoVCkYAdL2e4UpgVPJlGfyZGamnkKnzS/hiK7aO7LvgTLkRprKRJFcYhnqKcTEbcjeDT3cmMdxW8v7VA2jh5PwDUw1alwSYVmgvNO+DEC1JUuzUDVCQ9MUyfwfSBBSqQl9DUXApSr6woYuAxT3+ipPNdIhFIH4aq7+Vvq5xFKQKHvCg3karNSKI/0CiKaZ163cVSVE+ef2g1Uvk6zr6Gum6+FiROk8bNNMlhwWE7dNiHljsb7qIhs7rhOAO4bSleLDmffXs8ChyMtxS/KDqYZ4J0BTpKLO2kGsYSGgrUua+hzqb1x+rJupQNWV/TQ3o+R5ZsUoWpWihbtVPJ5eIgBeSj+s34AXca4+; bm_so=4EF420EB20E17CA7AAC5A000373485629488D90EDCE988647471EFDF7C61A678~YAAQmB4SAos6KGmdAQAAQ4uihgd3sNcgUjJ28gkPU4/o0Np6rv/U4EwaCiN/cL3nCgxar4H/nQlCZahKugMZEwVkGDHpAC+qBOspsBM8u4Nxb9FrYFDiGz+zZC9/eB4qEDHwB60Gmbz60DUNnipWKXKUzrgKObYmT+5iGGPvn/e5Pfyw2J20Kg7gaulQjk12yr90kgW5mtwEByBkKSjO0/Z4rgHASxtQGSFZpTwSbp/3wW1cH4lXQw4nT5Yiu2hmPon/I8dh73tbG7REkFisD40S0EmWPlZF5QPJ3UA7GfaSS86jV6DqopXQSX40ZQcS8PCLZw6m+fGYEkslZNWk+oYpAMMDvdLHRbEArDS4rJig0qyT357Cl/bwy7i6hYubBcFiQDXUrwym401HDTbp296KUH+vbrUvXjxcjEs2gbLdsmTU34oVuM4alzPpN88GFy1hs1AlLlsCbuwwgcl+HRk92VVGaP0a8gVo9w==; bm_ss=ab8e18ef4e; bm_sz=CA033370AF944C57E3BCEB86C6980D7B~YAAQmB4SAow6KGmdAQAAQ4uihh81CdJyfvlROtil44xzmtEQmCdZfoFz3y7PROY5ZAMt7IMPclxtuRw8uO/m54VQHw7NMMjIhnDDRzyd0y1q9871eqsWN3rnhqxVqgnVUCbjs2Fw06eEeRVReH0x4Qrdko7mcRsi2h8pyc407KPqWW1GeZepnLnquU0kZBWfcVJ9m6hMHcLk/mtTjOjfj3PvE/JzKoIu18N/AVgnOXOmIk6YLKRuR1X0qGR6O+9EghOCFIwDDXaSZsFvYesr+/8glbbkOPgBmR58sow7QDZwUMs3AGsZiXL28CqY119eRcmvYOki/e+jBWCXG9W4XpDkAQskcII+s1MpQhJJHTDjiF4PHtgJlGU=~3158085~3359283'
}



