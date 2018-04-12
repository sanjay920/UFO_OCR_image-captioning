#!/usr/bin/env python
# -*- coding: utf-8 -*-

# REFERENCE : https://gist.github.com/chrismattmann/cd8f853bdc6e287bddb83fea0f515dfd

import requests
import json
from time import sleep

def writeLinks(lks, summary, latitude, longitude):
    with open('ufo_stalker_urls_v3.csv', 'a') as usu:
        for l in lks:
            usu.write(l+ "," + summary + "," + latitude + "," + longitude + "\n")

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

url = "http://ufostalker.com:8080/eventsByTag"
totalPages = 0
totalElements = 0

with open('ufo_stalker_urls_v3.csv', 'a') as usu:
    usu.write("URL,Summary,Latitude,Longitude" + "\n")

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
    summary = ""
    latitude = "0"
    longitude = "0"
    if d["latitude"] != None:
        latitude = str(d["latitude"])
    if d["longitude"] != None:
        longitude = str(d["longitude"])
    if d["summary"] != None and is_ascii(d["summary"]):
        summary = d["summary"]
        # print summary
    if d["urls"] != None and len(d["urls"]) > 0:
        writeLinks(d["urls"], summary, latitude, longitude)

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
        summary = ""
        if d["summary"] != None and is_ascii(d["summary"]):
            summary = d["summary"]
        if d["urls"] != None and len(d["urls"]) > 0:
            writeLinks(d["urls"], summary, latitude, longitude)

    sleep(2)
