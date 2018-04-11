import json
import os


# NOTE : Just a utility script

IMAGE_CACHE_FILE_PAV = "image_cache_v2_prerana.txt"
IMAGE_CACHE_FILE = "image_cache_v2.txt"
IMAGE_URLS = "img_url.txt"
MATTMANN_URL = "ufo_stalker_urls.csv"

# image_map = json.load(open(IMAGE_CACHE_FILE))
#
# new_image_map = {}
#
# unique_urls = set()
# case_id = sorted(image_map.keys())
# print case_id[0], case_id[len(case_id)-1]
# num_photo = 0
#
# for key_id, val in image_map.items():
#     num_photo += len(val['photos'])
#     # for photo in val['photos']:
#     #     with open(IMAGE_URLS, 'a+') as f:
#     #         f.write(photo + '\n')
#     for photo_url in val['photos']:
#         if photo_url not in unique_urls:
#             unique_urls.add(photo_url)
#             # with open(IMAGE_URLS, 'a+') as f:
#             #     f.write(photo_url + '\n')

with open(MATTMANN_URL) as f:
    content = f.readlines()

content = [x.strip() for x in content]

def writeToCache(data, file_name):
    with open(file_name, 'w') as file:
        file.write(json.dumps(data))

writeToCache({"all": list(content)}, "new_all_url.txt")

# print len(case_id)
# print num_photo
# print "unique_urls",len(unique_urls)
