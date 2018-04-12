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

# Keeps track of the urls already processed
PROCESSED_URLS = "processed_url_tika_classes.txt"
# List of all urls that we need to extract
URL_LIST = "new_all_url.txt"

IMG_URL_LIST = "only_images.txt"

# utility function to write json objects to files
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

# This function is used to talk to make requests to the tika vision api and extract the classes
async def fetch(ufo_url, session):
    try:
        url = TIKA_VISION_API + ufo_url
        async with session.get(url) as response:
            status = response.status
            print(status, ufo_url)
            if status == 200:
                print("Inside fetch")
                processed_map['processed'].append(url)
                json_data =  await response.json()
                return {"url": ufo_url,"class_names": json_data.get('classnames')}
        return {"url": "NA", "class_names": "NA"}
    except:
        print("Error processing the url ",url)
        return {"url": "NA", "class_names": "NA"}

# This function loops over all the urls, and records the reults we get from tika vision api
async def run(dframe, processed_url, all_url):
    loop = asyncio.get_event_loop()
    tasks = []
    # If the csv has been generated before, load the urls and classes previously generated and the append the new ones to the list
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
            # only considering images
            if ('.jpg' in ufo_url.lower() or '.png' in ufo_url.lower() or '.jpeg' in ufo_url.lower()):
                # do not process requests which are already processed
                if url not in processed_url:
                    task = asyncio.ensure_future(fetch(ufo_url,session))
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

        # write the generated responses into a csv and also write the processed urls to a file, so we don't have to process them
        df = pd.DataFrame({"URL": urls, "Class": classes})
        df.to_csv('data_set_v2_with_classes.csv', index=False)
        processed_map = {'processed': processed_url}
        writeToCache(processed_map, PROCESSED_URLS)

# IF the output csv is already created, then load the csv as a data frame
try:
    data_frame = pd.read_csv('data_set_v2_with_classes.csv', encoding='ISO-8859-1')
except:
    data_frame = None

all_url_map = json.load(open(URL_LIST))
all_url = all_url_map['all']

processed_map = get_processed_urls()
processed_url = processed_map['processed']

url_to_consider = all_url[2410:2500]

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(data_frame, processed_url, url_to_consider))
loop.run_until_complete(future)
