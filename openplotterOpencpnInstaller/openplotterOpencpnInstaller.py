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
		
		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.apps = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('Install'))
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
		self.pageOutput()

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': self.Maximize()
		
		self.Centre() 
		self.read()

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

	def pageApps(self):
		self.text = wx.StaticText(self.apps, label=_('Installing from Debian/Ubuntu PPA (recommended for most cases)'))

		self.toolbar2 = wx.ToolBar(self.apps, style=wx.TB_TEXT)
		installButton = self.toolbar2.AddTool(201, _('Install'), wx.Bitmap(self.currentdir+"/data/launchpad.png"))
		self.Bind(wx.EVT_TOOL, self.OnInstallButton, installButton)
		updateButton = self.toolbar2.AddTool(203, _('Update'), wx.Bitmap(self.currentdir+"/data/caution.png"))
		self.Bind(wx.EVT_TOOL, self.OnInstallButton, updateButton)
		self.toolbar2.AddSeparator()
		uninstallButton = self.toolbar2.AddTool(202, _('Uninstall'), wx.Bitmap(self.currentdir+"/data/uninstall.png"))
		self.Bind(wx.EVT_TOOL, self.OnUninstallButton, uninstallButton)
		self.toolbar2.AddSeparator()
		toolStartup = self.toolbar2.AddCheckTool(205, _('Autostart'), wx.Bitmap(self.currentdir+"/data/autostart.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStartup, toolStartup)
		toolFull = self.toolbar2.AddCheckTool(206, _('Full Screen'), wx.Bitmap(self.currentdir+"/data/fullscreen.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolFull, toolFull)
		self.toolbar2.AddSeparator()
		openButton = self.toolbar2.AddTool(204, _('Open'), wx.Bitmap(self.currentdir+"/data/open.png"))
		self.Bind(wx.EVT_TOOL, self.OnOpenButton, openButton)

		self.textFP = wx.StaticText(self.apps, label=_('Installing from Flatpak (recommended for 64-bit)'))

		self.toolbar3 = wx.ToolBar(self.apps, style=wx.TB_TEXT)
		installButtonFP = self.toolbar3.AddTool(301, _('Install'), wx.Bitmap(self.currentdir+"/data/flatpak.png"))
		self.Bind(wx.EVT_TOOL, self.OnInstallButtonFP, installButtonFP)
		updateButtonFP = self.toolbar3.AddTool(303, _('Update'), wx.Bitmap(self.currentdir+"/data/caution.png"))
		self.Bind(wx.EVT_TOOL, self.OnUpdateButtonFP, updateButtonFP)
		self.toolbar3.AddSeparator()
		uninstallButtonFP = self.toolbar3.AddTool(302, _('Uninstall'), wx.Bitmap(self.currentdir+"/data/uninstall.png"))
		self.Bind(wx.EVT_TOOL, self.OnUninstallButtonFP, uninstallButtonFP)
		self.toolbar3.AddSeparator()
		toolStartupFP = self.toolbar3.AddCheckTool(305, _('Autostart'), wx.Bitmap(self.currentdir+"/data/autostart.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStartupFP, toolStartupFP)
		toolFullFP = self.toolbar3.AddCheckTool(306, _('Full Screen'), wx.Bitmap(self.currentdir+"/data/fullscreen.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolFullFP, toolFullFP)
		self.toolbar3.AddSeparator()
		openButtonFP = self.toolbar3.AddTool(304, _('Open'), wx.Bitmap(self.currentdir+"/data/open.png"))
		self.Bind(wx.EVT_TOOL, self.OnOpenButtonFP, openButtonFP)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.text, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.toolbar2, 0, wx.ALL | wx.EXPAND, 5)
		sizer.AddSpacer(10)
		sizer.Add(self.textFP, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.toolbar3, 0, wx.ALL | wx.EXPAND, 5)
		self.apps.SetSizer(sizer)

	def pageOutput(self):
		self.logger = rt.RichTextCtrl(self.output, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.logger, 1, wx.EXPAND, 0)
		self.output.SetSizer(sizer)

	def OnInstallButton(self,e):
		msg = _('Are you sure you want to install OpenCPN from Debian/Ubuntu PPA and its dependencies?')+'\n\n'+_('OpenCPN version: ')+self.candidate
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(1)
			command = self.platform.admin+' python3 '+self.currentdir+'/install.py'
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Installing package, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			self.read()
			self.notebook.ChangeSelection(0)
			self.SetStatusText('')
		dlg.Destroy()

	def OnUninstallButton(self,e):
		msg = _('Are you sure you want to uninstall OpenCPN and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(1)
			command = self.platform.admin+' apt autoremove -y opencpn'
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Uninstalling packages, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			self.read()
			self.notebook.ChangeSelection(0)
			self.SetStatusText('')
		dlg.Destroy()

	def OnOpenButton(self,e):
		subprocess.call(['pkill', '-15', 'opencpn'])
		subprocess.Popen('opencpn')

	def OnToolStartup(self, e):
		if self.toolbar2.GetToolState(205):
			self.conf.set('OPENCPN', 'autostart', '1')
			self.ShowStatusBarBLACK(_('OpenCPN autostart enabled'))
			self.toolbar2.EnableTool(206,True)
		else: 
			self.conf.set('OPENCPN', 'autostart', '0')
			self.ShowStatusBarBLACK(_('OpenCPN autostart disabled'))
			self.toolbar2.EnableTool(206,False)

	def OnToolFull(self, e):
		if self.toolbar2.GetToolState(206):
			self.conf.set('OPENCPN', 'fullscreen', '1')
			self.ShowStatusBarBLACK(_('OpenCPN fullscreen autostart enabled'))
		else: 
			self.conf.set('OPENCPN', 'fullscreen', '0')
			self.ShowStatusBarBLACK(_('OpenCPN fullscreen autostart disabled'))

	def OnInstallButtonFP(self,e):
		pass

	def OnUpdateButtonFP(self,e):
		pass

	def OnUninstallButtonFP(self,e):
		pass

	def OnOpenButtonFP(self,e):
		pass

	def OnToolStartupFP(self, e):
		if self.toolbar3.GetToolState(305):
			self.conf.set('OPENCPN', 'autostartFP', '1')
			self.ShowStatusBarBLACK(_('OpenCPN autostart enabled'))
			self.toolbar3.EnableTool(306,True)
		else: 
			self.conf.set('OPENCPN', 'autostartFP', '0')
			self.ShowStatusBarBLACK(_('OpenCPN autostart disabled'))
			self.toolbar3.EnableTool(306,False)

	def OnToolFullFP(self, e):
		if self.toolbar3.GetToolState(306):
			self.conf.set('OPENCPN', 'fullscreenFP', '1')
			self.ShowStatusBarBLACK(_('OpenCPN fullscreen autostart enabled'))
		else: 
			self.conf.set('OPENCPN', 'fullscreenFP', '0')
			self.ShowStatusBarBLACK(_('OpenCPN fullscreen autostart disabled'))

	def read(self):
		command = 'LC_ALL=C apt-cache policy opencpn'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if 'Installed:' in line: installed = line
			if 'Candidate:' in line: candidate = line
		if installed:
			installed = installed.split(':')
			self.installed = installed[1].strip()
		if candidate:
			candidate = candidate.split(':')
			self.candidate = candidate[1].strip()
		if '(none)' in self.installed:
			self.toolbar2.EnableTool(201,True)
			self.toolbar2.EnableTool(202,False)
			self.toolbar2.EnableTool(203,False)
			self.toolbar2.EnableTool(204,False)
			self.toolbar2.EnableTool(205,False)
			self.toolbar2.EnableTool(206,False)
		else:
			self.toolbar2.EnableTool(201,False)
			self.toolbar2.EnableTool(202,True)
			self.toolbar2.EnableTool(204,True)
			self.toolbar2.EnableTool(205,True)
			self.toolbar2.EnableTool(203,False)
			if self.installed != self.candidate:
				installed = self.installed.split('.')
				candidate = self.candidate.split('.')
				lastInstalled = ''
				lastCandidate = ''
				for i in installed[2]:
					try:
						int(i)
						lastInstalled += i
					except:break
				for i in candidate[2]:
					try:
						int(i)
						lastCandidate += i
					except:break
				try:
					if int(candidate[0]) > int(installed[0]): 
						self.toolbar2.EnableTool(203,True)
						self.ShowStatusBarYELLOW(_('There is a new OpenCPN version: ')+self.candidate)
					if int(candidate[0]) == int(installed[0]):
						if int(candidate[1]) > int(installed[1]): 
							self.toolbar2.EnableTool(203,True)
							self.ShowStatusBarYELLOW(_('There is a new OpenCPN version: ')+self.candidate)
						if int(candidate[1]) == int(installed[1]):
							if int(lastCandidate) > int(lastInstalled): 
								self.toolbar2.EnableTool(203,True)
								self.ShowStatusBarYELLOW(_('There is a new OpenCPN version: ')+self.candidate)
				except: self.toolbar2.EnableTool(203,True)
			if self.conf.get('OPENCPN', 'autostart') == '1': self.toolbar2.ToggleTool(205,True)
			if self.conf.get('OPENCPN', 'fullscreen') == '1': self.toolbar2.ToggleTool(206,True)
			if self.toolbar2.GetToolState(205): self.toolbar2.EnableTool(206,True)
			else: self.toolbar2.EnableTool(206,False)

		
		self.toolbar3.EnableTool(301,False)
		self.toolbar3.EnableTool(302,False)
		self.toolbar3.EnableTool(303,False)
		self.toolbar3.EnableTool(304,False)
		self.toolbar3.EnableTool(305,False)
		self.toolbar3.EnableTool(306,False)
		if self.conf.get('OPENCPN', 'autostartFP') == '1': self.toolbar3.ToggleTool(305,True)
		if self.conf.get('OPENCPN', 'fullscreenFP') == '1': self.toolbar3.ToggleTool(306,True)
		if self.toolbar3.GetToolState(305): self.toolbar3.EnableTool(306,True)
		else: self.toolbar3.EnableTool(306,False)

def main():
	try:
		platform2 = platform.Platform()
		if not platform2.postInstall(version,'opencpn'):
			subprocess.Popen(['openplotterPostInstall', platform2.admin+' opencpnPostInstall'])
			return
	except: pass

	app = wx.App()
	MyFrame().Show()
	time.sleep(1)
	app.MainLoop()

if __name__ == '__main__':
	main()
