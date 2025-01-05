import requests, os, csv, sys
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import SPREADSHEET_ID, CLIENT_ID, CLIENT_SECRET, PATH
import spotipy

# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Function to download a Google Sheet as a CSV file
def getGoogleSeet(SPREADSHEET_ID, outDir, outFile):
    # Construct the URL to export the Google Sheet as a CSV file
    url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv'
    response = requests.get(url)  # Send a GET request to the URL
    
    if response.status_code == 200:
        # If the request is successful, construct the file path
        filepath = os.path.join(outDir, outFile)
        # Open the file in write-binary mode and save the content
        with open(filepath, 'wb') as f:
            f.write(response.content)
            print('CSV file saved to: {}'.format(filepath))
        return filepath  # Return the file path
    else:
        # If the request fails, print an error message and exit
        print(f'Error downloading Google Sheet: {response.status_code}')
        sys.exit(1)

# Function to load a CSV file into a dictionary
def load_csv_to_dict(filepath):
    data = {}  # Initialize an empty dictionary to store the data
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # Create a CSV reader object
        for i, row in enumerate(csv_reader):
            data[i] = row  # Add each row to the dictionary with the index as the key
    return data  # Return the populated dictionary

# Function to get Spotify track ID for a song
def get_spotify_track_id(artist, track):
    query = f"track:{track} artist:{artist}"
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        return track_id
    return None

# Function to extract Spotify track ID from URL
def extract_spotify_track_id(url):
    if url:
        return url.split('/')[-1]
    return None

# Create a cache for Spotify track IDs
spotify_cache = {}

def update_csv_with_spotify_track_ids(data_dict, filepath):
    not_found = []
    with open(filepath, mode='w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i, row in data_dict.items():
            if len(row) == 4:
                track, artist, year, url = row
                spotify_track_id = extract_spotify_track_id(url)
            else:
                track, artist, year = row
                spotify_track_id = None

            # Check cache before making an API call
            if not spotify_track_id:
                cache_key = (artist, track)
                if cache_key in spotify_cache:
                    spotify_track_id = spotify_cache[cache_key]
                else:
                    spotify_track_id = get_spotify_track_id(artist, track)
                    if spotify_track_id:
                        spotify_cache[cache_key] = spotify_track_id

            if spotify_track_id:
                csv_writer.writerow(row[:3] + [spotify_track_id])  # Write row with Spotify Track ID and URL

            else:
                csv_writer.writerow(row[:3] + [""])  # Write row with empty Spotify Track ID
                not_found.append(f"{track} - {artist}")

    if not_found:
        print("Songs not found on Spotify:")
        for song in not_found:
            print(song)

# Download the CSV file from Google Sheets and load it into a dictionary
csv_filepath = getGoogleSeet(SPREADSHEET_ID, PATH, "Hitster.csv")
data_dict = load_csv_to_dict(csv_filepath)

# Update CSV file with Spotify track IDs
update_csv_with_spotify_track_ids(data_dict, csv_filepath)