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
fileCount = (len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))]))
data = []
countList = []
files = os.listdir(path)
files.sort()
for file in files:
	if file.endswith('json'):
		count = file
		count = file.replace('endsong_', '')
		count2 = count.replace('.json', '')
		count2 = int(count2)
		countList.append(count2)
		
sortedList = countList.sort()
for json in countList:
	df = pd.read_json(r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/Extended Streaming History/endsong_' + str(json) + '.json')
	data.append(df)
data = pd.concat(data)
data.reset_index(drop = True, inplace = True)
data = data[data.ms_played >= 30000] #streams longer than 30 seconds
artistList = (data['master_metadata_album_artist_name']).tolist()
trackList = (data['master_metadata_track_name']).tolist()
albumNameList = (data['master_metadata_album_album_name']).tolist()
uriList = (data['spotify_track_uri']).tolist()
msPlayedList = (data['ms_played']).tolist()
endReasonList = (data['reason_end']).tolist()
dateList = (data['ts']).tolist()
est = pytz.timezone('US/Eastern')
utc = pytz.utc
fmt = '%Y-%m-%d %H:%M:%S'
for ind in data.index:
	date = (data['ts'][ind])
	holdTS = datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]), int(date[17:19]), tzinfo = utc)
	estTS = holdTS.astimezone(est).strftime(fmt)
	data.at[ind, 'ts'] = estTS
dateList = data['ts'].tolist()
#data.to_excel(f'{outputPath}/all_streaming_data.xlsx', index = False)
print('Minutes Played:', round(sum(msPlayedList)/60000))
trackArtistDf = pd.DataFrame(list(zip(dateList, trackList, artistList, uriList)), columns = ['Date', 'Track', 'Artist', 'URI'])
trackArtistDf['Date'] = pd.to_datetime(trackArtistDf['Date'])
trackArtistDf = trackArtistDf.sort_values(by = 'Date')
trackArtistDf = trackArtistDf[trackArtistDf['Track'].str.contains('None') == False]
trackArtistDf = trackArtistDf[trackArtistDf['Artist'].str.contains('None') == False]
trackArtistDf = trackArtistDf[trackArtistDf['URI'].str.contains('None') == False]
trackArtistDf = trackArtistDf.reset_index(drop = True)
for ind in trackArtistDf.index:
	trackUri = (trackArtistDf['URI'][ind])
	holdTrackUri = trackUri.replace('spotify:track:', '')
	trackArtistDf.at[ind, 'URI'] = holdTrackUri
uriList = trackArtistDf['URI'].tolist()
#trackArtistDf.to_excel(f'{outputPath}/trackArtistDf.xlsx', index = False)

print('Top Spotify Data 06/04/2016 - 09/22/2022. Streams greater than 30 seconds.')
print('Top Artists 06/04/2016 - 09/22/2022')
topArtistsColNames = ['Rank', 'Artist', 'Streams']
topArtistsDf = pd.DataFrame(columns = topArtistsColNames)
topArtists = []
topArtists = trackArtistDf['Artist'].tolist()
for i in range (50):
	def most_frequent(artistList):
		return max(set(artistList), key = artistList.count)
	topArtist = most_frequent(artistList)
	topArtistsDf = topArtistsDf.append({'Rank': i+1, 'Artist': topArtist, 'Streams': artistList.count(topArtist)}, ignore_index = True)
	topArtists.append(topArtist)
	artistList = [i for i in artistList if i != topArtist]
display(topArtistsDf.to_string(index = False))
topArtistsDf.to_excel(f'{outputPath}/topArtists.xlsx', index = False)

print('URI List Length:', len(uriList))
print('Starting URI Mapping --- %s seconds ---' % (time.time() - start_timer_sec))
trackList = trackArtistDf['Track'].tolist()
artistList = trackArtistDf['Artist'].tolist()

for i in range(len(uriList)):
	for j in range(len(uriList)):
		if((trackList[i] == trackList[j]) and (artistList[i] == artistList[j]) and (uriList[i] != uriList[j])):
			uriList[i] = uriList[j]
			
matchedTrackUriDf = pd.DataFrame(list(zip(trackList, artistList, uriList)), columns = ['Track', 'Artist', 'URI'])
matchedTrackUriDfGroupBy = matchedTrackUriDf.groupby(['URI'], as_index = False)
uniqueTrackUriDf = matchedTrackUriDfGroupBy.first()
#matchedTrackUriDf.to_excel(f'{outputPath}/matchedTrackUriDf.xlsx', index = False)
#uniqueTrackUriDf.to_excel(f'{outputPath}/uniqueTrackUriDf.xlsx', index = False)
done_uri_mapping = datetime.now()
done_uri_mapping = done_uri_mapping.strftime("%H:%M:%S")
print('Done URI Mapping:' , done_uri_mapping)
print('Done URI Mapping --- %s seconds ---' % (time.time() - start_timer_sec))
print('Top Tracks 06/04/2016 - 09/22/2022')
uniqueTrackList = uniqueTrackUriDf['Track'].tolist()
uniqueArtistList = uniqueTrackUriDf['Artist'].tolist()
uniqueUriList = uniqueTrackUriDf['URI'].tolist()
uriList = matchedTrackUriDf['URI'].tolist()
start_timer_sec = time.time()
cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
spotify = spotipy.Spotify(auth=client_credentials_manager, requests_timeout = 50, retries = 50)
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