import math
import time
import spotipy
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import tree
import spotipy.util as util
from datetime import datetime
import matplotlib.pyplot as plt
#from dtreeviz.trees import dtreeviz
from imblearn.over_sampling import SMOTE
from requests.exceptions import ReadTimeout
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score, plot_confusion_matrix
start_time = datetime.now()
start_time = start_time.strftime("%H:%M:%S")
print('Start Time:', start_time)

myData = pd.read_excel(r'')
spotifyData = pd.read_excel(r'')
outputPath = r''

spotifyDataUriList = spotifyData['URI']
myData = myData[myData.Streams >= 25] #keeping songs with over 25 streams
#myData = myData.iloc[:1500] #keeping first 1500 songs
myDataUriList = myData['URI']
print('Unique songs before dropping ones in common with my top streams:', len(spotifyData))

# only need to run once. cleaned data is sent to excel after first run
#for i in range (len(spotifyDataUriList)):
#	for j in range (len(myDataUriList)):
#		if (myDataUriList[j] == spotifyDataUriList[i]):
#			spotifyData.drop([i], axis = 0, inplace = True)
#
#spotifyData.reset_index(inplace = True, drop = True)
#spotifyData.to_excel(f'{outputPath}/uriCleanedSpotifyData.xlsx', index = False)

spotifyData = pd.read_excel(r'/Users/martinweiss/Documents/Python/Random Python Scripts/Spotify/uriCleanedSpotifyData.xlsx')
print('Songs after dropping ones in common with my top streams:', len(spotifyData))

myTopStream = [1 for i in range(len(myData))]
myData['My Top Stream'] = myTopStream
myData = myData.drop(['Rank', 'Track', 'Artist', 'Streams'], axis=1)
spotifyTopStream = [0 for i in range(len(spotifyData))]
spotifyData['My Top Stream'] = spotifyTopStream
allData = pd.concat([myData, spotifyData], axis = 0)
allData = allData.sample(frac = 1)

X = allData.drop(columns=['URI', 'My Top Stream'])
y = allData['My Top Stream']
X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size = 0.10, random_state = 42)
y_train = pd.Series(y_train)
y_test = pd.Series(y_test)
oversample = SMOTE()
X_train, y_train = oversample.fit_resample(X, y) 
#featureNames = [col for col in X_train.columns]

dtc = DecisionTreeClassifier(max_depth = 40).fit(X_train, y_train)
accuracyScore = cross_val_score(dtc, X_train, y_train, cv = 10, scoring = 'accuracy')
accuracyScore = np.mean(accuracyScore)
print('Mean accuracy score from training: ', accuracyScore)
#plot_confusion_matrix(dtc, X_train, y_train)
dtPrediction = dtc.predict(X_test)
dtPrediction = dtPrediction.tolist()

cf_matrix = confusion_matrix(y_test, dtPrediction)
group_names = ['True Negative','False Positive','False Negative', 'True Positive']
group_counts = ['{0:0.0f}'.format(value) for value in cf_matrix.flatten()]
group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten()/np.sum(cf_matrix)]
labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
labels = np.asarray(labels).reshape(2,2)
cmPlot = plt.figure()
sns.heatmap(cf_matrix, annot = labels, fmt = '', cmap = 'Blues', xticklabels = ['Songs I would not like', 'Songs I would like'], yticklabels = ['Not a Top Stream', 'Top Stream'])
plt.title('Confusion Matrix (test data and prediction)')
plt.xlabel('Predicted New Liked Songs', rotation = 'horizontal')
plt.ylabel('My Top Streamed Songs')
#plt.show()

print('R2:', r2_score(y_test, dtPrediction))
print('Accuracy on test y_test and prediction:', accuracy_score(y_test, dtPrediction))
print('MAE:', mean_absolute_error(y_test, dtPrediction))
#print('New songs I should like based on my top streamed songs (test set (10%)):', dtcPrediction.count(1))

print('Now using entire Spotify data set.')
predictionProbabilities = dtc.predict_proba(spotifyData.drop(['URI','My Top Stream'], axis = 1))
threshold = 0.075 #higher = less songs, lower = more songs
songPredictions = [1 if predictionProbabilities[i][1] > threshold else 0 for i in range(len(predictionProbabilities))]
spotifyData['Recommended Song'] = songPredictions
print('Number of recommend songs:', songPredictions.count(1))
newUris = [spotifyData['URI'][i] for i in range (len(spotifyData)) if spotifyData['Recommended Song'][i] == 1]

cid = ''
secret = ''
username = ''
redirect_uri = 'http://localhost:8888/callback'
scope = 'user-top-read playlist-modify-private playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id = cid, client_secret = secret, redirect_uri = redirect_uri)

if token:
	sp = spotipy.Spotify(auth = token)

mlPlaylistName = 'Python Machine Learning Made Playlist'
makePlaylist = sp.user_playlist_create(username, mlPlaylistName, description = 'This playlist was made by my Python machine learning algorithm and populated with the Spotify API.')

playlists = sp.user_playlists(username)
myPlaylistUris = [playlist['id'] for playlist in playlists['items']]
myPlaylistNames = [playlist['name'] for playlist in playlists['items']]
playlistsDf = pd.DataFrame({'URI': myPlaylistUris, 'Name': myPlaylistNames})
playlist_id = [playlistsDf['URI'][i] for i in range (len(playlistsDf)) if (playlistsDf['Name'][i] == mlPlaylistName)][0]

count = 0
mlMadePlaylist = []
while count < len(newUris):
	mlMadePlaylist += sp.user_playlist_add_tracks(username, playlist_id, tracks = newUris[count:count + 50])
	count += 50

#Mean accuracy score from training:  0.9335411583988436
#R2: 0.907462249414215
#Accuracy on test y_test and prediction: 0.9973624054861966
#MAE: 0.0026375945138034113
#Number of recommend songs: 161