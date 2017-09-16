import csv
import json
d = []
with open('questions.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		#print(row['question'], row['image'])
		d.append([row["title"].strip(), row['content'].strip()])

#print(d)
#print(json.dumps(d))
f = open('card.json', 'w')
f.write(json.dumps(d))
