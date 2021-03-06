import http.client
import json

conn = http.client.HTTPSConnection("api.mindbodyonline.com")

headers = {
    'Content-Type': "application/json",
    'Api-Key': "a0e9d29c240c45af8873fbd407844e4c",
    'SiteId': "-99",
    'User-Agent': "DBA"
    }

def GetAccessToken():
    #TO GET AN AUTHORIZATION NUMBER (like: 3f8eb187d220492fbaf456a51c6962bee3a62e86070b4a5194344f88ee06fa3d)
    payload = "{\r\n\t\"Username\": \"Siteowner\",\r\n\t\"Password\": \"apitest1234\"\r\n}"
    conn.request("POST", "/public/v6/usertoken/issue", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsondata = json.loads(data.decode("utf-8"))
    return jsondata["AccessToken"]