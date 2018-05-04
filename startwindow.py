#!/usr/bin/env python3
#FIXME:
# This is an example class generated using a bare glade file.
#
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
VERSIONSTR = 'v. {}'.format(__version__)

#RETURN ERROR CODES
ERROR_IMPORT_LIBRARIES_FAIL = -1
ERROR_INVALID_GLADE_FILE = -2
ERROR_GLADE_FILE_READ = -3


MENU_ENUM_FILE_OPEN = 1
MENU_ENUM_FILE_VIEW = 2
MENU_ENUM_FILE_ADD = 3
MENU_ENUM_FILE_REPLACE = 4
MENU_ENUM_FILE_RESTORE = 5
MENU_ENUM_FILES_DIFF = 6


class ConditionEnums:
    CONDITION_OK = 0
    CONDITION_REMOVE = 1
    CONDITION_REPLACE = 2
    CONDITION_ADD = 3
    BACKUP_ERROR = 16
    OTHER_ERROR = 256
    def __init__(self):
        pass

myenums = ConditionEnums()
CONDITION_OK = myenums.CONDITION_OK
CONDITION_REMOVE = myenums.CONDITION_REMOVE
CONDITION_REPLACE = myenums.CONDITION_REPLACE
CONDITION_ADD = myenums.CONDITION_ADD

BACKUP_ERROR = myenums.BACKUP_ERROR
OTHER_ERROR = myenums.OTHER_ERROR

try:
    import os
    import sys
    import tempfile
    import subprocess
    import multiprocessing
    from multiprocessing import Process
    import urllib

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GObject, Pango
    gi_require_version('GtkSource', '3.0')
    from gi.repository import GtkSource

    # Localization
    import locale
    from locale import gettext as _
    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox

    from documents import LODocument, ChooserDialog
    from themes import ThemeManager

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

settings = None # Keep window related options
options = None #Keep application wide options in a 'General Options' section

class PyloStartWindow(Gtk.ApplicationWindow):
    #FIXME: fix the docstring.
    """ Main window with all components. """

    def __init__(self, *args, **kwargs):
        # Set the app
        if 'parent' in kwargs:#use the same application
            self.myparent = kwargs['parent']
            self.app = kwargs['parent'].app
        elif 'application' in kwargs:
            self.myparent = None
            self.app = kwargs['application']
        if self.myparent and 'modal' in kwargs:
            # "modal" means caller require transient
            self.set_transient_for(self.myparent)
            # but modality can be false, and parent may not be present
            if self.myparent:
                self.set_modal(kwargs['modal'])
        if 'custom_args' in kwargs:
            self.custom_args = kwargs['custom_args']
            # do not pass them to Gtk.ApplicationWindow init
            # otherwise will trigger an error
            del kwargs['custom_args']
            if 'trigger_before_exit' in self.custom_args:
                # must be a function on calling class
                self.trigger_before_exit = self.custom_args['trigger_before_exit']

        # Before super initialization.

        # init super.
        # First init the window, otherwise MRO will mess it.
        Gtk.ApplicationWindow.__init__(self, *args, **kwargs)

        # Any nitializations required before loading the glade file.
        GObject.type_register(GtkSource.View)

        # Now load builder.
        self._get_from_builder()

        # Load any settings or run extra initializations.
        self._post_initialisations()

#********* Auto created "class defs" START ************************************************************
    def _get_from_builder(self):
        """ Load components from a glade file. """
        # Load the ui from a glade file.
        self.builder = Gtk.Builder()
        try:
            self.builder.add_from_file(os.path.join(self.app.BASE_DIR,
                'ui',
                'startwindow.glade')
            )
        except Exception as ex:
            print(str(ex))
            print('\n{}:\n{}\n{}'.format(_('Error loading from Glade file'),
                os.path.join(self.app.BASE_DIR,
                'ui',
                'startwindow.glade'), repr(ex))
            )
            sys.exit(ERROR_INVALID_GLADE_FILE)

        # Get gui objects.
        self.MainBox = self.builder.get_object('MainBox')
        self.boxForFooter = self.builder.get_object('boxForFooter')
        self.boxForHeader = self.builder.get_object('boxForHeader')
        self.boxForSource = self.builder.get_object('boxForSource')
        self.boxForSourceButtons = self.builder.get_object('boxForSourceButtons')
        self.boxList = self.builder.get_object('boxList')
        self.boxListButtons = self.builder.get_object('boxListButtons')
        self.buttonAbout = self.builder.get_object('buttonAbout')
        self.buttonAddNew = self.builder.get_object('buttonAddNew')
        self.buttonEditSelected = self.builder.get_object('buttonEditSelected')
        self.buttonExit = self.builder.get_object('buttonExit')
        self.buttonKeepSelected = self.builder.get_object('buttonKeepSelected')
        self.buttonRemoveSelected = self.builder.get_object('buttonRemoveSelected')
        self.buttonReplaceSelected = self.builder.get_object('buttonReplaceSelected')
        self.buttonRun = self.builder.get_object('buttonRun')
        self.buttonSelectLODocument = self.builder.get_object('buttonSelectLODocument')
        self.buttonViewSelected = self.builder.get_object('buttonViewSelected')
        self.cellrendererpixbuf1 = self.builder.get_object('cellrendererpixbuf1')
        self.cellrenderertext1 = self.builder.get_object('cellrenderertext1')
        self.cellrenderertext2 = self.builder.get_object('cellrenderertext2')
        self.comboTheme = self.builder.get_object('comboTheme')
        self.entryLODocument = self.builder.get_object('entryLODocument')
        self.fontbuttonForSource = self.builder.get_object('fontbuttonForSource')
        self.imageAbout = self.builder.get_object('imageAbout')
        self.imageAdd = self.builder.get_object('imageAdd')
        self.imageEdit = self.builder.get_object('imageEdit')
        self.imageExecute = self.builder.get_object('imageExecute')
        self.imageFind = self.builder.get_object('imageFind')
        self.imageOk = self.builder.get_object('imageOk')
        self.imageQuit = self.builder.get_object('imageQuit')
        self.imageRemove = self.builder.get_object('imageRemove')
        self.imageRevert = self.builder.get_object('imageRevert')
        self.labelLODocument = self.builder.get_object('labelLODocument')
        self.labelSelectedRow = self.builder.get_object('labelSelectedRow')
        self.labelVersion = self.builder.get_object('labelVersion')
        self.scriptlist = self.builder.get_object('scriptlist')
        self.scrolledwindowList = self.builder.get_object('scrolledwindowList')
        self.scrolledwindowSource = self.builder.get_object('scrolledwindowSource')
        self.separatorInListButtons1 = self.builder.get_object('separatorInListButtons1')
        self.separatorInListButtons2 = self.builder.get_object('separatorInListButtons2')
        self.srcviewOutput = self.builder.get_object('srcviewOutput')
        self.treeviewcolumn1 = self.builder.get_object('treeviewcolumn1')
        self.treeviewcolumn2 = self.builder.get_object('treeviewcolumn2')
        self.treeviewcolumn3 = self.builder.get_object('treeviewcolumn3')
        self.treeviewselection1 = self.builder.get_object('treeviewselection1')
        self.vpaned = self.builder.get_object('vpaned')

        # Connect signals existing in the Glade file.
        self.builder.connect_signals(self)

        # Reparent our main container from glader file,
        # this way we have all Gtk.Window functionality using "self".
        thechild = self.builder.get_object('PyloStartWindow').get_child()
        thechild.get_parent().remove(thechild)
        self.add(thechild)

        # Connect generated signals:
        # top window signals and/or other generated signals.
        # top window signals were connected, by builder's "connect_signals" function,
        # to builder's main window
        self.buttonAbout.connect('clicked', self.on_buttonAbout_clicked)
        self.buttonAddNew.connect('clicked', self.on_buttonAddNew_clicked)
        self.buttonEditSelected.connect('clicked', self.on_buttonEditSelected_clicked)
        self.buttonExit.connect('clicked', self.on_buttonExit_clicked)
        self.buttonKeepSelected.connect('clicked', self.on_buttonKeepSelected_clicked)
        self.buttonRemoveSelected.connect('clicked', self.on_buttonRemoveSelected_clicked)
        self.buttonReplaceSelected.connect('clicked', self.on_buttonReplaceSelected_clicked)
        self.buttonRun.connect('clicked', self.on_buttonRun_clicked)
        self.buttonSelectLODocument.connect('clicked', self.on_buttonSelectLODocument_clicked)
        self.buttonViewSelected.connect('clicked', self.on_buttonViewSelected_clicked)
        self.connect('delete-event', self.on_PyloStartWindow_delete_event)
        self.connect('destroy', self.on_PyloStartWindow_destroy)
        self.connect('size-allocate', self.on_PyloStartWindow_size_allocate)
        self.connect('window-state-event', self.on_PyloStartWindow_window_state_event)
        self.vpaned.connect('size-allocate', self.on_vpaned_size_allocate)


        # :builder top window properties.
        # Set the label for labelVersion
        self.labelVersion.set_label(VERSIONSTR)
        self.can_focus = 'False'

        # Set the label for labelVersion
        self.labelVersion.set_label(VERSIONSTR)
        self.labelVersion.set_tooltip_text(_("""This is the version of this window.
Not the version of the application."""))

        # Load window icon from app, if any.
        self.set_icon(self.app.icon)

    def _post_initialisations(self):
        """ Do some extra initializations.

        Display the version if a labelVersion is found.
        Set defaults (try to load them from a configuration file):
            - Window size and state (width, height and if maximized)
        Load saved custom settings.
        """
        # Init the settings module.
        self.dummy_for_settings = SectionConfig(self.app.id, self.__class__.__name__)
        global settings
        settings = self.dummy_for_settings

        self.dummy_for_options = OptionConfig(self.app.id)
        global options
        options = self.dummy_for_options

        # Bind message boxes.
        self.MessageBox = MessageBox(self)
        self.msg = self.MessageBox.Message
        self.are_you_sure = self.MessageBox.are_you_sure

        # Set previous size and state.
        width = settings.get('width', 350)
        height = settings.get('height', 350)
        self.set_title(self.app.localizedname)
        self.resize(width, height)
        if settings.get_bool('maximized', False):
            self.maximize()
        # Load any other settings here.
        self.last_LO_path = '.'
        self.base_model = None
        self.selected_iter = None
        self.tempdir = tempfile.TemporaryDirectory(prefix = 'pylo')
        dialoginst = ChooserDialog()
        self.select_file = dialoginst.select_file

        self.thememanager = ThemeManager(self.comboTheme)
        self.thememanager.load_and_show_themes(settings.get('theme_id',
                None))
        self.srcviewOutput.set_buffer(self.thememanager.bufferOutput)

        self.fontbuttonForSource.set_font_name(settings.get(
                'font_for_source', 'Monospace Regular 8'))

        self.last_LO_path = settings.get('last_LO_path',
                os.path.abspath('.'))
        self.last_search_path = settings.get('last_search_path',
                self.last_LO_path)
        i = Gtk.IconTheme.get_default()
        conditions = {}
        conditions[CONDITION_OK] = {'icon': Gtk.IconTheme.load_icon(i,
            "gtk-ok", 22, Gtk.IconLookupFlags.USE_BUILTIN),
            'str': _('Keep')}
        conditions[CONDITION_REMOVE] = {'icon':
            Gtk.IconTheme.load_icon(i,
            "gtk-no", 22, Gtk.IconLookupFlags.USE_BUILTIN),
            'str': _('Remove')}
        conditions[CONDITION_REPLACE] = {'icon':
            Gtk.IconTheme.load_icon(i,
            "edit-redo", 22, Gtk.IconLookupFlags.USE_BUILTIN),
            'str': _('Replace')}
        conditions[CONDITION_ADD] = {'icon':
            Gtk.IconTheme.load_icon(i,
            "list-add", 22, Gtk.IconLookupFlags.USE_BUILTIN),
            'str': _('Add')}
        self.conditions = conditions
        # Set drag manipulation for some widgets.
        self.entryLODocument.drag_dest_set(0, [], 0)
        self.scrolledwindowList.drag_dest_set(0, [], 0)

        if hasattr(self, 'custom_args'):
            print('===self.custom_args===\n', self.custom_args)
            if 'parentclassnamefunction' in self.custom_args:
                print('== Calling parentclassnamefunction:')
                dummy = self.custom_args['parentclassnamefunction']()
                print('== Response ==\n', dummy)

#********* Auto created handlers START *********************************
    def on_PyloStartWindow_delete_event(self, widget, event, *args):
        """ Handler for PyloStartWindow.delete-event. """
        print("""3 Handler for PyloStartWindow.delete-event. """)
        return self.exit_requested('from_delete_event')

    def on_PyloStartWindow_destroy(self, widget, *args):
        """ Handler for PyloStartWindow.destroy. """
        print( """1 Handler for PyloStartWindow.destroy. """)
        self.exit_requested('from_destroy')
        print( """2 Handler for PyloStartWindow.destroy. """)
        return False

    def on_PyloStartWindow_size_allocate(self, widget, allocation, *args):
        """ Handler for PyloStartWindow.size-allocate. """
        self.save_my_size()

    def on_PyloStartWindow_window_state_event(self, widget, event, *args):
        """ Handler for PyloStartWindow.window-state-event. """
        settings.set('maximized',
            ((int(event.new_window_state) & Gdk.WindowState.ICONIFIED) != Gdk.WindowState.ICONIFIED) and
            ((int(event.new_window_state) & Gdk.WindowState.MAXIMIZED) == Gdk.WindowState.MAXIMIZED)
            )
        self.save_my_size()

    def on_buttonAbout_clicked(self, widget, *args):
        """ Handler for buttonAbout.clicked. """
        self.MessageBox.AboutBox()

    def on_buttonAddNew_clicked(self, widget, *args):
        """ Handler for buttonAddNew.clicked. """
        start_in = settings.get('last_python_path', '.')
        selected_file = self.select_file(self, 'python', start_in)
        if not selected_file:
            return False
        self.try_add_new_script(selected_file)

    def on_buttonEditSelected_clicked(self, widget, *args):
        """ Handler for buttonEditSelected.clicked. """
        thecondition = self.base_model.get_value(self.selected_iter, 3)
        if thecondition == CONDITION_OK or CONDITION_REMOVE:
            message = _("""This will create a temporary file.

  If you want to make changes you must save
the file with a valid name and use that new file
to replace the embeded.
Otherwise all your changes will be lost!
""")
            self.msg(message, boxtype = 'WARNING')

            the_embeded_name = self.base_model.get_value(self.selected_iter, 0)
            content = self.current_doc.get_source(the_embeded_name)

            handle, tmpfile = tempfile.mkstemp('Unsaved.py')
            with open(tmpfile,'w') as f:
                f.write(content)
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', tmpfile))
                return True # event has been handled
            elif os.name == 'nt':
                os.startfile(tmpfile)
                return True # event has been handled
            elif os.name == 'posix':
                p = Process(target=open_file_async, args=('xdg-open', tmpfile))
                p.start()
                return True # event has been handled
            os.close(handle)
            return False # event has not been handled

    def on_buttonExit_clicked(self, widget, *args):
        """ Handler for buttonExit.clicked. """
        self.exit_requested()

    def on_buttonKeepSelected_clicked(self, widget, *args):
        """ Handler for buttonKeepSelected.clicked. """
        theoldcondition = self.base_model.get_value(self.selected_iter, 3)
        new_condition = CONDITION_OK
        self.base_model.set_value(self.selected_iter, 3,
                new_condition)
        self.base_model.set_value(self.selected_iter, 6,
                self.base_model.get_value(self.selected_iter, 0))
        self.base_model.set_value(self.selected_iter, 1,
                self.conditions[new_condition]['icon'])
        self.show_buttons_for_selected()

    def on_buttonRemoveSelected_clicked(self, widget, *args):
        """ Handler for buttonRemoveSelected.clicked. """
        theoldcondition = self.base_model.get_value(self.selected_iter, 3)
        if theoldcondition == CONDITION_OK:
            new_condition = CONDITION_REMOVE
            self.base_model.set_value(self.selected_iter, 3,
                    new_condition)
            self.base_model.set_value(self.selected_iter, 6,
                    "")
            self.base_model.set_value(self.selected_iter, 1,
                    self.conditions[new_condition]['icon'])
            self.show_buttons_for_selected()
        elif theoldcondition == CONDITION_ADD:
            self.remove_selected_script()

    def on_buttonReplaceSelected_clicked(self, widget, *args):
        """ Handler for buttonReplaceSelected.clicked. """
        the_embeded_name = self.base_model.get_value(self.selected_iter, 0)
        start_in = settings.get('last_python_path', '.')
        selected_file = self.select_file(self, 'python', start_in)
        if not selected_file: return False
        self.try_replace_selected_script(the_embeded_name, selected_file)

    def on_buttonRun_clicked(self, widget, *args):
        """ Handler for buttonRun.clicked. """
        files_to_remove = []
        files_to_append = []
        for x in self.base_model:
            if len(x[0]):# file was embeded
                if x[3] == CONDITION_REMOVE:
                    files_to_remove.append(x[0])
                    print('CONDITION_REMOVE',x[0])
                elif x[3] == CONDITION_REPLACE:
                    files_to_remove.append(x[0])
                    print('CONDITION_REPLACE','files_to_remove',x[0])
                    files_to_append.append(x[5])
                    print('CONDITION_REPLACE','files_to_append',x[5])
            else:
                files_to_append.append(x[5])
        # TODO: Let user select the backup folder or name
        backup_file = os.path.join(self.current_doc.thepath, 'backup',
                self.current_doc.thefile)
        ok, changes_result = self.current_doc.make_requested_changes(files_to_remove,
                files_to_append, backup_file)
        if ok:
            a = _('Changes were succesful')
            b = _('Old verion can be found at')
            self.msg('{}.\n{}:\n{}'.format(a, b, backup_file))
        else:
            a = _('Something went wrong')
            b = _('The error number was')
            self.msg('{}!\n{}:\n{}'.format(a, b, changes_result),
                    boxtype = 'ERROR')
        self.init_LO_file(None)

    def on_buttonSelectLODocument_clicked(self, widget, *args):
        """ Handler for buttonSelectLODocument.clicked. """
        if self.ask_dropping_LO_file():
            selected_file = self.select_file(self, 'LO',
                settings.get('last_lo_path','.')
            )
            if selected_file:
                self.init_LO_file(selected_file)

    def on_buttonViewSelected_clicked(self, widget, *args):
        """ Handler for buttonViewSelected.clicked. """
        the_embeded_name = self.base_model.get_value(self.selected_iter, 0)
        the_new_path = self.base_model.get_value(self.selected_iter, 5)
        if len(the_embeded_name):
            thesource = self.current_doc.get_source(the_embeded_name)
            self.srcviewOutput.get_buffer().set_text(thesource)
        elif len(the_new_path):
            with open(the_new_path, 'r') as f:
                thesource = f.read()
            self.srcviewOutput.get_buffer().set_text(thesource)
        if self.vpaned.get_position()>self.vpaned.get_allocated_height()-100:
            self.vpaned.set_position(self.vpaned.get_allocated_height()-100)

    def on_comboTheme_changed(self, widget, *args):
        """ Handler for comboTheme.changed. """
        selitr = self.comboTheme.get_active_iter()
        if selitr is None:
            return None
        # Value for column 0 (the theme name)
        themename = self.thememanager.listTheme.get_value(selitr, 0)
        self.thememanager.set_theme(themename)
        settings.set('theme_id', self.thememanager.theme_name)

    def on_entryLODocument_drag_data_received(self, widget, context, x, y, selection_data, info, time_, *args):
        """ Handler for entryLODocument.drag-data-received. """
        #print(widget, context, x, y, selection_data, info, time_)
        allfiles = selection_data.get_text().rstrip('\n').split('\n')
        allfiles_decoded = [urllib.request.url2pathname(url)  for url in allfiles]
        if len(allfiles_decoded) == 1:
            if self.ask_dropping_LO_file():
                file_components = urllib.parse.urlparse(allfiles_decoded[0])
                self.init_LO_file(file_components.path)

    def on_entryLODocument_drag_drop(self, widget, context, x, y, time_, *args):
        """ Handler for entryLODocument.drag-drop. """
        widget.drag_get_data(context, context.list_targets()[-1], time_)

    def on_entryLODocument_drag_motion(self, widget, context, x, y, time_, *args):
        """ Handler for entryLODocument.drag-motion. """
        Gdk.drag_status(context,Gdk.DragAction.COPY, time_)
        return True

    def on_fontbuttonForSource_font_set(self, widget, *args):
        """ Handler for fontbuttonForSource.font-set. """
        font = widget.get_font_name()
        settings.set('font_for_source', font)
        self.srcviewOutput.modify_font(Pango.FontDescription(font))

    def on_scriptlist_button_press_event(self, widget, event, *args):
        """ Handler for scriptlist.button-press-event. """
        return False
        if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
            return False
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            pthinfo = self.scriptlist.get_path_at_pos(event.x, event.y)
            if pthinfo != None:
                path,col,cellx,celly = pthinfo
                self.on_scriptlist_row_activated(self.scriptlist, path, col)
                print(path,col,cellx,celly)
                return True # event has been handled
        elif event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            pthinfo = self.scriptlist.get_path_at_pos(event.x, event.y)
            if pthinfo != None:

                pass

        return False # event has not been handled
    def on_scriptlist_row_activated(self, widget, path, column, *args):
        """ Handler for scriptlist.row-activated. """
        #print(widget)
        themodel = self.sorted_model
        theiter = themodel.get_iter(path)
        path_in_filtered_model = self.sorted_model.convert_path_to_child_path(path)
        path_in_base_model = self.filtered_model.convert_path_to_child_path(path_in_filtered_model)
        self.selected_iter = self.base_model.get_iter(path_in_base_model)
        self.show_buttons_for_selected()

    def on_scrolledwindowList_drag_data_received(self, widget, context, x, y, selection_data, info, time_, *args):
        """ Handler for scrolledwindowList.drag-data-received. """
        if self.base_model:
            #print(widget, context, x, y)
            allfiles = selection_data.get_text().rstrip('\n').split('\n')
            allfiles_decoded = [urllib.request.url2pathname(url)  for url in allfiles]
            for afile in allfiles_decoded:
                self.try_add_new_script(afile)
        else:
            return

    def on_scrolledwindowList_drag_drop(self, widget, context, x, y, time_, *args):
        """ Handler for scrolledwindowList.drag-drop. """
        widget.drag_get_data(context, context.list_targets()[-1], time_)

    def on_scrolledwindowList_drag_motion(self, widget, context, x, y, time_, *args):
        """ Handler for scrolledwindowList.drag-motion. """
        Gdk.drag_status(context,Gdk.DragAction.COPY, time_)
        # Returning True which means "I accept this data".
        return True

    def on_vpaned_size_allocate(self, widget, allocation, *args):
        """ Handler for vpaned.size-allocate. """
        settings.set('vpaned',self.vpaned.get_position())
        pass


#********* Auto created handlers  END **********************************

    def exit_requested(self, *args, **kwargs):
        """ Final work before exit. """
        if hasattr(self, 'continue_closing'):
            pass
        else:
            if self.there_are_changes():
                a = _('Exit the application')
                b = _('  But you have made changes')
                c = _('Any changes to the current document will be lost')
                addmessage = '{}!\n{}!\n{}!'.format(a, b, c)
                if not self.are_you_sure(addmessage):
                    return True # a.k.a. do not destroy...
                self.continue_closing = True
        self.set_transient_for()
        self.set_modal(False)
        self.set_unhandled_settings()# also saves all settings
        if 'from_destroy' in kwargs or 'from_delete_event' in kwargs:
            return True
        else:
            # Check if we should provide info to caller
            if hasattr(self, 'custom_args'):
                if 'trigger_on_exit' in self.custom_args:
                    self.trigger_on_exit(exiting = True,
                        return_parameters = self.return_parameters)
            self.destroy()

    def present(self):
        """ Show the window. """
        self.show_all()
        #"enable" next line to have some interactive view of potentiallities of GUI
        #self.set_interactive_debugging (True)
        super().present()

    def save_my_size(self):
        """ Save the window size into settings, if not maximized. """
        if not settings.get_bool('maximized', False):
            width, height = self.get_size()
            settings.set('width', width)
            settings.set('height', height)

    def set_unhandled_settings(self):
        """ Set, before exit, settings not applied during the session.

        Additionally, flush all settings to .conf file.
        """
        # Set any custom settings
        # which where not setted (ex. on some widget's state changed)

        # Save all settings
        settings.save()

#********* Auto created "class defs" END **************************************************************

    def ask_dropping_LO_file(self):
        if self.there_are_changes():
            a = _('Load a new file.')
            b = _('Any changes to the current document will be lost')
            addmessage = '{}\n{}!'.format(a,b)
            if not self.are_you_sure(addmessage):
                return False
        return True

    def init_LO_file(self, selected_file):
        if selected_file:
            self.current_doc = LODocument(selected_file, myenums)
            settings.set('last_lo_path', self.current_doc.thepath)
            self.entryLODocument.set_text(self.current_doc.thefile)
            self.buttonAddNew.set_sensitive(self.current_doc.isLOfilelike)
            if self.current_doc.isLOfilelike:
                self.boxForHeader.modify_bg(Gtk.StateType.NORMAL,
                        Gdk.color_parse("#228b22"))#forest green
                self.boxForHeader.set_tooltip_text(self.current_doc.fullpath)
                self.set_title('Pylo - ' + self.current_doc.thefile)
                self.labelLODocument.set_label(_('LibreOffice Document'))
            else:
                self.boxForHeader.set_tooltip_text(_('Not a valid Document!'))
                self.boxForHeader.modify_bg(Gtk.StateType.NORMAL,
                        Gdk.color_parse("#ff2733"))#some red
                a = _('Invalid')
                self.set_title('Pylo - {} - '.format(a) + self.current_doc.thefile)
                self.labelLODocument.set_label(_('Invalid Document'))
            self.fill_list()
            self.buttonRun.set_sensitive(True)
            return
        else:
            self.current_doc = None
            self.entryLODocument.set_text("")
            self.buttonAddNew.set_sensitive(False)
            self.buttonRun.set_sensitive(False)
            a = _('No file selected.')
            self.set_title('Pylo - {}'.format(a))
            self.fill_list()

    def fill_list(self):
        """ Fill model with embeded scripts.

        Clear the model (if exists) and no file is valid or selected.
        """
        if (not self.current_doc) or (not self.current_doc.isLOfilelike):
            if self.base_model:
                self.base_model.clear()
                self.refilter_me()
            return
        howmany = len(self.current_doc.python_files)

        self.base_model = Gtk.TreeStore('gchararray', 'GdkPixbuf',
                'gchararray','glong','gboolean','gchararray','gchararray')

        for apyscript in self.current_doc.python_files:
            depth0 = self.base_model.append(None)
            self.base_model.set_value(depth0, 0, apyscript)
            self.base_model.set_value(depth0, 1,
                    self.conditions[CONDITION_OK]['icon'])
            self.base_model.set_value(depth0, 2, "")
            self.base_model.set_value(depth0, 3, CONDITION_OK)
            self.base_model.set_value(depth0, 4, True)
            # full path to new file for modified
            self.base_model.set_value(depth0, 5, '')
            #unique name inside modified
            self.base_model.set_value(depth0, 6, apyscript)

        self.filtered_model = self.base_model.filter_new()
        self.filtered_model.set_visible_column(4)
        self.sorted_model = Gtk.TreeModelSort(self.filtered_model)

        self.scriptlist.set_model(None)
        self.scriptlist.set_model(self.sorted_model)
        self.scriptlist.get_column(0).set_sort_column_id(0)
        self.scriptlist.get_column(1).set_sort_column_id(3)
        self.scriptlist.get_column(2).set_sort_column_id(6)
        self.sorted_model.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.refilter_me()

    def msg_not_yet(self):
        self.msg(_('Not yet implemented'))

    def refilter_me(self):
        self.filtered_model.refilter()
        self.show_buttons_for_selected(True)

    def show_list_menu(self):
        self.current_menu = Gtk.Menu()
        self.current_menu.afilepath = filepath

    def show_buttons_for_selected(self, setNone = False):
        if setNone:
            self.labelSelectedRow.set_label(_("No selection."))
            self.labelSelectedRow.set_tooltip_text(_('Make a selection first'))
            self.buttonRemoveSelected.set_sensitive(False)
            self.buttonReplaceSelected.set_sensitive(False)
            self.buttonKeepSelected.set_sensitive(False)
            self.buttonEditSelected.set_sensitive(False)
            self.buttonViewSelected.set_sensitive(False)
            return
        themodel = self.base_model
        theiter = self.selected_iter
        theEmbededscript = themodel.get_value(theiter,0)
        # 1 = theicon
        theresult = themodel.get_value(theiter,2)
        thecondition = themodel.get_value(theiter,3)
        thefilepath = themodel.get_value(theiter,5)

        text = self.conditions[thecondition]['str'] + ' : '
        if thecondition == CONDITION_OK: # embeded
            text += ' : ' + theEmbededscript
        elif thecondition == CONDITION_ADD: # added
            text += theresult
        elif thecondition == CONDITION_REMOVE: # for removing
            text += ' : ' + theEmbededscript
        elif thecondition == CONDITION_REPLACE: #replacing embeded
            text += ':' + theresult
        else:
            text += ':' + _('A BUG FOUND')
        self.labelSelectedRow.set_label(text)
        self.labelSelectedRow.set_tooltip_text(thefilepath)
        if len(theEmbededscript): # an old embeded
            self.buttonRemoveSelected.set_sensitive(thecondition == CONDITION_OK)
            self.buttonReplaceSelected.set_sensitive(thecondition != CONDITION_REPLACE)
            self.buttonKeepSelected.set_sensitive(thecondition != CONDITION_OK)
        else:# not an old embeded
            self.buttonKeepSelected.set_sensitive(False)
            self.buttonRemoveSelected.set_sensitive(True)
            self.buttonReplaceSelected.set_sensitive(False)
        self.buttonEditSelected.set_sensitive(True)
        self.buttonViewSelected.set_sensitive(True)
        self.scriptlist.grab_focus()

    def try_add_new_script(self, selected_file):
        thefolder, thename = os.path.split(selected_file)
        settings.set('last_python_path', thefolder)
        for x in self.base_model:
            if x[6] == thename:
                a = _('Same name exists')
                b = _('Please remove it first')
                if len(x[2]):
                    d = '!'
                else:
                    thename = x[2]
                    c = _('or use the button to replace it')
                    d = ',\n{}.'.format(c)
                self.msg('{}!\n{}\n{}{}'.format(a, thename, b, d))
                return
        self.add_new_script(selected_file)

    def add_new_script(self, selected_file):
        thefolder, thename = os.path.split(selected_file)
        depth0 = self.base_model.append(None)
        self.base_model.set_value(depth0, 0, "")
        self.base_model.set_value(depth0, 1,
                self.conditions[CONDITION_ADD]['icon'])
        self.base_model.set_value(depth0, 2, thename)
        self.base_model.set_value(depth0, 3, CONDITION_ADD)
        self.base_model.set_value(depth0, 4, True)
        self.base_model.set_value(depth0, 5, selected_file)
        self.base_model.set_value(depth0, 6, thename)
        self.refilter_me()

    def remove_selected_script(self):
        thefilepath = self.base_model.get_value(self.selected_iter, 5)
        addmessage = '{}:\n{}'.format(_('Remove the file'),thefilepath)
        if not self.are_you_sure(addmessage):
            return
        self.base_model.remove(self.selected_iter)
        self.show_buttons_for_selected(True)

    def try_replace_selected_script(self, the_embeded_name, selected_file):
        thefolder, thename = os.path.split(selected_file)
        settings.set('last_python_path', thefolder)
        if the_embeded_name != thename:
            a = _('Names do not match!')
            for x in self.base_model:
                if x[6] == thename:
                    b = _('Additionally a script with same name exists.')
                    c = _('Cannot continue!')
                    message = '{}\n{}\n{}'.format(a,b,c)
                    self.msg(message)
                    return
            b = _('Add instead of replacing?')
            message = '{}\n{}'.format(a, b)
            ok = self.msg(message, buttons='YESCANCEL', boxtype = 'QUESTION')
            if not ok:
                return
            self.add_new_script(selected_file)
            return
        self.replace_selected_script(selected_file)

    def replace_selected_script(self, selected_file):
        thefolder, thename = os.path.split(selected_file)
        new_condition = CONDITION_REPLACE
        # new icon
        self.base_model.set_value(self.selected_iter, 1,
                self.conditions[new_condition]['icon'])
        # the name for
        self.base_model.set_value(self.selected_iter, 2,
                thename)
        self.base_model.set_value(self.selected_iter, 3,
                new_condition)
        self.base_model.set_value(self.selected_iter, 5,
                selected_file)
        self.base_model.set_value(self.selected_iter, 6,
                thename)
        self.show_buttons_for_selected()

    def there_are_changes(self):
        result = False
        if self.base_model:
            for x in self.base_model:
                if x[3] != CONDITION_OK:
                    return True
        return result

    @staticmethod
    def clear_box(thelistbox):
        allchildren = thelistbox.get_children()
        for achild in allchildren[:]:
            achild.destroy()
        thelistbox.show_all()

#********* Window class  END***************************************************************************
def open_file_async(*args):
    subprocess.call((args[0], args[1]))
