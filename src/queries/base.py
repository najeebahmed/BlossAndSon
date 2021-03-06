import requests
import getauth
import http.client
import json

conn = http.client.HTTPSConnection("api.mindbodyonline.com")

HEADERS = {
    'Api-Key': "a0e9d29c240c45af8873fbd407844e4c",
    'SiteId': "-99",
    'Authorization': getauth.GetAccessToken()
    }

def GetRequest(uri, array_name):
    """The point of this function is..."""
    pagesize = 1
    results = []
    offset = 0
    while pagesize > 0:
        conn.request("GET", f'{uri}?Limit=200&offset={offset}', headers=HEADERS)
        offset = offset + 200
        res = conn.getresponse()
        data = json.loads(res.read().decode('utf-8'))

    if "PaginationResponse" in data:
        pagesize = data["PaginationResponse"]["PageSize"]
    else:
        print(data)
        pagesize = 0
    if (array_name in data):
        results.extend(data[array_name])

    return results
