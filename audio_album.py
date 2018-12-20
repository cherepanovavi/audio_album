import os
from audio_objects import Song, Album, Artist, Genre, Playlist
from sound_analyzer import Analyzer


class AudioAlbum:
    def __init__(self, dir_path):
        if dir_path == "":
            raise ValueError
        self.dir_path = dir_path
        self.file_names = {}
        self.songs = []
        self.next_id = len(self.songs)
        self.songs_titles = {}
        self.album_titles = {}
        self.artist_titles = {}
        self.albums = []
        self.artists = []
        self.playlists = []
        self.playlists_titles = {}
        self.song_playlists = {}
        self.genres_titles = {}
        self.genres = []
        self.files = self.get_unique_files()
        self.get_songs()
        self.group_by_albums_and_artists()
        self.sort_everything()
        self.songs_id = {}
        self.count_songs_id()

    def update(self):
        self.files = self.get_unique_files()
        self.get_songs()
        self.group_by_albums_and_artists()
        self.sort_everything()
        self.songs_id = {}
        self.count_songs_id()

    def add_songs_to_playlist(self, songs, playlist):
        for song in songs:
            if not self.add_song_to_playlist(song, playlist):
                return False
        return True

    def add_song_to_playlist(self, song, playlist):
        if song in self.songs:
            if playlist in self.song_playlists[song]:
                return False
            if playlist in self.playlists:
                self.song_playlists[song].add(playlist)
            else:
                self.add_playlist(playlist.title, playlist.songs)
            playlist.add_song(song)
            return True
        else:
            raise ValueError

    def count_songs_id(self):
        for song in self.songs:
            self.songs_id[song.id] = song

    def add_playlist(self, title, song_list=None):
        if title in self.playlists_titles:
            return False
        if song_list is None:
            song_list = []
        pl = Playlist(title, song_list)
        for song in song_list:
            self.song_playlists[song].add(pl)
        self.playlists.append(pl)
        self.playlists_titles[pl.title] = pl
        return pl

    def group_by_albums_and_artists(self):
        for song in self.songs:
            self.add_song_to_groups(song)

    def add_song_to_groups(self, song):
        alb = add_song_to_group(song, song.album, self.album_titles, self.albums, lambda s: Album(s.album, s.artist))
        add_song_to_group(song, song.artist, self.artist_titles, self.artists, lambda s: Artist(s.artist), alb)
        add_song_to_group(song, song.genre, self.genres_titles, self.genres, lambda s: Genre(s.genre))

    def sort_everything(self):
        sort_by_title(self.artists)
        sort_by_title(self.albums)
        for album in self.albums:
            sort_by_track_num(album.songs)
        for artist in self.artists:
            sort_by_title(artist.songs)
            sort_by_title(artist.albums)
        sort_by_title(self.songs)

    def get_songs(self):
        i = 0
        for file in self.files:
            file_name = self.file_names[file]
            song = Song(self, file, file_name, i)
            self.songs.append(song)
            self.songs_titles[song.title] = song
            self.song_playlists[song] = set()
            i += 1

    def get_unique_files(self):
        audio_files = get_files_from_dir(self.dir_path)
        paths = audio_files[0]
        self.file_names = audio_files[1]
        a = Analyzer(paths)
        return a.get_unique()

    def add_song(self, song_file, file_name):
        song = Song(self, song_file, file_name, self.next_id)
        self.songs.append(song)
        self.songs_titles[song.title] = song
        self.song_playlists[song] = set()
        self.add_song_to_groups(song)
        self.sort_everything()
        self.songs_id[song.id] = song
        return song

    def delete_song_from_playlist(self, song, playlist):
        if song in self.songs:
            if playlist in self.song_playlists[song]:
                delete_song_from_group(song, playlist.title, self.playlists_titles, self.playlists)
                self.song_playlists[song].remove(playlist)
            else:
                raise ValueError
        else:
            raise ValueError

    def delete_song(self, song):
        self.songs.remove(song)
        self.songs_titles.pop(song.title)
        self.songs_id.pop(song.id)
        delete_song_from_group(song, song.album, self.album_titles, self.albums)
        delete_song_from_group(song, song.artist, self.artist_titles, self.artists)
        delete_song_from_group(song, song.genre, self.genres_titles, self.genres)
        for playlist in self.song_playlists[song]:
            delete_song_from_group(song, playlist.title, self.playlists_titles, self.playlists)
        self.song_playlists.pop(song)

    def delete_playlist(self, playlist):
        if playlist in self.playlists:
            for song in playlist.songs:
                self.song_playlists[song].remove(playlist)
            self.playlists.remove(playlist)
            self.playlists_titles.pop(playlist.title)
        else:
            raise ValueError


def sort_by_title(objects):
    objects.sort(key=lambda s: s.title)


def sort_by_track_num(songs):
    songs.sort(key=lambda s: s.number)


def add_song_to_group(song, song_group, group_dict, group_list, create_group, *args):
    if song_group not in group_dict.keys():
        tag = create_group(song)
        group_dict[song_group] = tag
        group_list.append(tag)
    else:
        tag = group_dict[song_group]
    tag.add_song(song, *args)
    return tag


def delete_song_from_group(song, group_title, group_dict, group_list):
    group = group_dict[group_title]
    group.delete_song(song)
    if len(group.songs) == 0 and type(group) != Playlist:
        group_list.remove(group)
        group_dict.pop(group_title)


def get_files_from_dir(top_dir_path):
    paths = []
    file_names = {}
    for directory in os.walk(top_dir_path):
        for file in directory[2]:
            dir_path = directory[0]
            if file.endswith(".mp3"):
                path = os.path.join(dir_path, file)
                paths.append(path)
                file_names[path] = file
    return paths, file_names
