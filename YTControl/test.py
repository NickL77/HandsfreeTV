import time
from YTControl import YTControl

yt = YTControl('https://www.youtube.com/watch?v=mvMJl_0oQ_8')
time.sleep(1)
"""
yt.maximize()
time.sleep(1)
yt.pause()
time.sleep(1)
yt.play()
time.sleep(1)
yt.volume_down()
time.sleep(1)
yt.volume_up()
time.sleep(1)
yt.seek_forward()
time.sleep(1)
yt.seek_back()
time.sleep(1)
yt.minimize()
"""

yt.search("team 254 2019 robot reveal")
