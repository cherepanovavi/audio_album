from eyed3 import id3


class Song:
    def __init__(self, file, i):
        self.id = i
        self.file = file
        tag = id3.Tag()
        tag.parse(file)
        self.title = tag.title
        self.album = tag.album
        self.artist = tag.artist
        self.genre = str(tag.genre)
        # self.genre = tag.genre.name
        self.number = tag.track_num[0]

    def __hash__(self):
        return self.title.__hash__() ^ self.artist.__hash__() ^ self.album.__hash__()

    def __eq__(self, other):
        return self.title == other.title and self.artist == other.artist and self.album == self.album


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

    def __hash__(self):
        return self.title.__hash__() ^ self.artist_name.__hash__()

    def __eq__(self, other):
        return self.title == other.title and self.artist_name == other.artist_name
