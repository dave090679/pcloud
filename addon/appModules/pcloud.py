#appModules/pcloud.py
# Ein Teil von NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NVDA Mitwirkende
# Diese Datei unterliegt der GNU General Public License.
# Weitere Informationen finden Sie in der Datei COPYING.
import appModuleHandler
import controlTypes
import api
from scriptHandler import script
import addonHandler
from NVDAObjects.UIA import UIA
# Entfernen Sie das Kommentarzeichen (#) aus der nächsten Zeile, wenn (und sobald) die Datei zu einem Addon gehört. Dadurch werden Lokalisierungsfunktionen (Übersetzungsfunktionen) in Ihrer Datei aktiviert. Weitere Informationen finden Sie im Entwicklungshandbuch für NVDA-Addons.
#addonHandler.initTranslation()
class pcloudcheckbox(UIA):
	def _get_name(self):
		return self.next.next.name
class pcloudlink(UIA):
	def _get_name(self):
		return self.firstChild.name

class pcloudbutton(UIA):
	def _get_name(self):
		l = list()
		for x in self.children:
			if x.name:
				l.append(x.name)
		return "; ".join(l)

class pcloudtabitem(UIA):
	def _get_name(self):
		return self.children[1].name

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


