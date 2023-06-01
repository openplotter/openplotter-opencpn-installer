#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2023 by Sailoog <https://github.com/openplotter/openplotter-opencpn-installer>
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
import os, subprocess
from openplotterSettings import conf
from openplotterSettings import language

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(os.path.abspath(__file__))

	shortcut = conf2.home+'/.local/share/flatpak/exports/share/applications/org.opencpn.OpenCPN.desktop'
	if os.path.exists(shortcut):
		file = open(shortcut, 'r')
		file2 = ''
		while True:
			line = file.readline()
			if not line: break
			if 'Categories=' in line: file2 += 'Categories=OpenPlotter\n'
			elif 'Name=' in line: file2 += 'Name=OpenCPN FP\n'
			else: file2 += line
		file.close()
		file1 = open(shortcut, 'w')
		file1.write(file2)
		file1.close()

	if not os.path.exists(conf2.home+'/.var'): os.mkdir(conf2.home+'/.var')
	if not os.path.exists(conf2.home+'/.var/app'): os.mkdir(conf2.home+'/.var/app')
	if not os.path.exists(conf2.home+'/.var/app/org.opencpn.OpenCPN'): os.mkdir(conf2.home+'/.var/app/org.opencpn.OpenCPN')
	if not os.path.exists(conf2.home+'/.var/app/org.opencpn.OpenCPN/config'): os.mkdir(conf2.home+'/.var/app/org.opencpn.OpenCPN/config')
	if not os.path.exists(conf2.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn'): os.mkdir(conf2.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn')
	if not os.path.exists(conf2.home+'/.var/app/org.opencpn.OpenCPN/config/gtk-3.0'): os.mkdir(conf2.home+'/.var/app/org.opencpn.OpenCPN/config/gtk-3.0')
	if not os.path.exists(conf2.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf'): os.system('cp -fR '+currentdir+'/data/FP/opencpn.conf'+' '+conf2.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn')

	if conf2.get('GENERAL', 'touchscreen') == '1':
		subprocess.call(['flatpak', 'kill', 'org.opencpn.OpenCPN'])
		if os.path.exists(conf2.home+'/.config/gtk-3.0'):
			os.system('cp -fa '+conf2.home+'/.config/gtk-3.0/. '+conf2.home+'/.var/app/org.opencpn.OpenCPN/config/gtk-3.0/')
		path1 = conf2.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf'
		if os.path.exists(path1):
			os.system('sed -i "s/MobileTouch = 0/MobileTouch = 1/g" '+path1)
			os.system('sed -i "s/MobileTouch=0/MobileTouch=1/g" '+path1)
			os.system('sed -i "s/mobiletouch = 0/mobiletouch = 1/g" '+path1)
			os.system('sed -i "s/mobiletouch=0/mobiletouch=1/g" '+path1)

if __name__ == '__main__':
	main()
