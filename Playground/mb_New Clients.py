import http.client
import json
import math
import datetime
import dateutil.parser
import pandas as pd

MaxLimit = 200

conn = http.client.HTTPSConnection("api.mindbodyonline.com")

headers = {
    'Api-Key': "a0e9d29c240c45af8873fbd407844e4c",
    'SiteId': "-99",
    'Authorization': "fd3088837630414eb0e855739ceaf7bdc385ce092a004c26a699850e8b8c1acc"
    }
getclients = "/public/v6/client/clients?limit=" + str(MaxLimit)
conn.request("GET", getclients, headers=headers)

res = conn.getresponse()
data = res.read()

jsondata = json.loads(data.decode("utf-8"))

Pagdata = jsondata["PaginationResponse"]

Clients = jsondata["Clients"]

print(f'jsondata: {type(jsondata)} Clients: {type(Clients[0])} Data: {type(data)}')


#print(df.head())

TotalClients = Pagdata["TotalResults"]

Requests = math.ceil(TotalClients / MaxLimit)

# print(Clients[0]["Id"])
# print(Clients[1]["Id"])

#Requests = 3 

for x in range(1, Requests):
    conn.request("GET", getclients +"&Offset=" +str(x * 200), headers=headers)
    res = conn.getresponse()
    data = res.read()
    jsondata = json.loads(data.decode("utf-8"))
    MoreClients = jsondata["Clients"]
    Clients.extend(MoreClients)

#print(len(Clients))

DateChange = datetime.datetime.now() - datetime.timedelta(90)

TotalNewClients = 0

NewClients = []

for Client in Clients:
    # try:
    #     CreationDate = datetime.datetime.strptime(Client["CreationDate"],'%Y-%m-%dT%H:%M:%S')
    # except:
    #     CreationDate = datetime.datetime.strptime(Client["CreationDate"],'%Y-%m-%dT%H:%M:%S.%f')      
    CreationDate = dateutil.parser.parse(Client["CreationDate"])
    if (CreationDate >= DateChange and not Client["IsProspect"] and not Client["IsCompany"]):
        TotalNewClients = TotalNewClients + 1  
        NewClients.append(Client)
    #print(f'{Client["Id"]:>10}    {str(CreationDate)[:19]}')
    #print(f'{Client["Id"]:>10}{"":^5}{str(CreationDate)}')
    
print(len(NewClients))

# df= pd.DataFrame(NewClients)
# df.to_csv('NewClients.csv')
# print(df.info())

# print(TotalNewClients)