#!/usr/bin/python
# -*- coding: utf-8 -*-
"""inludes some useful functions and constants

get_disk_by_UUID - get disk path by uuid
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

#based on TUBITAK/UAKAE version
def get_disk_by_uuid(uuid):
    """get disk path by uuid"""
    from os import path, readlink
    uuid_p = "/dev/disk/by-uuid" #uuidpath
    if path.exists(uuid_p+"/%s" % uuid):
        return path.realpath(path.join("/dev/disk/by-uuid/",
                                       readlink(uuid_p+"/%s" % uuid)))
    else:
        return uuid


from boot_manager_gtk.translation import _
EDIT_WINDOW_LABELS = {
    "title":_("Title"),
    "root":_("Disk"),
    "kernel":_("Kernel"),
    "initrd":_("Ramdisk File"),
    "options":_("Boot Options")
    }
EDIT_WINDOW_INFOS = {
    "title":_("Name of the boot entry to be shown at the boot menu."),
    "root":_("Disk that contains operating system."),
    "initrd": _("File that contains a micro operating system for preloading kernel modules."),
    "kernel":_("Operating system kernel."),
    "options":_("Boot options for operating system.")
    }
def dummy_entry(systems, name):
    """returns a dummy entry using name

    Arguments:
    - `systems`: iface.getSystems()
    - `name`: linux|windows|xen etc.
    """
    entry = {"title":"", "os_type":name, "index":-1}
    for item in systems[name][1]:
        entry[unicode(item)] = ""
    for item in systems[name][2]:
        entry[unicode(item)] = ""
    return entry
