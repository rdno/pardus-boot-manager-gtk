# -*- coding: utf-8 -*-
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
from asma.addon import AsmaAddon
from boot_manager_gtk import BootManager
from boot_manager_gtk.translation import _
class BootManagerAddon(AsmaAddon):
    """Boot Manager Asma addon"""
    def __init__(self):
        """init the variables"""
        super(BootManagerAddon, self).__init__()
        self._uuid = "fa2e9fe7-7f3f-4a7a-aea8-e1a7a46aafef"
        self._icon_name = "computer"
        self._label = _("Boot Manager")
        self._widget = BootManager 
