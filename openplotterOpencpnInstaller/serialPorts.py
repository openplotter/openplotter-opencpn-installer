#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-opencpn-installer>
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

import configparser

class SerialPorts:
	def __init__(self,conf):
		self.conf = conf
		self.connections = []
		# {'app':'xxx', 'id':'xxx', 'data':'NMEA0183/NMEA2000/SignalK', 'device': '/dev/xxx', "baudrate": nnnnnn, "enabled": True/False}

	def usedSerialPorts(self):
		try:
			confFile = self.conf.home+'/.opencpn/opencpn.conf'
			confData = configparser.SafeConfigParser()
			confData.read(confFile)
			tmp = confData.get('Settings/NMEADataSource', 'DataConnections')
			connections = tmp.split('|')
			c = 1
			for connection in connections:
				#0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18
				#serial/network;TCP/UDP/GPSD;address;port;?;serialport;bauds;?;0=input/1=input+output/2=output;?;?;?;?;?;?;?;?;enabled/disabled;comments
				items = connection.split(';')
				if items[0] == '0': # serial
					enabled = False
					if items[17] == '1': enabled = True
					self.connections.append({'app':'OpenCPN','id':str(c), 'data':'NMEA0183', 'device': items[5], 'baudrate': items[6], "enabled": enabled})
				c = c + 1
		except:pass

		return self.connections