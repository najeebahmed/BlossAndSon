from base import GetRequest
import datetime

count = 0
clients = GetRequest("/public/v6/client/clients", "Clients", onepageonly=True)
DateChange = datetime.datetime.now() - datetime.timedelta(90)
StartDate = datetime.datetime.strftime(DateChange, '%Y-%m-%dT%H:%M:%S')

visits = {}
for client in clients:
    if (client["Status"] == "Active"):
        result = GetRequest(f'/public/v6/client/clientvisits?clientid={client["UniqueId"]}&StartDate={StartDate}', "Visits")
        visits[client["UniqueId"]] = len(result)

print(visits)