# -*- coding: utf-8 -*-
"""Boot Manager gtk translation module

_  - trans.ugettext [usage: _('String to translate')]
bind_glade_domain - sets translation domain for glade files
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

import gettext

APP_NAME="boot_manager_gtk"
LOCALE_DIR= "/usr/share/locale"
fallback = False
try:
    trans = gettext.translation(APP_NAME, LOCALE_DIR, fallback=fallback)
except IOError: #dev mode (no install mode)
    trans = gettext.translation(APP_NAME, "locale", fallback=fallback)
_ = trans.ugettext
def bind_glade_domain():
    from gtk import glade
    glade.bindtextdomain(APP_NAME, LOCALE_DIR)
    glade.textdomain(APP_NAME)
