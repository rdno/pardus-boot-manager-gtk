#!/usr/bin/python
# -*- coding: utf-8 -*-
"""inludes some useful functions

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
