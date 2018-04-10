import asyncio
import aiohttp
import concurrent.futures
import requests
import json
from aiohttp import ClientSession
import pandas


def create_csv(urls, case_ids, classes):
    df = pandas.DataFrame({"URL": urls, "Case_ID": case_ids, "Class": classes})
    df.to_csv('data_set_v2.csv', index=False)

TIKA_VISION_API = "http://localhost:8764/inception/v4/classify/image?topn=1&min_confidence=0.03&url="

async def fetch(url, case_id, session):
    try:
        async with session.get(url) as response:
            status = response.status
            print(status, url)
            if status == 200:
                print("Inside fetch")
                json_data =  await response.json()
                return {"url": url, "case_id": case_id, "class_names": json_data.get('classnames')}
        return {"url": "NA", "case_id": "NA", "class_names": "NA"}
    except:
        print(url,case_id)
        return {"url": "NA", "case_id": "NA", "class_names": "NA"}

async def run(data, dframe):
    loop = asyncio.get_event_loop()
    tasks = []
    case_ids = []
    urls = []
    classes = []

    async with ClientSession() as session:
        for client_id, client_details in data.items():
            if 'photos' in client_details:
                for photo_url in client_details['photos']:
                    if '.jpg' in photo_url or '.png' in photo_url or '.jpeg' in photo_url:
                        url = TIKA_VISION_API + photo_url
                        task = asyncio.ensure_future(fetch(url, client_id, session))
                        tasks.append(task)
                        await asyncio.sleep(1)

        responses = await asyncio.gather(*tasks)
        for resp in responses:
            print("The response is ", resp)
            case_ids.append(resp['case_id'])
            urls.append(resp['url'])
            classes.append(resp['class_names'])

        df = pandas.DataFrame({"URL": urls, "Case_ID": case_ids, "Class": classes})
        df.to_csv('data_set_v2.csv', index=False)



data_frame = pd.read_csv('data_set_v2.csv', encoding='ISO-8859-1')

image_cache_map = json.load(open('image_cache_v2.txt'))
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(image_cache_map))
loop.run_until_complete(future)
