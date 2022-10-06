#!/usr/bin/env python3

import pytz
import time
import math
import spotipy
import itertools
import os, os.path
import pandas as pd
from datetime import datetime
from IPython.display import display
from requests.exceptions import ReadTimeout
from spotipy.oauth2 import SpotifyClientCredentials
start_time = datetime.now()
start_time = start_time.strftime("%H:%M:%S")
print('Start Time:', start_time)
start_timer_sec = time.time()
path = r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/Extended Streaming History'
outputPath = r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify'

topTracksDf = pd.read_excel (r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/topTracksDfTest.xlsx')

start_timer_sec = time.time()
cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
spotify = spotipy.Spotify(auth=client_credentials_manager, requests_timeout = 5000, retries = 5000)
songDataColNames = ['danceability', 'energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
topTracksDfList = []
songDataDfList = []
dropIndexList = []

for t in range (math.floor(len(topTracksDf)/100)):
	danceability = []
	energy = []
	key = []
	loudness = []
	mode = []
	acousticness = []
	instrumentalness = []
	liveness = []
	valence = []
	tempo = []
	time_signature = []
	topUriList = topTracksDf['URI']
	for i in range (len(topUriList)):
		songData = sp.audio_features(topUriList)[i]
		if (songData is None):
			dropIndexList.append(((100*t)+i+1))
		if (songData is not None):
			danceability.append(songData['danceability'])
			energy.append(songData['energy'])
			key.append(songData['key'])
			loudness.append(songData['loudness'])
			mode.append(songData['mode'])
			acousticness.append(songData['acousticness'])
			instrumentalness.append(songData['instrumentalness'])
			liveness.append(songData['liveness'])
			valence.append(songData['valence'])
			tempo.append(songData['tempo'])
			time_signature.append(songData['time_signature'])
	songDataDf = pd.DataFrame(list(zip(danceability, energy, key, loudness, mode, acousticness, instrumentalness, liveness, valence, tempo, time_signature)), columns = songDataColNames)
	songDataDfList.append(songDataDf)
	
for t in range (math.floor(len(topTracksDf)%100)):
	danceability = []
	energy = []
	key = []
	loudness = []
	mode = []
	acousticness = []
	instrumentalness = []
	liveness = []
	valence = []
	tempo = []
	time_signature = []
	topUriList = topTracksDf['URI']
	for i in range (len(topUriList)):
		songData = sp.audio_features(topUriList)[i]
		if (songData is None):
			dropIndexList.append(((100*t)+i+1))
		if (songData is not None):
			danceability.append(songData['danceability'])
			energy.append(songData['energy'])
			key.append(songData['key'])
			loudness.append(songData['loudness'])
			mode.append(songData['mode'])
			acousticness.append(songData['acousticness'])
			instrumentalness.append(songData['instrumentalness'])
			liveness.append(songData['liveness'])
			valence.append(songData['valence'])
			tempo.append(songData['tempo'])
			time_signature.append(songData['time_signature'])
	songDataDf = pd.DataFrame(list(zip(danceability, energy, key, loudness, mode, acousticness, instrumentalness, liveness, valence, tempo, time_signature)), columns = songDataColNames)
	songDataDfList.append(songDataDf)

allSongDataDfs = pd.concat(songDataDfList, ignore_index = True)
topTracksDf.drop(topTracksDf.index[dropIndexList])
allSongData = pd.concat([topTracksDf, allSongDataDfs], axis = 1)
allSongData.to_excel(f'{outputPath}/allSongData.xlsx', index = False)

end_time = datetime.now()
end_time = end_time.strftime("%H:%M:%S")
print('Start Time:', start_time)
print('End Time:', end_time)
