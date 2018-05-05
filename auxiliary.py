#!/usr/bin/env python3
"""
    Auxiliary classes.

    Copyright (C) ilias iliadis, 2018; ilias iliadis <iliadis@kekbay.gr>

    Auxiliary classes are free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Auxiliary classes are distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Auxiliary classes.  If not, see <http://www.gnu.org/licenses/>.
"""

#FIXME: correct the version
__version__ = '0.0.8'
VERSIONSTR = 'v. {}'.format(__version__)

ERROR_IMPORT_LIBRARIES_FAIL = -1

try:
    import os
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from configparser import ConfigParser
    import locale
    from locale import gettext as _
except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

settings = None # Keep window related options
options = None #Keep application wide options in a 'General Options' section

class MessageBox():
    def __init__(self, parent):
        self.parent = parent
        self.app = self.parent.app
        self.INFO_DIR = os.path.join(self.app.BASE_DIR, 'info')

        self.show = self.Message

    def AboutBox(self):
        aboutdialog = Gtk.AboutDialog()
        #show the localized name together with the international
        aboutdialog.set_program_name(self.app.localizedname)
        aboutdialog.set_version(self.app.name + ' v.' + self.app.version)
        AUTHORSFILE = os.path.join(self.INFO_DIR, 'AUTHORS')
        COPYRIGHTFILE = os.path.join(self.INFO_DIR, 'COPYRIGHT')
        COMMENTSFILE = os.path.join(self.INFO_DIR, 'COMMENTS')
        TRANSLATORSFILE = os.path.join(self.INFO_DIR, 'TRANSLATORS')
        if os.path.exists(AUTHORSFILE):
            with open(AUTHORSFILE, mode='rt', encoding='utf-8') as f:
                aboutdialog.set_authors(f.readlines())
        if os.path.exists(COPYRIGHTFILE):
            with open(COPYRIGHTFILE, mode='rt', encoding='utf-8') as f:
                aboutdialog.set_copyright(f.read())
        if os.path.exists(COMMENTSFILE):
            with open(COMMENTSFILE, mode='rt', encoding='utf-8') as f:
                aboutdialog.set_comments(f.read())
        if os.path.exists(TRANSLATORSFILE):
            with open(TRANSLATORSFILE, mode='rt', encoding='utf-8') as f:
                aboutdialog.set_translator_credits(f.read())
        aboutdialog.set_transient_for(self.parent)
        aboutdialog.set_logo(self.app.icon)
        aboutdialog.run()
        aboutdialog.destroy()

    def Message(self, message, buttons='', boxtype = 'INFO', usethetitle = None, *args):
        """Simple MessageBox.

        Keyword arguments:
        buttons -- string containing one or more of (delimited or no):
            YES, OK, CANCEL, NO
            defaults to: OK
        boxtype -- a string declaring the type of dialog. One of:
            INFO, ERROR, WARNING, QUESTION
            defaults to: INFO
        usethetitle -- override title with this string
        """
        Buttons = tuple()

        if 'YES' in buttons:
            Buttons += (_('_Yes'), Gtk.ResponseType.OK)
        elif 'OK' in buttons:
            Buttons += (_('_OK'), Gtk.ResponseType.OK)
        if 'NO' in buttons:
            Buttons += (_('_No'), Gtk.ResponseType.CANCEL)
        elif 'CANCEL' in buttons:
            Buttons += (_('_Cancel'), Gtk.ResponseType.CANCEL)
        if len(Buttons) == 0:
            Buttons += (_('OK'), Gtk.ResponseType.OK)
        if boxtype == 'ERROR':
            MessageType = Gtk.MessageType.ERROR
            title = _('ERROR')
        elif boxtype == 'WARNING':
            MessageType = Gtk.MessageType.WARNING
            title = _('WARNING')
        elif boxtype == 'QUESTION':
            MessageType = Gtk.MessageType.QUESTION
            title = _('QUESTION')
        else:
            MessageType = Gtk.MessageType.INFO
            title = _('INFO')
        title = boxtype
        if usethetitle:
            title = usethetitle
        dialog = Gtk.MessageDialog(self.parent, 0, MessageType, Buttons, title)
        dialog.format_secondary_text(message)
        dialog.set_title(self.parent.app.localizedname)
        dialog.vbox.set_spacing (3)
        for a in dialog.vbox:
            for b in a:
                if type(b) == Gtk.ButtonBox:
                    b.set_halign(Gtk.Align.CENTER)
        response = dialog.run()
        dialog.destroy()
        return True if response == Gtk.ResponseType.OK else False

    def are_you_sure(self, addmessage):
        message = _('You are about to:\n') + addmessage + '\n\n'
        message += _('Are you sure?')
        return self.Message(message, buttons='YESCANCEL', boxtype = 'WARNING')

class SectionConfig():
    """A very simplified configuration editor for multi usage.

    Read and write only one section from a conf file in user's home directory.
    Can be called from multiple "places"
    using the same filename, but different section names.
    Config file is only opened and closed at init and at save.
    All modifications during the existance of the instance
    are done in the instance's dict only for the specified section
    """
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.parser:
            self.save()

    def __init__(self, nameoffile, section):
        """Init the python's configparser.

        Read existing keys for "my" section only, if any.
        Modify only "my" section.
        Readings are done using python's configparser idioms.
        Methods:
        - get
        - set
        - get_bool
        - save
        """
        self.S = section

        self.ok = False
        self.parser = None
        self.configfile = os.path.join(os.path.expanduser('~'), '.config','OCP', nameoffile + '.conf')
        self.parser = ConfigParser()
        self.parser.add_section(self.S)
        self.parser_error = True
        #ensure path up to file exists
        #os.makedirs(os.path.dirname(self.configfile), exist_ok=True)
        #read the conf to a local parser and close it
        thetext = self.get_configfile_content()
        if self.parser_error:#an error occured. file unusable
            return
        if thetext != '':
            #get only the contents of self.S section
            dummyparser = ConfigParser()
            dummyparser.read_string(thetext)
            if dummyparser.has_section(self.S):
                for name, value in dummyparser.items(self.S):
                    self.parser.set(self.S, name, value)

    def get_configfile_content(self):
        try:
            with open(self.configfile, 'r') as f:
                thetext = f.read()
                self.parser_error = False
                return thetext
        except FileNotFoundError:
            pass
        except Exception:
            return None
        #the file not found
        try:
            with open(self.configfile, 'w') as f:
                self.parser_error = False
                return ''
        except Exception:
            return None

    def get(self, thekey, thedefault):
        """Get a value for a key based on the type of the provided default value.

        Return a default value if key does not exists.
        """
        if self.parser.has_option(self.S, thekey):
            if type(thedefault) == str:
                return self.parser.get(self.S, thekey)
            elif type(thedefault) == bool:
                return self.parser.getboolean(self.S, thekey)
            else:
                theoldkey = None
                try:#first if int
                    theoldkey = self.parser.getint(self.S, thekey)
                except ValueError:#otherwise a str
                    theoldkey = self.parser.get(self.S, thekey)
                except Exception as ex:#other error
                    print('LocalConfig other exception', repr(ex))
                    return theoldkey
                return theoldkey
        else:
            return thedefault

    def get_bool(self, thekey, thedefault):
        """Get a boolean value for a key. """
        b = self.get(thekey, thedefault)
        if type(b) == bool:
            return b
        if type(b) == str:
            if b.isalpha:
                return (b == 'False')
            else:
                return ( 0 == int(b))

    def set(self, thekey, thevalue):
        """Set the value for a key.

        Always convert to str.
        """
        try:
            self.parser.set(self.S, thekey, str(thevalue))
        except:
            print('(DEBUGprint) Option NOT setted (section, option,value)', self.S, thekey, str(thevalue))

    def save(self):
        """Save "my" section to the disk.

        1. Read all sections.
        2. Replace "my" section.
        3. Write all to disk (may re-arragne sections).
        """
        try:
            #open (a.k.a. and lock) the config file
            with open(self.configfile, 'r+') as f:
                #read the content
                thetext = f.read()
                #create a dummy parser with the content
                dummyparser = ConfigParser()
                dummyparser.read_string(thetext)
                if dummyparser.has_section(self.S):
                    #remove all keys for my section
                    dummyparser.remove_section(self.S)
                dummyparser.add_section(self.S)
                #if I have anything to write
                if self.parser.has_section(self.S):
                    #append the keys
                    #print('len(self.parser[self.S])',len(self.parser[self.S]))
                    for name, value in self.parser.items(self.S):
                        dummyparser.set(self.S, name, value)
                #write and free the conf file
                f.seek(0)
                f.truncate()
                dummyparser.write(f)
        except Exception as ex:
            print('write exception ', repr(ex),'\nwhile writing settings file: ', self.configfile)

class OptionConfig():
    def __init__(self, nameoffile):
        self.nameoffile = nameoffile
        self.general_section = 'General Options'

    def get(self, thekey, thedefault):
        with SectionConfig(self.nameoffile, self.general_section) as cf:
            return cf.get(thekey, thedefault)

    def get_bool(self, thekey, thedefault):
        with SectionConfig(self.nameoffile, self.general_section) as cf:
            return cf.get_bool(thekey, thedefault)

    def set(self, thekey, thevalue):
        with SectionConfig(self.nameoffile, self.general_section) as cf:
            cf.set(thekey, thevalue)
