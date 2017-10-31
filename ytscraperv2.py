"""
THIS PROGRAM IS AN OBSOLETE PROTOTYPE OF WHAT HAS BECOME YOUTUBERAKE. THIS PROGRAM SCRAPES DATA USING MOSTLY BEAUTIFULSOUP AND SELENIUM; IT DOES NOT UTILIZE 
THE YOUTUBE-DL COMMAND-LINE TOOL

"""

import subprocess
import math
import time
import os
import shutil
import re
import sys
import selenium.webdriver.chrome.webdriver as wd
import selenium.webdriver.common.action_chains as chain
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as sopa
import urllib.request as req
from selenium.common.exceptions import StaleElementReferenceException as stale

class Youtube_Rake:
	def __init__(self, vid_link, vid_type, genre = "", artist = "", album = ""):
		self.__vid_data    = (vid_link, vid_type, genre, artist, album)
		self.__driver      = wd.WebDriver()
		self.__action      = chain.ActionChains(self.__driver)
		self.__file_names  = []
		self.__vid_list    = []
		self.__failed_vids = []

		if vid_type == "playlist":			
			self.__vid_list = self.get_links(vid_link)
		else:
			self.__vid_list.append(vid_link)

		self.convert(self.__vid_list)


	def get_links(self, vid_link):
		yt_url = req.urlopen(vid_link)
		yt_page = sopa(yt_url, "html.parser")

		#Get all links
		temp_links = yt_page.find_all("a", href = True)

		#Filter playlist to get just the video links
		links = []

		for link in temp_links:
			if link["href"].startswith("/watch"):
				if "index" in link["href"]:
					link["href"] = "https://www.youtube.com" + link["href"]
					
					if link["href"] not in links:
						links.append(link["href"])			

		return links


	def convert(self, links):
		"""
		#open tabs
		for i in range(1, len(links) - 1):
			driver.execute_script("window.open('http://convert2mp3.net/en/', '_blank')")
		"""

		self.__failed_vids = []
		
		for link in links:
			try:
				#Go to MP3 converter homepage
				self.__driver.get("http://convert2mp3.net/en/")	
				self.__action = chain.ActionChains(self.__driver)		

				#Type in the video link
				urlinput = self.__driver.find_element_by_id("urlinput")				
				self.__action.send_keys_to_element(urlinput, link + Keys.ENTER).perform()			
				self.download()
			except ValueError:
				#If video fails to download, flag it and move on to next one
				self.__failed_vids.append(link)
				continue

		self.display_results()



	def download(self):
		#Get name of file
		src = self.__driver.page_source
		title = src[src.index('The video "<b>') + 14 : src.index('</b>" has been converted')] + ".mp3"

		#Get download link
		completion_base = src[src.index('http://cdl') : src.index('swf_player')]
		curr_url = self.__driver.current_url
		dl_link = completion_base + "download.php?id=" + curr_url[curr_url.index("youtube"):] + "&d=y"

		#Download
		self.__driver.get(dl_link)

		#Add the newly downloaded file to the name list for sorting to come later
		self.__file_names.append(title)

	def get_file_names(self):
		return self.__file_names

	def get_video_list(self):
		return self.__vid_list


	def get_failed_videos(self):
		return self.__failed_vids

	def get_video_data(self):
		return self.__vid_data


	def display_results(self):
		failures        = self.get_failed_videos()
		total_vids      = len(self.get_video_list())
		num_failed_vids = len(self.get_failed_videos())
		success_rate    = str(math.ceil(((total_vids - num_failed_vids) / total_vids) * 100)) + "%"
		results 	= """
  DOWNLOAD COMPLETE \n

  TOTAL VIDEOS IN LIST : ............................ %d \n
  TOTAL FAILED VIDEOS  : ............................ %d \n
  SUCCESS RATE	       : ............................ %s \n\n


  FAILED VIDEOS

  ************************************** \n\n
				  
""" % (total_vids, num_failed_vids, success_rate)

		for fail in failures:
			results += (fail + "  \n")

		print(results)
	

	#TO BE MOVED TO ANOTHER CLASS LATER
	def sort(self, title):
		#Fetch from downloads director
		src_folder = "/path/to/Downloads/"
		dest_folder = "/path/to/Music/"
		regex = re.compile(re.escape(title) + r"(.*)")

		for root, dirs, files in os.walk(src_folder):
			    for f in files:
				    if title in str(f):      
			                    shutil.move(src_folder + str(f), dest_folder)


if __name__ == "__main__":
	vid_link = input("Enter video or playlist here: ")
	
	if "list" in vid_link:
		vid_type = "playlist"
	else:
		vid_type = "video"

	#Start raking
	rake = Youtube_Rake(vid_link, vid_type)
	file_names = rake.get_file_names()

	#Start sorting
	
	

"""

THIS VERSION CAN DOWNLOAD ANY VIDEO OR PLAYLIST ALLOWED BY THE MP3 CONVERTER AND PUTS IT INTO THE HARD-CODED FOLDER; VIDEOS OVER 90 MINUTES ARE NOT ALLOWED


THIS VERSION USES THE CONVERT2MP3 WEBSITE FOR CONVERSION AND DOWNLOADING. SINCE THEN, I'VE FOUND A PYTHON-COMPATIBLE TOOL, YOUTUBE-DL. IT HAS PROVEN MORE EFFICIENT, SO 
THIS VERSION HAS BEEN ABANDONED IN FAVOR OF A YOUTUBE-DL OFF-SHOOT UNTIL FURTHER NOTICE


"""


