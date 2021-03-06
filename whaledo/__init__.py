#!/usr/bin/env python

# Example usage:
# $ git clone https://github.com/rubygems/rubygems.git
# $ cd rubygems
# $ whaledo rgdev rake test # Run `rake test` in the whaledo/rgdev image.

import os
import sys
import subprocess

### Commands ###

def print_help():
    print("Usage: whaledo USER/REPO COMMAND [ARGS...]")
    print("       whaledo WHALEDO_REPO COMMAND [ARGS...]")
    print("")
    print("If you want an official repo, prefix it with \"library/\".")
    print("E.g., to use the official Ruby image, you can do `whaledo library/ruby`.")
    return 0

def pull(argv):
    return subprocess.call(["docker", "pull", argv[2]])

def run(repo, command):
    if not "/" in repo:
        repo = "whaledo/" + repo

    user_id = subprocess.check_output(["id", "-u"]).strip()

    docker_cmd = ["docker", "run", "--rm", "-it"]
    docker_cmd += ["-v", os.getcwd() + ":/tmp/work"]
    docker_cmd += ["-w", "/tmp/work"]
    docker_cmd += ["-u", user_id]

    if os.path.isfile("env.whaledo"):
        docker_cmd += ["--env-file", "env.whaledo"]

    return subprocess.call(docker_cmd + [repo] + command)

def handle(argv):
    commands = {
        "-h": print_help,
        "--help": print_help,
        "help": print_help,
        "pull": pull,
    }

    if len(argv) < 2:
        return print_help()
    elif argv[1] in commands:
        return commands[argv[1]](argv)
    else:
        repo = argv[1]
        command = argv[2:]
        return run(repo, command)

def main():
    return handle(sys.argv)

if __name__ == '__main__':
    returncode = main()
    exit(returncode)
