#!/usr/bin/python3
"""
    LibreOffice manager classes for "Manage python scripts in LO Document".

    Copyright (C) ilias iliadis, 2018; ilias iliadis <iliadis@kekbay.gr>

    This file is part of "Manage python scripts in LO Document".

    "Manage python scripts in LO Document" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "Manage python scripts in LO Document" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "Manage python scripts in LO Document".
    If not, see <http://www.gnu.org/licenses/>.
"""


import os
import shutil
import tempfile
import zipfile

from bs4 import BeautifulSoup

from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')
from gi.repository import Gtk

# Localization
import locale
from locale import gettext as _

class LODocument:
    """ Manipulate the selected LibreOffice file. """

    def __init__(self, afile, myenums=None):
        self.fullpath = afile
        self.thepath, self.thefile = os.path.split(afile)
        self.isLOfilelike = False
        self.manifest = None
        self.myenums = myenums
        self.python_files = []
        self.python_scripts = {}

        try:
            self.zipread = zipfile.ZipFile(self.fullpath, 'r')
            self.isLOfilelike = True
        except zipfile.BadZipFile:
            pass
        if self.isLOfilelike :
            self.allfiles = self.zipread.namelist()
            if 'META-INF/manifest.xml' in self.allfiles:
                with self.zipread.open('META-INF/manifest.xml') as f:
                    self.manifest_xml = f.read()
                self.manifest = Manifest(self.manifest_xml)
                xcounter = 0
                for ascript in self.manifest.python_scripts:
                    self.python_scripts[xcounter] = {
                        'name' : ascript,
                        'embeded' : True,
                        'condition' : self.myenums.CONDITION_OK,
                        'full path' : ''
                    }
                    xcounter += 1
                self.python_files = self.manifest.python_scripts

    def _backup(self, backup_file):
        """Backs up the selected LibreOffice file.

        Internal function.
        File must be closed.
        """
        backupdir = os.path.join(self.thepath, 'backup')
        backupfullpath = os.path.join(backupdir, self.thefile)
        if os.path.exists(backupfullpath):
            print('exists')
            return False
        if not os.path.exists(backupdir):
            try:
                os.mkdir(backupdir)
            except Exception as e:
                print(e)
                return False
        if not os.path.isdir(backupdir):
            return False
        try:
            os.rename(self.fullpath, backupfullpath)
        except Exception as e:
            print(e)
            return False
        self.backupfullpath = backupfullpath
        return True

    def _recreate_manifest(self, list_to_remove, list_to_append_update):
        """ Return a new manifest based on changes. """
        for x in list_to_remove:
            self.manifest.remove(x)
        alist = self.manifest.python_scripts_list()[:]
        for x in list_to_append_update:
            self.manifest.append(os.path.basename(x))
        self.manifest.clear()
        return str(self.manifest)

    def make_requested_changes(self, list_to_remove, list_to_append_update, backup_file):
        """ Create a new LO Document based on changes. """
        manifest_fullnames_to_remove = ['Scripts/python/' + x for x in list_to_remove]
        manifest_fullnames_to_add_update = ['Scripts/python/' + os.path.basename(x) for x in list_to_append_update]
        newmanifest = self._recreate_manifest(list_to_remove, list_to_append_update)
        #TODO reopen if any error occures.
        if self.zipread:
            self.zipread.close()
        #TODO restore if any error occures.
        ok = self._backup(backup_file)
        if not ok:
            return False, self.myenums.BACKUP_ERROR
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpzip = os.path.join(tmpdir, self.thefile)
            with zipfile.ZipFile(self.backupfullpath, 'r') as zipread:
                with zipfile.ZipFile(tmpzip, 'w') as zipwrite:
                    for item in zipread.infolist():
                        if item.filename == 'META-INF/manifest.xml' or item.filename in manifest_fullnames_to_remove:
                            print('not copied----------------', item.filename)
                        else:
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item, data)
                    zipwrite.writestr('META-INF/manifest.xml', newmanifest.encode())
                    for data, arcname in zip(list_to_append_update, manifest_fullnames_to_add_update):
                        zipwrite.write(data, arcname)
            shutil.copyfile(tmpzip, self.fullpath)
            return True, 0
        #TODO: restore and reopen if any error occures.
        #Or at least, clear everything.
        return True, 0

    def get_source(self, pyfile):
        """ Get the text of the included python file. """
        thetext = ''
        with self.zipread.open('Scripts/python/' + pyfile) as f:
            thetext = f.read().decode()
        return thetext

class Manifest():
    """ Manipulate a manifest in a LibreOffice Document."""
    def __init__(self, manifestxml):
        self.passed_soup = BeautifulSoup(manifestxml,'xml')
        self.soup = BeautifulSoup(manifestxml,'xml')
        self.python_scripts = []

        for atag in self.soup.contents[0].find_all():
            script_basename = self.script_basename(atag)
            if script_basename and len(script_basename):
                self.python_scripts.append(script_basename)

    def __str__(self):
        """ Return an xml string as str. """
        return self.soup.prettify()

    def append(self, pyfilename):
        """ Append a python script. """
        if not self.soup.find_all(attrs={"manifest:full-path": "Scripts/"}):
            tag = self.soup.new_tag("manifest:file-entry")
            tag['manifest:full-path'] = 'Scripts/'
            tag['manifest:media-type'] = 'application/binary'
            self.soup.contents[0].append(tag)
        if not self.soup.find_all(attrs={"manifest:full-path": "Scripts/python/"}):
            tag = self.soup.new_tag("manifest:file-entry")
            tag['manifest:full-path'] = 'Scripts/python/'
            tag['manifest:media-type'] = 'application/binary'
            self.soup.contents[0].append(tag)
        if not self.soup.find_all(attrs={"manifest:full-path": "Scripts/python/" + pyfilename}):
            tag = self.soup.new_tag("manifest:file-entry")
            tag['manifest:full-path'] = "Scripts/python/" + pyfilename
            tag['manifest:media-type'] = ''
            self.soup.contents[0].append(tag)
        self.soup = BeautifulSoup(self.soup.prettify(),'xml')

    def clear(self):
        """ Remove all python scripts. """
        if len(self.python_scripts_list()):
            return
        thetag = self.soup.find(attrs={"manifest:full-path": "Scripts/"})
        if thetag:
            thetag.extract()
            self.soup = BeautifulSoup(self.soup.prettify(),'xml')
        thetag = self.soup.find(attrs={"manifest:full-path": "Scripts/python/"})
        if thetag:
            thetag.extract()
            self.soup = BeautifulSoup(self.soup.prettify(),'xml')
        self.soup = BeautifulSoup(self.soup.prettify(),'xml')

    def python_scripts_list(self):
        """ Return a list with included python scripts, if any. """
        the_list = []
        for atag in self.soup.contents[0].find_all():
            b = self.script_basename(atag)
            if b and len(b):
                the_list.append(b)
        return the_list

    def remove(self, pyfilename):
        """ Remove a python script. """
        thetag = self.soup.find(attrs={"manifest:full-path": "Scripts/python/" + pyfilename})
        if thetag:
            thetag.extract()
            self.soup = BeautifulSoup(self.soup.prettify(),'xml')

    def script_basename(self, atag):
        """ Return the name of the python file if any.  """
        if 'manifest:full-path' in atag.attrs:
            theattr = atag['manifest:full-path']
            if theattr.startswith('Scripts/python/'):
                return os.path.basename(theattr)

class ChooserDialog:
    def __init__(self):
        #self.test = 0
        pass

    def select_file(self, parentwindow, thetype='LO', startin=None):
        """ Select a LibreOffice Document or a python script. """
        a = _("Please choose a file")
        dialog = Gtk.FileChooserDialog('{} ({})'.format(a, thetype),
            parentwindow,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        if startin:
            dialog.set_current_folder(startin)
        if thetype == 'LO':
            self.add_LO_filters(dialog)
        else:
            self.add_py_filters(dialog)
        filter_any = Gtk.FileFilter()
        filter_any.set_name(_("All files"))
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return filename
        else:
            return None

    @staticmethod
    def add_LO_filters(dialog):
        """ Add localized filters for LibreOffice Documents. """
        filter_LO = Gtk.FileFilter()
        filter_LO.set_name(_("LibreOffice files"))
        filter_LO.add_mime_type("application/vnd.oasis.opendocument.text")
        filter_LO.add_mime_type("application/vnd.oasis.opendocument.spreadsheet")
        filter_LO.add_mime_type("application/vnd.oasis.opendocument.database")
        filter_LO.add_mime_type("application/vnd.oasis.opendocument.presentation")
        filter_LO.add_mime_type("application/vnd.oasis.opendocument.graphics")
        dialog.add_filter(filter_LO)

        filter_calc = Gtk.FileFilter()
        filter_calc.set_name(_("Calc files"))
        filter_calc.add_mime_type("application/vnd.oasis.opendocument.spreadsheet")
        dialog.add_filter(filter_calc)

        filter_write = Gtk.FileFilter()
        filter_write.set_name(_("Writer files"))
        filter_write.add_mime_type("application/vnd.oasis.opendocument.text")
        dialog.add_filter(filter_write)

        filter_base = Gtk.FileFilter()
        filter_base.set_name(_("Base files"))
        filter_base.add_mime_type("application/vnd.oasis.opendocument.database")
        dialog.add_filter(filter_base)

        filter_impress = Gtk.FileFilter()
        filter_impress.set_name(_("Impress files"))
        filter_impress.add_mime_type("application/vnd.oasis.opendocument.presentation")
        dialog.add_filter(filter_impress)

        filter_draw= Gtk.FileFilter()
        filter_draw.set_name(_("Draw files"))
        filter_draw.add_mime_type("application/vnd.oasis.opendocument.graphics")
        dialog.add_filter(filter_draw)

    @staticmethod
    def add_py_filters(dialog):
        """ Add localized filters for python scripts. """
        filter_py = Gtk.FileFilter()
        filter_py.set_name(_("Python files"))
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)
