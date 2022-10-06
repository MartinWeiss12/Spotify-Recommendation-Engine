#!/usr/bin/env python3

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
path = r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/Extended Streaming History'
outputPath = r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify'
start_time = datetime.now()
start_time = start_time.strftime("%H:%M:%S")
print('Start Time:' , start_time)

cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
spotify = spotipy.Spotify(auth = client_credentials_manager, requests_timeout = 5000, retries = 5000)
listOfPlaylistUris= []
playlists = sp.user_playlists('spotify')
spotifyPlaylistUriList = []
while playlists:
	for i, playlist in enumerate(playlists['items']):
		spotifyPlaylistUriList.append(playlist['uri'][-22:])
	if playlists['next']:
		playlists = sp.next(playlists)
	else:
		playlists = None
	spotifyPlaylistUriList[:20]
	
print(len(spotifyPlaylistUriList))
def trackUrisFromPlaylists(playlist_id):
	playlist = sp.user_playlist('spotify', playlist_id)
	for item in playlist['tracks']['items'][:2000]:
		track = item['track']
		if (track is not None):
			songUriList.append(track['id'])
	return

songUriList = []
for uri in spotifyPlaylistUriList[:2000]:
	trackUrisFromPlaylists(uri)
	songUriList[:5]

print('Total Tracks Found:', len(songUriList))
uniqueUris = list(dict.fromkeys(songUriList))
print('Unique Tracks Found:', len(uniqueUris))
spotifyPlayListSongDataList = []
songDataColNames = ['URI', 'danceability', 'energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
uri = []
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
uniqueUris.pop(14314) #14314 was None

for i in range (len(uniqueUris)):
	songData = sp.audio_features(uniqueUris[i])
	print(i)
	if (songData[0] is not None):
		uri.append(songData[0]['uri'].replace('spotify:track:', ''))
		danceability.append(songData[0]['danceability'])
		energy.append(songData[0]['energy'])
		key.append(songData[0]['key'])
		loudness.append(songData[0]['loudness'])
		mode.append(songData[0]['mode'])
		acousticness.append(songData[0]['acousticness'])
		instrumentalness.append(songData[0]['instrumentalness'])
		liveness.append(songData[0]['liveness'])
		valence.append(songData[0]['valence'])
		tempo.append(songData[0]['tempo'])
		time_signature.append(songData[0]['time_signature'])
		
print('All data in dataframe, exporting to Excel')
spotifyPlaylistSongDataDf = pd.DataFrame(list(zip(uri, danceability, energy, key, loudness, mode, acousticness, instrumentalness, liveness, valence, tempo, time_signature)), columns = songDataColNames)
spotifyPlaylistSongDataDf.to_excel(f'{outputPath}/spotifyPlaylistSongData.xlsx', index = False)

end_time = datetime.now()
end_time = end_time.strftime("%H:%M:%S")
print('End Time:', end_time)