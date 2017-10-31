"""
SOME DATA SUCH AS FILE DIRECTORY PATHS MAY HAVE CHANGED TO GENERIC NAMES TO PROTECT PERSONAL INFORMATION.

ALSO, THIS IS A PERSONAL PROJECT INTENDED TO SHOWCASE MY PERSONAL PROJECT EXPERIENCE. IT WAS TAILORED FOR MY PURPOSES ON MY MACHINE
"""

class Video:
	def __init__(self, json_data):
		self.__json_data   = json_data
		self.__video_data  = {
			"url"		 : None,
			"id"             : None,
			"title"          : None,
			"ext"            : None,
			"uploader"       : None,
			"release_date"   : None,
			"playlist_title" : None,
			"playlist_index" : None,
			"playlist_id"    : None,
			"track"          : None,
			"track_number"   : None,
			"track_id"       : None,
			"artist"         : None,
			"genre"          : None,
			"album"          : None,
			"album_artist"   : None,
			"disc_number"    : None,
			"release_year"   : None,
			"format_tag"     : None,
			"path"		 : None
		}


	def get_json_data(self):
		return self.__json_data


	def set_json_data(self, dic):
		self.__json_data = dic


	def get_video_data(self):
		return self.__video_data


	def get_values(self, key):
		if key in self.__video_data:
			return self.__video_data[key]


	def set_video_data(self, data):
		#Rebinds to entirely new dictionary
		self.__video_data = data


	def set_values(self, dic):
		#Sets specific values
		for key in dic:
			if key in self.__video_data:
				self.__video_data[key] = dic[key]





