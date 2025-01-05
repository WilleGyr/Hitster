import spotipy, requests
from spotipy.oauth2 import SpotifyOAuth
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, PATH

def scope():
    # Spotify OAuth setup
    scope = "user-modify-playback-state user-read-playback-state"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope
    ))

    return sp

sp = scope()

# Function to play a specific track
def play_song(track_id, device_id=None):
    track_uri = f"spotify:track:{track_id}"
    try:        
        # Add device_id if targeting a specific device
        if device_id:
            sp.start_playback(device_id=device_id, uris=[track_uri])
            download_cover_art(track_id)
        else:
            sp.start_playback(uris=[track_uri])
            download_cover_art(track_id)
    except Exception as e:
        print(f"Error: {e}")

# Function to download the cover art of a specific track
def download_cover_art(track_id, filename=f'{PATH}cover.png'):
    try:
        track = sp.track(track_id)
        cover_url = track['album']['images'][0]['url']
        response = requests.get(cover_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download cover art: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def seek_forward(seconds):
    current_playback = sp.current_playback()
    if current_playback and current_playback['is_playing']:
        current_position = current_playback['progress_ms']
        new_position = current_position + (seconds * 1000)
        sp.seek_track(new_position)

def seek_backward(seconds):
    current_playback = sp.current_playback()
    if current_playback and current_playback['is_playing']:
        current_position = current_playback['progress_ms']
        new_position = max(0, current_position - (seconds * 1000))
        sp.seek_track(new_position)

def set_volume(volume_percent):
    sp.volume(volume_percent)
