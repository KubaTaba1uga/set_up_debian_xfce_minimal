#!/usr/bin/env python3

from pathlib import Path
import sys
import os

MAIN_DIR = Path(sys.argv[0]).parent.parent

XFCE_CONFIGS_DIR = MAIN_DIR.joinpath("xfce_configs")

HOME = Path(os.environ["HOME"])

xsessionrc_path = HOME.joinpath(".xsessionrc")

with open(XFCE_CONFIGS_DIR.joinpath("xsessionrc.conf")) as conf:
    xsessionrc = conf.read()

with open(xsessionrc_path, "w") as conf:
    conf.write(xsessionrc)
