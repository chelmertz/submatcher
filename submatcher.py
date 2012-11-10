#!/usr/bin/env python

import os

subtitles = ["sub", "srt", "idx"]
movies = ["mkv", "avi"]

verbose = False
dryrun = False

def log(msg):
    if verbose:
        print msg

def submatcher(path=None):
    """ Search path for subtitles and rename them to match their movie's counterpart """
    if not path:
        path = "."
    sub = None
    subfile = None
    movie = None
    for root, dirs, files in os.walk(path):
        log("Entering " + root)
        for f in files:
            for s in subtitles:
                if f.endswith("."+s):
                    subfile = f
                    sub = s
                    break
            for m in movies:
                if f.endswith("."+m):
                    movie = f[:-len("."+m)]
                    break
        if sub and movie:
            old = root+"/"+subfile[:-len("."+s)]+"."+sub
            new = root+"/"+movie+"."+sub
            if old is not new:
                log("Renaming %s to %s" % (old, new))
                if not dryrun:
                    os.rename(old, new)

        sub = None
        subfile = None
        movie = None
        map(submatcher, filter(lambda d: d not in (".", ".."), dirs))


if __name__ == "__main__":
    import sys
    path = None
    for arg in sys.argv[1:]:
        if arg == "-v":
            verbose = True
        elif arg in ["-h", "--help"]:
            print """
%s [path] [-v] [-h|--help]

Recursively search through *path* for subtitles and movies, if found,
rename the subtitle so that it matches and can be found by media programs.

    path                  Defaults to .
    -v                    Be verbose
    -h|--help             Show this help
    """ % (sys.argv[0])
            sys.exit(0)
        elif arg in ["-d", "--dry-run"]:
            dryrun = True
        else:
            path = arg
    if not submatcher(path):
        sys.exit(1)
    sys.exit(0)
