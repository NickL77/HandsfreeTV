import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from pyautogui import press, typewrite, hotkey

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/watch?v=mvMJl_0oQ_8")

time.sleep(2)

elem = driver.find_element_by_id("movie_player")
elem.send_keys("f")
elem.send_keys(Keys.SPACE)

time.sleep(2)

elem.send_keys(Keys.RIGHT)
elem.send_keys(Keys.RIGHT)

