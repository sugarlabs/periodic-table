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

from periodic_elements import ELEMENTS_DATA
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject

from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics import iconentry

import logging


def match(pattern, element):
    # Keep it non case-sensitive
    pattern = pattern.lower()
    target = element["name"].lower()
    if pattern == element["symbol"].lower():
        return True
    try:
        if target.index(pattern) == 0:
            return True
    except ValueError:
        pass

    else:
        n, m = len(pattern), len(target)
        # If they're looking for an element with a long name,
        # allow for one character to be off
        if n < 6:
            return False

        if abs(m - n) > 1:  # lengths too different
            return False

        count = i = j = 0
        while i < m and j < n:
            if not pattern[i] == target[j]:  # if current characters dont match
                if count:
                    return False
                if m > n:  # try adjusting length
                    i += 1
                elif m < n:  # try adjusting length
                    j += 1
                else:
                    i += 1
                    j += 1
                count += 1
            else:  # if current characters match
                i += 1
                j += 1
        if i < m or j < n:
            count += 1

        return count == 1


class PeriodicTableToolbarBox(ToolbarBox):
    __gsignals__ = {
        "searched-element": (GObject.SIGNAL_RUN_FIRST,
                             None, (GObject.TYPE_PYOBJECT,)),
    }

    def __init__(self):
        ToolbarBox.__init__(self)

        self.search_entry = iconentry.IconEntry()
        self.search_entry.set_icon_from_name(iconentry.ICON_ENTRY_PRIMARY,
                                             'entry-search')
        text = "Search for element"
        self.search_entry.set_placeholder_text(text)
        self.search_entry.connect('activate', self._search_entry_activated_cb)
        self.search_entry.connect('changed', self._search_entry_changed_cb)
        self.search_entry.add_clear_button()
        self._autosearch_timer = None

    def _search_entry_activated_cb(self, search_entry):
        pattern = search_entry.get_text()
        if self._autosearch_timer:
            GObject.source_remove(self._autosearch_timer)
            self._autosearch_timer = None
            found_elements = []
            for key, element in ELEMENTS_DATA.iteritems():
                if match(pattern, element):
                    found_elements.append(element["number"])
            self.emit("searched-element", found_elements)

    def _search_entry_changed_cb(self, search_entry):
        self.search_entry = search_entry
        if not search_entry.props.text:
            search_entry.activate()
            return

        if self._autosearch_timer:
            GObject.source_remove(self._autosearch_timer)
        self._autosearch_timer = GObject.timeout_add(
            750,
            self._search_entry_activated_cb,
            search_entry
        )

    def _add_widget(self, widget, expand=False):
        tool_item = Gtk.ToolItem()
        tool_item.set_expand(expand)

        tool_item.add(widget)
        widget.show()

        self.toolbar.insert(tool_item, -1)
        tool_item.show()
