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
uniqueTrackUriDf.to_excel(f'{outputPath}/uniqueTrackUriDf.xlsx', index = False)
uriList = matchedTrackUriDf['URI'].tolist()
print('Top Tracks 06/04/2016 - 09/22/2022')
uniqueTrackList = uniqueTrackUriDf['Track'].tolist()
uniqueArtistList = uniqueTrackUriDf['Artist'].tolist()
uniqueUriList = uniqueTrackUriDf['URI'].tolist()
start_timer_sec = time.time()
topTracksDfList = []
songDataDfList = []
dropIndexList = []
rank = []
topTracks = []
topArtistsFromTracks = []
streamsFromTracks = []
topUris = []
elapsedTimeList = []
print('Unique URI List Length:', len(uniqueUriList))
for i in range (len(uniqueUriList)):
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
	rank.append(i+1)
	topTracks.append(topTrackIntermediate)
	topArtistsFromTracks.append(topTrackArtistIntermediate)
	streamsFromTracks.append(uriList.count(topUriIntermediate))
	topUris.append(topUriIntermediate)
	uriList = [i for i in uriList if i != topUriIntermediate]
	elapsedTime = (time.time() - start_timer_sec)
	elapsedTimeList.append(elapsedTime)
	print(i, ('--- %s seconds ---' % elapsedTime), 'difference = ',  elapsedTimeList[i] - elapsedTimeList[i-1])

topTracksDf = pd.DataFrame(list(zip(rank, topTracks, topArtistsFromTracks, streamsFromTracks, topUris)), columns = ['Rank', 'Track', 'Artist', 'Streams', 'URI'])
display(topTracksDf.to_string(index = False))
print('--- %s seconds ---' % (time.time() - start_timer_sec))
topTracksDf.to_excel(f'{outputPath}/topTracksDf.xlsx', index = False)
end_time = datetime.now()
end_time = end_time.strftime("%H:%M:%S")
print('Start Time:', start_time)
print('End Time:', end_time)
