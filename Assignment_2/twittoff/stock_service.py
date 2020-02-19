#Alphavantage.co
#example requests to a basic API (no python package wrapper):

import json
import requests

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=4406SX4YP3MCIZK8"

response = requests.get(request_url)

print(response)
print(response.status_code)

print(type(response.text)) #> string

parsed_response = json.loads(response.text)

print(type(parsed_response)) #> dict
print(parsed_response.keys())

# TODO: work with the parsed response