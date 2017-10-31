"""
THIS PROGRAM IS AN OBSOLETE PROTOTYPE OF WHAT HAS BECOME YOUTUBERAKE. THIS PROGRAM SCRAPES DATA USING MOSTLY BEAUTIFULSOUP AND SELENIUM; IT DOES NOT UTILIZE 
THE YOUTUBE-DL COMMAND-LINE TOOL

"""

import subprocess
import time
import os
import shutil
import re
import selenium.webdriver.chrome.webdriver as wd
import selenium.webdriver.common.action_chains as chain
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as sopa
import urllib.request as req
from selenium.common.exceptions import StaleElementReferenceException as stale

"""""""""""""""
GET LINKS
"""""""""""""""
yt_base = "https://www.youtube.com"
yt_url = req.urlopen("https://www.youtube.com/watch?v=jpbJbRE7ftY&list=PLRQGRBgN_Enp8AlpQw7vGS0mEANb7ufIz")

yt_page = sopa(yt_url, "html.parser")

#Get all links
temp_links = yt_page.find_all("a", href = True)
links = []

#Get title
title = ""

for l in temp_links:
	if l["href"].startswith("/playlist?"):
		title = l.get_text()


#Filter playlist
for l in temp_links:
	if l["href"] not in links and "index" in l["href"] and  l["href"].startswith("/watch"):
		links.append(l["href"])


"""""""""""""""
CONVERT
"""""""""""""""

driver = wd.WebDriver()
driver.get("http://convert2mp3.net/en/")
action = chain.ActionChains(driver)

"""
#open tabs
for i in range(1, len(links) - 1):
	driver.execute_script("window.open('http://convert2mp3.net/en/', '_blank')")
"""

urlinput = driver.find_element_by_id("urlinput")

test_vid = "https://www.youtube.com/watch?v=b7CUOa7wsd0"

action.send_keys_to_element(urlinput, test_vid + Keys.ENTER).perform()


"""""""""""""""
DOWNLOAD
"""""""""""""""

#Get name of file
src = driver.page_source
title = src[src.index('The video "<b>') + 14 : src.index('</b>" has been converted')] + ".mp3"

#Get download link
completion_base = src[src.index('http://cdl') : src.index('swf_player')]
curr_url = driver.current_url
dl_link = completion_base + "download.php?id=" + curr_url[curr_url.index("youtube"):] + "&d=y"

#Download
driver.get(dl_link)

"""""""""""""""
NAME AND SORT
"""""""""""""""

#Fetch from downloads director

src_folder = "/directory/path/"
dest_folder = "/path/to/Music/"
regex = re.compile(re.escape(title) + r"(.*)")

#Wait for download
print("Sleeping...")
time.sleep(2)
print("I'm awake!")

for root, dirs, files in os.walk(src_folder):
  for f in files:
      print(f)
      if title in str(f):      
          shutil.move(src_folder + str(f), dest_folder)

"""
THIS VERSION CAN DOWNLOAD ANY VIDEO ALLOWED BY THE MP3 CONVERTER AND PUTS IT INTO THE HARD-CODED FOLDER
"""
