#appModules/pcloud.py
# Ein Teil von NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NVDA Mitwirkende
# Diese Datei unterliegt der GNU General Public License.
# Weitere Informationen finden Sie in der Datei COPYING.
# Modify By Rainer Brell "NVDA Nachhaltig" 
# 2025.10.21: Added classes pcloudtogglebutton, pcloudcombobox 

import appModuleHandler
import controlTypes
import api
from scriptHandler import script
import addonHandler
from NVDAObjects.UIA import UIA, ListItem
import mouseHandler
# Entfernen Sie das Kommentarzeichen (#) aus der nächsten Zeile, wenn (und sobald) die Datei zu einem Addon gehört. Dadurch werden Lokalisierungsfunktionen (Übersetzungsfunktionen) in Ihrer Datei aktiviert. Weitere Informationen finden Sie im Entwicklungshandbuch für NVDA-Addons.
addonHandler.initTranslation()
class pcloudtabitem(UIA):
	def _get_name(self):
		return self.firstChild.next.name

class pcloudcheckbox(UIA):
	def _get_name(self):
		return self.next.next.name
class pcloudlistitem(ListItem):
	@script (
		category=_('pcloud'),
		description=_("do a left mouse click"),
		gestures=["kb:enter", "kb:space"]
	)
	def script_leftmouseclick(self, gesture):
		api.moveMouseToNVDAObject(self)
		mouseHandler.doPrimaryClick()

	def _get_name(self):
		l = list()
		for x in self.children:
			if x.name != "":
				l.append(x.name)
		return '; '.join(l)
class pcloudlink(UIA):
	def _get_name(self):
		try: 
			s = self.firstChild.name
		except AttributeError:
			s = ""
		return s

class pcloudbutton(UIA):
	def _get_name(self):
		l = list()
		for x in self.children:
			if x.name:
				l.append(x.name)
		return "; ".join(l)

class pcloudtogglebutton(UIA):
	def _get_name(self):
		try:
			try:
				return self.previous.previous.name
			except:
				if self.childCount > 0:
					return self.children[0].name
		except:
			return

class pcloudcombobox(UIA):
	def _get_name(self):
		try: 
			return self.previous.name 
		except:
			return 

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clslist):
		if isinstance(obj, UIA):
			if "System.Windows.Controls.TabItem" in obj.UIAElement.CachedName:
				clslist.insert(0, pcloudtabitem)
			elif obj.role == controlTypes.Role.CHECKBOX and obj.name == "":
				clslist.insert(0, pcloudcheckbox)
			elif obj.role == controlTypes.Role.LINK and obj.name.strip() == "":
				clslist.insert(0, pcloudlink)
			elif obj.role == controlTypes.Role.BUTTON and obj.name == "":
				clslist.insert(0, pcloudbutton)
			elif obj.role == controlTypes.Role.TOGGLEBUTTON and obj.name == "":
				clslist.insert(0, pcloudtogglebutton)
			elif obj.role == controlTypes.Role.COMBOBOX and obj.name == "":
				clslist.insert(0, pcloudcombobox)
			elif "WpfpCloud.Models.Languages" in obj.name and obj.role == controlTypes.Role.LISTITEM:
				clslist.insert(0,pcloudlistitem)
			elif obj.name == "System.Windows.Controls.ListViewItem":
				clslist.insert(0,pcloudlistitem)