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
trackArtistDf = pd.read_excel (r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/trackArtistDfEdited.xlsx')
uriList = trackArtistDf['URI'].tolist()
matchedTrackUriDf = pd.read_excel (r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/matchedTrackUriDfEdited.xlsx')
matchedTrackUriDfGroupBy = matchedTrackUriDf.groupby(['URI'], as_index = False)
uniqueTrackUriDf = matchedTrackUriDfGroupBy.first()
uriList = matchedTrackUriDf['URI'].tolist()
print('Top Tracks 06/04/2016 - 09/22/2022')
uniqueTrackList = uniqueTrackUriDf['Track'].tolist()
uniqueArtistList = uniqueTrackUriDf['Artist'].tolist()
uniqueUriList = uniqueTrackUriDf['URI'].tolist()
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
for t in range (math.floor(len(uniqueUriList)/100)):
	rank = []
	topTracks = []
	topArtistsFromTracks = []
	streamsFromTracks = []
	topUris = []
	elapsedTimeList = []
	print('Unique URI List Length:', len(uniqueUriList))
	for i in range (100):
		def most_frequent(uriList):
			return max(set(uriList), key = uriList.count)
		topUriIntermediate = most_frequent(uriList)
		for j in range(len(uniqueUriList)):
			if (topUriIntermediate == uniqueUriList[j]):
				topTrackIntermediate = (uniqueTrackList[j])
				break
		for k in range(len(uniqueArtistList)):
			if (topUriIntermediate == uniqueUriList[k]):
				topTrackArtistIntermediate = (uniqueArtistList[k])
				break
		rank.append(((100*t)+i+1))
		topTracks.append(topTrackIntermediate)
		topArtistsFromTracks.append(topTrackArtistIntermediate)
		streamsFromTracks.append(uriList.count(topUriIntermediate))
		topUris.append(topUriIntermediate)
		uriList = [i for i in uriList if i != topUriIntermediate]
		elapsedTime = (time.time() - start_timer_sec)
		elapsedTimeList.append(elapsedTime)
		print(((100*t)+i+1), ('--- %s seconds ---' % elapsedTime), 'difference = ',  elapsedTimeList[i] - elapsedTimeList[i-1])
	topTracksDf = pd.DataFrame(list(zip(rank, topTracks, topArtistsFromTracks, streamsFromTracks, topUris)), columns = ['Rank', 'Track', 'Artist', 'Streams', 'URI'])
	topTracksDfList.append(topTracksDf)
	display(topTracksDf.to_string(index = False))
	print('--- %s seconds ---' % (time.time() - start_timer_sec))
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
	
for t in range (math.floor(len(uniqueUriList)%100)):
	rank = []
	topTracks = []
	topArtistsFromTracks = []
	streamsFromTracks = []
	topUris = []
	elapsedTimeList = []
	for i in range (math.floor(len(uniqueUriList)%100)):
		def most_frequent(uriList):
			return max(set(uriList), key = uriList.count, default = '')
		topUriIntermediate = most_frequent(uriList)
		for j in range(len(uniqueUriList)):
			if (topUriIntermediate == uniqueUriList[j]):
				topTrackIntermediate = (uniqueTrackList[j])
				break
		for k in range(len(uniqueArtistList)):
			if (topUriIntermediate == uniqueUriList[k]):
				topTrackArtistIntermediate = (uniqueArtistList[k])
				break
		if (uriList.count(topUriIntermediate)) != 0:
			rank.append(math.floor(len(uniqueUriList)/100)*100 + (i + 1))
			topTracks.append(topTrackIntermediate)
			topArtistsFromTracks.append(topTrackArtistIntermediate)
			streamsFromTracks.append(uriList.count(topUriIntermediate))
			topUris.append(topUriIntermediate)
			uriList = [i for i in uriList if i != topUriIntermediate]
			elapsedTime = (time.time() - start_timer_sec)
			elapsedTimeList.append(elapsedTime)
			print((math.floor(len(uniqueUriList)/100)*100 + (i + 1)), ('--- %s seconds ---' % elapsedTime), 'difference = ',  elapsedTimeList[i] - elapsedTimeList[i-1])
	if 0 not in streamsFromTracks:
		topTracksDf = pd.DataFrame(list(zip(rank, topTracks, topArtistsFromTracks, streamsFromTracks, topUris)), columns = ['Rank', 'Track', 'Artist', 'Streams', 'URI'])
		topTracksDfList.append(topTracksDf)
		#display(topTracksDf.to_string(index = False))
		#print('--- %s seconds ---' % (time.time() - start_timer_sec))
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
		
allTopTracksDfs = pd.concat(topTracksDfList, ignore_index = True)
allSongDataDfs = pd.concat(songDataDfList, ignore_index = True)
allTopTracksDfs.drop(allTopTracksDfs.index[dropIndexList])
allSongData = pd.concat([allTopTracksDfs, allSongDataDfs], axis = 1)
allSongData.to_excel(f'{outputPath}/allSongData.xlsx', index = False)

end_time = datetime.now()
end_time = end_time.strftime("%H:%M:%S")
print('Start Time:', start_time)
print('End Time:', end_time)
