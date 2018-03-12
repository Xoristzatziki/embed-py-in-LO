#!/usr/bin/python3

import os, shutil, tempfile, zipfile, configparser

from bs4 import BeautifulSoup

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib

import locale
from locale import gettext as _


VERSION = '0.0.10'
#dummyAPPNAME = _('GUI for embeding a Python user script in a LibreOffrice Document.')
APPNAME = 'GUI for embeding a Python user script in a LibreOffrice Document.'
APPDOMAIN = 'gr.kekbay.embedpythoninlo'

thegladestr = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.18.3 -->
<interface>
  <requires lib="gtk+" version="3.12"/>
  <object class="GtkBox" id="boxMain">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="margin_left">3</property>
    <property name="margin_right">3</property>
    <property name="margin_top">3</property>
    <property name="margin_bottom">3</property>
    <property name="orientation">vertical</property>
    <property name="spacing">3</property>
    <child>
      <object class="GtkBox" id="box4">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="spacing">3</property>
        <child>
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="label" translatable="yes">LibreOffice file</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkEntry" id="entryLOfile">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="editable">False</property>
            <signal name="changed" handler="on_entryLOfile_changed" swapped="no"/>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonLofile">
            <property name="label" translatable="yes">...</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <signal name="clicked" handler="on_buttonLofile_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">True</property>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <object class="GtkPaned" id="vpaned">
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <property name="orientation">vertical</property>
        <property name="position">160</property>
        <property name="position_set">True</property>
        <property name="wide_handle">True</property>
        <child>
          <object class="GtkBox" id="box5">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="spacing">3</property>
            <child>
              <object class="GtkBox" id="box6">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <property name="spacing">3</property>
                <child>
                  <object class="GtkLabel" id="label2">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Existing</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkScrolledWindow" id="scrolledwindow2">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="shadow_type">in</property>
                    <child>
                      <object class="GtkViewport" id="viewport2">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <child>
                          <object class="GtkListBox" id="listboxexisting">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="box9">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <property name="spacing">3</property>
                <child>
                  <object class="GtkLabel" id="label5">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Remove</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkScrolledWindow" id="scrolledwindow5">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="shadow_type">in</property>
                    <child>
                      <object class="GtkViewport" id="viewport5">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <child>
                          <object class="GtkListBox" id="listboxremove">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="box7">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <property name="spacing">3</property>
                <child>
                  <placeholder/>
                </child>
                <child>
                  <placeholder/>
                </child>
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="box8">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <property name="spacing">3</property>
                <child>
                  <object class="GtkLabel" id="label4">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Add-Replace</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkButton" id="buttonAddReplace">
                    <property name="visible">True</property>
                    <property name="sensitive">False</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                    <property name="tooltip_text" translatable="yes">Select new python file to add or replace an old version</property>
                    <property name="halign">center</property>
                    <property name="valign">center</property>
                    <property name="always_show_image">True</property>
                    <signal name="clicked" handler="on_buttonAddReplace_clicked" swapped="no"/>
                    <child>
                      <object class="GtkImage" id="image1">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="stock">gtk-add</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkScrolledWindow" id="scrolledwindow4">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="shadow_type">in</property>
                    <child>
                      <object class="GtkViewport" id="viewport4">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <child>
                          <object class="GtkListBox" id="listboxaddreplace">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">2</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">3</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="resize">False</property>
            <property name="shrink">True</property>
          </packing>
        </child>
        <child>
          <object class="GtkScrolledWindow" id="scrolledwindow1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="shadow_type">in</property>
            <child>
              <object class="GtkViewport" id="viewport1">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <child>
                  <object class="GtkTextView" id="textviewSource">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="resize">True</property>
            <property name="shrink">True</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">True</property>
        <property name="fill">True</property>
        <property name="position">2</property>
      </packing>
    </child>
    <child>
      <object class="GtkLabel" id="labelpythontitle">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">Nothing selected.</property>
        <property name="track_visited_links">False</property>
        <attributes>
          <attribute name="foreground" value="#000000000000"/>
          <attribute name="background" value="#8a8ae2e23434"/>
        </attributes>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">True</property>
        <property name="position">3</property>
      </packing>
    </child>
    <child>
      <object class="GtkBox" id="boxFooter">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="spacing">3</property>
        <child>
          <object class="GtkButton" id="buttonRun">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="tooltip_text" translatable="yes">Run...</property>
            <property name="halign">center</property>
            <property name="valign">center</property>
            <signal name="clicked" handler="on_buttonRun_clicked" swapped="no"/>
            <child>
              <object class="GtkImage" id="image2">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="stock">gtk-execute</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="labelVersion">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="label" translatable="yes">Place for Version</property>
            <property name="track_visited_links">False</property>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonAbout">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="tooltip_text" translatable="yes">About...</property>
            <property name="halign">center</property>
            <property name="valign">center</property>
            <property name="yalign">0.49000000953674316</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonAbout_clicked" swapped="no"/>
            <child>
              <object class="GtkImage" id="image4">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="stock">gtk-about</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonForTests">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="tooltip_text" translatable="yes">Button to run tests</property>
            <property name="halign">center</property>
            <property name="valign">center</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonForTests_clicked" swapped="no"/>
            <child>
              <object class="GtkImage" id="image5">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="stock">gtk-edit</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonExit">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="tooltip_text" translatable="yes">Exit</property>
            <property name="halign">end</property>
            <property name="valign">center</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonExit_clicked" swapped="no"/>
            <child>
              <object class="GtkImage" id="image3">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="stock">gtk-quit</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="pack_type">end</property>
            <property name="position">4</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">True</property>
        <property name="position">4</property>
      </packing>
    </child>
  </object>
</interface>
'''

class UserSettings:
    '''User's GUI preferences.

    '''
    def __init__(self):
        self.user_config_path = ''
        self.Width = 600
        self.Height = 400
        self.Maximized = False
        self.vpaned_position = 160
        self.vpaned_position_m = 160
        self.last_LO_path = '.'
        self.last_python_path = '.'
        self.last_version = ''

class OCPUserConfigFile():
    def __init__(self, appdomain):
        '''Application config parser.

        '''
        userdir = os.getenv('USERPROFILE') or os.getenv('HOME')
        OCPconfigdir = os.path.join(userdir, '.config', 'OCP')
        self.thefile = os.path.join(OCPconfigdir, APPDOMAIN)
        self.unwriteable = False
        if os.path.exists(OCPconfigdir) and os.path.isdir(OCPconfigdir):
            pass
        else:
            try:
                os.makedirs(OCPconfigdir,exist_ok=True)
            except:
                self.unwriteable = True

        self.CP = configparser.ConfigParser(empty_lines_in_values=False)
        self.GUI = UserSettings()
        if not os.path.exists(self.thefile):
            try:
                with open(self.thefile, mode = 'at+') as f:
                    pass
            except:
                self.unwriteable = True
                print(_('WARNING! Configuration file unwriteable!'))
        if not self.unwriteable:
            with open(self.thefile, mode = 'rt') as f:
                self.CP.read_file(f)

    def sections(self):
        '''Return the available sections.

        '''
        return self.CP.sections()

    def options(self, wichsection):
        '''Return the available options of the specified section.

        '''
        return self.CP.options(wichsection)

    def deleteconfigvalue(self, wichsection, wichoption):
        '''Delete a value.

        '''
        try:
            existed = self.CP.remove_option(wichsection, wichoption)
        except configparser.NoSectionError:
            return False
        except configparser.NoOptionError:
            return False
        except:#oops...
            print(_("Exception: "), str(sys.exc_info()) )
            return False
        if not existed:
            return False #no need to delete it
        return True

    def readconfigvalue(self, wichsection, wichoption, default):
        '''Read a value.

        Return the default if no such section or option exists.
        '''
        try:
            return self.CP.get(wichsection,wichoption)
        except configparser.NoSectionError:
            return default
        except configparser.NoOptionError:
            return default
        except:#oops...
            print(_("Exception: "), str(sys.exc_info()) )
            return default

    def writeconfigvalue(self, whichsection, whichoption, whichvalue):
        '''Change a value.

        '''
        if not self.CP.has_section(whichsection):
            self.CP.add_section(whichsection)
        self.CP.set(whichsection, whichoption, str(whichvalue))

    def write(self):
        '''Writes configuration changes.

        '''
        if self.unwriteable:
            print(_('WARNING! Configuration file unwriteable!'))
            return
        #print(self.readconfigvalue('GUI','width',0))
        try:
            with open(self.thefile, mode='wt',encoding='utf-8') as f:
                self.CP.write(f)
        except Exception as e:
            print(_('WARNING! Configuration not saved!') , e)

class AboutBox:
    '''Custom AboutBox.

    '''
    def __init__(self, theApp):
        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_program_name( _(theApp.appName) )
        aboutdialog.set_version(theApp.appName  + 'v.' + theApp.appVersion + ' ')
        with open(os.path.join(theApp.working_dir, '_data', 'AUTHORS'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_authors(f.readlines())
        with open(os.path.join(theApp.working_dir, '_data', 'COPYRIGHT'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_copyright(f.read())
        with open(os.path.join(theApp.working_dir, '_data', 'COMMENTS'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_comments(f.read())
        with open(os.path.join(theApp.working_dir, '_data', 'TRANSLATORS'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_translator_credits(f.read())
        aboutdialog.set_transient_for(theApp)
        aboutdialog.set_logo(theApp.appIcon)
        aboutdialog.run()
        aboutdialog.destroy()

class LOFile:
    '''Manipulate the selected LibreOffice file.

    '''
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.zipread:
            self.zipread.close()

    def __init__(self, afile):
        self.isLOfilelike = True
        self.existedinmanifest = []
        self.fullpath = afile
        self.thepath, self.thefile = os.path.split(afile)
        #self.tmpdir = tempfile.TemporaryDirectory()
        try:
            self.zipread = zipfile.ZipFile(self.fullpath, 'r')
        except zipfile.BadZipFile:
            self.isLOfilelike = False
        if  self.isLOfilelike :
            self.allfiles = self.zipread.namelist()
            #print(self.allfiles)
            if 'META-INF/manifest.xml' in self.allfiles:
                with self.zipread.open('META-INF/manifest.xml') as f:
                    self.xml = f.read()
                self.manifest = ManifestWithPythonInLo(self.xml)
                self.existedinmanifest = self.manifest.dir_files()
            else:
                self.isLOfilelike = False

    def _backup(self):
        '''Backs up the selected LibreOffice file.

        Internal function. File must be closed.

        '''

        backupdir = os.path.join(self.thepath, 'backup')
        backupfullpath = os.path.join(backupdir, self.thefile)

        if not os.path.exists(backupdir):
            try:

                os.mkdir(backupdir)
            except:
                return None
        #print(self.fullpath, backupdir)
        if not os.path.isdir(backupdir):
            return None
        if os.path.exists(backupfullpath):
            print('exists')
            return None
        try:
            os.rename(self.fullpath, backupfullpath)
        except:
            return None
        return backupfullpath

    def _recreate_manifest(self, list_to_remove, list_to_append_update):
        for x in list_to_remove:
            self.manifest.remove(x)
        alist = self.manifest.dir_files()[:]
        for x in list_to_append_update:
            self.manifest.append(os.path.basename(x))
        self.manifest.clear()
        return str(self.manifest)
        #print(str(self.manifest))

    def recreate_LO_Document(self, list_to_remove, list_to_append_update):
        manifest_fullnames_to_remove = ['Scripts/python/' + x for x in list_to_remove]
        manifest_fullnames_to_add_update = ['Scripts/python/' + os.path.basename(x) for x in list_to_append_update]
        oldfilelist = self.manifest.dir_files()[:]
        newmanifest = self._recreate_manifest(list_to_remove, list_to_append_update)
        #TODO reopen if any error occures.
        if self.zipread:
            self.zipread.close()
        #TODO restore if any error occures.
        backedzip = self._backup()
        if not backedzip:
            print('not backed')
            return False
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpzip = os.path.join(tmpdir, self.thefile)
            print('created tmp dir')
            with zipfile.ZipFile(backedzip, 'r') as zipread:
                print('opened backedzip', backedzip)
                with zipfile.ZipFile(tmpzip, 'w') as zipwrite:
                    print('opened tmpzip', tmpzip)
                    for item in zipread.infolist():
                        print(item.filename)
                        if item.filename == 'META-INF/manifest.xml' or item.filename in manifest_fullnames_to_remove or item.filename in manifest_fullnames_to_add_update:
                            print('not copied----------------', item.filename)
                        else:
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item, data)
                    zipwrite.writestr('META-INF/manifest.xml', newmanifest.encode())
                    for data, arcname in zip(list_to_append_update, manifest_fullnames_to_add_update):
                        zipwrite.write(data, arcname)
            shutil.copyfile(tmpzip, self.fullpath)
            return True
        #TODO: restore and reopen if any error occures.
        #Or at least, clear everything.
        return False

    def get_source(self, pyfile):
        '''Get the text of the included python file.

        '''
        thetext = ''
        with self.zipread.open('Scripts/python/' + pyfile) as f:
            thetext = f.read()
        return thetext

    def update(self):
        #TODO:
        pass

class ManifestWithPythonInLo():
    def __init__(self, LOmanifestxml):
        self.soup = BeautifulSoup(LOmanifestxml,'xml')

    def __str__(self):
        return self.soup.prettify()

    def a_script(self, atag):
        '''Return the name of the python file if any.

        '''
        if 'manifest:full-path' in atag.attrs:
            theattr = atag['manifest:full-path']
            if theattr.startswith('Scripts/python/'):
                return os.path.basename(theattr)
        return None

    def dir_files(self):
        '''Return a list with the names of the python files.

        '''
        python_files_list = []
        for atag in self.soup.contents[0].find_all():
            b = self.a_script(atag)
            if b and len(b):
                python_files_list.append(b)
        return python_files_list

    def remove(self, pyfilename):
        thetag = self.soup.find(attrs={"manifest:full-path": "Scripts/python/" + pyfilename})
        if thetag:
            thetag.extract()
            self.soup = BeautifulSoup(self.soup.prettify(),'xml')

    def append(self, pyfilename):
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
        if len(self.dir_files()):
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

class MainApp(Gtk.Window):
    def __init__( self, working_dir, parent = None):
        self.xcounter = 0
        self.working_dir = working_dir
        self.appVersion = VERSION
        self.showtestbutton = False
        #self.configpath =
        #if we have a file named debug, get version from the directory name
        #else use the one already provided (in the begging of the file as VERSION)
        if os.path.exists(os.path.join(working_dir, 'debug')):
            forversion = os.path.basename(self.working_dir)
            if len(forversion) > 2 and (forversion.count('.') == 3):
                self.appVersion = forversion[2:]
            self.showtestbutton = True

        locale.bindtextdomain(APPDOMAIN, os.path.join(self.working_dir, '_locale'))
        locale.textdomain(APPDOMAIN)

        self.appName = APPNAME

        self.we_can_exit_now = False
        self.return_parameter = None

        self.init_config()

        self.addupdatelist = []

        #self.mybuilder = Gtk.Builder().new_from_file(os.path.join(self.working_dir, 'main.glade'))
        self.mybuilder = Gtk.Builder()
        self.mybuilder.add_from_string(thegladestr)
        Gtk.Window.__init__(self, name='windowMain')
        self.add(self.mybuilder.get_object('boxMain'))
        self.mybuilder.connect_signals(self)
        self.appIcon = GdkPixbuf.Pixbuf.new_from_file(os.path.join(self.working_dir, '_icons', "logo.png"))
        self.set_icon(self.appIcon)
        self.connect("delete-event", self.on_mainWindow_delete_event)
        self.connect("window-state-event", self.on_windowMain_window_state_event)
        self.connect("key-release-event", self.on_windowMain_key_release_event)
        self.connect("size-allocate", self.on_windowMain_size_allocate)
        self.theObject('vpaned').connect("size-allocate", self.on_vpaned_size_allocate)

        self.theObject('labelVersion').set_label(_(APPNAME) + ' v.' + self.appVersion)

        self.sourceviewer = self.theObject('textviewSource')

        set_object_style(self.sourceviewer, 'background-color', 'black')
        set_object_style(self.sourceviewer, 'color', 'green')

        self.theObject('buttonForTests').set_visible(self.showtestbutton)
        self.theObject('buttonForTests').set_no_show_all(not self.showtestbutton)

        self.theObject('listboxexisting').set_name('listboxexisting')
        self.theObject('listboxremove').set_name('listboxremove')
        self.theObject('listboxaddreplace').set_name('listboxaddreplace')

        self.lofile = None
        self.set_default_size (int(self.CONF.readconfigvalue('GUI', 'width', self.CONF.GUI.Width)),
                    int(self.CONF.readconfigvalue('GUI', 'height', self.CONF.GUI.Height)))
        if self.CONF.readconfigvalue('GUI','maximized','False')  == 'True':
            self.maximize()
            self.theObject('vpaned').set_position(int(self.CONF.readconfigvalue('GUI', 'vpaned_position_m', self.CONF.GUI.vpaned_position_m)))
        else:
            self.theObject('vpaned').set_position(int(self.CONF.readconfigvalue('GUI', 'vpaned_position', self.CONF.GUI.vpaned_position)))

    def init_config(self):
        self.CONF = OCPUserConfigFile(APPDOMAIN)
        self.CONF.GUI.last_LO_path = self.CONF.readconfigvalue('GUI', 'last_lo_path', '.')
        self.CONF.GUI.last_python_path = self.CONF.readconfigvalue('GUI', 'last_python_path', '.')

    def save_settings(self):
        self.CONF.write()

    def run(self):
        #now we can show the window
        self.show_all()
        #loop eternaly
        while True:
            #if we want to exit
            if self.we_can_exit_now:
                #print('we_can_exit_now')
                #break the loop
                break
            #else...
            #give others a change...
            while Gtk.events_pending():
                Gtk.main_iteration()
        #we can now return to calling procedure
        #can return any variable we want
        return self.return_parameter

    def theObject(self, a_builder_id):
        return self.mybuilder.get_object(a_builder_id)

    def has_changes(self):
        return (len(self.theObject('listboxremove').get_children()) + len(self.theObject('listboxaddreplace').get_children()) != 0)

    def on_entryLOfile_changed(self, widget, *args):
        tempvar = widget.get_text()
        self.clear_box(self.theObject('listboxexisting'))
        self.clear_box(self.theObject('listboxremove'))
        self.clear_box(self.theObject('listboxaddreplace'))
        widget.set_tooltip_text('')
        if os.path.exists(tempvar):
            self.lofile = LOFile(tempvar)
            if self.lofile.isLOfilelike:
                #TODO clear all and refresh
                self.show_existing()
            else:
                widget.set_tooltip_text(_('Damaged or not a LibreOffice file'))
        self.theObject('buttonAddReplace').set_sensitive(self.lofile.isLOfilelike)

    def on_mainWindow_delete_event(self, *args):
        self.save_settings()
        if self.has_changes() and (not self.ok_to_clear_all()):
            self.show_all()
            return True
        self.we_can_exit_now = True

    def on_vpaned_size_allocate(self, *args):
        position = self.theObject('vpaned').get_position()
        if self.is_maximized():
            self.CONF.GUI.vpaned_position_m = position
            self.CONF.writeconfigvalue('GUI', 'vpaned_position_M', self.CONF.GUI.vpaned_position_m)
        else:
            self.CONF.GUI.vpaned_position = position
            self.CONF.writeconfigvalue('GUI', 'vpaned_position', self.CONF.GUI.vpaned_position)

    def on_windowMain_size_allocate(self, *args):
        if not self.CONF.GUI.Maximized:
            self.CONF.GUI.Width, self.CONF.GUI.Height = self.get_size()
            self.CONF.writeconfigvalue('GUI', 'width', self.CONF.GUI.Width)
            self.CONF.writeconfigvalue('GUI', 'height', self.CONF.GUI.Height)

    def on_windowMain_window_state_event(self, *args):
        if (int(args[1].new_window_state) & Gdk.WindowState.ICONIFIED) != Gdk.WindowState.ICONIFIED:
            if (int(args[1].new_window_state) & Gdk.WindowState.MAXIMIZED) == Gdk.WindowState.MAXIMIZED:
                self.CONF.GUI.Maximized = True
                self.CONF.writeconfigvalue('GUI', 'maximized', self.CONF.GUI.Maximized)
            else:
                self.CONF.GUI.Maximized = False
                self.CONF.GUI.Width, self.CONF.GUI.Height = self.get_size()
                self.CONF.writeconfigvalue('GUI', 'width', self.CONF.GUI.Width)
                self.CONF.writeconfigvalue('GUI', 'height', self.CONF.GUI.Height)
                self.CONF.writeconfigvalue('GUI', 'maximized', self.CONF.GUI.Maximized)

    def on_windowMain_key_release_event(self, w, e):
        txt = Gdk.keyval_name(e.keyval)
        if type(txt) == type(None):
            # Make sure we don't trigger on unplugging the A/C charger etc
            return
        txt = txt.replace('KP_', '')
        #print(txt)
        #print('-----')
        #if e.state & Gdk.ModifierType.CONTROL_MASK:
            #print(txt, 'with control')
            #print('--C---')
        if txt == 'F4':
            #self.on_bfind_clicked(self, w, e)
            print(w,e)

    def on_buttonExit_clicked(self, widget, *args):
        #self.on_windowMain_destroy(*args)
        #if self.has_changes() and (not self.ok_to_clear_all()): return
        #self.set_transient_for()
        #self.set_modal(False)
        #self.hide()
        self.on_mainWindow_delete_event()

    def on_buttonAbout_clicked(self, widget, *args):
        app = AboutBox(self)

    def on_buttonLofile_clicked(self, widget, *args):
        if self.has_changes() and (not self.ok_to_clear_all()): return
        tempvar = select_file(self, self.theObject('entryLOfile'), 'LO', self.CONF.GUI.last_LO_path)
        if tempvar:
            self.theObject('entryLOfile').set_text(tempvar)
            #self.lofile = LOFile(tempvar)
            self.CONF.GUI.last_LO_path = os.path.dirname(tempvar)
            self.CONF.writeconfigvalue('GUI', 'last_lo_path', self.CONF.GUI.last_LO_path)
            #self.show_existing()

    def on_buttonAddReplace_clicked(self, widget, *args):
        tempvar = select_file(self, None, 'python', self.CONF.GUI.last_python_path)
        if tempvar:
            self.CONF.GUI.last_python_path = os.path.dirname(tempvar)
            self.CONF.writeconfigvalue('GUI', 'last_python_path', self.CONF.GUI.last_python_path)
            head, tail = os.path.split(tempvar)
            ok = True
            if self.is_in_the_list(self.theObject('listboxaddreplace'), tail):
                MessageInfo(self, _('Same name'),
                    _('A file with the same name already is listed:\n   «{0}»\nPlease first remove it from the list.').format(tail))
                return
            elif self.is_in_the_list(self.theObject('listboxexisting'), tail):
                ok = YesNo(self, _('Same name'),
                    _('A file with the same name already exists as script:\n   «{0}»\nDo you want to update it with this version?').format(tail))
                if not ok:
                    return
            self.add_a_row(self.theObject('listboxaddreplace'), tail, head)

    def on_buttonRun_clicked(self, widget, *args):
        if not self.has_changes():
            MessageInfo(self, _('Nothing to do'),
                    _('You have not made any changes. Nothing to do!'))
            return False
        self.files_to_remove = []
        allchildren = self.theObject('listboxremove').get_children()
        for achild in allchildren[:]:
            self.files_to_remove.append(achild.get_children()[0].get_children()[0].get_text())
        self.files_to_append = []
        allchildren = self.theObject('listboxaddreplace').get_children()
        for achild in allchildren[:]:
            widget = achild.get_children()[0].get_children()[0]
            name = widget.get_text()
            path = widget.get_tooltip_text().split('\n')[0]
            self.files_to_append.append(os.path.join(path, name))
        textformessage = _('You selected to:\n')
        if len(self.files_to_remove):
            textformessage += _(' Remove the files:\n')
            textformessage += "\t\n".join(self.files_to_remove) + "\n"
        if len(self.files_to_append):
            textformessage += _(' Add or update the files:\n')
            textformessage += "\t\n".join(self.files_to_append) + "\n"
        textformessage += _('Are you sure?')
        ok = YesNo(self, _('Commit changes'), textformessage)
        if not ok:
            return False
        ok = self.lofile.recreate_LO_Document(self.files_to_remove, self.files_to_append)
        print(ok)
        self.on_entryLOfile_changed(self.theObject('entryLOfile'))
        #self.lofile.recreate_manifest(self.files_to_remove, self.files_to_append)



    def on_buttonForTests_clicked(self, widget, *args):
        self.run_something()

    def run_something(self):
        self.show_source('pilo.py', '/home/ilias/Λήψεις/Προγραμματισμός1/Python/embedpythoninLO/v.0.0.5')
        #pass

    def show_existing(self):
        thelistbox = self.theObject('listboxexisting')
        self.clear_box(thelistbox)
        howmany = len(self.lofile.existedinmanifest)
        for x in range(howmany):
            self.add_a_row(thelistbox, self.lofile.existedinmanifest[x], 'Scripts/python/')
        #self.show_all()

    def clear_box(self, thelistbox):
        allchildren = thelistbox.get_children()
        for achild in allchildren[:]:
            achild.destroy()

    def add_a_row(self, thelistbox, thelabel, thepath):
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        label = Gtk.Label(thelabel)
        addremovetext = _('Right click to remove from file.') if self.theObject('listboxexisting') == thelistbox else _('Right click to remove from list.')
        label.set_tooltip_text(thepath + '\n' + addremovetext)
        label.set_has_window(True)
        label.connect("button-release-event", self.on_row__button_release_event, thelabel, thepath)
        hbox1.pack_start(label, False, False, 0)
        thelistbox.add(hbox1)
        self.show_all()

    def remove_a_row(self, widget):
        widget.get_parent().get_parent().destroy()
        self.show_all()

    def is_in_the_list(self, thelistbox, thefile):
        allchildren = thelistbox.get_children()
        for achild in allchildren[:]:
            if achild.get_children()[0].get_children()[0].get_label() == thefile:
                return True
        return False

    def ask_remove(self, widget):
        return YesNo(self, _('Remove from file'), _('Are you sure?').format(widget.get_label()))

    def on_row__button_release_event(self, widget, *args):
        if args[0].button == 3:#right click
            if (self.theObject('listboxexisting') == widget.get_parent().get_parent().get_parent()):
                thelabel = widget.get_label()
                exists = self.is_in_the_list(self.theObject('listboxremove'), thelabel)
                if not exists:
                    self.add_a_row(self.theObject('listboxremove'), thelabel, 'Scripts/python/')
                else:
                    NotYet(self,_(APPNAME))
                    #show_info(self,_('The file is already in remove list.'))
            elif (self.theObject('listboxremove') == widget.get_parent().get_parent().get_parent()):
                self.remove_a_row(widget)
            elif (self.theObject('listboxaddreplace') == widget.get_parent().get_parent().get_parent()):
                self.remove_a_row(widget)
            return False
        self.show_source(widget)

    def show_source(self, widget):
        if (self.theObject('listboxexisting') == widget.get_parent().get_parent().get_parent()) or \
                    (self.theObject('listboxremove') == widget.get_parent().get_parent().get_parent()):
            title = widget.get_text()
            self.theObject('textviewSource').props.buffer.set_text(self.lofile.get_source(title).decode())
            self.theObject('labelpythontitle').set_label( title + "(" +_('Icluded:') + ")")
            return
        if (self.theObject('listboxaddreplace') == widget.get_parent().get_parent().get_parent()):
            name = widget.get_text()
            path = widget.get_tooltip_text().split('\n')[0]
            with open(os.path.join(path, name)) as f:
                thetext = f.read()
            self.theObject('textviewSource').props.buffer.set_text(thetext)
            self.theObject('labelpythontitle').set_label(name + _(' (in: ') + path + ")")

    def ok_to_clear_all(self):
        return YesNo(self, _('Drop changes'),
                    _('You have made changes:\nThis will drop all changes.\nProceed?'))

def set_object_style(theobject, var, val):
    css = '''*{''' + var + ''':''' + val + ''';}'''
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css.encode('utf-8'))
    context = theobject.get_style_context()
    context.add_provider(style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def select_file(parentwindow, *args):
    dialog = Gtk.FileChooserDialog(_("Please choose a file ({0})").format(args[1]), parentwindow,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    dialog.set_current_folder(args[2])
    if args[1] == 'LO':
        add_LO_filters(dialog)
    else:
        add_py_filters(dialog)

    response = dialog.run()
    filename = dialog.get_filename()
    dialog.destroy()

    if response == Gtk.ResponseType.OK:
        return filename
    else:
        return None

def YesNo(forwindow, thetitle, thequestion, windowtitle = None):
    dialog = Gtk.MessageDialog(forwindow, 0, Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.YES_NO, thetitle)
    dialog.format_secondary_text(thequestion)
    if windowtitle:
        dialog.set_title(windowtitle)
    else:
        dialog.set_title(forwindow.appName)
    dialog.set_transient_for(forwindow)
    response = dialog.run()
    dialog.destroy()
    return (response == Gtk.ResponseType.YES)

def MessageInfo(forwindow, thetitle, thetext, windowtitle = None):
    dialog = Gtk.MessageDialog(forwindow, 0, Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK, _(thetitle))
    dialog.format_secondary_text(_(thetext))
    if windowtitle:
        dialog.set_title(windowtitle)
    else:
        dialog.set_title(forwindow.appName)
    dialog.set_transient_for(forwindow)
    dialog.run()
    dialog.destroy()

def NotYet(appwindow, appname):
    dialog = Gtk.MessageDialog(appwindow, 0, Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK, _("NOT YET!"))
    dialog.format_secondary_text(_("Not yet implemented!"))
    dialog.set_title(appname)
    #dialog.set_transient_for(appwindow)
    dialog.run()
    dialog.destroy()

def add_LO_filters(dialog):
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

    filter_any = Gtk.FileFilter()
    filter_any.set_name(_("All files"))
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

def add_py_filters(dialog):
    filter_py = Gtk.FileFilter()
    filter_py.set_name(_("Python files"))
    filter_py.add_mime_type("text/x-python")
    dialog.add_filter(filter_py)

    filter_any = Gtk.FileFilter()
    filter_any.set_name(_("All files"))
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

def main2():
    with open('testmanifest.xml') as fp:
        LOmanifestxml = fp.read()
    b = ManifestWithPythonInLo(LOmanifestxml)
    b.append('myother.py')
    print(str(b))
    b.remove('updatedbtest.py')
    print(str(b))
    b.remove('myother.py')
    b.clear()
    print(str(b))

def main(realfile_dir):
    #a = LOFile(os.path.join(realfile_dir, 'kmop.odb'))
    with LOFile(os.path.join(realfile_dir, 'kmop.odb')) as a:
    #print(a.python_files())
        for x in a.existedinmanifest:
            #print(a.show_file(x))
            print(x)

if __name__ == "__main__":
    realfile = os.path.realpath(__file__)
    working_dir = os.path.dirname(os.path.abspath(realfile))
    #main(realfile_dir)
    b = MainApp(working_dir)
    c = b.run()
    print(c)
