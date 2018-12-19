import os
import unittest
from searcher import Searcher
from audio_album import AudioAlbum


class SearcherTest(unittest.TestCase):
    def setUp(self):
        self.au_alb = AudioAlbum(os.getcwd() + '\\test_audio_files')
        self.searcher = Searcher(self.au_alb)

    def test_search(self):
        results = {('Song: King Of Kings', self.au_alb.songs_titles['King Of Kings']),
                   ('Song: Army Of The Dead , Part 1', self.au_alb.songs_titles['Army Of The Dead , Part 1']),
                   ('Album: Gods Of War', self.au_alb.album_titles['Gods Of War'])}
        self.assertSetEqual(results, set(self.searcher.get_search_results('of')))
        self.assertSetEqual(set(), set(self.searcher.get_search_results('Of')))
        self.assertSetEqual(set(), set(self.searcher.get_search_results('OF')))
