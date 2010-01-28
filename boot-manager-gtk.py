#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from boot_manager_gtk import BootManager
from boot_manager_gtk.translation import _

class MainWindow(gtk.Window):
    """MainWindow"""
    def __init__(self):
        """init"""
        gtk.Window.__init__(self)
        self.manager = BootManager()
        self._set_style()
        self._create_ui()
        self._listen_signals()
    def _set_style(self):
        #sets style of window
        self.set_title(_("Boot Manager"))
        self.set_default_size(483, 300)
    def _create_ui(self):
        self.add(self.manager)
    def _listen_signals(self):
        self.connect("destroy", gtk.main_quit)
    def run(self, arg):
        """run app
        
        Arguments:
        - `arg`: sys.argv
        """
        self.show_all()
        gtk.main()
    
        
if __name__ == '__main__':
    import sys
    MainWindow().run(sys.argv)
