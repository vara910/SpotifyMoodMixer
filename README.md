# SpotifyMoodMixer
SpotifyMoodMixer is a web application that leverages the Spotify API to provide personalized music recommendations based on users' mood preferences. Users can select their emotional state—be it happy, sad, or relaxed—and the app suggests tracks from various genres, including English, Hindi, and Telugu. 
# SpotifyMoodMixer

## Description

**SpotifyMoodMixer** is a web application that offers personalized music recommendations based on your mood. Using the Spotify API, the app allows users to select their emotional state—such as happy, sad, or relaxed—and provides tailored song suggestions in English, Hindi, and Telugu. 

## Features

- **Mood-Based Recommendations**: Choose your mood to receive curated playlists.
- **Multi-Language Support**: Enjoy song recommendations in English, Hindi, and Telugu.
- **User-Friendly Interface**: Designed with a professional and colorful layout for an engaging experience.

## Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Flask
- **API Integration**: Spotify Web API
- **Dependencies**: `Flask`, `Spotipy`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/SpotifyMoodMixer.git
   
THE MAIN EXECUTABLE CODE:
1.App.py
from flask import Flask, render_template, request, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Spotify API credentials
SPOTIPY_CLIENT_ID = "7f5c4cfa998d4d489066bc457135e5ee"
SPOTIPY_CLIENT_SECRET = "29421c87ee8448edb32a25343d67f1db"
SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"
scope = "user-library-read user-read-recently-played"

app.secret_key = "h29Je34yHt6Hks3k83jNs8"  # Random secret key

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                         client_secret=SPOTIPY_CLIENT_SECRET,
                         redirect_uri=SPOTIPY_REDIRECT_URI,
                         scope=scope)

@app.route('/')
def index():
    return render_template('home.html')  # Renders the homepage

@app.route('/login')
def login():
    return redirect(sp_oauth.get_authorize_url())

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect(url_for('index'))

def get_spotify():
    token_info = session.get('token_info', {})
    if not token_info or 'access_token' not in token_info:
        return None
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp

def get_tracks_based_on_mood(mood):
    sp = get_spotify()
    if sp is None:
        return []

    # Define seed genres and artists for different moods
    seeds = {
        'happy': {
            'genres': ['pop', 'dance'],
            'artists': ['4gzpq5DPGxSnKnm5B4q2kX'],  # Example artist IDs
        },
        'sad': {
            'genres': ['sad', 'chill'],
            'artists': ['2T6glwKMGsDO46X5IwaZUw'],
        },
        'energetic': {
            'genres': ['rock', 'dance'],
            'artists': ['6i4wWmtfbtbxM8N1M4D9X8'],
        },
        'relaxed': {
            'genres': ['acoustic', 'soft'],
            'artists': ['7jOl0StImH8iS8j0rXc5Fw'],
        },
    }

    # Get the seeds based on mood
    seed_data = seeds.get(mood, {})
    seed_genres = seed_data.get('genres', [])
    seed_artists = seed_data.get('artists', [])

    try:
        recommendations = sp.recommendations(seed_genres=seed_genres, seed_artists=seed_artists, limit=10)
        tracks = []
        for track in recommendations['tracks']:
            tracks.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'link': track['external_urls']['spotify']
            })
        return tracks
    except Exception as e:
        print(f"Error retrieving recommendations: {e}")
        return []

@app.route('/recommend', methods=['POST'])
def recommend():
    mood = request.form.get('mood')

    # Get tracks based on mood
    results = get_tracks_based_on_mood(mood)

    # Display the recommended songs
    return render_template('recommendations.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

2.Spotify_api.py:
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "7f5c4cfa998d4d489066bc457135e5ee"
SPOTIPY_CLIENT_SECRET = "29421c87ee8448edb32a25343d67f1db"
SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                         client_secret=SPOTIPY_CLIENT_SECRET,
                         redirect_uri=SPOTIPY_REDIRECT_URI)

def get_spotify(token_info):
    """Create a Spotify client using the provided token info."""
    return spotipy.Spotify(auth=token_info['access_token'])

def get_tracks_based_on_mood(mood, token_info):
    """Retrieve tracks from Spotify based on the user's mood."""
    sp = get_spotify(token_info)
    
    # Define seed genres and artists for different moods
    seeds = {
        'happy': {
            'genres': ['pop', 'dance'],
            'artists': ['4gzpq5DPGxSnKnm5B4q2kX'],  # Example artist IDs
        },
        'sad': {
            'genres': ['sad', 'chill'],
            'artists': ['2T6glwKMGsDO46X5IwaZUw'],
        },
        'energetic': {
            'genres': ['rock', 'dance'],
            'artists': ['6i4wWmtfbtbxM8N1M4D9X8'],
        },
        'relaxed': {
            'genres': ['acoustic', 'soft'],
            'artists': ['7jOl0StImH8iS8j0rXc5Fw'],
        },
    }

    # Get the seeds based on mood
    seed_data = seeds.get(mood, {})
    seed_genres = seed_data.get('genres', [])
    seed_artists = seed_data.get('artists', [])

    try:
        recommendations = sp.recommendations(seed_genres=seed_genres, seed_artists=seed_artists, limit=10)
        tracks = []
        for track in recommendations['tracks']:
            tracks.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'link': track['external_urls']['spotify']
            })
        return tracks
    except Exception as e:
        print(f"Error retrieving recommendations: {e}")
        return []
