import json
import requests
import os.path

with open("{}/headers.json".format(os.path.dirname(__file__)), 'r') as h:
    headers = json.loads(h.read())



def nearby(loc):

    url = "https://citymapper.com/api/2/nearby?"
    kinds = "kinds=railstation&"
    location = "location=" + loc
    other = "&limit=5&region_id=es-madrid"
    data = kinds + location + other

    r = requests.get(url+data, headers=headers)
    j = json.loads(r.text)
    x = j['elements']
    response = {'railstations': []}
    for i in range(x.__len__()):
        data = {}
        try:
            data['name'] = x[i]['name']
            data['alias'] = x[i]['alias']
            data['id'] = x[i]['id']
        except:
            pass
        response['railstations'].append(data)

    return response


def get_departures(stop_id):
    ids = str(stop_id)
    ids= 'MadridStation_NuevosMinisterios'
    url = 'https://citymapper.com/api/1/raildepartures?ids='

    r = requests.get(url + ids, headers=headers)
    j = json.loads(r.text)
    x = j['stations'][0]['departures']
    response = {'departures': []}
    for i in range(x.__len__()):
        data = {}
        try:
            data['route_id'] = x[i]['route_id'].split('Cercanias')[-1]
            data['destination'] = x[i]['pattern_destination']
            if x[i]['is_live']:
                data['is_live'] = True
                data['arrival'] = x[i]['time_seconds']
            else:
                data['is_live'] = False
                data['arrival'] = x[i]['departure_dt']
        except:
            pass
        try:
            data['platform_number'] = x[i]['platform_number']
        except:
            pass
        response['departures'].append(data)

    return response
