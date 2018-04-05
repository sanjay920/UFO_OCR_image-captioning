# TODO : 1 - Get URL from table for each sighting and open a new table
# 2 - From each induvidual url fetch the images(if any) for this, use the XPATh listed in the code
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

# Constants
IMAGE_CACHE_FILE = "image_cache.txt"

image_cache = dict()

def writeToCache(data):
    with open(IMAGE_CACHE_FILE, 'w') as file:
        file.write(json.dumps(data))

def get_images(browser):
    global image_cache

    try:
        case_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//table/tbody/tr[@ng-hide='!event.id']/td"))
        )
        case_number = case_element[1].text

        images = WebDriverWait(browser, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//table/tbody/tr/td/a[@target='_blank']"))
        )
        print "This page has ",len(images)
        image_cache[case_number] = [img.get_attribute('href') for img in images]
    except:
        # image_cache[case_number] = [""]
        print "No image found"


def get_ufo_sightings(browser):
    element = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='event-table ng-scope']/tbody"))
    )
    return element


def get_next_page_pointer(browser):
    pagination = browser.find_elements_by_xpath("//ul[@class='pagination ng-scope']/li/a")
    if len(pagination) == 13:
        return pagination[11]


def get_pg_pointer(browser):
    return browser.find_elements_by_xpath("//ul[@class='pagination ng-scope']/li/a")


def handle_page(browser):

    ufo_entry = get_ufo_sightings(browser)
    ufo_length = len(ufo_entry)
    ignored_exceptions=(EC.NoSuchElementException,EC.StaleElementReferenceException)

    print "UFO length is ", ufo_length

    action = ActionChains(browser)
    action.move_to_element(ufo_entry[0]).click(ufo_entry[0]).perform()

    # look for the visibility of this element before extracting the images.
    next_page_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//div[@class='sighting-questions']"))
    )

    # extract the images from the page and go back to the main page
    get_images(browser)
    body = browser.find_element_by_tag_name('body')
    browser.get("http://www.ufostalker.com/tag/photo")

    print "Back to main page"
    element = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='event-table ng-scope']/tbody/tr/td"))
    )

    # return the new instance of the browser as the old one is stale
    return browser

# Initializing webdriver with firefox
browser = webdriver.Firefox()
browser.get('http://www.ufostalker.com/tag/photo')
browser.maximize_window()
action = ActionChains(browser)

ignored_exceptions=(EC.NoSuchElementException,EC.StaleElementReferenceException)
element1 = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
    EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='event-table ng-scope']/tbody/tr/td"))
)


nxt_page_pointer = get_next_page_pointer(browser)
nxt_page_pointer.click()
#
element1 = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
    EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='event-table ng-scope']/tbody/tr/td"))
)

def go_to_page(browser):
    pages = range(1, 30)
    for page_num in pages:
        page_ptr_list = get_pg_pointer(browser)
        for ptr_index in range(len(page_ptr_list)):
            if str(page_num) == page_ptr_list[ptr_index].text:
                page_ptr_list[ptr_index].click()
                browser = handle_page(browser)
                page_ptr_list = get_pg_pointer(browser)



go_to_page(browser)

# handle_page(browser, 0)
# browser.back()

print image_cache
writeToCache(image_cache)

sleep(5)
browser.quit()
