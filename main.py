from urllib import response
import requests
import json
import datetime



class N2YO:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.n2yo.com/rest/v1/satellite/"
    
    def get_radiopass(self, id, lat, long, alt, min_elevation, days):
        req = "https://api.n2yo.com/rest/v1/satellite/radiopasses/{}/{}/{}/{}/{}/{}&apiKey={}".format(id, lat, long, alt, days, min_elevation, self.api_key)
        response = requests.get(req)
        return response


def parsePasses(data):
    count = data["info"]["passescount"]
    name = data["info"]["satname"]
    try:
        passes = data["passes"]
    except KeyError:
        passes = 0
    toRet = ""
    toRet += "Satellite: {}\n".format(name)
    if passes == 0:
        toRet += "No passes found\n"
    else:
        for i in range(int(count)):
            maxEl = passes[i]["maxEl"]
            startUTC = datetime.datetime.fromtimestamp(int(passes[i]["startUTC"]))
            endUTC = datetime.datetime.fromtimestamp(int(passes[i]["endUTC"]))
            toRet += "============================\n"
            toRet += "Pass {}: {} - {}\n".format(i, startUTC, endUTC)
            toRet += "Max Elevation: {}\n".format(maxEl)
            toRet += "Azimuth: {}".format(passes[i]["maxAz"])
            if (i != int(count) - 1):
                toRet += "\n"
            
    return toRet

with open("saves.json") as f:
        data = json.load(f)
sat_list = data["sat_list"]


if data["isFirstTime"] == 1:
    lat = input("Enter your latitude: ")
    long = input("Enter your longitude: ")
    data["lat"] = lat
    data["long"] = long
    data["isFirstTime"] = 0
    with open("saves.json", "w") as f:
        json.dump(data, f, indent=4)
else:
    lat = data["lat"]
    long = data["long"]
alt = 0
min_elevation = input("Enter the minimum elevation: ")
days = input("Enter the number of days to search: ")

print("Making request...")

client = N2YO("YOUR_API_KEY")
for i in range(len(sat_list)):
    response = client.get_radiopass(sat_list[i], lat, long, alt, min_elevation, days)
    data = response.json()
    print(parsePasses(data))
    print("============================================================\n\n")