import json
import os


# NOTE : Just a utility script

IMAGE_CACHE_FILE_PAV = "image_cache_v2_prerana.txt"
IMAGE_CACHE_FILE = "image_cache_v2.txt"
IMAGE_URLS = "img_url.txt"

image_map = json.load(open(IMAGE_CACHE_FILE))
image_map_pav = json.load(open(IMAGE_CACHE_FILE_PAV))

new_image_map = {}

unique_urls = set()
case_id = sorted(image_map.keys())
print case_id[0], case_id[len(case_id)-1]
num_photo = 0

for key_id, val in image_map.items():
    new_image_map[key_id] = val

for key_id, val in image_map_pav.items():
    if key_id not in new_image_map:
        new_image_map[key_id] = val
# if 72296 in case_id:
# print image_map['72296']

for key_id, val in new_image_map.items():
    num_photo += len(val['photos'])
    # for photo in val['photos']:
    #     with open(IMAGE_URLS, 'a+') as f:
    #         f.write(photo + '\n')
    for photo_url in val['photos']:
        if photo_url not in unique_urls:
            unique_urls.add(photo_url)
            # with open(IMAGE_URLS, 'a+') as f:
            #     f.write(photo_url + '\n')

def writeToCache(data):
    with open(IMAGE_CACHE_FILE, 'w') as file:
        file.write(json.dumps(data))

writeToCache(new_image_map)

print len(case_id)
print num_photo
print "unique_urls",len(unique_urls)
