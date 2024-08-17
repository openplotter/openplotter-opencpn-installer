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

import time, subprocess, configparser, os, sys
from openplotterSettings import platform
from openplotterSettings import language

class Start():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		self.platform = platform.Platform()
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)
		self.initialMessage = ''
		if self.conf.get('OPENCPN', 'autostart') == '1' or self.conf.get('OPENCPN', 'autostartFP') == '1': self.initialMessage = _('Starting OpenCPN...')
				
	def start(self):
		green = ''
		black = ''
		red = ''

		subprocess.call('pkill -15 opencpn', shell=True)

		if self.platform.isInstalled('opencpn'):
			path = self.conf.home+'/.opencpn/opencpn.conf'
			if os.path.exists(path):
				if self.conf.get('OPENCPN', 'autostart') == '1':
					if self.conf.get('OPENCPN', 'fullscreen') == '1':
						black = _('fullscreen')
						subprocess.Popen(['opencpn', '-f'])
					else:
						black = _('non fullscreen')
						subprocess.Popen('opencpn')

		FP = subprocess.check_output(['flatpak','list']).decode(sys.stdin.encoding)
		if 'OpenCPN' in FP:
			pathfp = self.conf.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf'
			if os.path.exists(pathfp):
				if self.conf.get('OPENCPN', 'autostartFP') == '1':
					if self.conf.get('OPENCPN', 'fullscreenFP') == '1':
						black = _('fullscreen')
						subprocess.Popen(['flatpak', 'run', 'org.opencpn.OpenCPN', '-f'])
					else:
						black = _('non fullscreen')
						subprocess.Popen(['flatpak', 'run', 'org.opencpn.OpenCPN'])

		time.sleep(2)
		return {'green': green,'black': black,'red': red}

class Check():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		self.platform = platform.Platform()
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)
		self.initialMessage = ''
		self.installed = False
		self.installedFP = False
		if self.platform.isInstalled('opencpn'): self.installed = True
		FP = subprocess.check_output(['flatpak','list']).decode(sys.stdin.encoding)
		if 'OpenCPN' in FP: self.installedFP = True
		if self.installed or self.installedFP: self.initialMessage = _('Checking OpenCPN...')

	def check(self):
		green = ''
		black = ''
		red = ''
		test = subprocess.check_output(['ps','aux']).decode(sys.stdin.encoding)
		test2 = test.replace('openplotter-opencpn', '')
		if 'opencpn' in test2: green = _('running')
		else: black = _('not running')

		if self.installed:
			try: 
				codeName = self.conf.get('GENERAL', 'codeName')
				hostID = self.conf.get('GENERAL', 'hostID')
				CompatOsVersion = ''
				if hostID == 'debian':
					if codeName:
						if codeName == 'buster': CompatOsVersion = '10'
						elif codeName == 'bullseye': CompatOsVersion = '11'
						elif codeName == 'bookworm': CompatOsVersion = '12'

				path = self.conf.home+'/.opencpn/opencpn.conf'
				if os.path.exists(path):
					data_conf = configparser.SafeConfigParser()
					data_conf.read(path)
				else:
					if not os.path.exists(self.conf.home+'/.opencpn'): os.mkdir(self.conf.home+'/.opencpn')
					opencpnconf = '[Settings]\n'
					if self.platform.isRPI and hostID == 'debian' and codeName and CompatOsVersion:
						opencpnconf += 'CompatOS=debian-arm64\nCompatOsVersion='+CompatOsVersion+'\n'
					if self.conf.get('GENERAL', 'touchscreen') == '1':
						opencpnconf += 'MobileTouch=1\n'
					opencpnconf += '[Settings/NMEADataSource]\nDataConnections=1;3;localhost;3000;0;;4800;1;0;0;;0;;1;0;0;0;1;;1;;0;0;\n'
					file = open(path, 'w')
					file.write(opencpnconf)
					file.close()
					time.sleep(2)
					data_conf = configparser.SafeConfigParser()
					data_conf.read(path)
			except Exception as e:
				msg = _('Error checking opencpn.conf: ')+str(e)
				if red: red += '\n   '+msg
				else: red = msg

		if self.installedFP:
			try:
				pathfp = self.conf.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf'
				if os.path.exists(pathfp):
					data_conffp = configparser.SafeConfigParser()
					data_conffp.read(pathfp)
				else:
					if not os.path.exists(self.conf.home+'/.var'): os.mkdir(self.conf.home+'/.var')
					if not os.path.exists(self.conf.home+'/.var/app'): os.mkdir(self.conf.home+'/.var/app')
					if not os.path.exists(self.conf.home+'/.var/app/org.opencpn.OpenCPN'): os.mkdir(self.conf.home+'/.var/app/org.opencpn.OpenCPN')
					if not os.path.exists(self.conf.home+'/.var/app/org.opencpn.OpenCPN/config'): os.mkdir(self.conf.home+'/.var/app/org.opencpn.OpenCPN/config')
					if not os.path.exists(self.conf.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn'): os.mkdir(self.conf.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn')
					opencpnconf = '[Settings]\n'
					if self.conf.get('GENERAL', 'touchscreen') == '1':
						opencpnconf += 'MobileTouch=1\n'
					opencpnconf += '[Settings/NMEADataSource]\nDataConnections=1;3;localhost;3000;0;;4800;1;0;0;;0;;1;0;0;0;1;;1;;0;0;\n'
					file = open(pathfp, 'w')
					file.write(opencpnconf)
					file.close()
					time.sleep(2)
					data_conffp = configparser.SafeConfigParser()
					data_conffp.read(pathfp)
			except Exception as e:
				msg = _('Error checking flatpak opencpn.conf: ')+str(e)
				if red: red += '\n   '+msg
				else: red = msg

		if self.installed:
			if self.platform.isRPI:
				if hostID == 'debian':
					if codeName:
						if os.path.exists(path):
							try:
								if data_conf.get('Settings','CompatOsVersion') != CompatOsVersion or data_conf.get('Settings','CompatOS') != 'debian-arm64':
									if 'opencpn' in test2:
										subprocess.call(['pkill', '-15', 'opencpn'])
										time.sleep(2)
									os.system('cp -f '+path+' '+path+'_back')
									file = open(path, 'r')
									out = ''
									while True:
										line = file.readline()
										if not line: break
										if 'CompatOsVersion' in line or 'compatosversion' in line: 
											out += 'CompatOsVersion='+CompatOsVersion+'\n'
										elif 'CompatOS' in line or 'compatos' in line: 
											out += 'CompatOS=debian-arm64\n'
										else: out += line
									file.close()
									try: 
										file = open(path, 'w')
										file.write(out)
										file.close()
									except Exception as e:
										os.system('cp -f '+path+'_back '+path)
										msg = _('Error editing CompatOS: ')+str(e)
										if red: red += '\n   '+msg
										else: red = msg
							except Exception as e:
								msg = _('Error checking CompatOS: ')+str(e)
								if red: red += '\n   '+msg
								else: red = msg
							else:
								msg = _('CompatOS checked')
								if not black: black = msg
								else: black+= ' | '+msg

			if self.conf.get('OPENCPN', 'autostart') == '1':
				if self.conf.get('OPENCPN', 'fullscreen') == '1':
					black += _(' | fullscreen autostart enabled')
				else: black += _(' | autostart enabled')
			else: black += _(' | autostart disabled')

			if self.conf.get('GENERAL', 'touchscreen') == '1':
				if os.path.exists(path):
					if data_conf.get('Settings','MobileTouch') == '1':
						msg = _('touchscreen enabled')
						if not black: black = msg
						else: black+= ' | '+msg
					else:
						msg = _('touchscreen disabled')
						if red: red += '\n   '+msg
						else: red = msg

			shortcut = '/usr/share/applications/opencpn.desktop'
			if os.path.exists(shortcut):
				file = open(shortcut, 'r')
				exists = False
				while True:
					line = file.readline()
					if not line: break
					if 'Categories=OpenPlotter' in line: exists = True
				file.close()
				if not exists:
					msg = _('OpenCPN shortcut is broken, click "Install" in OpenCPN Installer app to rebuild it.')
					if red: red += '\n   '+msg
					else: red = msg

		if self.installedFP:
			if self.conf.get('OPENCPN', 'autostartFP') == '1':
				if self.conf.get('OPENCPN', 'fullscreenFP') == '1':
					black += _(' | FP fullscreen autostart enabled')
				else: black += _(' | FP autostart enabled')
			else: black += _(' | FP autostart disabled')

			if self.conf.get('GENERAL', 'touchscreen') == '1':
				if os.path.exists(pathfp):
					if data_conffp.get('Settings','MobileTouch') == '1':
						msg = _('FP touchscreen enabled')
						if not black: black = msg
						else: black+= ' | '+msg
					else:
						msg = _('FP touchscreen disabled')
						if red: red += '\n   '+msg
						else: red = msg

			shortcut = self.conf.home+'/.local/share/flatpak/exports/share/applications/org.opencpn.OpenCPN.desktop'
			if os.path.exists(shortcut):
				file = open(shortcut, 'r')
				exists = False
				while True:
					line = file.readline()
					if not line: break
					if 'Categories=OpenPlotter' in line: exists = True
				file.close()
				if not exists:
					msg = _('OpenCPN FP shortcut is broken, click "Install" in OpenCPN Installer app to rebuild it.')
					if red: red += '\n   '+msg
					else: red = msg

		if self.installed:
			if self.platform.skDir:
				try:
					resultSK = False
					resultNMEA = False
					tmp = data_conf.get('Settings/NMEADataSource', 'DataConnections')
					connections = tmp.split('|')
					#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18,19
					#serial/network;TCP/UDP/GPSD/SK;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments;0=not autodiscover sk/0=autodiscover sk
					for connection in connections:
						items = connection.split(';')
						if items[0] == '1':
							if items[1] == '0':
								if items[2] == 'localhost':
									if items[3] == '10110':
										if items[8] == '0' or items[8] == '1':
											if items[17] == '1': resultNMEA = 'enabled'
											else: resultNMEA = 'disabled'

					for connection in connections:
						items = connection.split(';')
						if items[0] == '1':
							if items[1] == '3':
								if items[2] == 'localhost':
									if items[3] == self.platform.skPort:
										if items[17] == '1': resultSK = 'enabled'
										else: resultSK = 'disabled'

					if resultSK != 'enabled' and resultNMEA == 'enabled': 
						msg = _('TIP: Since version 5.2 and above OpenCPN can manage Signal K data, you should replace the NMEA 0183 connection "TCP localhost 10110" by a Signal K connection.')	
						if black: black += '\n'+msg
						else: black = msg				
					elif resultSK == 'enabled' and resultNMEA == 'enabled':
						msg = _('WARNING: You have enabled the old NMEA 0183 connection "TCP localhost 10110" and a Signal K connection in OpenCPN. Make sure you do not have duplicated data.')	
						if black: black += '\n'+msg
						else: black = msg
					if resultNMEA != 'enabled' and not resultSK:
						msg = _('The default OpenCPN connection is missing and is not getting data from Signal K. Please create this connection in OpenCPN:\n    Network\n    Protocol: Signal K\n    Address: localhost\n    DataPort: '+self.platform.skPort)
						if red: red += '\n'+msg
						else: red = msg				
					elif resultNMEA != 'enabled' and resultSK == 'disabled':
						msg = _('The default OpenCPN connection is disabled and is not getting data from Signal K. Please enable the Signal K connection in OpenCPN')
						if red: red += '\n'+msg
						else: red = msg			
				except:
					msg = _('Unable to read OpenCPN configuration')
					if red: red += '\n'+msg
					else: red = msg

		if self.installedFP:
			if self.platform.skDir:
				try:
					resultSK = False
					resultNMEA = False
					tmp = data_conffp.get('Settings/NMEADataSource', 'DataConnections')
					connections = tmp.split('|')
					#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18,19
					#serial/network;TCP/UDP/GPSD/SK;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments;0=not autodiscover sk/0=autodiscover sk
					for connection in connections:
						items = connection.split(';')
						if items[0] == '1':
							if items[1] == '0':
								if items[2] == 'localhost':
									if items[3] == '10110':
										if items[8] == '0' or items[8] == '1':
											if items[17] == '1': resultNMEA = 'enabled'
											else: resultNMEA = 'disabled'

					for connection in connections:
						items = connection.split(';')
						if items[0] == '1':
							if items[1] == '3':
								if items[2] == 'localhost':
									if items[3] == self.platform.skPort:
										if items[17] == '1': resultSK = 'enabled'
										else: resultSK = 'disabled'

					if resultSK != 'enabled' and resultNMEA == 'enabled': 
						msg = _('TIP: Since version 5.2 and above OpenCPN can manage Signal K data, you should replace the NMEA 0183 connection "TCP localhost 10110" by a Signal K connection.')
						if black: black += '\n'+msg
						else: black = msg
					elif resultSK == 'enabled' and resultNMEA == 'enabled':
						msg = _('WARNING: You have enabled the old NMEA 0183 connection "TCP localhost 10110" and a Signal K connection in OpenCPN. Make sure you do not have duplicated data.')
						if black: black += '\n'+msg
						else: black = msg
					if resultNMEA != 'enabled' and not resultSK:
						msg = _('The default OpenCPN connection is missing and is not getting data from Signal K. Please create this connection in OpenCPN:\n    Network\n    Protocol: Signal K\n    Address: localhost\n    DataPort: '+self.platform.skPort)
						if red: red += '\n'+msg
						else: red = msg				
					elif resultNMEA != 'enabled' and resultSK == 'disabled':
						msg = _('The default OpenCPN connection is disabled and is not getting data from Signal K. Please enable the Signal K connection in OpenCPN')
						if red: red += '\n'+msg
						else: red = msg
				except:
					msg = _('Unable to read OpenCPN FP configuration')
					if red: red += '\n'+msg
					else: red = msg

		return {'green': green,'black': black,'red': red}

