import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import collections
import json

BASE_URL = "http://www.ufostalker.com/event/"

# Enter the range
START_ID = 81000
END_ID = 90000
IMAGE_CACHE_FILE = "image_cache.txt"

image_map = dict()
image_map = json.load(open(IMAGE_CACHE_FILE))

def writeToCache(data):
    with open(IMAGE_CACHE_FILE, 'w') as file:
        file.write(json.dumps(data))

def get_images(browser, case_id):
    global image_map

    try:
        case_element = WebDriverWait(browser, 5).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//table/tbody/tr[@ng-hide='!event.id']/td"))
        )
        images = WebDriverWait(browser, 5).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//table/tbody/tr/td/a[@target='_blank']"))
        )
        print "This page has ",len(images)
        image_map[case_id] = [img.get_attribute('href') for img in images]
    except:
        # image_cache[case_number] = [""]
        print "No image found"
        image_map[case_id] = ""

browser = webdriver.Firefox()

def process(browser):
    for case_id in range(START_ID, END_ID):
        if case_id not in image_map:
            browser.get(BASE_URL+str(case_id))
            browser.maximize_window()
            get_images(browser, case_id)
            sleep(5)

process(browser)
writeToCache(image_map)

# print sorted(image_map.keys())

browser.quit()
