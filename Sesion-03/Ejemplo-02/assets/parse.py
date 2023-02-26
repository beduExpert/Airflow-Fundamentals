import json
from datetime import datetime, timedelta
from pprint import pprint


with open('response.json','r') as f:
    data = json.load(f)

hoy = datetime.today()
futuro = hoy + timedelta(days=2)
# print(hoy)
# print(futuro)
hoy_iso8601 = hoy.strftime("%Y-%m-%dT%H:00")
futuro_iso8601 = futuro.strftime("%Y-%m-%dT%H:00")
temperatura = dict(zip(data['hourly']['time'], data['hourly']['temperature_2m']))
pprint({k:v for k,v in temperatura.items() if k in [hoy_iso8601, futuro_iso8601]})
