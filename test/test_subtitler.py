#!/usr/bin/env python
import unittest
import shutil
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import subtitler

class TestSubtitler(unittest.TestCase):

    def setUp(self):
        base = os.path.abspath(os.path.dirname(__file__))
        self.tempdir = base+"/current_run/"
        shutil.copytree(base+"/fixtures", self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def exists(self, filename):
        return os.path.exists(self.tempdir+filename)

    def test_simple(self):
        self.assertFalse(self.exists("mkv_sub/a_movie.sub"), "a_movie.sub should not exist yet")
        self.assertTrue(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should exist")
        subtitler.subtitler(self.tempdir)
        self.assertTrue(self.exists("mkv_sub/a_movie.sub"), "a_movie.sub should exist")
        self.assertFalse(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should have been moved")

    @unittest.skip("not implemented")
    def test_verbosity(self):
        pass

    def test_is_recursive(self):
        self.assertFalse(self.exists("subdir/avi_srt/leven.srt"), "leven.srt should not exist yet")
        self.assertTrue(self.exists("subdir/avi_srt/shtein.srt"), "shtein.srt should exist")
        subtitler.subtitler(self.tempdir)
        self.assertTrue(self.exists("subdir/avi_srt/leven.srt"), "leven.srt should exist")
        self.assertFalse(self.exists("subdir/avi_srt/shtein.srt"), "shtein.srt should have been moved")
        pass

    @unittest.skip("not implemented")
    def test_defaults_to_current_working_dir(self):
# change dir
        pass

    @unittest.skip("not implemented")
    def test_can_pass_dir(self):
# change dir
        pass


if __name__ == '__main__':
    unittest.main()
