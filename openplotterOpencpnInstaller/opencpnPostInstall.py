#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-opencpn-installer>
#
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

import subprocess, os, sys
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import platform
from .version import version

def main():
	conf2 = conf.Conf()
	platform2 = platform.Platform()
	currentdir = os.path.dirname(os.path.abspath(__file__))
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)

	print(_('Checking sources...'))
	codeName = conf2.get('GENERAL', 'codeName')
	hostID = conf2.get('GENERAL', 'hostID')
	backports = codeName+'-backports'
	if hostID == 'debian': 
		deb = 'deb http://deb.debian.org/debian '+backports+' main contrib non-free'
		RELEASE_DATA = platform2.RELEASE_DATA
		if RELEASE_DATA['ID'] == 'raspbian': os.system('dpkg -i '+currentdir+'/data/debian-archive-keyring_2021.1.1_all.deb')
	elif hostID == 'ubuntu': deb = 'deb http://archive.ubuntu.com/ubuntu/ '+backports+' main restricted universe multiverse'
	else: print(_('FAILED. Unknown host system'))
	try:
		os.system('flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo')
		if codeName:
			os.system('rm -f /etc/apt/sources.list.d/opencpn.list')
			sources = subprocess.check_output('apt-cache policy', shell=True).decode(sys.stdin.encoding)
			if not backports in sources:
				fo = open('/etc/apt/sources.list.d/opencpn-backports.list', "w")
				fo.write(deb)
				fo.close()
				os.system('apt update')
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Setting version...'))
	try:
		conf2.set('APPS', 'opencpn', version)
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

if __name__ == '__main__':
	main()
