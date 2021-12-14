#!/usr/bin/env python
"""Axway Docker Creator."""

import argparse
import os
import stat
import sys
import time
import os
import subprocess


subprocess.call(['sh', 'download_installer.sh']) 


os.system("python build_base_image.py --installer=APIGateway.run --os=centos7")

os.system("python build_anm_image.py --default-cert --default-user --license=license.lic")

os.system("python build_gw_image.py --license=license.lic --merge-dir tmp/apigateway --default-cert --group-id=defaultgroup --api-manager")


