import os
import unittest
from audio_album import get_files_from_dir
from sound_analyzer import Analyzer


class SoundAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer(get_files_from_dir(os.getcwd() + os.sep + 'test_audio_files')[0])

    def test_same(self):
        mask = '{}{}test_audio_files{}{}.mp3'.format(os.getcwd(), os.sep, os.sep, '{}')
        result = {mask.format(1), mask.format('subdirectory{}subdirectory_2{}2'.format(os.sep, os.sep)),
                  mask.format('subdirectory{}3'.format(os.sep)), mask.format(4)}
        self.assertSetEqual(set(self.analyzer.get_unique()), result)
