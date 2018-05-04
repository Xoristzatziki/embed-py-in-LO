#!/usr/bin/env python3
#FIXME:
"""
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


#FIXME: correct the version
__version__ = '0.0.1'

#RETURN ERROR CODES
ERROR_IMPORT_LIBRARIES_FAIL = -1

try:
    import os
    import sys

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GdkPixbuf, GObject, Gio, GLib

    # Localization
    import locale
    from locale import gettext as _

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox

    from startwindow import PyloStartWindow as StartWindow

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

settings = None # Keep window related options
options = None #Keep application wide options in a 'General Options' section

class MyApplication(Gtk.Application):
    #FIXME: fix the docstring.
    """ Main entry of the application. """

    def __init__(self, *args, **kwargs):
        args2 = tuple()
        kwargs2 = {}

        self.name = 'pylo'
        self.id = 'org.kekbay.pylo'
        self.START_DIR = kwargs['START_DIR']
        self.BASE_DIR = kwargs['BASE_DIR']
        self.version = __version__
        self.localizedname = _('pylo')
        # Bind the locale.
        print("os.path.join(self.BASE_DIR, 'locale')",os.path.join(self.BASE_DIR, 'locale'))
        print("#"+self.id+"#")
        locale.bindtextdomain(self.id, os.path.join(self.BASE_DIR, 'locale'))
        locale.textdomain(self.id)
        super().__init__(*args2,
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs2)

        # Init the settings module.
        self.dummy_for_settings = SectionConfig(self.name, self.__class__.__name__)
        global settings
        settings = self.dummy_for_settings

        self.dummy_for_options = OptionConfig(self.name)
        global options
        options = self.dummy_for_options

        theiconfile = os.path.join(self.BASE_DIR, 'icons', 'logo.png')
        try:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(theiconfile)
        except Exception:
            self.icon = None

        self.window = None
        # Set any command line options here.
        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            #FIXME: remove custom args if not needed
            some_custom_args = {}
            some_custom_args['haha'] = 'ena'
            # we can provide anything, even a local function
            some_custom_args['parentclassnamefunction'] = self.custom_function
            self.window = StartWindow(application=self,
                custom_args = some_custom_args)

        self.window.present()

    #FIXME: remove if not needed
    def custom_function(self, *args, **kwargs):
        """ Dummy custom function on parent.

        Can be used to:
        - Return a value here.
        - Get a value from here.
        """
        # dummy printout of passed dict (kwargs
        print('== kwargs from child ==')
        print(kwargs)
        # dummy return of my class name
        return self.__class__.__name__

    def on_quit(self, action, param):
        """ Connected, above, to our action "quit". """
        self.quit()

    def do_command_line(self, command_line):
        """ Parse command line and activate the application. """
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()

        return 0

if __name__ == '__main__':
    #Main entry point if running the program from command line
    START_DIR = os.path.dirname(os.path.abspath('.'))
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    myapp = MyApplication(START_DIR=START_DIR, BASE_DIR=BASE_DIR)
    myapp.run(sys.argv)

