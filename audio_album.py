import os
from audio_objects import Song, Album, Artist, Genre


def sort_by_title(objects):
    objects.sort(key=lambda s: s.title)


def sort_by_track_num(songs):
    songs.sort(key=lambda s: s.number)


class AudioAlbum:
    def __init__(self, dir_selector):
        if dir_selector == "":
            raise ValueError
        self.audio_files = []
        self.songs = []
        self.album_titles = {}
        self.artist_titles = {}
        self.albums = []
        self.artists = []
        self.playlists = []
        self.genres_titles = {}
        self.genres = []
        self.get_audio_files(dir_selector)
        self.get_tags()
        self.group_by_albums_and_artists()
        self.sort_everything()
        self.songs_id = {}
        self.count_songs_id()
        # self.debug()

    def count_songs_id(self):
        for song in self.songs:
            self.songs_id[song.id] = song

    def add_playlist(self, playlist):
        if type(playlist) == Album:
            self.playlists.append(playlist)

    def get_tags(self):
        i = 0
        for file in self.audio_files:
            self.songs.append(Song(file, i))
            i += 1

    def group_by_albums_and_artists(self):
        for song in self.songs:
            if song.album not in self.album_titles.keys():
                album = Album(song.album, song.artist)
                self.album_titles[song.album] = album
                self.albums.append(album)
            if song.artist not in self.artist_titles.keys():
                artist = Artist(song.artist)
                self.artist_titles[song.artist] = artist
                self.artists.append(artist)
            if song.genre not in self.genres_titles.keys():
                genre = Genre(song.genre)
                self.genres_titles[song.genre] = genre
                self.genres.append(genre)
            genre = self.genres_titles[song.genre]
            genre.add_song(song)
            album = self.album_titles[song.album]
            album.add_song(song)
            self.artist_titles[song.artist].add_song(song, album)

    def sort_everything(self):
        sort_by_title(self.artists)
        sort_by_title(self.albums)
        for album in self.albums:
            sort_by_track_num(album.songs)
        for artist in self.artists:
            sort_by_title(artist.songs)
            sort_by_title(artist.albums)
        sort_by_title(self.songs)

    def get_audio_files(self, dir_selector):
        for file in os.listdir(dir_selector):
            if file.endswith(".mp3"):
                self.audio_files.append(os.path.join(dir_selector, file))

    def debug(self):
        for album in self.albums:
            print(album.title)
            for song in album.songs:
                print('     ' + song.title)
        for artist in self.artists:
            print(artist.title)
            for song in artist.songs:
                print('     ' + song.title)
            print("ALBUMS")
            for album in artist.albums:
                print('   ' + album.title)
