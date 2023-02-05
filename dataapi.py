from requests import *
import json
url = "https://my.api.mockaroo.com/finale.json?key=93d0f180"

arr = []

for i in range(5):
	arr = []
	for j in range(10):
		dat = get(url).json()
		for x in dat:
			arr.append(x)
	with open(f'data{i}.json','w') as f:
		f.write(json.dumps(arr))
