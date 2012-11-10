#!/usr/bin/env python
import unittest
import shutil
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import submatcher

base = os.path.abspath(os.path.dirname(__file__))

class Testsubmatcher(unittest.TestCase):

    def setUp(self):
        self.tempdir = base+"/current_run/"
        shutil.copytree(base+"/fixtures", self.tempdir)
        os.chdir(self.tempdir)
        submatcher.verbose = False
        submatcher.dryrun = False
        self.addCleanup(shutil.rmtree, self.tempdir)

    def exists(self, filename):
        return os.path.exists(filename)

    def test_simple(self):
        self.assertFalse(self.exists("mkv_sub/a_movie.sub"), "a_movie.sub should not exist yet")
        self.assertTrue(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should exist")
        submatcher.submatcher(self.tempdir)
        self.assertTrue(self.exists("mkv_sub/a_movie.sub"), "a_movie.sub should exist")
        self.assertFalse(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should have been moved")

    def test_is_recursive(self):
        self.assertFalse(self.exists("subdir/avi_srt/leven.srt"), "leven.srt should not exist yet")
        self.assertTrue(self.exists("subdir/avi_srt/shtein.srt"), "shtein.srt should exist")
        submatcher.submatcher(self.tempdir)
        self.assertTrue(self.exists("subdir/avi_srt/leven.srt"), "leven.srt should exist")
        self.assertFalse(self.exists("subdir/avi_srt/shtein.srt"), "shtein.srt should have been moved")

    def test_defaults_to_current_working_dir(self):
        os.chdir("mkv_sub")
        self.assertFalse(self.exists("a_movie.sub"), "a_movie.sub should not exist yet")
        self.assertTrue(self.exists("some_subs.sub"), "some_subs.sub should exist")
        self.assertTrue(self.exists("../subdir/avi_srt/shtein.srt"), "file above cwd should exist prior to call")
        self.assertFalse(self.exists("../subdir/avi_srt/shtein.avi"), "movie above cwd shouldn't match subtitle file")
        submatcher.submatcher()
        self.assertTrue(self.exists("a_movie.sub"), "a_movie.sub should exist")
        self.assertFalse(self.exists("some_subs.sub"), "some_subs.sub should have been renamed")

        self.assertTrue(self.exists("../subdir/avi_srt/shtein.srt"), "should not have touched files above cwd")

    def test_can_pass_dir(self):
        self.assertFalse(self.exists("mkv_sub/a_movie.sub"), "a_movie.sub should not exist yet")
        self.assertTrue(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should exist")
        self.assertTrue(self.exists("subdir/avi_srt/shtein.srt"), "file above cwd should exist prior to call")
        self.assertFalse(self.exists("subdir/avi_srt/shtein.avi"), "movie above cwd shouldn't match subtitle file")
        submatcher.submatcher("mkv_sub")
        self.assertTrue(self.exists("mkv_sub/a_movie.sub"), "a_movie.sub should exist")
        self.assertFalse(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should have been renamed")

        self.assertTrue(self.exists("subdir/avi_srt/shtein.srt"), "should not have touched files above cwd")

    def test_dryrun(self):
        submatcher.dryrun = True
        self.assertTrue(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should exist")
        self.assertTrue(self.exists("mkv_sub/a_movie.mkv"), "there should be a matching movie, ready to be matched against")
        submatcher.submatcher("mkv_sub")
        self.assertTrue(self.exists("mkv_sub/some_subs.sub"), "some_subs.sub should still exist")


if __name__ == '__main__':
    unittest.main()
