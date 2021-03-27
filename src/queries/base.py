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

def GetRequest(uri, array_name, onepageonly=False):
    """The point of this function is..."""
    pages_remaining = 9999
    results = []
    offset = 0
    
    if onepageonly:
        pages_remaining = 1

    #Backwards compatibility for '/public/v6' prefix and whether intial '/' is used:
    if uri[0:11] == '/public/v6/':
        bridge1 = ''
    elif uri[0:10] == 'public/v6/':
        bridge1 = '/'
    elif uri[0] == '/':
        bridge1 = '/public/v6'
    else:
        bridge1 = '/public/v6/'
    
    #If '?' Parameter is already used in uri, add '&' to request string, otherwise add the '?'
    if '?' in uri:
        bridge2 = '&'
    else:
        bridge2 = '?'
    
    while pages_remaining > 0:
        conn.request("GET", f'{bridge1}{uri}{bridge2}Limit=200&offset={offset}', headers=HEADERS)
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

if __name__ == "__main__":
    clients = GetRequest("/client/clients", "Clients", True)
    print(clients[15]["FirstName"])

    clients = GetRequest("client/clients", "Clients", True)
    print(clients[15]["FirstName"])

    clients = GetRequest("/public/v6/client/clients", "Clients", True)
    print(clients[15]["FirstName"])
    
    clients = GetRequest("public/v6/client/clients", "Clients", True)
    print(clients[15]["FirstName"])