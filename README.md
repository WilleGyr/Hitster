# Custom Hitster

## Table of Contents
- [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Spotipy Setup](#spotipy-setup)
    - [Usage](#usage)
- [License](#license)

## Getting Started
### Installation
1. Make sure you have **[Python](https://www.python.org/downloads/)** installed
2. Install **[Requests](https://pypi.org/project/requests/)**, **[Spotipy](https://spotipy.readthedocs.io/en/2.24.0/)** and **[PyQt5](https://pypi.org/project/PyQt5/)** by running the following in the command line:
    ```
    $ pip install requests
    $ pip install spotipy
    $ pip install pyqt5
    ```
3. An active **[Spotify Developer account](https://developer.spotify.com/)**
4. A google sheet containing all songs you want to use. In the following format:
    ```
    Song name | Artist | Year
    ```
    Find your **SPREADSHEET_ID** from the Google Sheets url:<br>
    h<span>ttps://docs.goo</span>gle.com/spreadsheets/d/**SPREADSHEET_ID**/edit?gid=0#gid=0 <br>
    Paste your **SPREADSHEET_ID** into `credentials.py`
5. (***Optional***) Replace ```app_logo.png``` with the image of your choice.
6. (***Optional***) Add the path to your current directory to **PATH** in ```credentials.py```.

### Spotipy Setup
1. Browse to **[Spotify for developers](https://developer.spotify.com/dashboard/applications)**
2. Log in with your Spotify account
3. Click on **'Create an app'** and provide the required information
4. After creation, you see your **CLIENT_ID** and you can click on ‘Show client secret` to unhide your **CLIENT_SECRET**
5. Paste your **CLIENT_ID** and **SECRET_ID** into `credentials.py`

### Usage
1. Run ```csv_processor.py``` to create the CSV file containing all your songs.
2. Start playing Hitster by starting ```hitster.py```.
3. **"Ny låt"** will start the next song.
4. **"Klar"** will show the song name, artist and year of the current song.

### Controls
- **Spacebar or Return**: Triggers either "Ny låt" or "Klar" depending on what is visible on screen.
- **Backspace**: Restarts the song from the beginning.
- **Left and right arrow keys**: Skip backward or forward by 10 seconds in the song.

## License
Distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.