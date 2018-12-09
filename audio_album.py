import os
from audio_objects import Song, Album, Artist, Genre, Playlist


def sort_by_title(objects):
    objects.sort(key=lambda s: s.title)


def sort_by_track_num(songs):
    songs.sort(key=lambda s: s.number)


def add_song_to_group(song, song_tag, tag_dict, tag_list, create_tag, *args):
    if song_tag not in tag_dict.keys():
        tag = create_tag(song)
        tag_dict[song_tag] = tag
        tag_list.append(tag)
    else:
        tag = tag_dict[song_tag]
    tag.add_song(song, *args)
    return tag


def delete_song_from_group(song, group_title, group_dict, group_list):
    group = group_dict[group_title]
    group.delete_song(song)
    if len(group.songs) == 0 and type(group) != Playlist:
        group_list.remove(group)
        group_dict.pop(group_title)


class AudioAlbum:
    def __init__(self, dir_path):
        if dir_path == "":
            raise ValueError
        self.dir_path = dir_path
        self.audio_files = []
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
        self.get_songs()
        self.group_by_albums_and_artists()
        self.sort_everything()
        self.songs_id = {}
        self.count_songs_id()
        # self.debug()

    def update(self):
        self.get_songs()
        self.get_tags()
        self.group_by_albums_and_artists()
        self.sort_everything()
        self.songs_id = {}
        self.count_songs_id()

    def add_songs_to_playlist(self, songs, playlist):
        for song in songs:
            self.add_song_to_playlist(song, playlist)

    def add_song_to_playlist(self, song, playlist):
        if song in self.songs and playlist in self.playlists:
            self.song_playlists[song.title].append(playlist)
            playlist.add_song(song)
        elif playlist not in self.playlists:
            self.add_playlist(playlist.title, playlist.songs)
        else:
            raise ValueError

    def count_songs_id(self):
        for song in self.songs:
            self.songs_id[song.id] = song

    def add_playlist(self, title, song_list=[]):
        pl = Playlist(title, song_list)
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
        for file in os.listdir(self.dir_path):
            if file.endswith(".mp3"):
                song = Song(self, os.path.join(self.dir_path, file), file, i)
                self.songs.append(song)
                self.songs_titles[song.title] = song
                self.song_playlists[song.title] = []
                i += 1

    def add_song(self, song_file, file_name):
        song = Song(self, song_file, file_name, self.next_id)
        self.songs.append(song)
        self.songs_titles[song.title] = song
        self.song_playlists[song.title] = []
        self.add_song_to_groups(song)
        self.sort_everything()
        self.songs_id[song.id] = song
        return song

    def delete_song(self, song):
        self.songs.remove(song)
        self.songs_titles.pop(song.title)
        self.songs_id.pop(song.id)
        delete_song_from_group(song, song.album, self.album_titles, self.albums)
        delete_song_from_group(song, song.artist, self.artist_titles, self.artists)
        delete_song_from_group(song, song.genre, self.genres_titles, self.genres)
        for playlist in self.song_playlists[song.title]:
            delete_song_from_group(song, playlist.title, self.playlists_titles, self.playlists)
        self.song_playlists.pop(song.title)
