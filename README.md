# pylo
GUI writen in python3 and Gtk to embed a python script in a LibreOffice Document.

This project aims in creating a simple GUI which will be used to embed code written as python sript into any LibreOffice Document.
This project will not be involved on how this python script is going to interact with the LibreOffice Document.

**main.py** inserts, updates or deletes python scripts (Macro) into a LibreOffice document using a gui.   
   
Tested with LibreOffice 5.1.6~rc2-0ubuntu1~xenial3, at least.

Dependencies:
-------------

pylo has several GTK-related dependencies. If you are already creating GTK
apps then you may have some of these installed already.

###System packages:

Installed with your package manager, like [apt](https://wiki.debian.org/apt-get).

* **gir1.2-gtk-3.0** - *Provides helpers and access to GIRepository.*
* **python3-gi** - *Provides python bindings for gobject-introspection.*
* **python3-bs4**
* **libgtksourceview-3.0-dev** - *Provides the `GtkSourceView` widget.*

There may be others, I will fill in the missing dependencies as they are found.
Message me or file an issue if you run into errors.

    
Usage
=====
Download all files in a folder of your choise and run:

     $ python3 main.py

or rename the file and make it executable.


Python scripts in LibreOffice.
==============================
In order to access a python script embedded in a LibreOffice document there are steps required:

1 You must have installed python script provider.
* -On Windows this is done automatically by the installer
* -On other systems possibly you should add this functionality by yourself. Example:
* --in Ubuntu you must install using your preferred method (apt-get in terminal or synaptic or software center) the libreoffice-script-provider-python package.

2. You must include your python file in the LibreOffice.
* -Use this gui
* -Or, alternatively, install the extention https://extensions.libreoffice.org/extensions/apso-alternative-script-organizer-for-python

In order to access python scripts from LibreOffice Basic you must create a LibreOffice Basic FUNCTION or SUB that will call the script. You can find a very "elementary" sample Calc Document with a simple function. The file is named «examplewithpythonmacro.ods». You must enable macros in order to use the function.

If your functions in the python script are going to access the LibreOffice Document and will not require special parameter passing, then there is no actual need to call them from LibreOffice Basic. Just assign them to events as explained in http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html

License
=======

Licensed as [GPL v3](http://www.gnu.org/licenses/gpl-3.0.en.html) or higher.   
