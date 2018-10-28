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

import os

from constants import DATA_DIR
from periodic_elements import ELEMENTS_DATA

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("EvinceDocument", "3.0")
gi.require_version("EvinceView", "3.0")

from gi.repository import Gtk
from gi.repository import EvinceDocument
from gi.repository import EvinceView


EvinceDocument.init()


class PDFViewer(EvinceView.View):

    def __init__(self):
        EvinceView.View.__init__(self)

        self.model = None

    def load_document(self, file_path):
        self.model = EvinceView.DocumentModel()
        document = EvinceDocument.Document.factory_get_document(file_path)
        self.model.set_document(document)
        self.set_model(self.model)


class InfoView(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        scroll = Gtk.ScrolledWindow()
        self.pack_start(scroll, True, True, 0)

        self.view = PDFViewer()
        scroll.add(self.view)

        self.show_all()

    def load_info(self, number):
        path = "file://" + os.path.join(DATA_DIR, str(number)) + ".pdf"
        self.view.load_document(path)
