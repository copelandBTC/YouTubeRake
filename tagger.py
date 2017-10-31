#!/usr/bin/env python3

"""
SOME DATA SUCH AS FILE DIRECTORY PATHS MAY HAVE CHANGED TO GENERIC NAMES TO PROTECT PERSONAL INFORMATION.

ALSO, THIS IS A PERSONAL PROJECT INTENDED TO SHOWCASE MY PERSONAL PROJECT EXPERIENCE. IT WAS TAILORED FOR MY PURPOSES ON MY MACHINE
"""

from mutagen.easyid3 import EasyID3 as id3

import sys
import os
import glob

class Tagger:
	def __init__(self, mp3 = None, raw_title = None, artist = None, album_artist = None, album = None, title = None, track_num = None):
		self.__mp3	    = mp3
		self.__raw_title    = raw_title
		self.__artist       = artist
		self.__album_artist = album_artist
		self.__album        = album
		self.__title	    = title
		self.__track_num    = track_num
		

	def tag(self):
		raw_title = self.__raw_title + ".mp3"
		title     = self.__title + ".mp3"
		path      = self.__mp3.replace(raw_title, "")

		if raw_title in os.listdir(path) or title in os.listdir(path):
			if raw_title not in os.listdir(path):
				self.__mp3 = self.__mp3.replace(raw_title, title)	
	
			mp3                 = id3(self.__mp3)
			mp3["artist"]       = self.__artist
			mp3["album"]        = self.__album
			mp3["title"]        = self.__title

			mp3.save()


	def rename(self):
		try:
			raw_title = self.__raw_title + ".mp3"
			new_title = self.__mp3[0 : self.__mp3.index(self.__raw_title)] + self.__title + ".mp3"
			path      = self.__mp3.replace(raw_title, "")

			if raw_title in os.listdir(path):
				os.rename(self.__mp3, new_title)
		except (FileNotFoundError, ValueError) as e:	
			print("FILE: %s NOT FOUND; SKIPPING" %raw_title)
			pass




if __name__ == "__main__":
	pass	

	
