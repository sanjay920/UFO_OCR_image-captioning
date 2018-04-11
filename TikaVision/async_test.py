import asyncio
import aiohttp
import concurrent.futures
import requests
import json
from aiohttp import ClientSession
import pandas as pd


# def create_csv(urls, case_ids, classes):
#     df = pandas.DataFrame({"URL": urls, "Case_ID": case_ids, "Class": classes})
#     df.to_csv('data_set_v2.csv', index=False)

TIKA_VISION_API = "http://localhost:8764/inception/v4/classify/image?topn=1&min_confidence=0.03&url="

PROCESSED_URLS = "processed_url_tika_classes.txt"
URL_LIST = "new_all_url.txt"
IMG_URL_LIST = "only_images.txt"

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


async def fetch(url, session):
    try:
        async with session.get(url) as response:
            status = response.status
            print(status, url)
            if status == 200:
                print("Inside fetch")
                processed_map['processed'].append(url)
                json_data =  await response.json()
                return {"url": url,"class_names": json_data.get('classnames')}
        return {"url": "NA", "class_names": "NA"}
    except:
        print("Error processing the url ",url)
        return {"url": "NA", "class_names": "NA"}

async def run(dframe, processed_url, all_url):
    loop = asyncio.get_event_loop()
    tasks = []
    if dframe is None:
        urls = []
        classes = []
    else:
        urls = dframe['URL'].tolist()
        classes = dframe['Class'].tolist()

    invalid_url_count = 0

    async with ClientSession() as session:
        for ufo_url in all_url:
            url = TIKA_VISION_API + ufo_url
            if ('.jpg' in ufo_url.lower() or '.png' in ufo_url.lower() or '.jpeg' in ufo_url.lower()):
                if url not in processed_url:
                    task = asyncio.ensure_future(fetch(url,session))
                    tasks.append(task)
                    await asyncio.sleep(1)
                else:
                    print("URL is already processed, ",ufo_url)
            else:
                print("Cannot process the url ", ufo_url)

        responses = await asyncio.gather(*tasks)
        for resp in responses:
            if resp['class_names'] != "NA":
                urls.append(resp['url'])
                classes.append(resp['class_names'])

        df = pd.DataFrame({"URL": urls, "Class": classes})
        df.to_csv('data_set_v2_with_classes.csv', index=False)
        processed_map = {'processed': processed_url}
        writeToCache(processed_map, PROCESSED_URLS)



# data_frame = pd.read_csv('data_set_v2.csv', encoding='ISO-8859-1')
# data_frame['Case_ID'] = data_frame['Case_ID'].fillna(0)
# data_frame[['Case_ID']] = data_frame[['Case_ID']].astype(int)

try:
    data_frame = pd.read_csv('data_set_v2_with_classes.csv', encoding='ISO-8859-1')
except:
    data_frame = None

all_url_map = json.load(open(URL_LIST))
all_url = all_url_map['all']

processed_map = get_processed_urls()
processed_url = processed_map['processed']

url_to_consider = all_url[1300:1400]

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(data_frame, processed_url, url_to_consider))
loop.run_until_complete(future)
