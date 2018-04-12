import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from time import sleep
import collections
import json


BASE_URL = "http://www.ufostalker.com/event/"
PATH_TO_CHROME_PLUGIN = "/Users/sachingb/Development/USC/CSCI_599/Assignments/HW2/UFO_ocr_image-captioning_enrichment/chrome_extensions/"
# Enter the range


START_ID = 80900
END_ID = 81000
IMAGE_CACHE_FILE = "image_cache_v2.txt"

image_map = dict()
image_map = json.load(open(IMAGE_CACHE_FILE))

def writeToCache(data):
    with open(IMAGE_CACHE_FILE, 'w') as file:
        file.write(json.dumps(data))

def get_images(browser, case_id):
    global image_map
    print "Case id ", case_id
    try:

        images = WebDriverWait(browser, 3).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//table/tbody/tr/td/a[@target='_blank']"))
        )

        latitude = WebDriverWait(browser, 2).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//tr[@ng-hide='!event.latitude']/td[@class='ng-binding']"))
        )

        longitude = WebDriverWait(browser, 2).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//tr[@ng-hide='!event.longitude']/td[@class='ng-binding']"))
        )

        date_sighted_at = WebDriverWait(browser, 2).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//tr[@ng-hide='!event.occurred']/td[@class='ng-binding']/a/b"))
        )

        date_reported_at = WebDriverWait(browser, 2).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//tr[@ng-hide='!event.submitted']/td[@class='ng-binding']/a/b"))
        )

        summary = WebDriverWait(browser, 2).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//p[@id='summary']"))
        )

        print "This page has ",len(images)
        image_map[case_id] = {
            'lat': latitude[0].text,
            'lon': longitude[0].text,
            'sighted_at': date_sighted_at[0].text,
            'reported_at': date_reported_at[0].text,
            'summary': summary[0].text,
            'photos': [img.get_attribute('href') for img in images]
        }
    except:
        print "No image found"

chrome_options = Options()
chrome_options.add_extension(PATH_TO_CHROME_PLUGIN+'hola.crx') #anonymox
chrome_options.add_extension(PATH_TO_CHROME_PLUGIN+'adblock.crx') #adblock
browser = webdriver.Chrome(executable_path='browser_drivers/chromedriver', chrome_options=chrome_options)

def process(browser):
    global image_map
    try:
        for case_id in range(START_ID, END_ID):
            if case_id not in image_map:
                browser.get(BASE_URL+str(case_id))
                browser.maximize_window()
                get_images(browser, case_id)
                sleep(3)
    except:
        print "Error occurred"
    finally:
        writeToCache(image_map)

process(browser)
writeToCache(image_map)
browser.quit()
