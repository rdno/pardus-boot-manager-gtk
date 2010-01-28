# -*- coding: utf-8 -*-
"""boot manager gtk main module"""
#
# Rıdvan Örsvuran (C) 2010
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import gtk
import gobject

from boot_manager_gtk.backend import Interface
from boot_manager_gtk.translation import _
from boot_manager_gtk.widgets import BootTimer
from boot_manager_gtk.widgets import BootItemContainer

from dbus.mainloop.glib import DBusGMainLoop

class BootManager(gtk.VBox):
    """BootManager main widget"""
    def __init__(self):
        """init"""
        gtk.VBox.__init__(self, homogeneous=False, spacing=5)
        self._dbus_loop()
        self.iface = Interface()
        self._create_ui()
    def _dbus_loop(self):
        #runs dbus main loop
        DBusGMainLoop(set_as_default = True)
    def _create_ui(self):
        #creates ui
        self.entries = self.iface.getEntries()
        self.options =  self.iface.getOptions()
        self.container = BootItemContainer(self.entries,
                                           self.listen_boot_item_signals)
        self.pack_start(self.container, expand=True, fill=True)

        hbox2 = gtk.HBox(homogeneous=False, spacing=5)
        self.timer = BootTimer(int(self.options["timeout"]))
        self.timer.listen_signal(self.on_timeout_change)
        hbox2.pack_end(self.timer, expand=False, fill=False)
        self.pack_start(hbox2, expand=False, fill=False)
        self.show_all()
    def listen_boot_item_signals(self, widget, data):
        """listen BootItem signals

        Arguments:
        - `widget`: widget
        - `data`: {action:(make_default|edit|delete),
                   props: (ex :{index:0,
                          title:'Pardus',
                          root:/dev/sda1,
                          os_type:linux,
                          default:True})}
        """
        action = data["action"]
        if action == "make_default":
            print "make_default"
        elif action == "edit":
            print "edit"
        elif action == "delete":
            print "delete"
    def on_timeout_change(self, widget, timeout):
        """BootTimer apply button clicked

        Arguments:
        - `widget`: apply_btn of BootTimer
        - `timeout`: function (usage: timeout())
        """
        self.iface.setOption("timeout", str(int(timeout())))
