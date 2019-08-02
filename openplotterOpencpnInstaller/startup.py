#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2015 by sailoog <https://github.com/sailoog/openplotter>
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
import time, subprocess

class Start():
	def __init__(self, conf):
		self.conf = conf
		self.initialMessage = ''
		subprocess.call(['pkill', '-15', 'opencpn'])
		if self.conf.get('OPENCPN', 'autostart') == '1':
			self.initialMessage = _('Starting OpenCPN...')
		
	def start(self):
		green = ''
		black = ''
		red = ''
		if self.conf.get('OPENCPN', 'fullscreen') == '1':
			black = _('fullscreen')
			subprocess.Popen(['opencpn', '-fullscreen'])
		else:
			black = _('non fullscreen')
			subprocess.Popen('opencpn')
		time.sleep(2)
		return {'green': green,'black': black,'red': red}

class Check():
	def __init__(self, conf):
		self.conf = conf
		self.initialMessage = _('Checking OpenCPN...')

	def check(self):
		green = ''
		black = ''
		red = ''
		test = subprocess.check_output(['ps','aux']).decode()
		test2 = test.replace('openplotter-opencpn', '')
		if 'opencpn' in test2: green = _('running')
		else: black = _('not running ')

		if self.conf.get('OPENCPN', 'autostart') == '1':
			if self.conf.get('OPENCPN', 'fullscreen') == '1':
				black += _('fullscreen autostart enabled')
			else: black += _('autostart enabled')
		else: black += _('autostart disabled')

		return {'green': green,'black': black,'red': red}

