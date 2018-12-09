import unittest
import os
from audio_album import AudioAlbum


class AudioAlbumsTest(unittest.TestCase):
    def setUp(self):
        self.au_alb = AudioAlbum(os.getcwd()+'\\test_audio_files')

    def test_albums_init(self):
        self.assertTrue(len(self.au_alb.albums) == 3)
        l = ['Fighting The World', 'Gods Of War', 'The Game']
        i = 0
        for album in self.au_alb.albums:
            self.assertEqual(album.title, l[i])
            i += 1
        g = ['King Of Kings', 'Army Of The Dead , Part 1']
        i = 0
        for song in self.au_alb.album_titles['Gods Of War'].songs:
            self.assertEqual(g[i], song.title)
            i += 1

    def test_songs_init(self):
        self.assertTrue(len(self.au_alb.songs) == 4)
        l = ['Army Of The Dead , Part 1', 'Carry On', "Don't Try Suicide", 'King Of Kings']
        i = 0
        for song in self.au_alb.songs:
            self.assertEqual(song.title, l[i])
            self.assertEqual(self.au_alb.songs_id[song.id], song)
            i += 1

    def test_artists_init(self):
        self.assertEqual(len(self.au_alb.artists), 2)
        l = ['Manowar', 'Queen']
        m_songs = ['Army Of The Dead , Part 1', 'Carry On', 'King Of Kings']
        m_albums = ['Fighting The World', 'Gods Of War']
        q_songs = ["Don't Try Suicide"]
        q_albums = ['The Game']
        i = 0
        for artist in self.au_alb.artists:
            self.assertEqual(artist.title, l[i])
            i += 1
        i = 0
        for song in self.au_alb.artist_titles['Manowar'].songs:
            self.assertEqual(m_songs[i], song.title)
            i += 1
        i = 0
        for album in self.au_alb.artist_titles['Manowar'].albums:
            self.assertEqual(m_albums[i], album.title)
            i += 1
        i = 0
        for song in self.au_alb.artist_titles['Queen'].songs:
            self.assertEqual(q_songs[i], song.title)
            i += 1
        i = 0
        for album in self.au_alb.artist_titles['Queen'].albums:
            self.assertEqual(q_albums[i], album.title)
            i += 1

    def test_add_song_to_playlist(self):
        title = 'playlist'
        self.au_alb.add_playlist(title)
        pl = self.au_alb.playlists_titles[title]
        song = self.au_alb.songs[0]
        self.au_alb.add_song_to_playlist(song, pl)
        self.assertTrue(pl in self.au_alb.song_playlists[song.title])
        self.assertTrue(song in pl.songs)

    def test_add_delete_song(self):
        song = self.au_alb.songs_titles["Don't Try Suicide"]
        self.au_alb.delete_song(song)
        self.assertTrue("Don't Try Suicide" not in self.au_alb.songs_titles.keys())
        self.assertTrue("Queen" not in self.au_alb.artist_titles.keys())
        self.assertTrue("The Game" not in self.au_alb.album_titles.keys())
        self.au_alb.add_song(os.getcwd()+'\\test_audio_files\\4.mp3', '4.mp3')
        self.assertTrue("Don't Try Suicide" in self.au_alb.songs_titles.keys())
        self.assertTrue("Queen" in self.au_alb.artist_titles.keys())
        self.assertTrue("The Game" in self.au_alb.album_titles.keys())

    def test_delete_song_2(self):
        song = self.au_alb.songs_titles["Carry On"]
        self.au_alb.delete_song(song)
        self.assertTrue("Carry On" not in self.au_alb.songs_titles.keys())
        self.assertTrue("Manowar" in self.au_alb.artist_titles.keys())
        self.assertTrue("Fighting The World" not in self.au_alb.album_titles.keys())
