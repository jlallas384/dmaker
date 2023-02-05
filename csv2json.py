import json

with open('total-account.csv', 'r') as f:
	arr = []
	chk = []
	for line in f:
		email, password = line.rstrip().split(",")
		em = email.split("@")
		arr.append({'username': em[0], 'password': password, 'email': em[1]})


	with open('datass.json','w') as g:
		g.write(json.dumps(arr))