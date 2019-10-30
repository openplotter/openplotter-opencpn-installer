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
import time, subprocess, configparser, os, sys
from openplotterSettings import platform
from openplotterSettings import language

class Start():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		self.platform = platform.Platform()
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)
		self.initialMessage = ''
		if self.platform.isInstalled('opencpn'):
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
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		self.platform = platform.Platform()
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)
		self.initialMessage = ''
		if self.platform.isInstalled('opencpn'):
			self.initialMessage = _('Checking OpenCPN...')

	def check(self):
		green = ''
		black = ''
		red = ''
		test = subprocess.check_output(['ps','aux']).decode(sys.stdin.encoding)
		test2 = test.replace('openplotter-opencpn', '')
		if 'opencpn' in test2: green = _('running')
		else: black = _('not running | ')

		if self.conf.get('OPENCPN', 'autostart') == '1':
			if self.conf.get('OPENCPN', 'fullscreen') == '1':
				black += _('fullscreen autostart enabled')
			else: black += _('autostart enabled')
		else: black += _('autostart disabled')

		if self.platform.skDir:
			try:
				confFile = self.conf.home+'/.opencpn/opencpn.conf'
				confData = configparser.SafeConfigParser()
				result = False
				confData.read(confFile)
				tmp = confData.get('Settings/NMEADataSource', 'DataConnections')
				connections = tmp.split('|')
				for connection in connections:
					#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18
					#serial/network;TCP/UDP/GPSD;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments
					items = connection.split(';')
					if items[0] == '1':
						if items[1] == '0':
							if items[2] == 'localhost':
								if items[3] == '10110':
									if items[8] == '0' or items[8] == '1':
										if items[17] == '1': result = 'enabled'
										else: result = 'disabled'
				if not result:
					red = _('The default OpenCPN connection is missing and is not getting data from Signal K. Please create this connection in OpenCPN:\nNetwork\nProtocol: TCP\nAddress: localhost\nData Port: 10110')
				elif result == 'disabled':
					red = _('The default OpenCPN connection is disabled and is not getting data from Signal K. Please enable this connection in OpenCPN:\nNetwork\nProtocol: TCP\nAddress: localhost\nData Port: 10110')
			except:pass

		return {'green': green,'black': black,'red': red}

