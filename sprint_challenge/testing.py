import openaq
import requests

api = openaq.OpenAQ()

#status, body = api.measurements(city='Los Angeles', parameter='pm25')

r = requests.get('https://api.openaq.org/v1/measurements', auth=('user', 'pass'))
print(r.status_code)