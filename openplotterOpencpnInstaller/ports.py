#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-opencpn-installer>
#						e-sailing <https://github.com/e-sailing/openplotter>
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

import configparser, os, subprocess, sys
from openplotterSettings import platform
from openplotterSettings import language

class Ports:
	def __init__(self,conf, currentLanguage):
		self.conf = conf
		self.platform = platform.Platform()
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)
		self.connections = []

	def usedPorts(self):
		usedPorts = []
		if self.platform.isInstalled('opencpn'):
			try:
				confFile = self.conf.home+'/.opencpn/opencpn.conf'
				confData = configparser.SafeConfigParser()
				confData.read(confFile)
				tmp = confData.get('Settings/NMEADataSource', 'DataConnections')
				connections = tmp.split('|')
				c = 1
				for connection in connections:
					result = False
					#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18:19
					#serial/network;TCP/UDP/GPSD;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments;0=not autodiscover sk/0=autodiscover sk
					items = connection.split(';')
					if items[0] == '1': # network
						if items[17] == '1': # enabled
							if items[1] == '0': # TCP
								if items[2] == 'localhost' or items[2] == '127.0.0.1' or items[2] == '0.0.0.0' or not items[2]:
									if items[2] == '0.0.0.0': mode = 'server'
									else: mode = 'client'
									ctype = 'TCP'
									address = 'localhost'
									port = items[3]
									result = {'id':'opencpnConn'+str(c),'description':_('OpenCPN connection'), 'data':[], 'type':ctype, 'mode':mode, 'address':address, 'port':port, 'editable':'0'}
							elif items[1] == '1': # UDP
								if items[2] == 'localhost' or items[2] == '127.0.0.1' or items[2] == '0.0.0.0' or not items[2]:
									if items[8] == '0' or items[8] == '1': mode = 'server'
									else: mode = 'client'
									ctype = 'UDP'
									address = 'localhost'
									port = items[3]
									result = {'id':'opencpnConn'+str(c),'description':_('OpenCPN connection'), 'data':[], 'type':ctype, 'mode':mode, 'address':address, 'port':port, 'editable':'0'}
					if result: 
						usedPorts.append(result)
						c = c +1
			except:pass

		installedFP = False
		FP = subprocess.check_output(['flatpak','list']).decode(sys.stdin.encoding)
		if 'OpenCPN' in FP: installedFP = True

		if installedFP:
			try:
				confFile = self.conf.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf'
				confData = configparser.SafeConfigParser()
				confData.read(confFile)
				tmp = confData.get('Settings/NMEADataSource', 'DataConnections')
				connections = tmp.split('|')
				c = 1
				for connection in connections:
					result = False
					#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18:19
					#serial/network;TCP/UDP/GPSD;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments;0=not autodiscover sk/0=autodiscover sk
					items = connection.split(';')
					if items[0] == '1': # network
						if items[17] == '1': # enabled
							if items[1] == '0': # TCP
								if items[2] == 'localhost' or items[2] == '127.0.0.1' or items[2] == '0.0.0.0' or not items[2]:
									if items[2] == '0.0.0.0': mode = 'server'
									else: mode = 'client'
									ctype = 'TCP'
									address = 'localhost'
									port = items[3]
									result = {'id':'opencpnFPConn'+str(c),'description':_('OpenCPN FP connection'), 'data':[], 'type':ctype, 'mode':mode, 'address':address, 'port':port, 'editable':'0'}
							elif items[1] == '1': # UDP
								if items[2] == 'localhost' or items[2] == '127.0.0.1' or items[2] == '0.0.0.0' or not items[2]:
									if items[8] == '0' or items[8] == '1': mode = 'server'
									else: mode = 'client'
									ctype = 'UDP'
									address = 'localhost'
									port = items[3]
									result = {'id':'opencpnFPConn'+str(c),'description':_('OpenCPN FP connection'), 'data':[], 'type':ctype, 'mode':mode, 'address':address, 'port':port, 'editable':'0'}
					if result: 
						usedPorts.append(result)
						c = c +1
			except:pass
		if usedPorts: return usedPorts
