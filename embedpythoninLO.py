#!/usr/bin/python3
AUTHOR = 'Xoristzatziki στο github.com'
LICENCE = 'CC-BY-SA'
VERSION = '0.1.1'
APPNAME = 'EMBED PYTHON IN LO DOCUMENT'
APPFILENAME = 'embedpythoninLO'
COMMENTS = 'Πρόγραμμα ενσωμάτωσης ενός αρχείου python σε ένα αρχείο LibreOffice\rώστε να μπορεί να χρησιμοποιηθεί ως user script.'
BACKUPCOPIES = 10

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os, sys

import shutil
import tempfile
import zipfile


myglade = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.16.1 -->
<interface>
  <requires lib="gtk+" version="3.6"/>
  <object class="GtkWindow" id="window1">
    <property name="can_focus">False</property>
    <child>
      <object class="GtkGrid" id="grid1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="halign">baseline</property>
        <property name="valign">baseline</property>
        <property name="margin_left">5</property>
        <property name="margin_right">5</property>
        <property name="margin_top">5</property>
        <property name="margin_bottom">5</property>
        <property name="hexpand">True</property>
        <property name="vexpand">True</property>
        <property name="resize_mode">immediate</property>
        <property name="row_spacing">5</property>
        <property name="column_spacing">5</property>
        <child>
          <object class="GtkEntry" id="entry1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="tooltip_text" translatable="yes">Γράψτε την πλήρη διαδρομή για το αρχείο LibreOffice ή επιλέξτε το κάνοντας κλικ στο κουμπί δεξιά.</property>
            <property name="valign">center</property>
            <property name="hexpand">True</property>
            <property name="caps_lock_warning">False</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="top_attach">0</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonLO">
            <property name="label" translatable="yes">...</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="tooltip_text" translatable="yes">Επιλέξτε ένα αρχείο LibreOffice</property>
            <property name="halign">start</property>
            <property name="valign">center</property>
            <property name="hexpand">False</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonLO_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="left_attach">2</property>
            <property name="top_attach">0</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="halign">end</property>
            <property name="valign">center</property>
            <property name="label" translatable="yes">Αρχείο LibreOffice</property>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">0</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="halign">end</property>
            <property name="valign">center</property>
            <property name="label" translatable="yes">Αρχείο Python</property>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">1</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkEntry" id="entry2">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="tooltip_text" translatable="yes">Γράψτε την πλήρη διαδρομή για το αρχείο python ή επιλέξτε το κάνοντας κλικ στο κουμπί δεξιά.</property>
            <property name="valign">center</property>
            <property name="hexpand">True</property>
            <property name="caps_lock_warning">False</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="top_attach">1</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonpy">
            <property name="label" translatable="yes">...</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="tooltip_text" translatable="yes">Επιλέξτε ένα αρχείο python</property>
            <property name="halign">start</property>
            <property name="valign">center</property>
            <property name="hexpand">False</property>
            <signal name="clicked" handler="on_buttonpy_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="left_attach">2</property>
            <property name="top_attach">1</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonrun">
            <property name="label">gtk-execute</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="halign">center</property>
            <property name="use_stock">True</property>
            <property name="image_position">right</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonrun_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="left_attach">2</property>
            <property name="top_attach">3</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonabout">
            <property name="label">gtk-about</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="halign">start</property>
            <property name="valign">baseline</property>
            <property name="use_stock">True</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonabout_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">3</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="labelversion">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="hexpand">True</property>
            <property name="vexpand">False</property>
            <property name="label" translatable="yes">v.</property>
            <property name="selectable">True</property>
            <property name="single_line_mode">True</property>
            <property name="track_visited_links">False</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="top_attach">3</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="buttonexit">
            <property name="label">gtk-quit</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="halign">center</property>
            <property name="valign">center</property>
            <property name="use_stock">True</property>
            <property name="always_show_image">True</property>
            <signal name="clicked" handler="on_buttonexit_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="left_attach">3</property>
            <property name="top_attach">3</property>
            <property name="width">1</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label3">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="valign">end</property>
            <property name="hexpand">True</property>
            <property name="vexpand">True</property>
            <property name="label" translatable="yes">label</property>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">2</property>
            <property name="width">4</property>
            <property name="height">1</property>
          </packing>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
    </child>
  </object>
</interface>
'''
class EmbedScriptGUI(Gtk.Window):
    def __init__( self, realfile_dir, parent = None):
        Gtk.Window.__init__(self, name='windowMain')
        self.working_dir = realfile_dir
        if parent != None:
            self.set_transient_for(parent)
            self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)#_ON_PARENT
            self.set_modal(True)

        self.mybuilder = Gtk.Builder()
        self.mybuilder.add_objects_from_string(myglade, ('grid1',))
        self.add(self.mybuilder.get_object('grid1'))

        self.mybuilder.connect_signals(self)
        self.connect("hide", self.hideme)

        self.mybuilder.get_object('labelversion').set_label(APPFILENAME + ' v.' + VERSION)
        self.mybuilder.get_object('label3').set_label(COMMENTS)

        self.resize(500,150)
        self.set_title (APPNAME)
        self.LASTPATH = self.working_dir

        self.wecanexitnow = False
        self.returnparameter = None

    def run(self):
        #now we can show the window
        self.show_all()
        #loop eternaly
        while True:
            #if we want to exit
            if self.wecanexitnow:
                #print('wecanexitnow')
                #break the loop
                break
            #else...
            #give others a change...
            while Gtk.events_pending():
                Gtk.main_iteration()
        #we can now return to calling procedure
        #can return any variable we want
        #or we can check the widgets and/or variables
        #from inside calling procedure
        #print('from abstract',self.returnparameter)
        return self.returnparameter

    def hideme(self, *args):
        #self.savemysettings()
        #print('hide triggered')
        self.wecanexitnow = True

    def on_buttonabout_clicked(self, widget,*args):
        #from .aboutbox import AboutBox #as AboutBox
        #app = AboutBox(self)
        #pass
        AboutBox(self)

    def on_buttonrun_clicked(self, widget,*args):
        #pass
        LOfpath = self.mybuilder.get_object('entry1').get_text()
        pyfpath = self.mybuilder.get_object('entry2').get_text()
        if not os.path.exists(LOfpath):
            txt1 = 'Δεν υπάρχει αρχείο LibreOffice με το όνομα: \r%s\r' % LOfpath
            self.show_error(txt1)
            return
        if not os.path.exists(pyfpath):
            txt1 = 'Δεν υπάρχει αρχείο python με το όνομα: \r%s\r' % pyfpath
            self.show_error(txt1)
            return
        if not is_LO_file(LOfpath):
            txt1 = 'Πρόβλημα'
            txt2 = 'Το αρχείο:\r\t%s\r δεν φαίνεται να είναι έγγραφο του LibreOffice.\r' % LOfpath
            txt2 += 'Να συνεχίσω;'
            response = self.ask_continue(txt1,txt2)
            if not response:
                return
        if not is_python_file(pyfpath):
            txt1 = 'Πρόβλημα'
            txt2 = 'Το αρχείο:\r\t%s\r δεν φαίνεται να είναι αρχείο python.' % LOfpath
            txt2 += 'Να συνεχίσω;'
            response = self.ask_continue(txt1,txt2)
            if not response:
                return
        pyftail = os.path.split(pyfpath)[1]
        if file_existed(pyftail, LOfpath):
            txt1 = 'Το αρχείο υπάρχει!'
            txt2 = 'Το αρχείο:\r\t%s\r περιέχει ήδη ένα αρχείο python με το ίδιο όνομα:\r\t%s\r' % (LOfpath,pyftail)
            txt2 += 'Να συνεχίσω; (το αρχείο python θα αντικατασταθεί)'
            response = self.ask_continue(txt1,txt2)
            if not response:
                return
        txt1 = 'Σημαντική ενημέρωση!'
        txt2 = 'Το πρόγραμμα και ο προγραμματιστής δεν φέρουν καμία ευθύνη για όποια προβλήματα παρουσιαστούν.'
        txt2 += '\rΚρατήστε αντίγραφα ασφαλείας!'
        txt2 += '\rΝα συνεχίσω;'
        response = self.ask_continue(txt1,txt2)
        if not response:
            return
        response = insertpythonfile(pyfpath, LOfpath)
        if response > 0:
            label1 = 'Επιτυχής ενσωμάτωση'
            label2 = 'Το αρχικό αρχείο:\r\t%s\r μετονομάστηκε σε:\r\t%s\r' % (LOfpath, LOfpath + "." + str(response))
            label2 += 'Το αρχείο του Libreoffice:\r\t%s\r περιέχει πλέον το αρχείο python:\r\t%s\r ενσωματωμένο.' % (LOfpath, pyfpath)
            self.show_info(label1, label2)
        elif response == -1:
            label =  'Υπάρχουν ήδη πολλά αντίγραφα στον ίδιο φάκελο!!!\r'
            label +=  'Παρακαλώ διαγράψτε ή μετονομάστε ή μετακινήστε κάποια αυτά\r(π.χ. το %s)\rκαι επαναλάβετε την προσπάθεια.' % (LOfpath + "." + str(BACKUPCOPIES),)
            self.show_error(label)
        else:
            label =  'Παρουσιάστηκε κάποιο πρόβλημα στην εισαγωγή του αρχείου python!!!'
            self.show_error(label)

    def on_buttonLO_clicked(self, widget,*args):
        #pass
        dialog = Gtk.FileChooserDialog("Παρακαλώ επιλέξτε ένα αρχείο LibreOffice", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        add_LO_filters(dialog)
        dialog.set_current_folder(self.LASTPATH)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.mybuilder.get_object('entry1').set_text(dialog.get_filename())
            self.LASTPATH = dialog.get_current_folder()
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def on_buttonpy_clicked(self, widget,*args):
        #pass
        dialog = Gtk.FileChooserDialog("Παρακαλώ επιλέξτε ένα αρχείο python", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        add_py_filters(dialog)
        dialog.set_current_folder(self.LASTPATH)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.mybuilder.get_object('entry2').set_text(dialog.get_filename())
            self.LASTPATH = dialog.get_current_folder()
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def on_buttonexit_clicked(self, widget,*args):
        self.set_transient_for()
        self.set_modal(False)
        self.hide()

    def show_error(self,label2):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, "ΣΦΑΛΜΑ!")
        dialog.format_secondary_text(label2)
        dialog.run()
        dialog.destroy()

    def show_info(self, label1, label2):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, label1)
        dialog.format_secondary_text(label2)
        dialog.run()
        dialog.destroy()

    def ask_continue(self, label1, label2):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, label1)
        dialog.format_secondary_text(label2)
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.YES

class AboutBox:
    def __init__(self, appwindow):
        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_program_name(APPNAME)
        #print(appwindow.App.appname)
        aboutdialog.set_version('v.' + VERSION + ' ')
        #TODO aboutdialog.set_license_type(Gtk.GTK_LICENSE_LGPL_3_0)
        #with  open(os.path.join(appwindow.App.workingdir, '_data', 'AUTHORS'), mode='rt', encoding='utf-8') as f:
            #aboutdialog.set_authors(f.readlines())
        aboutdialog.set_authors((AUTHOR,))
        aboutdialog.set_comments(COMMENTS)
        aboutdialog.set_license(LICENCE)
        aboutdialog.set_transient_for(appwindow)
        #aboutdialog.set_logo(appwindow.App.icon)
        aboutdialog.run()
        aboutdialog.destroy()

def file_existed(pyftail, LOfpath):
    pyfinxml = "Scripts/python/" + pyftail
    #print("checking files: %s - %s" % (pyftail, LOfpath))
    with zipfile.ZipFile(LOfpath, 'r') as zipread:
        for item in zipread.infolist():
            #print(item.filename,end=", ")
            if item.filename == pyfinxml:
                return True
    #print("checked: %s - %s" % (pyftail, LOfpath))
    return False

def is_python_file(pyfpath):
    if os.path.exists(pyfpath):
        if pyfpath.endswith('.py'):
            return True
    return False

def is_LO_file(LOfpath):
    if os.path.exists(LOfpath):
        with zipfile.ZipFile(LOfpath, 'r') as zipread:
            for item in zipread.infolist():
                if item.filename == 'META-INF/manifest.xml':
                    return True
    return False

def nextbackupnum(LOfpath):
    #up to 10 copies!!!
    for x in range(BACKUPCOPIES):
        if not os.path.exists(LOfpath + "." + str(x+1)):
            return x+1
    return -1

def add_LO_filters(dialog):
    filter_LO = Gtk.FileFilter()
    filter_LO.set_name("Αρχεία LibreOffice")
    filter_LO.add_mime_type("application/vnd.oasis.opendocument.text")
    filter_LO.add_mime_type("application/vnd.oasis.opendocument.spreadsheet")
    filter_LO.add_mime_type("application/vnd.oasis.opendocument.database")
    filter_LO.add_mime_type("application/vnd.oasis.opendocument.presentation")
    filter_LO.add_mime_type("application/vnd.oasis.opendocument.graphics")
    dialog.add_filter(filter_LO)

    filter_calc = Gtk.FileFilter()
    filter_calc.set_name("Αρχεία Calc")
    filter_calc.add_mime_type("application/vnd.oasis.opendocument.spreadsheet")
    dialog.add_filter(filter_calc)

    filter_write = Gtk.FileFilter()
    filter_write.set_name("Αρχεία Writer")
    filter_write.add_mime_type("application/vnd.oasis.opendocument.text")
    dialog.add_filter(filter_write)

    filter_base = Gtk.FileFilter()
    filter_base.set_name("Αρχεία Base")
    filter_base.add_mime_type("application/vnd.oasis.opendocument.database")
    dialog.add_filter(filter_base)

    filter_impress = Gtk.FileFilter()
    filter_impress.set_name("Αρχεία Impress")
    filter_impress.add_mime_type("application/vnd.oasis.opendocument.presentation")
    dialog.add_filter(filter_impress)

    filter_draw= Gtk.FileFilter()
    filter_draw.set_name("Αρχεία Draw")
    filter_draw.add_mime_type("application/vnd.oasis.opendocument.graphics")
    dialog.add_filter(filter_draw)

    filter_any = Gtk.FileFilter()
    filter_any.set_name("Όλα")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

def add_py_filters(dialog):
    filter_py = Gtk.FileFilter()
    filter_py.set_name("Αρχεία python")
    filter_py.add_mime_type("text/x-python")
    dialog.add_filter(filter_py)

    filter_any = Gtk.FileFilter()
    filter_any.set_name("Όλα")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

#WARNING: This will overwrite an existing python file with the same name!
def insertpythonfile(pyfpath, LOfpath):
    valuetoreturn = -3
    pyftail = os.path.split(pyfpath)[1]
    LOftail = os.path.split(LOfpath)[1]
    LObackupnum = nextbackupnum(LOfpath)
    if LObackupnum < 1:
        valuetoreturn = -1
        return valuetoreturn
    pyfinxml = "Scripts/python/" + pyftail
    xmlmypythonfileline = ' <manifest:file-entry manifest:full-path="%s" manifest:media-type=""/>' % ('Scripts/python/'+ pyftail)
    manifestoldlines = []
    manifesttmplines = []
    manifestnewlines = []
    for path in ['Scripts/','Scripts/python/']:
        manifesttmplines.append(' <manifest:file-entry manifest:full-path="%s" manifest:media-type="application/binary"/>' % path)
    manifesttmplines.append(xmlmypythonfileline)
    manifesttmplines.append('</manifest:manifest>')

    with tempfile.TemporaryDirectory() as tmpdir:
        newzipfpath = os.path.join(tmpdir, LOftail)
        with zipfile.ZipFile(LOfpath, 'r') as zipread:
            with zipread.open('META-INF/manifest.xml') as f:
                manifestoldlines = [x.decode('utf8').rstrip() for x in f.read().splitlines()]
                oldmanifest = f.read()
            with zipfile.ZipFile(newzipfpath, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename == 'META-INF/manifest.xml' or item.filename == pyfinxml:
                        pass
                    else:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
                if xmlmypythonfileline.strip() in [x.strip() for x in manifestoldlines]:
                    zipwrite.writestr('META-INF/manifest.xml', oldmanifest)
                else:
                    for everyline in manifestoldlines[:]:
                        if everyline.strip() not in [x.strip() for x in manifesttmplines]:
                            manifestnewlines.append(everyline)
                    for everyline in manifesttmplines[:]:
                        manifestnewlines.append(everyline)
                    zipwrite.writestr('META-INF/manifest.xml', '\n'.join(manifestnewlines))
                zipwrite.write(pyfpath, pyfinxml)
        shutil.copyfile(LOfpath, LOfpath + "." + str(LObackupnum))
        shutil.copyfile(newzipfpath, LOfpath)
        valuetoreturn = LObackupnum
    return valuetoreturn

def main(realfile_dir):
    mainwindow = EmbedScriptGUI(realfile_dir)
    mainwindow.set_position(Gtk.WindowPosition.CENTER)
    response = mainwindow.run()

    sys.exit(response)

if __name__ == "__main__":
    realfile = os.path.realpath(__file__)
    realfile_dir = os.path.dirname(os.path.abspath(realfile))
    main(realfile_dir)
