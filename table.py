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

import cairo

from periodic_elements import Element
from periodic_elements import Category
from periodic_elements import ELEMENTS_DATA
from constants import Color
from utils import get_color_by_type
from utils import get_all_categories
from utils import get_category_name
from center_box import CenterBox

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject

ITEM_SIZE = min(Gdk.Screen.width() / 21, Gdk.Screen.height() / 13)


class TempScale(Gtk.HBox):

    __gsignals__ = {
        "value-changed": (GObject.SIGNAL_RUN_FIRST, None, [int]),
        "reset": (GObject.SIGNAL_RUN_FIRST, None, []),
    }

    def __init__(self):
        Gtk.HBox.__init__(self)

        self.min_value = 0
        self.max_value = 6000
        self.value = 273
        self._bar_x = 0
        self._bar_width = 0
        self._reset_id = None

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(ITEM_SIZE * 4, 1)
        self.area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                             Gdk.EventMask.BUTTON_RELEASE_MASK |
                             Gdk.EventMask.BUTTON_MOTION_MASK)
        self.area.connect("draw", self.__draw_cb)
        self.area.connect("motion-notify-event", self.__motion_cb)
        self.area.connect("button-release-event", self.__release_cb)
        self.pack_start(self.area, False, False, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("273")
        self.entry.set_width_chars(4)
        self.entry.modify_font(Pango.FontDescription("9"))
        self.entry.connect("changed", self.__entry_changed_cb)
        self.entry.connect("activate", self.__entry_activated_cb)
        self.pack_end(self.entry, False, False, 0)

    def __draw_cb(self, widget, context):
        alloc = self.area.get_allocation()

        slider_width = 20
        slider_height = 20
        bar_x = slider_width / 2.0
        bar_width = alloc.width - slider_width
        bar_height = 10
        bar_y = alloc.height / 2.0 - bar_height / 2.0
        slider_x = (bar_width / float(self.max_value)) * self.value + bar_x
        slider_y = alloc.height / 2.0 - slider_height / 2.0

        self.__draw_bg(context, bar_x, bar_y, bar_width, bar_height)
        self.__draw_slider(
            context,
            slider_x, slider_y,
            slider_width, slider_height
        )

        self._bar_x = bar_x
        self._bar_width = bar_width

        return False

    def __draw_bg(self, context, x, y, width, height):
        alloc = self.area.get_allocation()

        lg = cairo.LinearGradient(x, y, width, height)
        lg.add_color_stop_rgb(
            0.25 - (x / 4.0),
            0.176470588235,
            0.305882352941,
            0.933333333333
        )

        lg.add_color_stop_rgb(0.5, 1.0, 1.0, 1.0)
        lg.add_color_stop_rgb(
            0.75,
            0.98431372549,
            0.952941176471,
            0.38431372549
        )
        lg.add_color_stop_rgb(
            1.0,
            0.819607843137,
            0.133333333333,
            0.164705882353
        )

        context.rectangle(x, y, width, height)
        context.set_source(lg)
        context.fill()

    def __draw_slider(self, context, x, y, width, height):
        context.set_source_rgb(0, 0, 0)
        context.rectangle(x - width / 2.0, y, width, height)
        context.fill()

    def __motion_cb(self, widget, event):
        self.__update_value(self.max_value / self._bar_width *
                            (event.x - self._bar_x))

    def __release_cb(self, widget, event):
        self.reset()

    def __entry_changed_cb(self, widget):
        text = self.entry.get_text()
        text = "".join([i for i in text if i in "0123456789"])[:4]
        self.entry.set_text(text)

        if self._reset_id is not None:
            GObject.source_remove(self._reset_id)

        self._reset_id = GObject.timeout_add(2000, self.reset)

    def __entry_activated_cb(self, widget):
        self.__update_value(int(self.entry.get_text()))

    def __update_value(self, value):
        if value < self.min_value:
            value = self.min_value

        elif value > self.max_value:
            value = self.max_value

        self.value = int(value)
        self.entry.set_text(str(self.value))

        self.emit("value-changed", self.value)

        GObject.idle_add(self.queue_draw)

    def reset(self):
        if self._reset_id is not None:
            GObject.source_remove(self._reset_id)
            self._reset_id = None

        self.emit("reset")


class TableItem(Gtk.EventBox):

    __gsignals__ = {
        "selected": (GObject.SIGNAL_RUN_FIRST, None, []),
        "mouse-enter": (GObject.SIGNAL_RUN_FIRST, None, []),
        "mouse-leave": (GObject.SIGNAL_RUN_FIRST, None, []),
    }

    def __init__(self, element):
        Gtk.EventBox.__init__(self)

        self.element = element
        self.color = get_color_by_type(element["category"])
        self.labels = []
        self._current_color = self.color

        self.set_size_request(ITEM_SIZE, ITEM_SIZE)
        self.modify_bg(Gtk.StateType.NORMAL, self.color)
        self.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK |
                        Gdk.EventMask.LEAVE_NOTIFY_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)

        self.connect("enter-notify-event", self.__enter_cb)
        self.connect("leave-notify-event", self.__leave_cb)
        self.connect("button-release-event", self.__release_cb)

        self.vbox = Gtk.VBox()
        self.add(self.vbox)

        label = Gtk.Label(str(element["number"]))
        label.props.xalign = 1
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        label.set_margin_top(2)
        label.set_margin_right(2)
        self.vbox.pack_start(label, False, False, 0)
        self.labels.append(label)

        label = Gtk.Label(element["symbol"])
        label.modify_font(Pango.FontDescription("Bold 15"))
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        self.vbox.pack_start(label, False, False, 0)
        self.labels.append(label)

        self.show_all()

    def __enter_cb(self, widget, event):
        if self._current_color == self.color:
            self.modify_bg(Gtk.StateType.NORMAL, Color.SELECTED)
            self.emit("mouse-enter")

    def __leave_cb(self, widget, event):
        if self._current_color == self.color:
            self.modify_bg(Gtk.StateType.NORMAL, self.color)
            self.emit("mouse-leave")

    def __release_cb(self, widget, event):
        self.__leave_cb(None, None)
        self.emit("selected")

    def set_temperature(self, temp=None):
        if temp is None:
            self._current_color = self.color
            label_color = Gdk.Color(0, 0, 0)

        else:
            label_color = Gdk.Color(65535, 65535, 65535)
            if temp >= self.element["boil"]:
                self._current_color = Color.GASEUS

            elif temp >= self.element["melt"]:
                self._current_color = Color.LIQUID

            else:
                self._current_color = Color.SOLID

        self.modify_bg(Gtk.StateType.NORMAL, self._current_color)

        for label in self.labels:
            label.modify_fg(Gtk.StateType.NORMAL, label_color)


class DetailedTableItem(Gtk.EventBox):

    def __init__(self, element):
        Gtk.EventBox.__init__(self)

        self.modify_bg(
            Gtk.StateType.NORMAL,
            get_color_by_type(element["category"])
        )

        self.vbox = Gtk.VBox()
        self.add(self.vbox)

        hbox = Gtk.HBox()
        self.vbox.pack_start(hbox, False, False, 0)

        label = Gtk.Label(element["atomic-mass"])
        label.modify_font(Pango.FontDescription("8"))
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        label.set_margin_left(8)
        hbox.pack_start(label, False, False, 0)

        label = Gtk.Label(str(element["number"]))
        label.props.xalign = 1
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        label.set_margin_top(8)
        label.set_margin_right(8)
        label.modify_font(Pango.FontDescription("12"))
        hbox.pack_end(label, False, False, 0)

        label = Gtk.Label(element["symbol"])
        label.modify_font(Pango.FontDescription("26"))
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        label.props.xalign = 0.1
        self.vbox.pack_start(label, False, False, 0)

        label = Gtk.Label(element["name"])
        label.modify_font(Pango.FontDescription("10"))
        label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        label.props.xalign = 0.1
        self.vbox.pack_start(label, False, False, 0)

        self.show_all()


class ReferencesBox(Gtk.HBox):

    def __init__(self):
        Gtk.HBox.__init__(self)

        self.set_size_request(ITEM_SIZE * 6, ITEM_SIZE * 2)

        vbox1 = Gtk.VBox()
        self.pack_start(vbox1, False, False, 20)

        vbox2 = Gtk.VBox()
        self.pack_start(vbox2, False, False, 20)

        index = 0

        for category in get_all_categories():
            color = get_color_by_type(category)
            box = Gtk.HBox()

            if index <= 5:
                vbox1.pack_start(box, False, False, 0)

            else:
                vbox2.pack_start(box, False, False, 0)

            cbox = Gtk.EventBox()
            cbox.set_size_request(15, 15)
            cbox.modify_bg(Gtk.StateType.NORMAL, color)
            box.pack_start(cbox, False, False, 8)

            label = Gtk.Label(get_category_name(category))
            label.modify_font(Pango.FontDescription("8"))
            box.pack_start(label, False, False, 0)

            index += 1

        self.show_all()


class Table(Gtk.ScrolledWindow):

    __gsignals__ = {
        "element-selected": (GObject.SIGNAL_RUN_FIRST, None, [int]),
    }

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.grid = Gtk.Grid()
        self.grid.set_hexpand(True)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_column_spacing(1)
        self.grid.set_row_spacing(1)

        self.cbox = CenterBox(self.grid)
        self.add(self.cbox)

        self.detailed_item = None
        self.items = []

        for element in range(1, 119):
            data = ELEMENTS_DATA[element]
            x = data["x"] * 2
            y = data["y"] * 2

            item = TableItem(data)
            item.connect("selected", self.__item_selected_cb)
            item.connect("mouse-enter", self.__item_enter_cb)
            item.connect("mouse-leave", self.__item_leave_cb)

            if (data["category"] == Category.ACTINIDE or
                    data["category"] == Category.LANTHANIDE):
                self.grid.attach(Gtk.VBox(), x, y, 2, 2)
                y += 2

            self.grid.attach(item, x, y, 2, 2)
            self.items.append(item)

        self.references = ReferencesBox()
        self.grid.attach(self.references, 13, 4, 12, 4)

        for group in range(1, 19):
            label = Gtk.Label(str(group))
            label.modify_font(Pango.FontDescription("12"))
            label.props.yalign = 0.75
            self.grid.attach(label, group * 2, 0, 2, 2)

        for period in range(1, 8):
            label = Gtk.Label(str(period))
            label.modify_font(Pango.FontDescription("12"))
            label.props.xalign = 0.75
            self.grid.attach(label, 0, period * 2, 2, 2)

        self.temp_scale = TempScale()
        self.temp_scale.connect("value-changed", self.__temp_changed)
        self.temp_scale.connect("reset", self.__reset_temp)
        self.grid.attach(self.temp_scale, 24, 2, 10, 2)

        self.show_all()

    def __item_selected_cb(self, item):
        element = ELEMENTS_DATA.values().index(item.element) + 1
        self.emit("element-selected", element)

    def __item_enter_cb(self, item):
        self.detailed_item = DetailedTableItem(item.element)
        self.grid.attach(self.detailed_item, 8, 3, 4, 4)

    def __item_leave_cb(self, item):
        if self.detailed_item is not None:
            self.grid.remove(self.detailed_item)

        self.detailed_item = None

    def __temp_changed(self, scale, value):
        GObject.idle_add(self.update_temperature, value)

    def __reset_temp(self, scale):
        GObject.idle_add(self.update_temperature, None)

    def update_temperature(self, temp):
        for item in self.items:
            item.set_temperature(temp)
