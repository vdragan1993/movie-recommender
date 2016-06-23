__author__ = 'Dragan Vidakovic'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_imdb_link(movie_name):
    """
    Get IMDB link for given movie.
    :param movie_name: Movie name
    :return: IMDB link
    """
    # connect to google
    browser = webdriver.Chrome('D:/chromedriver.exe')
    browser.get('http://www.google.com')
    # search
    search = browser.find_element_by_name('q')
    search.send_keys(movie_name + " imdb")
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    # click on result
    first_link = browser.find_elements_by_xpath("//div[@id='rso']/div[@class='g']/div/div/h3/a")
    first_link[0].click()
    time.sleep(1)
    # get url
    string_url = browser.current_url
    # getting poster
    poster = ""
    try:
        image = browser.find_element_by_xpath('//div[@class="poster"]//img[@src]')
        poster = image.get_attribute('src')
    except:
        pass

    browser.quit()
    return string_url, poster
