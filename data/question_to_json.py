import csv
import json
import argparse
d = []


parser = argparse.ArgumentParser(description="Flash card extraction")
parser.add_argument("-f","--file", help="Enter the input path")


args = parser.parse_args()

file1 = args.file
with open(file1) as csvfile:
	reader = csv.DictReader(csvfile, skipinitialspace=True)
	for row in reader:
		#print(row['question'], row['image'])
		d.append([row["title"].strip(), row['content'].strip()])
		# print(row["title"], row['content'])

#print(d)
#print(json.dumps(d))
f = open('card.json', 'w')
f.write(json.dumps(d))
