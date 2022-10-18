from flask import Flask, render_template, request, session
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import pandas as pd
import numpy as np
from joblib import load
import sklearn
#from flask_session import flask.session
app = Flask(__name__)
app.secret_key = '24'

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    return render_template('home.html')
@app.route('/resume', methods = ['GET', 'POST'])
def resume():
    return render_template('resume.html')
@app.route('/moods', methods = ['GET', 'POST'])
def project():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html')
    elif request_type_str == 'POST':
        str = moodPredictor(request.form["artist_name"],  request.form["song_title"])
        session['str'] = 'this_string' #tbd
        #return redirect(url_for('result')) #tbd
        return render_template("result.html", result = str)
        #return str
@app.route('/result', methods = ['GET', 'POST']) #tbd
def result(): #tbd
    result = session.get('this_string', None) #tbd
    return render_template("result.html",result = result) #tbd

@app.route('/projects', methods = ['GET', 'POST'])
def projects():
    return render_template('all_projects.html')

def searchSong(artist, title):
    clientID = #######
    clientSecret = #######
    ccm = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
    sp = spotipy.Spotify(client_credentials_manager=ccm)
    query = f"artist:%{artist} track:%{title}"
    results = sp.search(query, type="track", limit=1)
    return results['tracks']['items'][0]['uri']

def predictMood(uri):
    model = load('improved_model.joblib')
    scaler = load('improved_scaler.joblib')
    clientID = ######
    clientSecret = #####
    ccm = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
    sp = spotipy.Spotify(client_credentials_manager=ccm)
    song_features = sp.audio_features(uri)[0]
    features_column = pd.DataFrame.from_dict(song_features, orient = 'index')
    features_row = features_column.T
    trim_row = features_row[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']]
    trim_row = scaler.transform(trim_row)
    return model.predict(trim_row)

def moodPredictor(artist, title):
    try:
        prediction = (predictMood(searchSong(artist, title)))[0]
        x = f'It looks like this song is {prediction}!'
    except:
        x = "Oops! I couldn't find that song. Did you spell everything right?"
    return x


