from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from eyed3 import id3
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
        self.tags = MP3File(file).get_tags()
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

    def change_id3_tags(self, dir_tags):
        tag = id3.Tag()
        tag.parse(self.file)
        tag.title = dir_tags['title']
        tag.album = dir_tags['album']
        tag.artist = dir_tags['artist']
        tag.save(self.file)

    def change_id3_tags(self, dir_tags, version):
        tag = MP3File(self.file)
        if version == 2:
            tag.set_version(VERSION_2)
        else:
            tag.set_version(VERSION_1)
        tag.artist = dir_tags['Artist']
        tag.album = dir_tags['Album']
        tag.song = dir_tags['Title']
        tag.track = dir_tags['Track number']
        # tag.comment = dir_tags['Comments']
        tag.year = dir_tags['Date']
        tag.genre = dir_tags['Genre']
        if version == 2:
            tag.composer = dir_tags['Composer']
            tag.copyright = dir_tags['Copyright']
            tag.url = dir_tags['URL']
            tag.publisher = dir_tags['Publisher']
        tag.save()


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
