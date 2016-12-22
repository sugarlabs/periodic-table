#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, Cristian García <cristian99garcia@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class CenterBox(Gtk.VBox):
    # A box with a centered child, with set_center_widget
    # the child don't auto-resize

    def __init__(self, child):
        Gtk.VBox.__init__(self)

        hbox = Gtk.HBox()
        hbox.pack_start(child, True, False, 0)
        self.pack_start(hbox, True, False, 0)
