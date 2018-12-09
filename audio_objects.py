from eyed3 import id3
from song_menu import SongMenu, SongSubMenu


def delete_song(group, song):
    if type(song) == Song:
        if song in group.songs:
            group.songs.remove(song)


class Song:
    def __init__(self, audio_album, file, file_name, i):
        self.id = i
        self.file = file
        self.file_name = file_name
        tag = id3.Tag()
        tag.parse(file)
        self.title = 'untitled' if tag.title is None else tag.title
        self.album = 'untitled' if tag.album is None else tag.album
        self.artist = 'untitled' if tag.artist is None else tag.artist
        self.genre = 'not stated' if tag.genre is None else tag.genre.name
        # self.genre = tag.genre.name
        self.number = 0 if tag.track_num is None else tag.track_num[0]
        self.submenu = lambda: SongSubMenu(audio_album, self)
        self.menu = lambda: SongMenu(audio_album, self)

    def __hash__(self):
        return self.title.__hash__() ^ self.artist.__hash__() ^ self.album.__hash__()

    def __eq__(self, other):
        return self.title == other.title and self.artist == other.artist and self.album == self.album

    def change_id3_tags(self, dir_tags):
        tag = id3.Tag()
        tag.parse(self.file)
        tag.title = dir_tags['title']
        tag.album = dir_tags['album']
        tag.artist = dir_tags['artist']
        tag.save(self.file)


class Artist:
    def __init__(self, title):
        self.title = title
        self.songs = []
        self.albums = []

    def add_song(self, song, album):
        if type(song) == Song:
            if song.artist == self.title:
                self.songs.append(song)
                # защита целостности страдает
                if album not in self.albums:
                    self.albums.append(album)
                return True
            else:
                return False
        else:
            raise ValueError()

    def delete_song(self, song):
        delete_song(self, song)

    def delete_album(self, album):
        if type(album) == Album:
            if album in self.albums:
                album.remove(Song)


class Genre:
    def __init__(self, title):
        self.title = title
        self.songs = []

    def add_song(self,  song):
        if type(song) == Song:
            if song.genre == self.title:
                self.songs.append(song)
                return True
            return False
        raise ValueError

    def delete_song(self, song):
        delete_song(self, song)


class Album:
    def __init__(self, title, artist_name):
        self.title = title
        self.songs = []
        self.artist_name = artist_name

    def add_song(self, song):
        if type(song) == Song:
            if song.album == self.title and song.artist == self.artist_name:
                self.songs.append(song)
                return True
            return False
        raise ValueError()

    def delete_song(self, song):
        delete_song(self, song)

    def __hash__(self):
        return self.title.__hash__() ^ self.artist_name.__hash__()

    def __eq__(self, other):
        return self.title == other.title and self.artist_name == other.artist_name


class Playlist:
    def __init__(self, title, song_list=[]):
        self.title = title
        self.songs = song_list

    def add_song(self, song):
        if type(song) == Song:
            self.songs.append(song)
        else:
            raise ValueError()

    def add_songs(self, song_list):
        for song in song_list:
            self.add_song(song)

    def delete_song(self, song):
        delete_song(self, song)
