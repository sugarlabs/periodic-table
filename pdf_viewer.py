#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import time

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk

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


"""
class EvinceViewer():

    def __init__(self):
        self._view_notify_zoom_handler = None
        EvinceDocument.init()
        self._view = EvinceView.View()

    def setup(self, activity):
        self._activity = activity
        self._view.connect('selection-changed',
                           activity._view_selection_changed_cb)
        self._view.connect('external-link', self.__handle_link_cb)


        activity._scrolled.add(self._view)
        self._view.show()

        self._view.set_events(self._view.get_events() |
                              Gdk.EventMask.TOUCH_MASK)
        self._view.connect('event', self.__view_touch_event_cb)

        activity._hbox.pack_start(activity._scrolled, True, True, 0)
        activity._scrolled.show()

        self.dpi = activity.dpi

    def load_document(self, file_path):
        try:
            self._document = \
                EvinceDocument.Document.factory_get_document(file_path)
        except GObject.GError, e:
            _logger.error('Can not load document: %s', e)
            return
        else:
            self._model = EvinceView.DocumentModel()
            self._model.set_document(self._document)
            self._view.set_model(self._model)

            # set dpi
            # TODO why we need set this?
            ""
            min_scale = self._model.get_min_scale()
            max_scale = self._model.get_max_scale()
            logging.error("min scale %s max_scale %s", min_scale, max_scale)
            logging.error("setting min scale %s", min_scale * self.dpi / 72.0)
            logging.error("setting max scale %s", max_scale * self.dpi / 72.0)
            self._model.set_min_scale(min_scale * self.dpi / 72.0)
            self._model.set_max_scale(max_scale * self.dpi / 72.0)
            "

    def __view_touch_event_cb(self, widget, event):
        if event.type == Gdk.EventType.TOUCH_BEGIN:
            x = event.touch.x
            view_width = widget.get_allocation().width
            if x > view_width * 3 / 4:
                self._view.scroll(Gtk.ScrollType.PAGE_FORWARD, False)
            elif x < view_width * 1 / 4:
                self._view.scroll(Gtk.ScrollType.PAGE_BACKWARD, False)

    def __handle_link_cb(self, widget, url_object):
        url = url_object.get_uri()
        logging.debug('Create journal entry for URL: %s', url)
        jobject = datastore.create()
        metadata = {
            'title': "%s: %s" % (_('URL from Read'), url),
            'title_set_by_user': '1',
            'icon-color': profile.get_color().to_string(),
            'mime_type': 'text/uri-list', }

        for k, v in metadata.items():
            jobject.metadata[k] = v
        file_path = os.path.join(get_activity_root(),
                                 'instance', '%i_' % time.time())
        open(file_path, 'w').write(url + '\r\n')
        os.chmod(file_path, 0755)
        jobject.set_file_path(file_path)
        datastore.write(jobject)
        show_object_in_journal(jobject.object_id)
        jobject.destroy()
        os.unlink(file_path)

    def get_current_page(self):
        return self._model.props.page

    def set_current_page(self, page):
        if page >= self._document.get_n_pages():
            page = self._document.get_n_pages() - 1
        elif page < 0:
            page = 0
        self._model.props.page = page

    def next_page(self):
        self._view.next_page()

    def previous_page(self):
        self._view.previous_page()

    def rotate_left(self):
        rotation = self._model.get_rotation()
        self._model.set_rotation(rotation - 90)

    def rotate_right(self):
        rotation = self._model.get_rotation()
        self._model.set_rotation(rotation + 90)

    def can_rotate(self):
        return True

    def get_pagecount(self):
        '''
        Returns the pagecount of the loaded file
        '''
        return self._document.get_n_pages()

    def load_metadata(self, activity):

        self.metadata = activity.metadata

        if not self.metadata['title_set_by_user'] == '1':
            title = self._document.get_title()
            if title:
                self.metadata['title'] = title

        sizing_mode = self.metadata.get('Read_sizing_mode', 'fit-width')
        _logger.debug('Found sizing mode: %s', sizing_mode)
        if sizing_mode == "best-fit":
            self._model.set_sizing_mode(EvinceView.SizingMode.BEST_FIT)
            if hasattr(self._view, 'update_view_size'):
                self._view.update_view_size(self._scrolled)
        elif sizing_mode == "free":
            self._model.set_sizing_mode(EvinceView.SizingMode.FREE)
            self._model.set_scale(float(self.metadata.get('Read_zoom', '1.0')))
            _logger.debug('Set zoom to %f', self._model.props.scale)
        elif sizing_mode == "fit-width":
            self._model.set_sizing_mode(EvinceView.SizingMode.FIT_WIDTH)
            if hasattr(self._view, 'update_view_size'):
                self._view.update_view_size(self._scrolled)
        else:
            # this may happen when we get a document from a buddy with a later
            # version of Read, for example.
            _logger.warning("Unknown sizing_mode state '%s'", sizing_mode)
            if self.metadata.get('Read_zoom', None) is not None:
                self._model.set_scale(float(self.metadata['Read_zoom']))

    def update_metadata(self, activity):
        self.metadata = activity.metadata
        self.metadata['Read_zoom'] = str(self._model.props.scale)

        if self._model.get_sizing_mode() == EvinceView.SizingMode.BEST_FIT:
            self.metadata['Read_sizing_mode'] = "best-fit"
        elif self._model.get_sizing_mode() == EvinceView.SizingMode.FREE:
            self.metadata['Read_sizing_mode'] = "free"
        elif self._model.get_sizing_mode() == EvinceView.SizingMode.FIT_WIDTH:
            self.metadata['Read_sizing_mode'] = "fit-width"
        else:
            _logger.error("Don't know how to save sizing_mode state '%s'" %
                          self._model.get_sizing_mode())

    def can_highlight(self):
        return False

    def can_do_text_to_speech(self):
        return False

    def get_zoom(self):
        '''
        Returns the current zoom level
        '''
        return self._model.props.scale * 100

    def set_zoom(self, value):
        '''
        Sets the current zoom level
        '''
        self._model.props.sizing_mode = EvinceView.SizingMode.FREE

        if not self._view_notify_zoom_handler:
            return

        self._model.disconnect(self._view_notify_zoom_handler)
        try:
            self._model.props.scale = value / 100.0
        finally:
            self._view_notify_zoom_handler = self._model.connect(
                'notify::scale', self._zoom_handler)

    def zoom_in(self):
        '''
        Zooms in (increases zoom level by 0.1)
        '''
        self._model.props.sizing_mode = EvinceView.SizingMode.FREE
        self._view.zoom_in()

    def zoom_out(self):
        '''
        Zooms out (decreases zoom level by 0.1)
        '''
        self._model.props.sizing_mode = EvinceView.SizingMode.FREE
        self._view.zoom_out()

    def zoom_to_width(self):
        self._model.props.sizing_mode = EvinceView.SizingMode.FIT_WIDTH

    def can_zoom_in(self):
        '''
        Returns True if it is possible to zoom in further
        '''
        return self._view.can_zoom_in()

    def can_zoom_out(self):
        '''
        Returns True if it is possible to zoom out further
        '''
        return self._view.can_zoom_out()

    def can_zoom_to_width(self):
        return True

    def zoom_to_best_fit(self):
        self._model.props.sizing_mode = EvinceView.SizingMode.BEST_FIT

    def zoom_to_actual_size(self):
        self._model.props.sizing_mode = EvinceView.SizingMode.FREE
        self._model.props.scale = 1.0

    def connect_zoom_handler(self, handler):
        self._zoom_handler = handler
        self._view_notify_zoom_handler = \
            self._model.connect('notify::scale', handler)
        return self._view_notify_zoom_handler

    def setup_find_job(self, text, updated_cb):
        self._find_job = EvinceView.JobFind.new(
            document=self._document, start_page=0,
            n_pages=self._document.get_n_pages(),
            text=text, case_sensitive=False)
        self._find_updated_handler = self._find_job.connect('updated',
                                                            updated_cb)
        self._view.find_started(self._find_job)
        EvinceView.Job.scheduler_push_job(
            self._find_job, EvinceView.JobPriority.PRIORITY_NONE)
        return self._find_job, self._find_updated_handler

    def connect_page_changed_handler(self, handler):
        self._model.connect('page-changed', handler)

    def update_toc(self, activity):
        if self._validate_min_version(3, 5, 92):
            # check version because does not work and crash with older evince
            doc = self._model.get_document()
            if not doc.has_document_links():
                logging.error('The pdf file does not have a index')
                return False
            else:
                self._job_links = EvinceView.JobLinks.new(document=doc)
                self._job_links.connect('finished', self.__index_loaded_cb,
                                        activity)
                EvinceView.Job.scheduler_push_job(
                    self._job_links,
                    EvinceView.JobPriority.PRIORITY_NONE)
                return True
        else:
            return False

    def handle_link(self, link):
        self._view.handle_link(link)

    def _validate_min_version(self, major, minor, micro):
        ""
        Check if Evince version is at major or equal than the requested
        ""
        evince_version = [EvinceDocument.MAJOR_VERSION,
                          EvinceDocument.MINOR_VERSION,
                          EvinceDocument.MICRO_VERSION]
        return evince_version >= [major, minor, micro]

    def __index_loaded_cb(self, job, activity):
        self._index_model = job.get_model()
        if job.get_model() is None:
            return False

        activity.show_navigator_button()
        activity.set_navigator_model(self._index_model)
        return True

    def get_current_link(self):
        _iter = self._index_model.get_iter_first()
        link_found = ""
        current_page = self._model.props.page
        while True:
            link = self._index_model.get_value(_iter, 1)
            if self._document.get_link_page(link) > current_page:
                break
            else:
                link_found = link
                _iter = self._index_model.iter_next(_iter)
                if _iter is None:
                    break
        return link_found

    def get_link_iter(self, link):
        _iter = self._index_model.get_iter_first()
        while True:
            value = self._index_model.get_value(_iter, 1)
            if value == link:
                break
            else:
                _iter = self._index_model.iter_next(_iter)
                if _iter is None:
                    break
        return _iter

    def find_set_highlight_search(self, set_highlight_search):
        self._view.find_set_highlight_search(set_highlight_search)

    def find_next(self):
        '''
        Highlights the next matching item for current search
        '''
        self._view.find_next()

    def find_previous(self):
        '''
        Highlights the previous matching item for current search
        '''
        self._view.find_previous()

    def find_changed(self, job, page=None):
        pass

    def scroll(self, scrolltype, horizontal):
        '''
        Scrolls through the pages.
        Scrolling is horizontal if horizontal is set to True
        Valid scrolltypes are:
        Gtk.ScrollType.PAGE_BACKWARD, Gtk.ScrollType.PAGE_FORWARD,
        Gtk.ScrollType.STEP_BACKWARD, Gtk.ScrollType.STEP_FORWARD,
        Gtk.ScrollType.START and Gtk.ScrollType.END
        '''
        _logger.error('scroll: %s', scrolltype)

        if scrolltype == Gtk.ScrollType.PAGE_BACKWARD:
            self._view.scroll(Gtk.ScrollType.PAGE_BACKWARD, horizontal)
        elif scrolltype == Gtk.ScrollType.PAGE_FORWARD:
            self._view.scroll(Gtk.ScrollType.PAGE_FORWARD, horizontal)
        elif scrolltype == Gtk.ScrollType.STEP_BACKWARD:
            self._scroll_step(False, horizontal)
        elif scrolltype == Gtk.ScrollType.STEP_FORWARD:
            self._scroll_step(True, horizontal)
        elif scrolltype == Gtk.ScrollType.START:
            self.set_current_page(0)
        elif scrolltype == Gtk.ScrollType.END:
            self.set_current_page(self._document.get_n_pages())
        else:
            print ('Got unsupported scrolltype %s' % str(scrolltype))

    def _scroll_step(self, forward, horizontal):
        if horizontal:
            adj = self._activity._scrolled.get_hadjustment()
        else:
            adj = self._activity._scrolled.get_vadjustment()
        value = adj.get_value()
        step = adj.get_step_increment()
        if forward:
            adj.set_value(value + step)
        else:
            adj.set_value(value - step)

    def copy(self):
        self._view.copy()
"""