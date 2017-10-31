#!/usr/bin/env python3

"""
SOME DATA SUCH AS FILE DIRECTORY PATHS MAY HAVE CHANGED TO GENERIC NAMES TO PROTECT PERSONAL INFORMATION.

ALSO, THIS IS A PERSONAL PROJECT INTENDED TO SHOWCASE MY PERSONAL PROJECT EXPERIENCE. IT WAS TAILORED FOR MY PURPOSES ON MY MACHINE
"""

from yt_formats import *

import subprocess as sp
import os
import json
import eyed3
import sys
import glob
import re

class YouTubeRake:
	__downloaded_playlists = "/path/topl_archive.txt"
	__frequent_playlists   = "/path/to/frequent.txt"
	__format_types         = {
		None  : DefaultFormat,
		"cl"  : NightcoreFormat,
		"gg"  : GrumpFormat,
		"ka"  : KhanAcademyFormat,
		"nc"  : NostalgiaCriticFormat,
		"tpc" : TopicFormat,
		"kp"  : KpopFormat
	}


	def __init__ (
		self, url, _id = None, title = None, ext = None, uploader = None, release_date = None,
		playlist_title = None, playlist_index = None, playlist_id = None, track = None, track_number = None,
		track_id = None, artist = None, genre = None, album = None, album_artist = None, disc_number = None, 
		release_year = None, format_tag = None
	):

		self.__url = url

		if self.is_already_downloaded():
			print("This playlist has already been downloaded.")
			exit(0)

		self.__json_data      = self.fetch_json_data()		
		self.__defined_values = self.get_args(locals())
		self.__formatter      = self.determine_format()
		self.__videos	      = self.__formatter.get_videos()
		self.__command        = self.__formatter.get_command()

		self.rake()
		self.__formatter.tag()
		self.__formatter.update_playlist_archive()

		#TEMP
		#move all the files to flash drive
		src  = '"' + self.__videos[0].get_values("path") + '"'
		dest = src.replace("/path/to/", "/flashdrive/")

		print("\n\n\n")
		if input("Would you like to move the files? y/n").lower() == "y":

			sp.run("python3 /path/to/scripts/mv.py %s %s" %(src, dest), shell = True)		

		#Remove JSON file from disk
		os.remove("/path/to/scripts/ytrake/jdump_" + self.__url.split("=")[1] + ".json")
		

	def is_already_downloaded(self):
		if "playlist" in self.__url:
			with open(YouTubeRake.__downloaded_playlists, "r") as download_list:
				for line in download_list:
					downloaded_id = str(line).strip("\n")

					if downloaded_id != self.__url:
						continue
					else:
						return True

		return False

	#LOCK
	def fetch_json_data(self):
		while True:
			data = []
			path = "/path/to/scripts/ytrake/jdump_" + self.__url.split("=")[1] + ".json"

			#Create JSON file if not already there
			if not os.path.exists(path):
				try:
					sp.run("youtube-dl -j %s > %s" % (self.__url, path), shell = True)	

				except (KeyboardInterrupt, Exception) as e:	
					#Remove json file from disk
					sp.run("rm %s" %path, shell = True)

			with open(path, "r") as j_file:					
				if "playlist" in self.__url:
					#Use loads as opposed to load; this is how it needs to be done with playlists
					for dic in j_file:
						data.append(json.loads(dic))
				else:
					#Get the single JSON-like dictionary
					data.append(json.load(j_file))

					if self.__url != data[0]["webpage_url"]:
						continue
					else:
						break
				try:
					if data[0]["playlist_id"] not in self.__url and self.__url != data[0]["webpage_url"]:
						os.remove(path)
						continue
					else:
						break
				except IndexError:
					print("EMPTY FILE; ATTEMPTING TO DOWNLOAD AGAIN")
					os.remove(path)
					continue

		return data


	def get_args(self, args):
		def_values = {}

		for key in args:
			if args[key] is not None:
				def_values[key] = args[key]

		return def_values


	def determine_format(self):
		json_sample = str(self.__json_data[0]).lower()
		title       = self.__json_data[0]["title"].lower()
		format_tag  = None

		if "format_tag" in self.__defined_values:
			format_tag = self.__defined_values["format_tag"]
		else:
			if "nightcore" in json_sample:
				format_tag = "cl"
			elif "grumps" in json_sample:
				format_tag = "gg"
			elif "khan academy" in json_sample:
				format_tag = "ka"
			elif "nostalgia critic" in json_sample:
				format_tag = "nc"
			elif "topic" in json_sample:
				format_tag = "tpc"
			elif not all(ord(char) < 128 for char in self.__json_data[0]["title"]):
				if "han|rom|eng" in title or "k-pop" in json_sample or "kpop" in json_sample or "korea" in json_sample:
					format_tag = "kp"

			else:
				pass

		formatter = YouTubeRake.__format_types[format_tag](format_tag, self.__url, self.__json_data, self.__defined_values)

		return formatter


	def get_videos(self):
		return self.__videos
			

	def rake(self):
		path = self.__videos[0].get_video_data()["path"]	

		#Look for partially downloaded files. If they still exist, start over and keep downloading
		while True:	
			for i in range(5): sp.run(self.__command, shell = True)

			"""
			files = glob.glob(path + "*.mp?")

			if len(files) != len(self.__videos):
				while len(self.__json_data) < len(files):
					#If, for some reason, the JSON file has not completely downloaded, go ahead and try to redownload it
					jpath = "/path/to/scripts/ytrake/jdump_" + self.__url.split("=")[1] + ".json"
					os.remove(jpath)
					self.__json_data = self.fetch_json_data()

			#Incomplete download flag
			incompl = False

			for f in files:
				if ".jpg" in f or ".part" in f or ".webm" in f:	
					incompl = True
					break
					
			if incompl:
				continue
			else:
				break

			#TEST
			print("LOOP")
			"""
					

if __name__ == "__main__":
	args = sys.argv

	params = {
		"title"          : None,
		"ext"            : None,
		"uploader"       : None,
		"playlist_title" : None,
		"playlist_index" : None,
		"artist"         : None,
		"album"          : None,
		"format_tag"     : None
	}

	for arg in args:
		key = arg.split("=")[0]	

		if key in params:	
			arg         = arg.split("=")[1].strip()	
			params[key] = arg


	rake = YouTubeRake(
				url            = args[1],
				title          = params["title"],
				ext            = params["ext"],
				uploader       = params["uploader"],
				playlist_title = params["playlist_title"],
				playlist_index = params["playlist_index"],
				artist         = params["artist"],
				album          = params["album"],
				format_tag     = params["format_tag"]
				)
				
