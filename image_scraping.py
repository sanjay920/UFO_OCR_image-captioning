# TODO : 1 - Get URL from table for each sighting and open a new table
# 2 - From each induvidual url fetch the images(if any) for this, use the XPATh listed in the code
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep

processed_req = set()

def get_images(browser):
    images = browser.find_elements_by_xpath("//table/tbody/tr/td/a[@target='_blank']")
    print "This page has ",len(images)
    for img in images:
        print img.get_attribute('href')

def get_ufo_sightings(browser):
    ufo_entry = browser.find_elements_by_xpath("//table[@class='event-table ng-scope']/tbody")
    return ufo_entry

browser = webdriver.Chrome('browser_drivers/chromedriver')
browser.get('http://www.ufostalker.com/tag/photo')
ufo_entry = browser.find_elements_by_xpath("//table[@class='event-table ng-scope']/tbody")

ufo_length = len(ufo_entry)

# 1) get a list of sightings,
# 2) click on each entry, wait till it opens the second page and extract the images
# 3) Go back to the previous page
# 4) Get a list of ufo sightings (We do this again to avoid stale state, so we recompute and continue from where we left off)
for i in range(ufo_length):
    print i, len(ufo_entry)
    ufo_entry[i].click()
    sleep(2)
    get_images(browser)
    sleep(2)
    browser.back()
    sleep(2)
    ufo_entry = get_ufo_sightings(browser)

browser.back()

print len(ufo_entry)

sleep(5)
browser.quit()
