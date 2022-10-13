import pandas as pd
import json
#create a script to load data from a csv and convert it to a list of dictionaries

#load data from csv
df = pd.read_csv('coords_route (1).csv')
df = df.drop(columns=['Unnamed: 0'])
#convert to list of dictionaries
data = df.to_dict('records')

print(data)
# save to json
with open('data.json', 'w') as f:
    json.dump(data, f)

#load data from json
with open('data.json', 'r') as f:
    data = json.load(f)
