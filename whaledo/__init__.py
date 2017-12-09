#!/usr/bin/env python

# Example usage:
# $ git clone https://github.com/rubygems/rubygems.git
# $ cd rubygems
# $ whaledo rgdev rake test # Run `rake test` in the whaledo/rgdev image.

import os
import sys
import subprocess

### Commands ###

def run(argv):
    if len(argv) == 1:
        # lol this is a fucking Docker container because I'm a smartass.
        argv += ["help"]

    _, repo, *command = argv

    if not "/" in repo:
        repo = "whaledo/" + repo

    mounts = ["-v", os.getcwd() + ":/tmp/work"]
    user_id = subprocess.check_output(["id", "-u"]).strip()
    subprocess.call(["docker", "pull", repo])
    subprocess.call(["docker", "run", "--rm", "-it", *mounts, "-w", "/tmp/work", "-u", user_id, repo, *command])

def main():
    run(sys.argv)

if __name__ == '__main__':
    main()
