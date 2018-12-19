import os
import unittest
from audio_album import get_files_from_dir
from sound_analyzer import Analyzer


class SoundAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer(get_files_from_dir(os.getcwd()+'\\test_audio_files'))

    def test_same(self):
        mask = os.getcwd()+'\\test_audio_files\\{}.mp3'
        result = {mask.format(1), mask.format(2), mask.format(3), mask.format(4)}
        self.assertSetEqual(set(self.analyzer.get_unique()), result)
