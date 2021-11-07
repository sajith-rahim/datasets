

uri = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/'
files = ['train-v2.0.json','dev-v2.0.json']

import os
import requests

if not os.path.exists('./squad2'):
  os.makedirs('./squad2')

r.content

for f in files:
  res = requests.get(uri+f)
  with open(os.path.join('./squad2',f),'wb') as fp:
    fp.write(res.content)
    #for chunk in r.iter_content(chunk_size=100):
    #  fp.write(chunk)

import json

with open(os.path.join('./squad2',files[0]),'rb') as f:
  train = json.load(f)

train['data'][0]

train_ = []

for group in train['data']:
  for paragraph in group['paragraphs']:
    context = paragraph['context']
    for qa in paragraph['qas']:
      question = qa['question']
      if 'answers' in qa.keys() and len(qa['answers']) > 0:
        answer = qa['answers'][0]['text']
      elif 'plausible_answers' in qa.keys() and len(qa['plausible_answers']) > 0:
        answer = qa['plausible_answers'][0]['text']
      else:
        answer = None
      
      train_.append({'context':context,'question':question,'answer':answer})

import pandas as pd

df = pd.DataFrame(train_)

df.to_csv(os.path.join('./squad2','sqaud2-train.csv'),index=False)