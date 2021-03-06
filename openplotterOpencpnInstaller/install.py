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
import os, sys

def main():
	os.system('apt install -y '+sys.argv[1])
	
	currentdir = os.path.dirname(os.path.abspath(__file__))
	source = currentdir+'/data/opencpn.desktop'
	os.system('cp -f '+source+' /usr/share/applications')

if __name__ == '__main__':
	main()
