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
from .version import version

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(os.path.abspath(__file__))
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)

	print(_('Checking sources...'))
	codename_debian = conf2.get('GENERAL', 'debianCodeName')
	codename_ubuntu = 'focal'
	if codename_debian == 'buster': codename_ubuntu = 'bionic'
	if codename_debian == 'bullseye': codename_ubuntu = 'focal'
	s = 'http://ppa.launchpad.net/opencpn/opencpn/ubuntu '+codename_ubuntu
	deb = 'deb http://ppa.launchpad.net/opencpn/opencpn/ubuntu '+codename_ubuntu+' main'
	try:
		os.system('flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo')
		sources = subprocess.check_output('apt-cache policy', shell=True).decode(sys.stdin.encoding)
		if not s in sources:
			fo = open('/etc/apt/sources.list.d/opencpn.list', "w")
			fo.write(deb)
			fo.close()
			os.system('apt-key add - < '+currentdir+'/data/source/opencpn.gpg.key' )
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
