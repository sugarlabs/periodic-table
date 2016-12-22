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
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk


class Color:
    UNKNOWN               = Gdk.Color(51143.0, 51143.0, 51143.0)
    DIATOMIC_NONMETAL     = Gdk.Color(63993.0, 37265.0, 65535.0)
    ALKALI_METAL          = Gdk.Color(65535.0, 50629.0, 37265.0)
    ALKALINE_EARTH_METAL  = Gdk.Color(65535.0, 57311.0, 37265.0)
    TRANSITION_METAL      = Gdk.Color(59881.0, 64764.0, 36751.0)
    LANTHANIDE            = Gdk.Color(53970.0, 65535.0, 37265.0)
    ACTINIDE              = Gdk.Color(47288.0, 65535.0, 37265.0)
    POST_TRANSITION_METAL = Gdk.Color(65535.0, 63993.0, 37265.0)
    METALLOID             = Gdk.Color(37522.0, 65535.0, 40863.0)
    NONMETAL              = Gdk.Color(43947.0, 37265.0, 65535.0)
    NOBLE_GAS             = Gdk.Color(37265.0, 57311.0, 65535.0)
    SYNTHETIC             = Gdk.Color(65535.0, 0.0, 10794.0)

    SELECTED              = Gdk.Color(60000.0, 60000.0, 60000.0)

    SOLID  = Gdk.Color(0.0, 0.0, 0.0)
    LIQUID = Gdk.Color(0.0, 0.0, 56797.0)
    GASEUS = Gdk.Color(39321.0, 0.0, 0.0)


class Screen:
    TABLE = 0
    INFO  = 1
