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

import os, sys, subprocess
from openplotterSettings import conf
from openplotterSettings import language

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(os.path.abspath(__file__))
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)

	codeName = conf2.get('GENERAL', 'codeName')
	os.system('apt install -y opencpn -t '+codeName+'-backports')

	shortcut = '/usr/share/applications/opencpn.desktop'
	if os.path.exists(shortcut):
		file = open(shortcut, 'r')
		file2 = ''
		while True:
			line = file.readline()
			if not line: break
			if 'Categories=' in line: file2 += 'Categories=OpenPlotter\n'
			else: file2 += line
		file.close()
		file1 = open(shortcut, 'w')
		file1.write(file2)
		file1.close()
		print(_('Shortcut rebuilt'))

	if conf2.get('GENERAL', 'touchscreen') == '1':
		subprocess.call(['pkill', '-15', 'opencpn'])
		path = conf2.home+'/.opencpn/opencpn.conf'
		if os.path.exists(path):
			os.system('sed -i "s/MobileTouch = 0/MobileTouch = 1/g" '+path)
			os.system('sed -i "s/MobileTouch=0/MobileTouch=1/g" '+path)
			os.system('sed -i "s/mobiletouch = 0/mobiletouch = 1/g" '+path)
			os.system('sed -i "s/mobiletouch=0/mobiletouch=1/g" '+path)

if __name__ == '__main__':
	main()
