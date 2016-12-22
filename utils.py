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

from gettext import gettext as _

from constants import Color
from elements import Category

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def make_separator(expand=False):
    separator = Gtk.SeparatorToolItem()
    if expand:
        separator.set_expand(True)
        separator.props.draw = False

    return separator


def get_color_by_type(element_type):
    if element_type == Category.UNKNOWN:
        return Color.UNKNOWN

    elif element_type == Category.DIATOMIC_NONMETAL:
        return Color.DIATOMIC_NONMETAL

    elif element_type == Category.ALKALI_METAL:
        return Color.ALKALI_METAL

    elif element_type == Category.ALKALINE_EARTH_METAL:
        return Color.ALKALINE_EARTH_METAL

    elif element_type == Category.TRANSITION_METAL:
        return Color.TRANSITION_METAL

    elif element_type == Category.LANTHANIDE:
        return Color.LANTHANIDE

    elif element_type == Category.ACTINIDE:
        return Color.ACTINIDE

    elif element_type == Category.POST_TRANSITION_METAL:
        return Color.POST_TRANSITION_METAL

    elif element_type == Category.METALLOID:
        return Color.METALLOID

    elif element_type == Category.NONMETAL:
        return Color.NONMETAL

    elif element_type == Category.NOBLE_GAS:
        return Color.NOBLE_GAS

    elif element_type == Category.SYNTHETIC:
        return Color.SYNTHETIC

    else:
        return Color.UNKNOWN


def get_all_categories():
    return [
        Category.ALKALI_METAL,
        Category.ALKALINE_EARTH_METAL,
        Category.POST_TRANSITION_METAL,
        Category.TRANSITION_METAL,
        Category.LANTHANIDE,
        Category.ACTINIDE,
        Category.METALLOID,
        Category.NONMETAL,
        Category.DIATOMIC_NONMETAL,
        Category.NOBLE_GAS,
        Category.SYNTHETIC,
        Category.UNKNOWN,
    ]


def get_category_name(element_type):
    if element_type == Category.UNKNOWN:
        return _("Unknown elements")

    elif element_type == Category.DIATOMIC_NONMETAL:
        return _("Halogens")

    elif element_type == Category.ALKALI_METAL:
        return _("Alkali metals")

    elif element_type == Category.ALKALINE_EARTH_METAL:
        return _("Alkaline metals")

    elif element_type == Category.TRANSITION_METAL:
        return _("Transition metals")

    elif element_type == Category.LANTHANIDE:
        return _("Lanthanoids")

    elif element_type == Category.ACTINIDE:
        return _("Actinoids")

    elif element_type == Category.POST_TRANSITION_METAL:
        return _("Post transition metals")

    elif element_type == Category.METALLOID:
        return _("Metaloids")

    elif element_type == Category.NONMETAL:
        return _("Nonmetals")

    elif element_type == Category.NOBLE_GAS:
        return _("Noble gases")

    elif element_type == Category.SYNTHETIC:
        return _("Synthetics elements")

    else:
        return _("Unknown")
