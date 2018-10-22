##################################################################################################
################  vuplus-images.co.uk########################
##################################################################################################
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from Screens.Screen import Screen
from Screens.Standby import *
from Tools.Directories import *
from Screens.MessageBox import MessageBox
from Components.Sources.List import List
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Label import Label
from Components.Button import Button
from Components.ScrollLabel import ScrollLabel
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListbox, eTimer, eConsoleAppContainer, eListboxPythonMultiContent, gFont
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, getDesktop, loadPNG, loadPic
from enigma import *
from os import listdir
import os, zipfile, sys, re
from xml.dom import Node, minidom
from twisted.web.client import getPage 
import urllib
DESKHEIGHT = getDesktop(0).size().height()
currversion = '3.1'
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/fonts'
skin_path = "/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/Skin/"
from images import Feeds
from enigma import addFont
try:   
    addFont('%s/Raleway-Black.ttf' % plugin_path, 'Rale', 100, 1) 						
except Exception as ex:
    print ex
	
def main(session, **kwargs):
    session.open(MenuA)

def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('VuPlus-Images Panel'),
          main,
          'VuPlus-Images Panel',
          34)]
    return []

def Plugins(**kwargs):
    list = []
    list.append(PluginDescriptor(icon='/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/addons.png', name='VuPlus-Images Panel', description='By https://vuplus-images.co.uk', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main))
    list.append(PluginDescriptor(icon='/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/addons.png', name='VuPlus-Images Panel', description='By https://vuplus-images.co.uk', where=PluginDescriptor.WHERE_MENU, fnc=menu))
    return list	

Amenu_list = [_('VuPlus Addons'),
 _('Download VuPlus Images'),
 _('Install 28.2E Bouquets'), 
 _('Panel News'),
 _('Panel Update'), 
 _('Panel Information')]

Bmenu_list = [_('Plugins'),
 _('Panels'),
 _('E2 Settings'),
 _('Softcams'),
 _('Picons'),
 _('Skins'),
 _('Dependencies')] 
 
class AmenuList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        if DESKHEIGHT < 1000:		
            self.l.setItemHeight(80)
            self.l.setFont(0, gFont('Rale', 60))
        else:
            self.l.setItemHeight(140)
            self.l.setFont(0, gFont('Rale', 74))			

def AmenuListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 1:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 2:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 3:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'	
    elif idx == 4:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'	
    elif idx == 5:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'			
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 0), size=(220, 132), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(5, 0), size=(1000, 320), font=0, text=name))
    return res

class MenuA(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'menuAHD.xml'
        else:	
		     skin = skin_path + 'menuAFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['text'] = AmenuList([])
        self.working = False
        self.selection = 'all'
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]

        list = []
        idx = 0
        for x in Amenu_list:
            list.append(AmenuListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1

        self['text'].setList(list)

    def okClicked(self):
        self.keyNumberGlobal(self['text'].getSelectedIndex())

    def keyNumberGlobal(self, idx):
        sel = self.menu_list[idx]
        if sel == _('VuPlus Addons'):
            self.session.open(MenuB)
        elif sel == _('Download VuPlus Images'):
            self.session.open(Feeds)
        elif sel == _('Panel News'):
            self.session.open(News)
        elif sel == _('Panel Information'):
            self.session.open(Infoo)
        elif sel == _('Install 28.2E Bouquets'):
            self.session.open(BouquetUpdate)
        elif sel == _('Panel Update'):
            self.session.open(Update)			
	
class BmenuList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        if DESKHEIGHT < 1000:		
            self.l.setItemHeight(75)
            self.l.setFont(0, gFont('Rale', 65))
        else:
            self.l.setItemHeight(110)
            self.l.setFont(0, gFont('Rale',74))			

def BmenuListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 1:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    if idx == 2:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 3:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    if idx == 4:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 5:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'
    elif idx == 6:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/VuPlusImagesCoUk/pics/'		
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 0), size=(0, 0), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(5, 0), size=(1000, 320), font=0, text=name))
    return res		

class MenuB(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'menuBHD.xml'
        else:	
		     skin = skin_path + 'menuBFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)	
        self['text'] = BmenuList([])
        self.working = False
        self.selection = 'all'
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,		
         'cancel': self.close}, -1)
        self.onLayoutFinish.append(self.updateMenuList)
		
    def remove(self):
        self.session.open(Remove)			

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]

        list = []
        idx = 0
        for x in Bmenu_list:
            list.append(BmenuListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1

        self['text'].setList(list)

    def okClicked(self):
        self.keyNumberGlobal(self['text'].getSelectedIndex())

    def keyNumberGlobal(self, idx):
        sel = self.menu_list[idx]
        if sel == _('Plugins'):
            self.session.open(Pluginss)
        elif sel == _('Panels'):
            self.session.open(Panelss)
        elif sel == _('E2 Settings'):
            self.session.open(Settingss)
        elif sel == _('Softcams'):
            self.session.open(Softcams)
        elif sel == _('Picons'):
            self.session.open(Picons)
        elif sel == _('Skins'):
            self.session.open(Skins)
        elif sel == _('Dependencies'):
            self.session.open(Dependencies)

###################	
class FirstList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		if DESKHEIGHT < 1000: 
		       self.l.setItemHeight(38)
		       textfont = int(34)
		else:
		       self.l.setItemHeight(55)
		       textfont = int(47)
                self.l.setFont(0, gFont("Rale", textfont))             

def FirstListEntry(name):
	res = [name]  

        res.append(MultiContentEntryText(pos=(5, 0), size=(1000, 320), font=0, text=name))

        return res

def showlist(data, list):                   
    icount = 0
    plist = []
    for line in data:

        name = data[icount]                               
        plist.append(FirstListEntry(name))                               
        icount = icount+1
	list.setList(plist)			
###################				
class OtherList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		if DESKHEIGHT < 1000: 
		       self.l.setItemHeight(30)
		       textfont = int(26)
		else:
		       self.l.setItemHeight(50)
		       textfont = int(42)
                self.l.setFont(0, gFont("Rale", textfont))                

def OtherListEntry(name):
	res = [name]  

        res.append(MultiContentEntryText(pos=(5, 0), size=(1000, 320), font=0, text=name))

        return res

def lastlist(data, list):                   
    icount = 0
    plist = []
    for line in data:

        name = data[icount]                               
        plist.append(OtherListEntry(name))                               
        icount = icount+1
	list.setList(plist)	
###################				
class PiconsList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		if DESKHEIGHT < 1000: 
		       self.l.setItemHeight(37)
		       textfont = int(24)
		else:
		       self.l.setItemHeight(44)
		       textfont = int(36)
                self.l.setFont(0, gFont("Rale", textfont))                

def PiconsListEntry(name):
	res = [name]  

        res.append(MultiContentEntryText(pos=(5, 0), size=(1000, 320), font=0, text=name))

        return res

def lastlist(data, list):                   
    icount = 0
    plist = []
    for line in data:

        name = data[icount]                               
        plist.append(PiconsListEntry(name))                               
        icount = icount+1
	list.setList(plist)	
###################	
class Pluginss(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'pluginsHD.xml'
        else:	
		     skin = skin_path + 'pluginsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []		
        self['text'] = FirstList([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))		
        self.downloading = False
        self["plug"] = Pixmap()		
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Plugins.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Pluginss data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Pluginss self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Pluginss match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...')					   
            
            showlist(self.list, self['text'])							
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installall, self.xml, name)
            except:
                return

        else:
            self.close

class Panelss(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'panelsHD.xml'
        else:	
		     skin = skin_path + 'panelsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []		
        self['text'] = FirstList([])  
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self.downloading = False
        self["pan"] = Pixmap()			
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Panels.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Panelss data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Panelss self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Panelss match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...')     
				   
            showlist(self.list, self['text'])			
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installall, self.xml, name)
            except:
                return

        else:
            self.close

class Settingss(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'settingsHD.xml'
        else:	
		     skin = skin_path + 'settingsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []
        self['text'] = FirstList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self.downloading = False
        self["sett"] = Pixmap()		
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/E2Settings.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Others data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Others self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Others match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...')  
				   
            showlist(self.list, self['text'])			
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installall, self.xml, name)
            except:
                return

        else:
            self.close			

class Softcams(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'softcamsHD.xml'
        else:	
		     skin = skin_path + 'softcamsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []
        self['text'] = FirstList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self.downloading = False
        self["soft"] = Pixmap()		
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Softcams.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Softcams data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Softcams self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Softcams match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...') 
				   
            showlist(self.list, self['text'])			
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installall, self.xml, name)
            except:
                return

        else:
            self.close

class Picons(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'piconsHD.xml'
        else:	
		     skin = skin_path + 'piconsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []
        self['text'] = FirstList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self.downloading = False
        self["pic"] = Pixmap()		
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Picons.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Picons data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Picons self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Picons match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...')
				   
            showlist(self.list, self['text'])			
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installallpicons, self.xml, name)
            except:
                return

        else:
            self.close

class Installallpicons(Screen):

    def __init__(self, session, data, name):
        self.session = session
        print "In Installall data =", data
        print "In Installall name =", name
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'allpiconsHD.xml'
        else:	
		     skin = skin_path + 'allpiconsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)					
        list = []
        """		
        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
 		            list.append(plugin.getAttribute('name').encode('utf8'))
					
        list.sort()
        """
        list.sort()		
        n1 = data.find(name, 0)
        n2 = data.find("</plugins>", n1)
        data1 = data[n1:n2]
        print "In Installall data1 =", data1
        self.names = []
        self.urls = []
        regex = '<plugin name="(.*?)".*?url>"(.*?)"'
	match = re.compile(regex,re.DOTALL).findall(data1)
	print "In Installall match =", match
        for name, url in match:
                self.names.append(name)
                self.urls.append(url)				

        print "In Installall self.names =", self.names
        self['text'] = PiconsList([])
        self['info'] = Label(_('Please select to install ...'))		
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.selclicked,
         'cancel': self.close}, -2)	 
        self.onLayoutFinish.append(self.start)

    def start(self):	
        showlist(self.names, self['text'])
		
    def selclickedX(self):
        try:
            selection_country = self['text'].getCurrent()
        except:
            return

        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
                    if plugin.getAttribute('name').encode('utf8') == selection_country:
                        urlserver = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
                        pluginname = plugin.getAttribute('name').encode('utf8')
                        self.prombt(urlserver, pluginname)

    def selclicked(self):
             idx = self["text"].getSelectionIndex()
             dom = self.names[idx]
             com = self.urls[idx]
             self.prombt(com, dom)

    def prombt(self, com, dom):
        self.com = com
        self.dom = dom
        self.session.open(Konzola, _('downloading-installing: %s') % dom, ['opkg install -force-overwrite -force-depends %s' % com])

    def callMyMsg(self, result):
        if result:
            dom = self.dom
            com = self.com
            self.session.open(Konzola, _('downloading-installing: %s') % dom, ['ipkg install -force-overwrite -force-depends %s' % com])					
			
class Skins(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'skinsHD.xml'
        else:	
		     skin = skin_path + 'skinsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []
        self['text'] = FirstList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self.downloading = False
        self["skin"] = Pixmap()		
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Skins.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Skins data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Skins self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Skins match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...')
				   
            showlist(self.list, self['text'])			
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installall, self.xml, name)
            except:
                return

        else:
            self.close
			
class Dependencies(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'dependenciesHD.xml'
        else:	
		     skin = skin_path + 'dependenciesFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.list = []
        self['text'] = FirstList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self.downloading = False
        self["dep"] = Pixmap()		
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.openTest)		

    def openTest(self):
        url = 'http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Dependencies.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText('Try again later ...')
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In Pluginss data =", data
        self.xml = data
        try:
            """
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.names = []		
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            """
            print "In Pluginss self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
	    match = re.compile(regex,re.DOTALL).findall(self.xml)
	    print "In Pluginss match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText('Please select ...')				   
            
            showlist(self.list, self['text'])			
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(Installall, self.xml, name)
            except:
                return

        else:
            self.close			
			
class Installall(Screen):

    def __init__(self, session, data, name):
        self.session = session
        print "In Installall data =", data
        print "In Installall name =", name
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'allHD.xml'
        else:	
		     skin = skin_path + 'allFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)					
        list = []
        """		
        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
 		            list.append(plugin.getAttribute('name').encode('utf8'))
					
        list.sort()
        """
        list.sort()		
        n1 = data.find(name, 0)
        n2 = data.find("</plugins>", n1)
        data1 = data[n1:n2]
        print "In Installall data1 =", data1
        self.names = []
        self.urls = []
        regex = '<plugin name="(.*?)".*?url>"(.*?)"'
	match = re.compile(regex,re.DOTALL).findall(data1)
	print "In Installall match =", match
        for name, url in match:
                self.names.append(name)
                self.urls.append(url)				

        print "In Installall self.names =", self.names
        self['text'] = OtherList([])
        self['info'] = Label(_('Please select to install ...'))		
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.selclicked,
         'cancel': self.close}, -2)	 
        self.onLayoutFinish.append(self.start)

    def start(self):	
        showlist(self.names, self['text'])
		
    def selclickedX(self):
        try:
            selection_country = self['text'].getCurrent()
        except:
            return

        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
                    if plugin.getAttribute('name').encode('utf8') == selection_country:
                        urlserver = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
                        pluginname = plugin.getAttribute('name').encode('utf8')
                        self.prombt(urlserver, pluginname)

    def selclicked(self):
             idx = self["text"].getSelectionIndex()
             dom = self.names[idx]
             com = self.urls[idx]
             self.prombt(com, dom)

    def prombt(self, com, dom):
        self.com = com
        self.dom = dom
        self.session.open(Konzola, _('downloading-installing: %s') % dom, ['opkg install -force-overwrite -force-depends %s' % com])

    def callMyMsg(self, result):
        if result:
            dom = self.dom
            com = self.com
            self.session.open(Konzola, _('downloading-installing: %s') % dom, ['ipkg install -force-overwrite -force-depends %s' % com])		

class Konzola(Screen):

    def __init__(self, session, title = 'Konzola', cmdlist = None, finishedCallback = None, closeOnSuccess = False):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'konzHD.xml'
        else:	
		     skin = skin_path + 'konzFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions'], {'ok': self.cancel,
         'back': self.cancel,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.newtitle = title
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        self['text'].setText(_('Execution Progress:') + '\n\n')
        print 'Console: executing in run', self.run, ' the command:', self.cmdlist[self.run]
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            str = self['text'].getText()
            str += _('Execution finished!!')
            self['text'].setText(str)
            self['text'].lastPage()
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not retval and self.closeOnSuccess:
                self.cancel()
        return

    def cancel(self):
        if self.run == len(self.cmdlist):
            self.close()
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)

    def dataAvail(self, str):
        self['text'].setText(self['text'].getText() + str)
			
class News(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'infoHD.xml'
        else:	
		     skin = skin_path + 'infoFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        info = ''
        self['text'] = ScrollLabel(info)
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions'], {'right': self['text'].pageDown,
         'ok': self.close,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown,
         'cancel': self.close,
         'left': self['text'].pageUp}, -1)
        try:
            fp = urllib.urlopen('http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/News.txt')
            count = 0
            self.labeltext = ''
            while True:
                s = fp.readline()
                count = count + 1
                self.labeltext = self.labeltext + str(s)
                if s:
                    continue
                else:
                    break
                    continue

            fp.close()
            self['text'].setText(self.labeltext)
        except:
            self['text'].setText('Unable to download...')			

class BouquetUpdate(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'bouquetHD.xml'
        else:	
		     skin = skin_path + 'bouquetFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['lbl'] = Label()
        self['lbl'].setText('')
        self['info'] = Label()
        self['info'].setText('Downloading bouquets, please wait...')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.close,
         'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.downloadbouquets)		 

    def downloadbouquets(self):
        ZipURL = 'http://panel.vuplus-images.co.uk/Donki/Donki.zip'
        TempLoc = '/tmp/Donki.zip'
        urlerror = 0
        self['info'].setText('')

        try:
            testfile = urllib.URLopener()
            testfile.retrieve(ZipURL, TempLoc)
            zfile = zipfile.ZipFile(TempLoc)
            zfile.extractall('/etc/enigma2/')
            testfile.close()
            zfile.close()

            eDVBDB.getInstance().reloadServicelist()
            eDVBDB.getInstance().reloadBouquets()

        except IOError:
            urlerror = 1

        if os.path.exists(TempLoc):
            os.remove(TempLoc)

        if urlerror == 0:
            self['lbl'].setText('Bouquets updated.\n\n\nThank you for using vuplus-images-addons\n\nSupport forum @ vuplus-images.co.uk')
        else:
            self['lbl'].setText('Server error - maybe server down!')			
			
class Infoo(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'aboutHD.xml'
        else:	
		     skin = skin_path + 'aboutFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        info = ''
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.close,
         'cancel': self.close}, -1)	

class Update(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:		
            skin = skin_path + 'upHD.xml'
        else:	
		     skin = skin_path + 'upFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        info = ''
        self['key_red'] = Button(_('Exit'))
        self['key_yellow'] = Button(_('Update'))
        self['text'] = Label()
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions', 'ColorActions'], {'ok': self.close,
         'cancel': self.close,
         'red': self.close,
         'yellow': self.runupdate}, -1)
        try:
            fp = urllib.urlopen('http://panel.vuplus-images.co.uk/VuPlus-Images-Panel/Version.txt')
            count = 0
            self.labeltext = ''
            s1 = fp.readline()
            s2 = fp.readline()
            s3 = fp.readline()
            s1 = s1.strip()
            s2 = s2.strip()
            s3 = s3.strip()
            self.link = s2
            self.version = s1
            self.info = s3
            fp.close()
            cstr = s1 + ' ' + s2
            if s1 == currversion:
                self['text'].setText('VuPlus-Images Panel version: ' + currversion + '\n\nNo updates available!')
                self.update = False
            else:
                updatestr = '\nVuPlus-Images Panel version: ' + currversion + '\n\nNew update ' + s1 + ' is available!  \n\nUpdates:' + self.info + '\n\n\n\nPress yellow button to start updating'
                self.update = True
                self['text'].setText(updatestr)
        except:
            self.update = False
            self['text'].setText('Unable to check for updates\n\nNo internet connection or server down\n\nPlease check later')

    def runupdate(self):
        if self.update == False:
            return
        com = self.link
        dom = 'Updating plugin to ' + self.version
        self.session.open(Konzola, _('downloading-installing: %s') % dom, ['opkg install -force-overwrite %s' % com])
		 