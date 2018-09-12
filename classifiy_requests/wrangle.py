import pandas as pd

import json

# get rid of the root dict 'objects'
with open('../data/messages.json') as json_data:
    mgs = json.load(json_data)['objects']

# get rid of the root dict 'objects'
with open('../data/requests.json') as json_data:
    reqs = json.load(json_data)['objects']


df = pd.read_json(json.dumps(mgs), orient='records')
print(df)

# only select first message
df = df.groupby('request').first().reset_index()
print(df)

df_req = pd.read_json(json.dumps(reqs), orient='records')
df_req = df_req.rename(index=str, columns={'resource_uri': 'request'})

df = df.set_index('request').join(df_req.set_index('request'), lsuffix='_what', rsuffix='_ever').reset_index()

# only select relevant columns
df = df[['subject', 'content', 'is_foi']]

# we don't need exact duplicates (happens for batch requests)
df = df.drop_duplicates()

print(df['is_foi'].value_counts())

df.to_csv('out.csv')