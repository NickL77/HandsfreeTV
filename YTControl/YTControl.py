from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YTControl:

    def __init__(self, link):
        self.driver = webdriver.Chrome()
        self.driver.get(link)
        self.paused = True
        self.fullscreen = False

        if 'YouTube' not in self.driver.title:
            raise RuntimeError('Invalid YouTube URL')

        self.element = None
        try:
            self.element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "movie_player"))
            )
        except Exception:
            raise RuntimeError()

        self.play()

    def play(self):
        if self.paused:
            self.element.send_keys('k')
            self.paused = False

    def pause(self):
        if not self.paused:
            self.element.send_keys('k')
            self.paused = True

    def volume_up(self):
        self.element.send_keys(Keys.UP)

    def volume_down(self):
        self.element.send_keys(Keys.DOWN)

    def seek_forward(self):
        self.element.send_keys(Keys.RIGHT)

    def seek_back(self):
        self.element.send_keys(Keys.LEFT)

    def maximize(self):
        if not self.fullscreen:
            self.element.send_keys('f')
            self.fullscreen = True

    def minimize(self):
        if self.fullscreen:
            self.element.send_keys('f')
            self.fullscreen = False

    def search(self, keyword):
        elem = self.driver.find_element_by_name("search_query")
        elem.clear()
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)

        try:
            self.element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "ytd-video-renderer"))
            )
        except Exception:
            raise RuntimeError()
        self.driver.find_element_by_tag_name("ytd-video-renderer").click()

