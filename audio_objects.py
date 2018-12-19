from eyed3 import id3
from eyed3.core import Date
from menus import SongMenu, SongPlaylistMenu, PlaylistMenu


def delete_song(group, song):
    if type(song) == Song:
        if song in group.songs:
            group.songs.remove(song)


class Song:
    def __init__(self, audio_album, file, file_name, i):
        self.id = i
        self.file = file
        self.file_name = file_name
        self.tag_v1 = None
        self.tag_v2 = None
        self.tags_v1 = {}
        self.tags_v2 = {}
        self.get_id3_tags()
        tag = id3.Tag()
        tag.parse(file)
        self.title = 'untitled' if tag.title is None else tag.title
        self.album = 'untitled' if tag.album is None else tag.album
        self.artist = 'untitled' if tag.artist is None else tag.artist
        self.genre = 'not stated' if tag.genre is None else tag.genre.name
        self.image_data = None if tag.images.get('') is None else tag.images.get('').image_data
        self.number = 0 if tag.track_num is None else tag.track_num[0]
        self.submenu = lambda: SongPlaylistMenu(audio_album, self)
        self.menu = lambda: SongMenu(audio_album, self)

    def __hash__(self):
        return self.title.__hash__() ^ self.artist.__hash__() ^ self.album.__hash__()

    def __eq__(self, other):
        return self.title == other.title and self.artist == other.artist and self.album == self.album

    def get_id3_tags(self):
        self.tag_v1 = id3.Tag()
        self.tag_v1.parse(self.file, (1, None, None))
        self.tags_v1['Track number'] = [(self.tag_v1.track_num[0], 0, 50)]
        self.tags_v1['Title'] = '' if self.tag_v1.title is None else self.tag_v1.title
        self.tags_v1['Artist'] = '' if self.tag_v1.artist is None else self.tag_v1.artist
        self.tags_v1['Album'] = '' if self.tag_v1.album is None else self.tag_v1.album
        self.tags_v1['Genre'] = None if self.tag_v1.genre is None else self.tag_v1.genre.id
        date = self.tag_v1.recording_date
        self.tags_v1['Date'] = [(date.day, 1, 31), (date.month, 1, 12), (date.year, 1950, 2020)] if date is not None else [(None, 1, 31), (None, 1, 12), (None, 1950, 2020)]
        self.tags_v1['Comments'] = self.tag_v1.comments.get('').text if self.tag_v1.comments.get('') is not None else ''
        self.tag_v2 = id3.Tag()
        self.tag_v2.parse(self.file, (2, None, None))
        self.tags_v2['Track number'] = [(self.tag_v2.track_num[0], 0, 50), (self.tag_v2.track_num[1], 0, 50)]
        self.tags_v2['Disc number'] = [(self.tag_v2.disc_num[0], 0, 100), (self.tag_v2.disc_num[1], 0, 100)]
        self.tags_v2['Title'] = '' if self.tag_v2.title is None else self.tag_v2.title
        self.tags_v2['Artist'] = '' if self.tag_v2.artist is None else self.tag_v2.artist
        self.tags_v2['Album'] = '' if self.tag_v2.album is None else self.tag_v2.album
        self.tags_v2['Album artist'] = '' if self.tag_v2.album_artist is None else self.tag_v2.album_artist
        self.tags_v2['Genre'] = None if self.tag_v2.genre is None else self.tag_v2.genre.id
        date = self.tag_v2.recording_date
        self.tags_v2['Date'] = [(date.day, 1, 31), (date.month, 1, 12), (date.year, 1950, 2020)] if date is not None else [(None, 1, 31), (None, 1, 12), (None, 1950, 2020)]
        self.tags_v2['Comments'] = self.tag_v2.comments.get('').text if self.tag_v2.comments.get('') is not None else ''
        self.tags_v2['Publisher'] = '' if self.tag_v2.publisher is None else self.tag_v2.publisher
        self.tags_v2['Composer'] = '' if self.tag_v2.composer is None else self.tag_v2.composer
        self.tags_v2['BPM'] = [(self.tag_v2.bpm, 0, 10000)]

    def change_id3_tags(self, dir_tags_v1, dir_tags_v2):
        self.tag_v1.track_num = (dir_tags_v1['Track number'][0], None)
        self.tag_v1.title = dir_tags_v1['Title'] if dir_tags_v1['Title'] != '' else None
        self.tag_v1.artist = dir_tags_v1['Artist'] if dir_tags_v1['Artist'] != '' else None
        self.tag_v1.album = dir_tags_v1['Album'] if dir_tags_v1['Album'] != '' else None
        if 0 < dir_tags_v1['Genre'] < 255:
            self.tag_v1.genre = dir_tags_v1['Genre']
        date = dir_tags_v1['Date']
        self.tag_v1.recording_date = Date(date[2], date[1], date[0])
        self.tag_v1.comments.set(dir_tags_v1['Comments'])
        self.tag_v1.save()
        tn = dir_tags_v2['Track number']
        dn = dir_tags_v2['Disc number']
        self.tag_v2.track_num = (tn[0], tn[1])
        self.tag_v2.disc_num = (dn[0], dn[1])
        self.tag_v2.title = dir_tags_v2['Title'] if dir_tags_v2['Title']!= '' else None
        self.tag_v2.artist = dir_tags_v2['Artist'] if dir_tags_v2['Artist']!= '' else None
        self.tag_v2.album = dir_tags_v2['Album'] if dir_tags_v2['Album']!= '' else None
        self.tag_v2.album_artist =  dir_tags_v2['Album artist'] if dir_tags_v2['Album artist']!= '' else None
        if 0 < dir_tags_v2['Genre'] < 255:
            self.tag_v2.genre = dir_tags_v2['Genre']
        date = dir_tags_v2['Date']
        self.tag_v2.recording_date = Date(date[2], date[1], date[0])
        self.tag_v2.comments.set(dir_tags_v1['Comments'])
        self.tag_v2.publisher = dir_tags_v2['Publisher'] if dir_tags_v2['Publisher'] != '' else None
        self.tag_v2.composer = dir_tags_v2['Composer'] if dir_tags_v2['Composer'] != '' else None
        self.tag_v2.bpm = dir_tags_v2['BPM'][0]
        self.tag_v2.save()


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
    def __init__(self, title, song_list=None):
        if song_list is None:
            song_list = []
        self.title = title
        self.songs = song_list
        self.menu = lambda au: PlaylistMenu(self, au)

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
