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
import configparser, os
from openplotterSettings import platform
from openplotterSettings import language

class Ports:
	def __init__(self,conf, currentLanguage):
		self.platform = platform.Platform()
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-opencpn-installer',currentLanguage)
		self.usedPorts=[]
		if self.platform.isInstalled('opencpn'):
			try:
				confFile = conf.home+'/.opencpn/opencpn.conf'
				confData = configparser.SafeConfigParser()
				confData.read(confFile)
				tmp = confData.get('Settings/NMEADataSource', 'DataConnections')
				connections = tmp.split('|')
				for connection in connections:
					result = False
					#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18
					#serial/network;TCP/UDP/GPSD;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments
					items = connection.split(';')
					if items[0] == '1':
						if items[17] == '1':
							if items[1] == '0':
								if items[2] == '0.0.0.0': 
									ctype = 'TCP'
									address = 'localhost'
									port = items[3]
									direction = ''
									if items[8] == '2': direction = 'out'
									if items[8] == '1': direction = 'both'
									result = {'description':_('OpenCPN connection'), 'type':ctype, 'address':address, 'port':port, 'direction':direction}
							elif items[1] == '1':
								if items[8] == '2' or items[8] == '1':
									if items[2] == 'localhost' or items[2] == '127.0.0.1' or not items[2]: 
										if items[8] == '2': direction = 'out'
										if items[8] == '1': direction = 'both'
										ctype = 'UDP'
										address = 'localhost'
										port = items[3]
										result = {'description':_('OpenCPN connection'), 'type':ctype, 'address':address, 'port':port, 'direction':direction}
					if result: self.usedPorts.append(result)
			except:pass