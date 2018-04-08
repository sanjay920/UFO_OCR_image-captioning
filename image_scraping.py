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
    # Before fetching pagination element emulate page down
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + Keys.ARROW_DOWN)
    pagination = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//ul[@class='pagination ng-scope']/li/a"))
    )
    # pagination = browser.find_elements_by_xpath("//ul[@class='pagination ng-scope']/li/a")
    if len(pagination) == 13:
        # 11th index in the array has '>' (next button)
        return pagination[11]


def get_pg_pointer(browser):
    # Before fetching pagination element emulate page down
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + Keys.ARROW_DOWN)
    pagination = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//ul[@class='pagination ng-scope']/li/a"))
    )
    return pagination


def handle_page(browser):

    try:
        browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + Keys.ARROW_UP)

        ufo_entry = get_ufo_sightings(browser)
        ufo_length = len(ufo_entry)
        ignored_exceptions=(EC.NoSuchElementException,EC.StaleElementReferenceException)

        print "UFO length is ", ufo_length

        action = ActionChains(browser)
        # TODO : Run this for all the 10 ufo entries instead of just the 1st one.
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
    except:
        print "Failed"

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

# function to go to a particular page
def find_page(browser, page_number):
    print "finding page ", page_number
    page_ptr_list = get_pg_pointer(browser)
    not_found = True
    pagination_characters = [item.text for item in page_ptr_list]
    while not_found:
        if str(page_number) in pagination_characters:
            not_found = False
        else:
            nxt_pointer = get_next_page_pointer(browser)
            nxt_pointer.click()
            page_ptr_list = get_pg_pointer(browser)
            pagination_characters = [item.text for item in page_ptr_list]

    element = WebDriverWait(browser, 10, ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='event-table ng-scope']/tbody/tr/td"))
    )
    return browser


# TODO : Need to modify this to make it more generic
def go_to_page(browser):
    pages = range(1, 30)
    for page_num in pages:
        page_ptr_list = get_pg_pointer(browser)
        pagination_characters = [item.text for item in page_ptr_list]
        sleep(5)
        # Check if the page number is visibile in the pagination
        if str(page_num) in pagination_characters:
            index = pagination_characters.index(str(page_num))
            page_ptr_list[index].click()
            browser = handle_page(browser)
            page_ptr_list = get_pg_pointer(browser)
        else:# Keep clicking on the next button till you find the page
            print "for page ", page_num
            find_page(browser, page_num)
            page_ptr_list = get_pg_pointer(browser)
            pagination_characters = [item.text for item in page_ptr_list]
            index = pagination_characters.index(str(page_num))
            page_ptr_list[index].click()
            browser = handle_page(browser)
            print pagination_characters

go_to_page(browser)

# print image_cache
writeToCache(image_cache)

sleep(5)
browser.quit()
