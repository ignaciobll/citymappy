import json
import requests
import os.path

stops = {}

with open("{}/stops.json".format(os.path.dirname(__file__)), 'r+') as f:
    print("Abierto fichero con la paradas")
    stops = json.loads(f.read())

with open("{}/headers.json".format(os.path.dirname(__file__)), 'r') as h:
    headers = json.loads(h.read())


def get_stop_time(idStop):

    url = 'https://citymapper.com/api/1/departures?headways=1&ids='

    ids = stops[str(idStop)]['id']
    r = requests.get(url + ids, headers=headers)
    j = json.loads(r.text)
    x = j['stops'][0]['services']
    response = {'stops': []}
    for i in range(x.__len__()):
        data = {}
        try:
            data['name'] = x[i]['route_id'].split('Bus')[-1]
        except:
            data['name'] = x[i]['route_id']
            
        data['headsign'] = x[i]['headsign']
        try:
            data['arrival'] = x[i]['live_departures_seconds'][0]
        except:
            data['arrival'] = str(x[i]['next_departures'][0])
        response['stops'].append(data)

    return response
