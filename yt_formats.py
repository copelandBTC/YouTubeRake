"""
SOME DATA SUCH AS FILE DIRECTORY PATHS MAY HAVE CHANGED TO GENERIC NAMES TO PROTECT PERSONAL INFORMATION.

ALSO, THIS IS A PERSONAL PROJECT INTENDED TO SHOWCASE MY PERSONAL PROJECT EXPERIENCE. IT WAS TAILORED FOR MY PURPOSES ON MY MACHINE
"""

from video  import Video
from tagger import Tagger

import json
import re
import eyed3


class Format:
	__downloaded_playlists = "/home/bc/scripts/ytrake/pl_archive.txt"
	__frequent_playlists   = "/home/bc/scripts/ytrake/frequent.txt"


	def __init__(self, format_tag, url, json, args):
		self._format         = format_tag
		self._url            = url
		self._json_data      = json
		self._defined_values = args
		self._videos         = self.fetch_video_data()
		self._path	     = self.format_path()
		self._command        = self.format_command()

		self.set_path()
	

	def is_playlist(self):
		if "playlist" in self._url:
			return True
		else:
			return False

	
	def is_video(self):
		ext = self._videos[0].get_video_data()["ext"]

		if ext == "mp4":
			return True
		else:
			return False


	def fetch_video_data(self):
		vids = []

		for dic in self._json_data:
			new_vid = Video(dic)
			data    = new_vid.get_video_data()

			#First, populate the video data with all user-specified values
			for key in self._defined_values:
				data[key] = self._defined_values[key]

			#Specially handled data
			if data["title"] is None:
				data["title"] = self.format_title(dic)

			if data["artist"] is None:
				data["artist"] = self.format_artist(dic)

			if data["album"] is None:
				data["album"] = self.format_album(dic)

			if data["ext"] is None:
				data["ext"] = self.format_extension()

			if data["format_tag"] is None:
				data["format_tag"] = self._format

			if data["track_number"] is None:
				data["track_number"] = self.format_track_number(dic)

			if data["format_tag"] is None:
				data["format_tag"] = self.set_format_tag()
			
			#Get the rest of the values
			for key in dic:
				if key in data and data[key] is None:

					data[key] = dic[key]

			new_vid.set_video_data(data)
			vids.append(new_vid)

		return vids

	
	def format_title(self, dic):
		title  = dic["title"]

		if "-" in title:
			title = title.split("-")[1].strip()

		return title


	def format_extension(self):
		return "mp3"


	def format_track_number(self, dic):
		if self.is_playlist:
			return dic["playlist_index"]
		elif re.match(".*[0-9]+.*", dic["title"]):
			track = re.split("")
			
			for str in track:
				if str.isnumeric():
					track = str
			
			return track
		else:
			return dic["track_number"]


	def format_artist(self, dic):
		artist = dic["uploader"]
		title  = dic["title"]

		#Unless it's in all caps, flatten it and capitalize
		if not re.match("[A-Z]+", artist):
			artist.lower().capitalize()

		#Try to guess at artist name with hyphen
		if "-" in title:
			artist = title.split("-")[0].strip()

		return artist


	def format_album(self, dic):
		if self.is_playlist():
			return dic["playlist_title"]
		else:
			return ""


	def format_path(self):
		artist = self._videos[0].get_video_data()["artist"]
		album  = self._videos[0].get_video_data()["album"]
		base   = "/home/bc/Desktop/Audio/Music/"

		if self.is_video():
			base = base.replace("Audio/Music", "Videos")

		path = base + artist + "/"
		
		if self.is_playlist() or album is not None:
			path = path + album + "/"

		return path


	def format_command(self):
		#USE SINGLE QUOTES INSTEAD OF DOUBLE QUOTES FOR THIS ONE LINE; BASH DOESN'T LIKE IT IF THERE IS A SINGLE QUOTE SOMEWHERE IN THE DIRECTORY
		command = 'youtube-dl -i -c -x -R infinite --fragment-retries infinite --embed-thumbnail --audio-format mp3 --download-archive "' + self._path + 'archive.txt" -o "' + self._path + '%(title)s.%(ext)s" ' + self._url
		
		if self.is_video():
			command = command.replace(" --audio-format mp3", "").replace(" -x", " -f 'best'").replace("--embed-thumbnail ", "")
		
		return command

	def tag(self):
		#The following characters are illegal for file names in Windows. Hence, youtube-dl will automatically convert them to _
		illegal = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

		for vid in self._videos:
			raw_title = vid.get_json_data()["title"]

			#Replace illegal characters
			raw_title = raw_title.replace(":", " -")
			raw_title = raw_title.replace("?", "")
			raw_title = raw_title.replace("|", "_")
			raw_title = raw_title.replace("/", "_")
			raw_title = raw_title.replace('"', "'")
			raw_title = raw_title.replace("<", "")
			raw_title = raw_title.replace(">", "")
			raw_title = raw_title.replace("\\", "")
			raw_title = raw_title.replace("*", "")

			data      = vid.get_video_data()
			mp3       = self._path + raw_title + "." + data["ext"]	
			tagger    = Tagger(mp3, raw_title, data["artist"], data["album_artist"], data["album"], data["title"], data["track_number"])
				
			if not self.is_video():
				tagger.tag()	

			tagger.rename()	


	#LOOK INTO SEMAPHORES/LOCKS
	def update_playlist_archive(self):
		if "playlist" not in self._url:
			#If not a playlist, nevermind
			return
		else:
			with open(Format.__frequent_playlists, "r") as lst:
				for line in lst:
					if self._url not in line:
						continue
					else:
						#If it's part of the frequent playlist, don't archive it
						return

			with open(Format.__downloaded_playlists, "a") as dl_file:
				dl_file.write(self._url + "\n")



	def set_format_tag(self):
		return self._format

	
	def set_path(self):	
		for vid in self._videos:
			vid.set_values({"path" : self._path})

	def get_videos(self):
		return self._videos


	def get_command(self):
		return self._command


class DefaultFormat(Format):
	def __init__(self, format_tag, url, json, args):
		super().__init__(format_tag, url, json, args)
	


class TopicFormat(Format):
	def __init__(self, format_tag, url, json, args):
		super().__init__(format_tag, url, json, args)


	def format_title(self, dic):
		return dic["title"]


	def format_artist(self):
		desc = self._json_data[0]["description"]
		desc = desc.split("\n")

		for str in desc:
			#Find the line in the description that contains the dot
			if "·" in str:
				desc = str

		desc   = desc.split("·")[1]
		desc   = desc.strip()
		artist = desc

		#Overwrite video data
		for vid in self._videos:
			if vid.get_values("artist") is not None:
				vid.set_values({"artist" : artist})

		return artist


	def format_album(self):
		desc = self._json_data[0]["description"]
		desc = desc.split("\n")

		for str in desc:
			#Find the line in the description that contains the dot
			if "·" in str:
				desc = desc[desc.index(str) + 2]

		desc  = desc.strip()
		album = desc	

		#Overwrite video data
		for vid in self._videos:
			if vid.get_values("album") is not None:
				vid.set_values({"album" : album})

		return album

		

class GrumpFormat(Format):
	def __init__(self, format_tag, url, json, args):
		super().__init__(format_tag, url, json, args)
		self.__format = "gg"


	def format_title(self, dic):
		raw_title = dic["title"]
		title     = raw_title

		if "the g club" not in raw_title.lower():
			title     = raw_title.split(" - ")
			title     = title[0].split(":")[0]

			if "PART" in raw_title:
				index = re.search("(?<=PART )([0-9]+)", raw_title).group(0)
	 
				if len(index) == 1:
					index = "0" + index

				title = title + " - " + index
			

		return title	


	def format_artist(self, dic):
		return "Game Grumps"


	def format_album(self, dic):
		if self.is_playlist():
			album = dic["playlist_title"]

			if "the g club" in album.lower():
				album = album.split(" [")[0]
		else:
			album = "Misc"

		return album


	def format_path(self):
		path = super().format_path()
		path = path.replace("/Music/", "/Podcasts/")

		return path


class NightcoreFormat(Format):
	def __init__(self, format_tag, url, json, args):
		super().__init__(format_tag, url, json, args)
		self.__format = "cl"


	def format_title(self, dic):
		title    = super().format_title(dic)
		uploader = dic["uploader"].lower()

		if "clublion" in uploader:
			#If a dance mix
			if "[" not in title and "mix" in title.lower():
				pass
			else:
				if "[" in title:
					title = title[title.index("- ") + 1 : title.index("[")].strip()
				else:
					title = title.split(" - ")[1]
		else:
			if "- " in title:
				title = title.split("- ")[1].strip()

		return title


	def format_artist(self, dic):
		title    = dic["title"]
		artist   = dic["uploader"]

		if "clublion" in artist.lower():
			#If a dance mix
			if "[" not in title and "mix" in title.lower():
				artist = "Nightcore"
			else:
				if "[" in title:
					artist = title[title.index("[") + 1 : title.index("]")]
				else:
					artist = "Nightcore"
		else:
			if "- " in title:
				artist = title.split("- ")[0].strip()

		return artist


	def format_album(self, dic):
		return "Nightcore"


	def format_path(self):
		return "/home/bc/Desktop/Audio/Music/Nightcore/"


	def format_command(self):
		command = super().format_command()
		command = command.replace("/Nightcore/Nightcore/", "/Nightcore/")

		return command


class KpopFormat(Format):	
	def __init__(self, format_tag, url, json, args):
		super().__init__(format_tag, url, json, args)
		self.__format = "kp"


	def format_album(self, dic):
		return "Kpop"
	

	def format_path(self):
		artist  = self._videos[0].get_values("artist")

		path = super().format_path()
		path = path.replace("/Music/", "/Music/Kpop/")
		path = path.replace("/%s/Kpop/" %artist, "/%s/" %artist)

		return path


	def format_command(self):
		artist  = self._videos[0].get_values("artist")

		command = super().format_command()
		command = command.replace(artist + "/archive.txt", "archive.txt")

		return command

class NostalgiaCriticFormat(Format):
	pass


class KhanAcademyFormat(Format):
	pass



"""

PREVIOUSLY...

YOU COMPLETED A BUNCH OF FORMATS. YOU'RE ALMOST THERE! JUST FINISH IT OFF

"""
