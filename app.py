#!/usr/bin/env python
"""Axway Docker Creator."""

import argparse
import os
import stat
import sys
import time
import urllib
import os


urllib.urlretrieve("http://habibs.de/APIGateway_7.7.20211130_Install_linux-x86-64_BN02.run", "APIGateway.run")

os.system("python build_base_image.py --installer=APIGateway.run --os=centos7")

os.system("python build_anm_image.py --default-cert --default-user --license=license.lic")

os.system("python build_gw_image.py --license=license.lic --merge-dir tmp/apigateway --default-cert --group-id=defaultgroup --api-manager")


