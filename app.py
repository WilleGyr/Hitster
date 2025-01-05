import csv, random
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtCore import Qt
from playback_utils import play_song, seek_forward, seek_backward, set_volume, scope
from credentials1 import PATH

sp = scope()

class HitsterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.num = 0
        uic.loadUi(f'{PATH}Hitster.ui', self)
        self.setWindowTitle(f"{PATH}Hitster")  # Set the window title
        self.setWindowIcon(QIcon(f'{PATH}app_logo.png'))
        self.setFixedSize(self.size())
        self.KlarButton.hide()
        self.Spelas.hide()
        self.SongLabel.hide()
        self.ArtistLabel.hide()
        self.YearLabel.hide()
        self.StartaOmButton.hide()
        self.CoverLabel.hide()
        self.Line.hide()
        self.data = self.load_csv(f'{PATH}Hitster.csv')
        self.selected_songs = set()
        self.NyButton.clicked.connect(self.on_ny_button_clicked)
        self.KlarButton.clicked.connect(self.on_klar_button_clicked)
        self.StartaOmButton.clicked.connect(self.on_starta_om_button_clicked)  # Connect the button

    def load_csv(self, filepath):
        data = {}
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                key = row[0]  # Use the first column as the key
                data[key] = row
        return data

    def on_starta_om_button_clicked(self):
        current_song = self.get_current_song()
        if current_song:
            play_song(current_song[3])

    def get_current_song(self):
        # Implement this method to return the current song
        # This is a placeholder implementation
        return self.current_song if hasattr(self, 'current_song') else None

    def get_random_song(self):
        if not self.data:
            return None
        available_keys = list(set(self.data.keys()) - self.selected_songs)
        if not available_keys:
            return None  # No more songs available
        key = random.choice(available_keys)
        self.selected_songs.add(key)  # Add the selected song to the set
        self.current_song = self.data[key]  # Store the current song
        return self.current_song

    def display_song(self, song):
        if song:
            self.SongLabel.setText(song[0])  # First element on SongLabel
            self.ArtistLabel.setText(song[1])  # Second element on ArtistLabel
            self.YearLabel.setText(song[2])  # Third element on YearLabel
            self.SongLabel.show()
            self.ArtistLabel.show()
            self.YearLabel.show()

    def on_ny_button_clicked(self):
        if self.num == 0:
            self.num = 1
        random_song = self.get_random_song()
        self.display_song(random_song)
        self.NyButton.hide()
        self.KlarButton.show()
        self.SongLabel.hide()
        self.ArtistLabel.hide()
        self.YearLabel.hide()
        self.Spelas.show()
        self.StartaOmButton.show()
        self.CoverLabel.hide()
        self.Line.hide()
        play_song(random_song[3])
        self.display_cover_art()

    def display_cover_art(self):
        pixmap = QPixmap(f'{PATH}cover.png')
        scaled_pixmap = pixmap.scaled(self.CoverLabel.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.CoverLabel.setPixmap(scaled_pixmap)

    def on_klar_button_clicked(self):
        self.KlarButton.hide()
        self.NyButton.show()
        self.SongLabel.show()
        self.ArtistLabel.show()
        self.YearLabel.show()
        self.Spelas.hide()
        self.StartaOmButton.hide()
        self.CoverLabel.show()
        self.Line.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.NyButton.isVisible():
                self.on_ny_button_clicked()
            elif self.KlarButton.isVisible():
                self.on_klar_button_clicked()
        if event.key() == Qt.Key_Return:
            if self.NyButton.isVisible():
                self.on_ny_button_clicked()
            elif self.KlarButton.isVisible():
                self.on_klar_button_clicked()
        if event.key() == Qt.Key_Backspace:
            if self.num == 1:
                self.on_starta_om_button_clicked()
        if event.key() == Qt.Key_Right:
            if self.num == 1:
                self.seek_forward()
        if event.key() == Qt.Key_Left:
            if self.num == 1:
                self.seek_backward()
        if event.key() == Qt.Key_Up:
            if self.num == 1:
                self.change_volume(10)
        if event.key() == Qt.Key_Down:
            if self.num == 1:
                self.change_volume(-10)

    def seek_forward(self):
        seek_forward(10)  # Seek forward by 10 seconds

    def seek_backward(self):
        seek_backward(10)  # Seek backward by 10 seconds

    def change_volume(self, delta):
        current_volume = sp.current_playback()['device']['volume_percent']
        new_volume = max(0, min(100, current_volume + delta))
        set_volume(new_volume)