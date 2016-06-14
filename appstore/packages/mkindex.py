#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

# Improvements:
# - run manifest through configparser
#   - only transfer entries needed for the store app
#   - make sure no mandatory entry is missing
# - check if zip file needs to be rebuild
#   - rebuild zip file automatically

import sys
import os

print("Building package index ...")

pkgfile = open("00packages", "w")
pkgfile.write("; list of packages\n")
pkgfile.write("; this file contains all manifests\n")

# scan the directory for app directories
for l in os.listdir("."):
    if os.path.isdir(l):
        m = os.path.join(l, "manifest")
        if os.path.isfile(m):
            print("Adding", l, "...")
            pkgfile.write("\n")
            pkgfile.write("["+l+"]\n")

            # copy manifest contents. Skip [app] entry
            f = open(m)
            for line in f:
                if not "[app]" in line:
                    pkgfile.write(line)
            f.close()

pkgfile.close()
