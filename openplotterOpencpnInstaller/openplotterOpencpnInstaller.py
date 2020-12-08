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

import wx, os, webbrowser, subprocess, sys, time
import wx.richtext as rt

from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import platform
from .version import version

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = conf.Conf()
		self.platform = platform.Platform()
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = language.Language(self.currentdir,'openplotter-opencpn-installer',currentLanguage)

		self.appsDict = []

		app = {
		'name': 'Test Plugin',
		'category': _('Others'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:plugins:safety:odraw1.6_pi',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Pypilot Plugin',
		'category': _('Others'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/pypilot.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Debugger Plugin',
		'category': _('Others'),
		'package': 'opencpn-plugin-ocpndebugger',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/debugger.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Launcher Plugin',
		'category': _('Others'),
		'package': 'opencpn-plugin-launcher',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/launcher.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'GPS Odometer',
		'category': _('Others'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:plugins:other:odometer',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Calculator Plugin',
		'category': _('Others'),
		'package': 'opencpn-plugin-calculator',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/calculator.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Status Bar Plugin',
		'category': _('Others'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/statusbar.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'ShipDriver Plugin',
		'category': _('Others'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/shipdriver.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'IAC Fleet Code Plugin',
		'category': _('Weather'),
		'package': 'opencpn-plugin-iacfleet',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/iacfleet.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Climatology Plugin',
		'category': _('Weather'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/climatology.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Weather Fax Plugin',
		'category': _('Weather'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/weatherfax.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Weather Routing Plugin',
		'category': _('Weather'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/weatherroute.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Windvane Autopilot',
		'category': _('Sailing Interests'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:plugins:sailing:windvane',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Tactics Plugin',
		'category': _('Sailing Interests'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/tactics.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Plots Plugin',
		'category': _('Sailing Interests'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/sweepplot.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Polar Plugin',
		'category': _('Sailing Interests'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/polar.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'SAR Plugin',
		'category': _('Safety'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/sar.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Ocpn Draw Plugin',
		'category': _('Safety'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/draw.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Watchdog Plugin',
		'category': _('Safety'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/watchdog.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'oTCurrent Plugin',
		'category': _('Navigation'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:plugins:navigation:otcurrent',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Dead Reckoning Positions Plugin',
		'category': _('Navigation'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:plugins:navigation:dead_reckoning',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Route Plugin',
		'category': _('Navigation'),
		'package': 'opencpn-plugin-route',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/route.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Celestial Navigation Plugin',
		'category': _('Navigation'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/celestialnav.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'sQuiddio Plugin',
		'category': _('Navigation'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/sQuiddio.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Dashboard-Tactics Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/dashboardtactics.html',
		'install': '',
		}
		self.appsDict.append(app)
		
		app = {
		'name': 'NmeaConverter Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/nmeaconvert.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Voyage Data Recorder Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/vdr.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Find-It Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/findit.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Logbook Konni Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/logbookkonni.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Race Start Display Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:developer_manual:plugins:beta_plugins:race-start',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Engine Dashboard Plugin',
		'category': _('Logs'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:developer_manual:plugins:beta_plugins:engine-dash',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'PhotoLayer Plugin',
		'category': _('Chart Support'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:developer_manual:plugins:beta_plugins:photolayer',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Projections Plugin',
		'category': _('Chart Support'),
		'package': 'opencpn-plugin-projections',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/projections.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Chart Object Search Plugin',
		'category': _('Chart Support'),
		'package': 'opencpn-plugin-objsearch',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/chartobject.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Chart Scale Plugin',
		'category': _('Chart Support'),
		'package': 'opencpn-plugin-chartscale',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/chartscale.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Chart Rotation Control Plugin',
		'category': _('Chart Support'),
		'package': 'opencpn-plugin-rotationctrl',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/chartrotation.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'VFkaps Plugin',
		'category': _('Chart Support'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:plugins:charts:vfkaps',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'S-63 Charts Plugin',
		'category': _('Chart Support'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/s63.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'oeRNC Charts Plugin',
		'category': _('Chart Support'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/oernc.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'oeSENC Charts Plugin',
		'category': _('Chart Support'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/oesenc.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'RTL-SDR Plugin',
		'category': _('AIS/Radar'),
		'package': 'opencpn-plugin-rtlsdr',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/rtlsdr.html',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		app = {
		'name': 'Radar PI Plugin',
		'category': _('AIS/Radar'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/radarPI.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'AIS Radar View Plugin',
		'category': _('AIS/Radar'),
		'package': '',
		'sources': [],
		'dev': '',
		'entryPoint': 'x-www-browser https://opencpn.org/OpenCPN/plugins/aisradarview.html',
		'install': '',
		}
		self.appsDict.append(app)

		app = {
		'name': 'OpenCPN',
		'category': _('Main Program'),
		'package': 'opencpn',
		'sources': ['http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser https://opencpn.org/',
		'install': 'install.py',
		}
		self.appsDict.append(app)

		wx.Frame.__init__(self, None, title=_('OpenCPN Installer')+' '+version, size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-opencpn-installer.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)

		self.toolbar1 = wx.ToolBar(self, style=wx.TB_TEXT)
		toolHelp = self.toolbar1.AddTool(101, _('Help'), wx.Bitmap(self.currentdir+"/data/help.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHelp, toolHelp)
		if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
		toolSettings = self.toolbar1.AddTool(106, _('Settings'), wx.Bitmap(self.currentdir+"/data/settings.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSettings, toolSettings)
		self.toolbar1.AddSeparator()
		toolStartup = self.toolbar1.AddCheckTool(102, _('Autostart OpenCPN'), wx.Bitmap(self.currentdir+"/data/autostart.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStartup, toolStartup)
		if self.conf.get('OPENCPN', 'autostart') == '1': self.toolbar1.ToggleTool(102,True)
		toolFull = self.toolbar1.AddCheckTool(103, _('Full Screen'), wx.Bitmap(self.currentdir+"/data/fullscreen.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolFull, toolFull)
		if self.conf.get('OPENCPN', 'fullscreen') == '1': self.toolbar1.ToggleTool(103,True)
		if self.toolbar1.GetToolState(102): self.toolbar1.EnableTool(103,True)
		else: self.toolbar1.EnableTool(103,False)
		self.toolbar1.AddSeparator()
		toolUpdate = self.toolbar1.AddTool(105, _('Update Data'), wx.Bitmap(self.currentdir+"/data/update.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolUpdate, toolUpdate)
		self.refreshButton = self.toolbar1.AddTool(104, _('Refresh'), wx.Bitmap(self.currentdir+"/data/refresh.png"))
		self.Bind(wx.EVT_TOOL, self.OnRefreshButton, self.refreshButton)
		
		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.apps = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('OpenCPN packages'))
		self.notebook.AddPage(self.output, '')
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/opencpn24.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/output.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.pageApps()
		self.onListAppsDeselected()
		self.pageOutput()

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': self.Maximize()
		
		self.Centre() 

	def ShowStatusBar(self, w_msg, colour):
		self.GetStatusBar().SetForegroundColour(colour)
		self.SetStatusText(w_msg)

	def ShowStatusBarRED(self, w_msg):
		self.ShowStatusBar(w_msg, (130,0,0))

	def ShowStatusBarGREEN(self, w_msg):
		self.ShowStatusBar(w_msg, (0,130,0))

	def ShowStatusBarBLACK(self, w_msg):
		self.ShowStatusBar(w_msg, wx.BLACK) 

	def ShowStatusBarYELLOW(self, w_msg):
		self.ShowStatusBar(w_msg,(255,140,0))

	def onTabChange(self, event):
		try:
			self.SetStatusText('')
		except:pass

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/opencpn/opencpn_app.html"
		webbrowser.open(url, new=2)

	def OnToolSettings(self, event): 
		subprocess.call(['pkill', '-f', 'openplotter-settings'])
		subprocess.Popen('openplotter-settings')

	def OnToolStartup(self, e):
		if self.toolbar1.GetToolState(102):
			self.conf.set('OPENCPN', 'autostart', '1')
			self.ShowStatusBarBLACK(_('OpenCPN autostart enabled'))
			self.toolbar1.EnableTool(103,True)
		else: 
			self.conf.set('OPENCPN', 'autostart', '0')
			self.ShowStatusBarBLACK(_('OpenCPN autostart disabled'))
			self.toolbar1.EnableTool(103,False)

	def OnToolFull(self, e):
		if self.toolbar1.GetToolState(103):
			self.conf.set('OPENCPN', 'fullscreen', '1')
			self.ShowStatusBarBLACK(_('OpenCPN fullscreen autostart enabled'))
		else: 
			self.conf.set('OPENCPN', 'fullscreen', '0')
			self.ShowStatusBarBLACK(_('OpenCPN fullscreen autostart disabled'))

	def OnToolUpdate(self, event):
		self.logger.Clear()
		self.notebook.ChangeSelection(1)
		command = self.platform.admin+' apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Updating packages data, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
		self.readApps()

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listApps.InsertColumn(0, _('Name'), width=210)
		self.listApps.InsertColumn(1, _('Category'), width=130)
		self.listApps.InsertColumn(2, _('Installed'), width=170)
		self.listApps.InsertColumn(3, _('Candidate'), width=170)
		self.listApps.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListAppsSelected)
		self.listApps.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListAppsDeselected)
		self.listApps.SetTextColour(wx.BLACK)

		self.toolbar2 = wx.ToolBar(self.apps, style=wx.TB_TEXT | wx.TB_VERTICAL)
		self.installButton = self.toolbar2.AddTool(201, _('Install'), wx.Bitmap(self.currentdir+"/data/install.png"))
		self.Bind(wx.EVT_TOOL, self.OnInstallButton, self.installButton)
		self.uninstallButton = self.toolbar2.AddTool(202, _('Uninstall'), wx.Bitmap(self.currentdir+"/data/uninstall.png"))
		self.Bind(wx.EVT_TOOL, self.OnUninstallButton, self.uninstallButton)
		self.toolbar2.AddSeparator()
		self.openButton = self.toolbar2.AddTool(204, _('Open'), wx.Bitmap(self.currentdir+"/data/open.png"))
		self.Bind(wx.EVT_TOOL, self.OnOpenButton, self.openButton)
		self.siteButton = self.toolbar2.AddTool(203, 'www', wx.Bitmap(self.currentdir+"/data/info.png"))
		self.Bind(wx.EVT_TOOL, self.OnSiteButton, self.siteButton)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.listApps, 1, wx.EXPAND, 0)
		sizer.Add(self.toolbar2, 0)
		self.apps.SetSizer(sizer)

		sources = subprocess.check_output(['apt-cache', 'policy']).decode(sys.stdin.encoding)
		for i in self.appsDict:
			item = self.listApps.InsertItem(0, i['name'])
			self.listApps.SetItem(item, 1, i['category'])
			candidate = ''
			missing = False
			for ii in i['sources']:
				if not ii in sources:  missing = ii
			if missing: 
				candidate = _('missing source: ')+missing
			if i['dev'] == 'yes': 
				candidate = _('coming soon')
			if candidate:
				self.listApps.SetItem(item, 3, candidate)
			else:
				self.listApps.SetItem(item, 2, _('Press Refresh'))
			self.listApps.SetItemBackgroundColour(item,(200,200,200))

	def pageOutput(self):
		self.logger = rt.RichTextCtrl(self.output, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.logger, 1, wx.EXPAND, 0)
		self.output.SetSizer(sizer)

	def OnInstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		package = apps[index]['package']
		script = self.currentdir+'/'+apps[index]['install']
		msg = _('Are you sure you want to install ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(1)
			command = self.platform.admin+' python3 '+script+' '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Installing package, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			dlg.Destroy()
			self.readApps()
		else: dlg.Destroy()

	def OnUninstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		package = apps[index]['package']
		msg = _('Are you sure you want to uninstall ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(1)
			command = self.platform.admin+' apt autoremove -y '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Uninstalling packages, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			self.ShowStatusBarGREEN(_('Done'))
			dlg.Destroy()
			self.readApps()
		else: dlg.Destroy()

	def OnRefreshButton(self,e):
		self.readApps()

	def OnSiteButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		entryPoint = apps[index]['entryPoint']
		popen = subprocess.Popen(entryPoint, shell=True)

	def readApps(self):
		self.notebook.ChangeSelection(0)
		self.listApps.DeleteAllItems()
		self.ShowStatusBarYELLOW(_('Checking plugins list, please wait... '))
		sources = subprocess.check_output(['apt-cache', 'policy']).decode(sys.stdin.encoding)
		for i in self.appsDict:
			item = self.listApps.InsertItem(0, i['name'])
			self.listApps.SetItem(item, 1, i['category'])

			installed = ''
			candidate = ''
			if not i['package']: installed = _('managed by OpenCPN')
			else:
				command = 'LC_ALL=C apt-cache policy '+i['package']
				popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
					if 'Installed:' in line: installed = line
					if 'Candidate:' in line: candidate = line
				if installed:
					installedL = installed.split(':')
					installed = installedL[1]
				if candidate:
					candidateL = candidate.split(':')
					candidate = candidateL[1]
				if '(none)' in installed: installed = ''

				missing = False
				for ii in i['sources']:
					if not ii in sources:  missing = ii
				if missing: 
					candidate = _('missing source: ')+missing
					self.listApps.SetItemBackgroundColour(item,(200,200,200))

				if i['dev'] == 'yes': 
					candidate = _('coming soon')
					self.listApps.SetItemBackgroundColour(item,(200,200,200))

				if installed and candidate:
					if installed != candidate: self.listApps.SetItemBackgroundColour(item,(220,255,220))

				if not candidate: self.listApps.SetItemBackgroundColour(item,(200,200,200))
				self.listApps.SetItem(item, 3, candidate)

			self.listApps.SetItem(item, 2, installed)
		self.toolbar2.EnableTool(201,False)
		self.toolbar2.EnableTool(202,False)
		self.toolbar2.EnableTool(203,False)
		self.ShowStatusBarGREEN(_('Done'))

	def onListAppsSelected(self, e):
		i = e.GetIndex()
		valid = e and i >= 0
		if not valid: return
		self.onListAppsDeselected()
		opencpnInstalled = self.listApps.GetItemText(0, 2)
		installed = self.listApps.GetItemText(i, 2)
		self.toolbar2.EnableTool(203,True)
		if self.listApps.GetItemBackgroundColour(i) != (200,200,200):
			if not installed: self.toolbar2.EnableTool(201,True)
			elif installed == _('managed by OpenCPN') and opencpnInstalled: self.toolbar2.EnableTool(204,True)
			else:
				if installed and opencpnInstalled:
					self.toolbar2.EnableTool(201,True)
					self.toolbar2.EnableTool(202,True)
					self.toolbar2.EnableTool(204,True)

	def onListAppsDeselected(self, event=0):
		self.toolbar2.EnableTool(201,False)
		self.toolbar2.EnableTool(202,False)
		self.toolbar2.EnableTool(203,False)
		self.toolbar2.EnableTool(204,False)

	def OnOpenButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		installed = self.listApps.GetItemText(index, 2)
		opencpnInstalled = self.listApps.GetItemText(0, 2)
		if installed and opencpnInstalled:
			subprocess.call(['pkill', '-15', 'opencpn'])
			subprocess.Popen('opencpn')

def main():
	app = wx.App()
	MyFrame().Show()
	time.sleep(1)
	app.MainLoop()

if __name__ == '__main__':
	main()
