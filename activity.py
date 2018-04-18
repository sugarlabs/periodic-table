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

import random

from table import Table
from info_view import InfoView
from constants import Screen, Color
from utils import make_separator
from toolbarbox import PeriodicTableToolbarBox
from fun_facts import *

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.radiotoolbutton import RadioToolButton
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton


class PeriodicTable(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.screen = None

        self.box = Gtk.VBox()
        self.set_canvas(self.box)

        self.make_toolbars()
        self.get_toolbar_box().connect("searched-element",
                                       self._searched_element_cb)

        self.table = Table()
        self.table.connect("element-selected", self._element_selected_cb)

        self.info_view = InfoView()

        self.set_screen(Screen.TABLE)

    def make_toolbars(self):
        toolbarbox = PeriodicTableToolbarBox()
        self.set_toolbar_box(toolbarbox)

        toolbar = toolbarbox.toolbar

        toolbar.insert(ActivityToolbarButton(self), -1)
        toolbar.insert(make_separator(False), -1)

        self.back_button = ToolButton("go-previous-paired")
        self.back_button.set_sensitive(False)
        self.back_button.connect("clicked", self._go_back)
        toolbar.insert(self.back_button, -1)

        self.forward_button = ToolButton("go-next-paired")
        self.forward_button.set_sensitive(False)
        self.forward_button.connect("clicked", self._go_forward)
        toolbar.insert(self.forward_button, -1)

        self.fun_fact_btn = ToolButton()
        self.fun_fact_btn.set_tooltip("Fun facts")
        #image = Gtk.Image.new_from_file('fun_facts.svg')
        self.fun_fact_btn.connect("clicked", self._fun_fact_cb)
        toolbar.insert(self.fun_fact_btn, -1)

        toolbarbox._add_widget(toolbarbox.search_entry, expand=True)

        toolbar.insert(make_separator(True), -1)
        toolbar.insert(StopButton(self), -1)

    def set_screen(self, screen):
        if screen == self.screen:
            return

        self.screen = screen

        if self.screen == Screen.TABLE:
            self.forward_button.set_sensitive(self.back_button.get_sensitive())
            self.back_button.set_sensitive(False)

            if self.info_view.get_parent() == self.box:
                self.box.remove(self.info_view)

            if self.table.get_parent() is None:
                self.box.pack_start(self.table, True, True, 0)
                self.box.reorder_child(self.table, 0)

        elif self.screen == Screen.INFO:
            self.forward_button.set_sensitive(False)
            self.back_button.set_sensitive(True)

            if self.table.get_parent() == self.box:
                self.box.remove(self.table)

            if self.info_view.get_parent() is None:
                self.box.pack_start(self.info_view, True, True, 0)
                self.box.reorder_child(self.info_view, 0)

        self.show_all()

    def _element_selected_cb(self, table, element):
        self.info_view.load_info(element)
        self.set_screen(Screen.INFO)

    def _searched_element_cb(self, toolbar, found_elements):
        for item in self.table.items:
            if item.element["number"] not in found_elements:
                item.modify_bg(Gtk.StateType.NORMAL, Color.GRAYED)
                item.active = False
            else:
                item.modify_bg(Gtk.StateType.NORMAL, item.color)
                item.active = True

    def _go_back(self, button):
        self.set_screen(Screen.TABLE)

    def _go_forward(self, button):
        self.set_screen(Screen.INFO)

    def _fun_fact_cb(self, button):
        message = get_fact(Facts)
        messagedialog = Gtk.MessageDialog(
                                         self,
                                         Gtk.DialogFlags.MODAL,
                                         Gtk.MessageType.INFO,
                                         message
                                         )
        messagedialog.run()
        messagedialog.destroy()
