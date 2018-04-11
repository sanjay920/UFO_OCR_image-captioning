#!/usr/bin/env python
# -*- coding: utf-8 -*-

# REFERENCE : https://gist.github.com/chrismattmann/cd8f853bdc6e287bddb83fea0f515dfd

import requests
import json
from time import sleep

def writeLinks(lks):
    with open('ufo_stalker_urls.csv', 'a') as usu:
        for l in lks:
            usu.write(l+"\n")


url = "http://ufostalker.com:8080/eventsByTag"
totalPages = 0
totalElements = 0

params = dict(
   page='1',
   size='25',
   tag='photo'
)

resp = requests.get(url=url, params=params)
data = resp.json()

totalPages = data["totalPages"]
totalElements = data["totalElements"]

print "Total Pages: ["+str(totalPages)+"] Total Elements: ["+str(totalElements)+"]"
print "Processing page 1 of "+str(totalPages)

for d in data["content"]:
    if d["urls"] != None and len(d["urls"]) > 0:
        writeLinks(d["urls"])

for i in range(2, totalPages):
    print "Processing page "+str(i)+" of "+str(totalPages)

    params = dict(
      page=str(i),
      size='25',
      tag='photo'
    )

    resp = requests.get(url=url, params=params)
    data = resp.json()

    for d in data["content"]:
        if d["urls"] != None and len(d["urls"]) > 0:
            writeLinks(d["urls"])

    sleep(2)
