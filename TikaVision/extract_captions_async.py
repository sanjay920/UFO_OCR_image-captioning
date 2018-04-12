import asyncio
import aiohttp
import concurrent.futures
import requests
import json
from aiohttp import ClientSession
import pandas as pd

TIKA_CAPTION_API = "http://localhost:8764/inception/v3/caption/image?url="
PROCESSED_URLS = "processed_url.txt"
URL_LIST = "new_all_url.txt"
all_url_map = {"all":[]}
processed_map = {"processed": []}

def writeToCache(data, file_name):
    with open(file_name, 'w') as file:
        file.write(json.dumps(data))

def get_all_urls():
    try:
        all_url_map = json.load(open(URL_LIST))
    except:
        all_url_map = {"all": []}

    return all_url_map

def get_processed_urls():
    try:
        processed_map = json.load(open(PROCESSED_URLS))
    except:
        processed_map = {"processed": []}

    return processed_map


async def fetch(ufo_url,session):
    try:
        url = TIKA_CAPTION_API + ufo_url
        if len(url) == 0:
            return {"description": "NA"}
        async with session.get(url) as response:
            status = response.status
            print(status, ufo_url)
            if status == 200:
                print("Inside fetch")
                json_data =  await response.json()
                processed_map['processed'].append(url)
                return {"url":ufo_url,"description": json_data['captions'][0]['sentence']}
        return {"url":ufo_url,"description": "NA"}
    except:
        print("Exception occurred ",url)
        return {"url":ufo_url,"description": "NA"}


async def run(df, processed_url, all_url):
    loop = asyncio.get_event_loop()
    urls = df['URL'].tolist()
    captions = df['Captions'].tolist()

    tasks = []
    async with ClientSession() as session:
        for ufo_url in all_url:
            url = TIKA_CAPTION_API + str(ufo_url)
            if ('.jpg' in ufo_url.lower() or '.png' in ufo_url.lower() or '.jpeg' in ufo_url.lower()):
                if url not in processed_url:
                    task = asyncio.ensure_future(fetch(ufo_url,session))
                    tasks.append(task)
                    await asyncio.sleep(1)
                else:
                    print("URL is already processed, ",ufo_url)
            else:
                print("Cannot process the url ", ufo_url)

        responses = await asyncio.gather(*tasks)
        print("Response is ",responses)

        for resp in responses:
            if resp['description'] != "NA":
                urls.append(resp['url'])
                captions.append(resp['description'])
                processed_url.append(resp['url'])

        df = pd.DataFrame({"URL": urls, "Captions": captions})
        df.to_csv('data_set_v2_with_caption.csv', index=False)
        processed_map = {'processed': processed_url}
        writeToCache(processed_map, PROCESSED_URLS)


all_url_map = json.load(open(URL_LIST))
all_url = all_url_map['all']
captions_data_frame = pd.read_csv('data_set_v2_with_caption.csv', encoding='ISO-8859-1')

processed_map = get_processed_urls()
# writeToCache(processed_map, PROCESSED_URLS)
processed_url = processed_map['processed']
print(len(all_url))
url_to_consider = all_url[2200:2300]

# print(all_url)
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(captions_data_frame ,processed_url, url_to_consider))
loop.run_until_complete(future)
