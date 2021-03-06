import os
import edje
import logging

from terra.core.task import Task
from terra.core.manager import Manager
from terra.core.model import Model, ModelFolder
from terra.core.plugin_prefs import PluginPrefs

manager = Manager()
PluginDefaultIcon = manager.get_class("Icon/Plugin")
Photos  = manager.get_class("Model/Folder/Image/All")

Button  = manager.get_class("Model/Settings/Action")
log = logging.getLogger("plugins.canola-twitpic.model")

class Icon(PluginDefaultIcon):
    terra_type = "Icon/Folder"
    icon = "icon/main_item/photos_local"
    plugin = "canola-twitpic"


class LocalPictures(Photos):
    terra_type = "Model/Folder/Image/Twitpic"

    def __init__(self,name, parent):
        Photos.__init__(self,name, parent)	

class MainModelFolder(ModelFolder, Task):
    terra_type = "Model/Folder/Task/Image/Twitpic"
    terra_task_type = "Task/Folder/Task/Image/Twitpic"

    def __init__(self, parent):
        Task.__init__(self)
        ModelFolder.__init__(self, "Twitpic", parent)

    def do_load(self):
        LocalPictures("All pictures", self)
        
################################################################################
# Twitpic Options Model
################################################################################

class OptionsModel(ModelFolder):
    terra_type = "Model/Settings/Folder/InternetMedia/Twitpic"
    title = "Twitpic"

    def __init__(self, parent=None):
        ModelFolder.__init__(self, self.title, parent)

    def do_load(self):
	print "test"
	UserPassModel(self)
	
class UserPassModel(Button):
        terra_type = "Model/Settings/Folder/InternetMedia/Twitpic/UserPass"
        title ="User/Password"
        
	def __init__(self, parent):
		Button.name = "adada"
        	Button.__init__(self, parent)

"""
MixedListItemOnOff = manager.get_class("Model/Settings/Folder/MixedList/Item/OnOff")
class ScrobblerOptionsModel(MixedListItemOnOff):
    terra_type = "Model/Settings/Folder/InternetMedia/Twitpic/UserPass"
    title = "Scrobble your music"

    def __init__(self, parent=None):
        MixedListItemOnOff.__init__(self, parent)    
    	self.state = True
              
    def get_state(self):
        return (self.title, self.state)

    def on_clicked(self):
        self.set_scrobbler(not self.state)
        self.callback_update(self)

    def set_scrobbler(self, enable):
        self.state = enable
"""

