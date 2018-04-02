# TODO : 1 - Get URL from table for each sighting and open a new table
# 2 - From each induvidual url fetch the images(if any) for this, use the XPATh listed in the code
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep


def get_images(browser):
    images = browser.find_elements_by_xpath("//table/tbody/tr/td/a[@target='_blank']")
    print "This page has ",len(images)
    for img in images:
        print img.get_attribute('href')


browser = webdriver.Chrome('browser_drivers/chromedriver')
browser.get('http://www.ufostalker.com/tag/photo')
ufo_entry = browser.find_elements_by_xpath("//table[@class='event-table ng-scope']/tbody")
ufo_entry[1].click()

print ufo_entry


sleep(5)
browser.quit()
