import http.client
import json
import math
import datetime
import dateutil.parser
import pandas as pd
import getauth

accessToken = getauth.GetAccessToken()

conn = http.client.HTTPSConnection("api.mindbodyonline.com")

MaxLimit = 200

payload = ""

headers = {
    'Content-Type': "application/json",
    'Api-Key': "a0e9d29c240c45af8873fbd407844e4c",
    'SiteId': "-99",
    'Authorization': accessToken
    }

getsales = "/public/v6/sale/sales"
conn.request("GET", getsales, payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))