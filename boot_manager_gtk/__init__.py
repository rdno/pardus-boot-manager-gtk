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
from boot_manager_gtk.utils import dummy_entry
from boot_manager_gtk.widgets import BootTimer
from boot_manager_gtk.widgets import BootItemContainer
from boot_manager_gtk.widgets import NewButton
from boot_manager_gtk.windows import EditWindow

from dbus.mainloop.glib import DBusGMainLoop

class BootManager(gtk.VBox):
    """BootManager main widget"""
    def __init__(self):
        """init"""
        gtk.VBox.__init__(self, homogeneous=False, spacing=5)
        self._dbus_loop()
        self.iface = Interface()
        self.entries = self.iface.getEntries()
        self.options =  self.iface.getOptions()
        self.systems = self.iface.getSystems()
        self._create_ui()
    def _dbus_loop(self):
        #runs dbus main loop
        DBusGMainLoop(set_as_default = True)
    def _create_ui(self):
        #creates ui
        header = gtk.HBox(homogeneous=False, spacing=5)
        self.new_btn = NewButton(self.systems)
        self.new_btn.connect_clicked(self.on_new_btn)
        header.pack_start(self.new_btn, expand=False, fill=False)
        self.pack_start(header, expand=False, fill=False)

        self.container = BootItemContainer(self.entries,
                                           self.listen_boot_item_signals)
        self.pack_start(self.container, expand=True, fill=True)

        footer = gtk.HBox(homogeneous=False, spacing=5)

        self.timer = BootTimer(int(self.options["timeout"]))
        self.timer.listen_signal(self.on_timeout_change)

        footer.pack_end(self.timer, expand=False, fill=False)
        self.pack_start(footer, expand=False, fill=False)
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
        props = data["props"]
        if action == "make_default":
            print "make_default"
        elif action == "edit":
            EditWindow(self.entries[props["index"]],
                       self.on_edit).show()
        elif action == "delete":
            m = _("Do you want to delete the entry '%s' ?") % \
                props["title"]
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_WARNING,
                                       buttons=gtk.BUTTONS_YES_NO,
                                       message_format=m)
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                try:
                    self.iface.removeEntry(props["index"],
                                           props["title"])
                except Exception, e:
                    self._on_exception(e)
            dialog.destroy()
    def _on_exception(self, e):
        if "Comar.PolicyKit" in e._dbus_error_name:
            self.open_error_dialog(_("Access Denied"))
        else:
            self.open_error_dialog(unicode(e))
    def on_timeout_change(self, widget, timeout):
        """BootTimer apply button clicked

        Arguments:
        - `widget`: apply_btn of BootTimer
        - `timeout`: function (usage: timeout())
        """
        self.iface.setOption("timeout", str(int(timeout())))
    def on_edit(self, entry, window):
        """on EditWindow ok_btn clicked"""
        default = "no"
        if entry.has_key("default"):
            if entry["default"] == "yes":
                default = "yes"
        try:
            self.iface.setEntry(entry["title"], entry["os_type"],
                                entry["root"], entry["kernel"],
                                entry["initrd"], entry["options"],
                                default, entry["index"])
            window.destroy()
        except Exception, e:
            self._on_exception(e)
    def on_new_btn(self, name):
        """on new button clicked and type of system selected

        Arguments:
        - `name`: system name
        """
        EditWindow(dummy_entry(self.systems, name),
                   self.on_edit).show()
    def open_error_dialog(self, text):
        """opens a error dialog"""
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                                   buttons=gtk.BUTTONS_OK,
                                   message_format=text)
        dialog.run()
        dialog.destroy()
