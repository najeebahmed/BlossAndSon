#https://developers.google.com/docs/api/quickstart/python

from __future__ import print_function
import requests
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

import http.client

conn = http.client.HTTPSConnection("api.mindbodyonline.com")

HEADERS = {
    'Content-Type': "application/json",
    'Api-Key': "a0e9d29c240c45af8873fbd407844e4c",
    'SiteId': "-99",
    'Authorization': "8daada4f04144094a66fb41a681eb060fc51cf360c654dbea7acb7bf2918501a",
    'User-Agent': "my-app"
    }

def GetRequest(uri, array_name):
    pagesize = 1
    results = []
    offset = 0
    while pagesize > 0:
        conn.request("GET", f'{uri}?Limit=200&offset={offset}', headers=HEADERS)
        offset = offset + 200
        res = conn.getresponse()
        data = json.loads(res.read())
    if "PaginationResponse" in data:
        pagesize = data["PaginationResponse"]["PageSize"]
    else:
        print(data)
        pagesize = 0
    if (array_name in data):
        results.extend(data[array_name])

    return results

# conn.request("GET", "/public/v6/client/clients", headers=HEADERS)
# res = conn.getresponse()
# print(res.code)
# data = res.read()

clients = GetRequest("/public/v6/client/clients", "Clients")
#clients = data["Clients"]
#clients = json.loads(data.decode("utf-8"))["Clients"]

print (f'{"ID":<15}{"Status":<15}{"FirstName":<15}{"LastName":<15}{"Visits":>5}')

DateChange = datetime.datetime.now() - datetime.timedelta(90)

StartDate = datetime.datetime.strftime(DateChange, '%Y-%m-%dT%H:%M:%S')

count = 0
for client in clients:
    if (client["Status"] == "Active"):
        visits = GetRequest(f'/public/v6/client/clientvisits?clientid={client["UniqueId"]}&StartDate={StartDate}', "Visits")
        count += len(visits)

print (count)

# for client in clients:
#     if (client["Status"] == "Active"):
#         visits = GetRequest(f'/public/v6/client/clientvisits?clientid={client["UniqueId"]}&StartDate={CreationDate}', "Visits")
#         count = len(visits)
#     else:
#         count = ''
#     print(f'{client["UniqueId"]:<15}{client["Status"]:<15}{client["FirstName"]:<15}{client["LastName"]:<15}{count:>5}')

#print (values)

exit()

# #amenities = json.loads(data.decode("utf-8"))["Locations"][0]["Amenities"]
# #print (amenities)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1AqOQUf42lbBSgAUsWm7aQTqdmD3kJk_pFssRyqDNFRg'
SAMPLE_RANGE_NAME = 'Sheet1!A1:B201'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # values = [["ID", "Name"]]
    # for amenity in amenities:
    #     # response = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(id))
    #     value = []
    #     # value.append(response.json()["forms"][0]["name"])
    #     value.append(amenity["Id"])
    #     value.append(amenity["Name"])
    #     values.append(value)

    print (values)

    body = {
        "range": "Sheet1!A1:B201",
        "majorDimension": "ROWS",
        "values": values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    main()

# curl -X POST https://api.mindbodyonline.com/public/v6/usertoken/issue -H 'Content-Type: application/json' -H 'Api-Key: a0e9d29c240c45af8873fbd407844e4c' -H 'SiteId: -99' -d '{"Username": "Siteowner","Password": "apitest1234"}'