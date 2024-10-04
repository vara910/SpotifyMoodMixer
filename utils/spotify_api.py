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
