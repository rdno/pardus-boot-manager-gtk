# -*- coding: utf-8 -*-
"""boot manager gtk's windows module

EditWindow - Edit Window for Boot Manager
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

from boot_manager_gtk.translation import _
from boot_manager_gtk.utils import EDIT_WINDOW_LABELS, EDIT_WINDOW_INFOS

class EditWindow(gtk.Window):
    """Edit Window for Boot Manager"""
    def __init__(self, entry, callback_func):
        """init

        Arguments:
        - `entry`: entry object
        - `callback_func`:a callback function for ok_btn clicked
        """
        gtk.Window.__init__(self)
        self._entry = entry.copy()
        self._callback_func = callback_func
        self.widgets = {} #gtk.Entry widgets 
        self._set_style()
        self._create_ui()
        self._listen_signals()
    def _set_style(self):
        #sets style of EditWindow
        if self._entry["title"]:
            self.set_title(_("Edit > %s") % self._entry["title"])
        else:
            self.set_title(_("New Entry"))
        self.set_modal(True)
        #self.set_default_size(500, 310)
    def _create_ui(self):
        #creates ui elements
        self.vbox = gtk.VBox(homogeneous=False, spacing=5)
        self.add(self.vbox)
        self.add_elements()
        hbox = gtk.HBox()
        self.ok_btn = gtk.Button(_("OK"))
        self.cancel_btn = gtk.Button(_("Cancel"))
        hbox.pack_end(self.ok_btn, fill=False, expand=False)
        hbox.pack_end(self.cancel_btn, fill=False, expand=False)
        self.vbox.pack_end(hbox, fill=False, expand=False)
        self.vbox.show_all()
    def add_elements(self):
        #adds elements Table
        self.elements = gtk.Table()
        self.elements.set_row_spacings(5)
        self.elements.set_col_spacings(5)
        self.vbox.pack_start(self.elements, expand=False, fill=False)

        options = ["title", "root", "kernel", "initrd", "options"]
        self._count = 0
        for option in options:
            if option in self._entry:
                self.add_element(EDIT_WINDOW_LABELS[option],
                                 EDIT_WINDOW_INFOS[option],
                                 self._entry[option],
                                 option)
            else:
                self._entry[option] = "" #for iface.setEntry

    def add_element(self, label, info, value, option):
        label_lb = gtk.Label("<b>"+label+"</b>")
        label_lb.set_alignment(0.0, 0.5)
        label_lb.set_use_markup(True)

        value_txt = gtk.Entry()
        value_txt.set_text(value)
        self.widgets[option]= value_txt

        info_lb = gtk.Label(info)
        info_lb.set_alignment(0.0, 0.5)

        e = self.elements
        e.attach(label_lb, 0, 1, self._count, self._count + 1,
                 gtk.FILL, gtk.SHRINK)
        e.attach(value_txt, 1, 2, self._count, self._count + 1,
                 gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        e.attach(info_lb, 1, 2, self._count + 1, self._count + 2,
                 gtk.EXPAND|gtk.FILL, gtk.SHRINK)

        self._count = self._count + 2
    def _listen_signals(self):
        self.cancel_btn.connect("clicked", lambda w:self.destroy())
        def on_ok(widget):
            result = self._entry
            for opt in self.widgets.keys():
                result[opt] = self.widgets[opt].get_text()
            self._callback_func(result, self)
        self.ok_btn.connect("clicked", on_ok)
