import logging
import ecore
from terra.core.manager import Manager
from terra.core.threaded_func import ThreadedFunction
from terra.ui.base import PluginThemeMixin

from twit import *

manager = Manager()
ThumbController = manager.get_class("Controller/Folder/Image")
EntryDialogModel = manager.get_class("Model/EntryDialog")
NotifyModel = manager.get_class("Model/Notify")
WaitNotifyModel = manager.get_class("Model/WaitNotify")

log = logging.getLogger("plugins.canola-twitpic.controller")

class TwitController(ThumbController):
	terra_type = "Controller/Folder/Image/Twitpic"
	def __init__(self, model, canvas, parent):
		ThumbController.__init__(self,model, canvas,parent)
	
	def _cb_on_clicked(self, image_frame):

		def th_function(upload):
			upload.upload()

		def th_finished(exception, retval):
			self.waitDialog.stop()
			code, msg = self.upload.getResponse()
			dialog = NotifyModel("Upload to Twitpic", msg , answer_callback=None)
			self.parent.show_notify(dialog)


		def do_search(ignored, text):
			if text is None:
				return
			self.upload = TwitPic("canolaplugin", "654321")

			self.upload.setPicture(image_frame.model.path)
			if text != "":
				self.upload.setMessage(text)

		        ThreadedFunction(th_finished, th_function, self.upload).start()
			self.waitDialog = WaitNotifyModel("Uploading picture...", 1000)
			self.parent.show_notify(self.waitDialog)

	        dialog = EntryDialogModel("Upload picture to Twitpic", "Enter message:", answer_callback=do_search)
		self.parent.show_notify(dialog)


