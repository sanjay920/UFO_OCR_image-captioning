#Extracting URLs

import re
import csv
import requests
import pandas
from requests import async

def extractURLs(fileContent):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fileContent)
    #print urls
    count = 0 
    captions = []
    urls_list = []
    content_type = []
    names = []
    types = []
    for url in urls:
    	#base_url = 'http://localhost:8764/inception/v4/classify/image?topn=1&min_confidence=0.03&url='
    	base_url = 'http://localhost:8764/inception/v4/classify/video?topn=1&min_confidence=0.03&url='
    	url1 = ''.join([base_url, url])
    	url_type = url.rsplit('.', 1)[-1]
    	#print url_type
    	content_type.append(url_type)
    	if(url_type=="mp4" or url_type=="MOV" or url_type=="mov" or url_type=="mpeg4" or url_type=="MP4" or url_type=="MPEG4"):
    		types.append("video")
    	else:
    		types.append("image")

    	#content_type.append(url.rpartition('.')[2])
    	r = requests.get(url1)
    	data = r.json()
    	classname = data.get('classnames')
    	#print(", ".join(classname))
    	print(r)
    	urls_list.append(url1)
    	names.append(", ".join(classname))
    	#captions.append(r.content)
    df = pandas.DataFrame({"URLs":urls_list, "Classnames":names,"Format":content_type, "Type":types}, columns=['URLs','Classnames','Format','Type'])
    df.to_csv("output_file.csv", sep=",", index=False)
    

myFile = open("image_cache_v2.txt")
fileContent = myFile.read()
extractURLs(fileContent)

