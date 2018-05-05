#!/usr/bin/env python3
"""
    Theme manager classes for "Manage python scripts in LO Document".

    Copyright (C) ilias iliadis, 2018; ilias iliadis <iliadis@kekbay.gr>

    This file is part of Manage python scripts in LO Document.

    Manage python scripts in LO Document is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Manage python scripts in LO Document is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Manage python scripts in LO Document.  If not, see <http://www.gnu.org/licenses/>.
"""

#FIXME: correct the version
__version__ = '0.0.8'
VERSIONSTR = 'v. {}'.format(__version__)

# Gtk and related
from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject, Pango
gi_require_version('GtkSource', '3.0')
from gi.repository import GtkSource

class ThemeManager:
    """ Theme manager for usage with a combo. """

    def __init__(self, comboTheme=None):
        GObject.type_register(GtkSource.View)
        self.comboTheme = comboTheme
        self.listTheme = Gtk.ListStore('gchararray')
        self.comboTheme.set_model(self.listTheme)
        self.theme_name = None

    def load_and_show_themes(self, oldthemename=None):
        # Set theme.
        self.themeManager = GtkSource.StyleSchemeManager()
        # Map from theme id to StyleScheme.
        self.themes = {
            tid: self.themeManager.get_scheme(tid)
            for tid in self.themeManager.get_scheme_ids()}
        # Holds the currently selected theme info.
        self.theme = None
        celltheme = Gtk.CellRendererText()
        self.comboTheme.pack_start(celltheme, True)
        self.comboTheme.add_attribute(celltheme, 'text', 0)
        self.bufferOutput = GtkSource.Buffer()
        self.langManager = GtkSource.LanguageManager()
        self.bufferLang = self.langManager.get_language('python3')
        self.bufferOutput.set_language(self.bufferLang)
        self.bufferOutput.set_highlight_syntax(True)
        self.bufferOutput.set_highlight_matching_brackets(True)
        self.build_theme_list(oldthemename)

    def build_theme_list(self, oldthemename=None):
        """ Build the content for self.listTheme based on self.themes.
            Sorts the names first.
        """
        selected = -1
        themeids = sorted(
            self.themes,
            key=lambda k: self.themes[k].get_name()
        )
        themenames = sorted((self.themes[k].get_name() for k in themeids))
        for i, themename in enumerate(themenames):
            newrow = self.listTheme.append((themename, ))
            self.listTheme.set_value(newrow, 0, themename)
            if themename == oldthemename:
                selected = i
        # Set the currently selected theme.
        if selected > -1:
            self.comboTheme.set_active(selected)

    def get_theme_by_name(self, name):
        """ Retrieves a StyleScheme from self.themes by it's proper name.
            Like: Kate, or Oblivion.
            Returns None if the theme can't be found.
        """
        for themeid, stylescheme in self.themes.items():
            themename = stylescheme.get_name()
            if name == themename:
                return stylescheme
        return None

    def set_theme(self, scheme_identifier):
        """ Sets the current highlight theme by id, name, or StyleScheme.
            or by prefetched StyleScheme.
            Return True if the theme was set, otherwise False.
        """
        possiblename = None
        if isinstance(scheme_identifier, str):
            # Id or name?
            theme = self.themes.get(scheme_identifier, None)
            if theme is None:
                possiblename = scheme_identifier
                # Name.
                theme = self.get_theme_by_name(scheme_identifier)
        elif isinstance(scheme_identifier, GtkSource.StyleScheme):
            # StyleScheme (prefetched)
            theme = scheme_identifier
        else:
            # Unknown type for set_theme().
            errfmt = 'Expected name, id, or StyleScheme. Got: {}'
            raise ValueError(errfmt.format(type(scheme_identifier)))
        if theme is not None:
            if possiblename:
                self.theme_name = possiblename
            self.bufferOutput.set_style_scheme(theme)
            return True
        return False
