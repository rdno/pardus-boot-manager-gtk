# -*- coding: utf-8 -*-
"""includes widgets for boot manager gtk

BootItem - BootItem widget
BootItemContainer - includes BootItem widgets (gtk.ScrolledWindow)
NewButton -
BootTimer - A widget for adjust boot timeout

"""
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

from boot_manager_gtk.translation import _
from boot_manager_gtk.utils import get_disk_by_uuid

class BootItem(gtk.Table):
    """BootItem widget"""
    def __init__(self, props):
        """init
        
        Arguments:
        - `props`: props (ex:{index:0,
                              title:'Pardus',
                              root:/dev/sda1,
                              os_type:linux,
                              default:True} )
        """
        gtk.Table.__init__(self, rows=2, columns=5)
        self._props = props
        self._create_ui()
        self._insert_data()
    def _create_ui(self):
        self.check_btn = gtk.CheckButton()

        self._name_lb = gtk.Label()
        self._name_lb.set_alignment(0.0, 0.5)
        self._device_lb = gtk.Label()
        self._device_lb.set_alignment(0.0, 0.5)
        self.edit_btn = gtk.Button(_("Edit"))
        self.delete_btn = gtk.Button(_("Delete"))

        self.attach(self.check_btn, 0, 1, 0, 2,
                    gtk.SHRINK, gtk.SHRINK)
        #icon goes here: self.attach(self._icon, 0, 2, 1, 2)
        self.attach(self._name_lb, 2, 3, 0, 1,
                    gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self.attach(self._device_lb, 2, 3, 1, 2,
                    gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self.attach(self.edit_btn, 3, 4, 0, 2,
                    gtk.SHRINK, gtk.SHRINK)
        self.attach(self.delete_btn, 4, 5, 0, 2,
                    gtk.SHRINK, gtk.SHRINK)
    def _insert_data(self):
        #show data
        self.check_btn.set_active(self._props["default"])
        self._name_lb.set_markup("<b>"+self._props["title"]+"</b>")
        self._device_lb.set_label(self._props["root"])
    def listen_signals(self, func):
        """listen BootItem signals

        Arguments:
        - `func`: callback function
        """
        self.check_btn.connect("clicked", func,
                               {"action":"make_default",
                                "props":self._props})
        self.edit_btn.connect("clicked", func,
                              {"action":"edit",
                               "props":self._props})
        self.delete_btn.connect("clicked", func,
                                {"action":"delete",
                                 "props":self._props})

gobject.type_register(BootItem)

class BootItemContainer(gtk.ScrolledWindow):
    """includes BootItem widgets (gtk.ScrolledWindow)"""
    def __init__(self, entries, callback_func):
        """init
        
        Arguments:
        - `entries`: boot entries
        - `callback_func`: callback function for BootItem signals
        """
        gtk.ScrolledWindow.__init__(self)
        self._entries = entries
        self._func = callback_func
        self._set_style()
        self._create_ui()
    def _set_style(self):
        #sets style of ScrolledWindow
        self.set_shadow_type(gtk.SHADOW_IN)
        self.set_policy(gtk.POLICY_NEVER,
                        gtk.POLICY_AUTOMATIC)
    def _create_ui(self):
        self.vbox = gtk.VBox(spacing=5)
        self.add_with_viewport(self.vbox)
        self.add_boot_items(self._entries)
    def add_boot_items(self, items):
        self._entries = items
        for child in self.vbox.get_children():
            self.vbox.remove(child)
        for index, entry in enumerate(items):
            props = {}
            props["index"] = index
            props["title"] = entry["title"]
            if "root" in entry:
                props["root"] = entry["root"]
            elif "uuid" in entry:
                props["root"] = get_disk_by_uuid(entry["uuid"])
            else:
                props["root"] = ""
            props["default"] = False
            if "default" in entry:
                if entry["default"] == "yes":
                    props["default"] = True
            props["os_type"] = entry["os_type"]
            self.add_boot_item(props)
    def add_boot_item(self, props):
        """adds a BootItem
        
        Arguments:
        - `props`: props
        """
        boot_item = BootItem(props)
        boot_item.listen_signals(self._func)
        self.vbox.pack_start(boot_item, expand=False, fill=False)
        self.vbox.show_all()
    
class BootTimer(gtk.HBox):
    """A widget for adjust boot timeout"""
    def __init__(self, current_timeout):
        """init

        Arguments:
        - `current_timeout`: current timeout
        """
        gtk.HBox.__init__(self, homogeneous=False, spacing=5)
        self._default = current_timeout
        self._create_ui()
        self._listen_signals()
    def _create_ui(self):
        #creates ui
        self._info_lb = gtk.Label(_("Boot menu display time:"))
        adj = gtk.Adjustment(value=self._default, lower=0, upper=1000,
                             step_incr=1)
        self._timeout_sb = gtk.SpinButton(adj)
        self.apply_btn = gtk.Button(_("Apply"))
        self.apply_btn.set_sensitive(False)
        self.pack_start(self._info_lb, expand=False, fill=False)
        self.pack_start(self._timeout_sb, expand=False, fill=False)
        self.pack_start(self.apply_btn, expand=False, fill=False)
    def set_timeout(self, value):
        self._timeout_sb.set_value(value)
        self._default = value
    def _listen_signals(self):
        #private signals
        def callback_func(widget):
            #if timeout value is equal to default then
            #no need to apply
            if widget.get_value() == self._default:
                self.apply_btn.set_sensitive(False)
            else:
                self.apply_btn.set_sensitive(True)
        self._timeout_sb.connect("value-changed", callback_func)
    def listen_signal(self, func):
        """listen apply_btn click signal

        Arguments:
        - `func`: callback_func
        """
        self.apply_btn.connect("clicked", func,
                               self._timeout_sb.get_value)


class NewButton(gtk.Button):
    """NewButton"""
    def __init__(self, systems):
        """init

        Arguments:
        - `systems`: iface.getSystems()
        """
        gtk.Button.__init__(self)
        self._systems = systems
        self._func = None
        self.menu = gtk.Menu()
        self._set_style()
        self._create_menu()
        self.connect_object("event", self._open_menu,
                            self.menu)
    def _set_style(self):
        self.set_label(_("Add New"))
    def _create_menu(self):
        for name in self._systems:
            item = gtk.MenuItem(self._systems[name][0])
            item.connect("activate", self._on_menu_item, name)
            self.menu.append(item)
            item.show()
    def _open_menu(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            widget.popup(None, None, None,
                         event.button, event.time)
    def _on_menu_item(self, widget, name):
        if self._func == None:
            print "use: NewButton.connect_clicked"
            return False
        self._func(name)
    def connect_clicked(self, func):
        self._func = func
