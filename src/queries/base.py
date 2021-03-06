import requests
import getauth
import http.client
import json
import math

conn = http.client.HTTPSConnection("api.mindbodyonline.com")

HEADERS = {
    'Api-Key': "a0e9d29c240c45af8873fbd407844e4c",
    'SiteId': "-99",
    'Authorization': getauth.GetAccessToken()
    }

#TODO: implement onepageonly parameter functionality
#TODO: investigate and resolve ? in conn.request when multiple parameters passed
def GetRequest(uri, array_name, onepageonly=False):
    """The point of this function is..."""
    pages_remaining = 9999
    results = []
    offset = 0
    while pages_remaining > 0:
        conn.request("GET", f'{uri}?Limit=200&offset={offset}', headers=HEADERS)
        offset += 200
        res = conn.getresponse()
        data = json.loads(res.read().decode('utf-8'))

        if "PaginationResponse" in data:
            if pages_remaining == 9999:
                pages_remaining = math.ceil(data["PaginationResponse"]["TotalResults"] / 200)
            if array_name in data:
                results.extend(data[array_name])
            pages_remaining -= 1
        else:
            print(data)
            pages_remaining = 0
        
    return results
