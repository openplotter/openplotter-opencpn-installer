#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by sailoog <https://github.com/sailoog/openplotter>
#                     e-sailing <https://github.com/e-sailing/openplotter>
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from openplotterOpencpnInstaller import version

setup (
	name = 'openplotterOpencpnInstaller',
	version = version.version,
	description = 'OpenPlotter app to manage OpenCPN installation',
	license = 'GPLv3',
	author="Sailoog",
	author_email='info@sailoog.com',
	url='https://github.com/openplotter/openplotter-opencpn-installer',
	packages=['openplotterOpencpnInstaller'],
	classifiers = ['Natural Language :: English',
	'Operating System :: POSIX :: Linux',
	'Programming Language :: Python :: 3'],
	include_package_data=True,
	entry_points={'console_scripts': ['openplotter-opencpn-installer=openplotterOpencpnInstaller.openplotterOpencpnInstaller:main']},
	data_files=[('share/applications', ['openplotterOpencpnInstaller/data/openplotter-opencpn-installer.desktop']),('share/pixmaps', ['openplotterOpencpnInstaller/data/openplotter-opencpn-installer.png']),],
	)
