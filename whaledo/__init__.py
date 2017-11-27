#!/usr/bin/env python

# whaledo [-h|--help|--version]
# whaledo alias SHORTNAME=LONGNAME # Alias SHORTNAME to the Docker Hub image LONGNAME.
# whaledo unalias SHORTNAME        # Unalias SHORTNAME.
# whaledo LONGNAME COMMAND         # Run command in the Docker image referenced by LONGNAME
# whaledo SHORTNAME COMMAND        # Run COMMAND in the Docker image referenced by the LONGNAME that SHORTNAME is aliased to.
#
# TODO: Figure out how to handle volumes and such.
# NOTE: I am going to be making a repo of Dockerfiles specifically for this, so I am okay using some kind of convention for mounting things instead of making it infinitely tweakable.
#       E.g., always mounting . to /tmp/work or $HOME to /tmp/home or something like that, or doing `whaledo [SHORTNAME|LONGNAME] COMMAND [MOUNTPOINTS...]` and just doing a 1:1 mapping.
#       An alternative approach could be to get metadata files from the whaledo-containers GitHub repo that explain what should be mounted where, but use the containers from Docker Hub just to make it quicker/less annoying.
#
# Example usage:
# $ whaledo alias rgdev=duckinator/rubygems-development
# $ whaledo rgdev rake test # Run `rake test` in a Docker container using the duckinator/rubygems-development image.
# $ whaledo unalias rgdev

import os
import sys
import json
import subprocess

### Helper functions ###

# ASSUMPTION: Will never be given a file with nothing but a newline in it.
def load_aliases(filename):
    ret = None
    if os.path.isfile(filename) and os.stat(filename).st_size != 0:
        with open(filename, 'r') as f:
            ret = json.load(f)

    if ret == None:
        ret = {}

    return ret

def save_aliases(filename, aliases):
    with open(filename, 'w') as f:
        json.dump(aliases, f)


### Commands ###

def cmd_help(argv, aliases):
    print("Usage: whaledo alias SHORT_NAME LONG_NAME")
    print("       whaledo unalias SHORT_NAME")
    print("       whaledo aliases")
    print("       whaledo run LONG_NAME COMMAND [ARGS...]")
    print("       whaledo run SHORT_NAME COMMAND [ARGS...]")
    print("       whaledo SHORT_NAME COMMAND [ARGS...]")
    return False

def cmd_alias(argv, aliases):
    if len(argv) < 3:
        print("Usage: whaledo alias SHORT_NAME LONG_NAME")
        return False

    _, _, short_name, long_name = argv

    aliases[short_name] = long_name
    return aliases

def cmd_unalias(argv, aliases):
    _, _, short_name = argv
    aliases.pop(short_name, None)
    return aliases

# FIXME: This function is pure sadness.
def cmd_aliases(argv, aliases):
    arbitrary_minimum_length = 20
    if len(aliases) > 0:
        separator_length = max(map(len, aliases)) + 8 # Arbitrary offset (8).
        separator_length = min(separator_length, arbitrary_minimum_length)
    else:
        separator_length = arbitrary_minimum_length

    print(("ALIAS{:<" + str(separator_length) + "}REPOSITORY").format(' '))
    for short_name in aliases:
        print(("{}{:<" + str(separator_length) + "}{}").format(short_name, ' ', aliases[short_name]))

    return False

def cmd_run(argv, aliases):
    _, _, repo_or_alias, *command = argv

    if repo_or_alias in aliases:
        repo = aliases[repo_or_alias]
    else:
        repo = repo_or_alias

    mounts = []
    user_id = subprocess.check_output(["id", "-u"]).strip()
    subprocess.call(["docker", "run", "--rm", "-it", *mounts, "-u", user_id, repo, *argv[3:]])

    return False

# NOTE: I did try using argument parsing libraries for this, but it wound up
#       being more complicated than just doing simple function lookup.
def handle(argv, aliases):
    commands = {
        "-h":       cmd_help,
        "--help":   cmd_help,
        "help":     cmd_help,
        "alias":    cmd_alias,
        "aliases":  cmd_aliases,
        "unalias":  cmd_unalias,
        "run":      cmd_run,
    }

    if len(argv) == 1:
        argv.append("help")
    elif argv[1] in aliases:
        # This makes it so that
        #   whaledo <known alias> <command>
        # is equivalent to
        #   whaledo run <known alias> command>
        #
        # However,
        #   whaledo <unknown alias> <command>
        # is not, to avoid situations where someone typos a command.
        argv.insert(1, "run")

    command = argv[1]

    if command in commands:
        aliases = commands[command](argv, aliases)
    else:
        aliases = commands["help"](argv, aliases)

    return aliases

def main():
    alias_filename = os.path.join(os.environ['HOME'], '.whaledo_aliases.json')
    original_aliases = load_aliases(alias_filename)
    updated_aliases = handle(sys.argv, original_aliases)

    if updated_aliases != False:
        save_aliases(alias_filename, updated_aliases)

if __name__ == '__main__':
    main()
