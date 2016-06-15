#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, os
from TouchStyle import *

class LicenseDialog(TouchDialog):
    def __init__(self,title,lic,parent):
        TouchDialog.__init__(self, title, parent)
        
        txt = QTextEdit()
        txt.setReadOnly(True)
        
        font = QFont()
        font.setPointSize(16)
        txt.setFont(font)
    
        # load gpl from disk
        name = os.path.join(os.path.dirname(os.path.realpath(__file__)), lic)
        text=open(name).read()
        txt.setPlainText(text)

        self.setCentralWidget(txt)

class SmallLabel(QLabel):
    def __init__(self, str, parent=None):
        super(SmallLabel, self).__init__(str, parent)
        self.setObjectName("smalllabel")

class VersionWidget(QWidget):
    def __init__(self,title,str,parent=None):
        super(VersionWidget,self).__init__(parent)
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(title))
        vbox.addWidget(SmallLabel(str))
        self.setLayout(vbox)

class VersionsDialog(TouchDialog):
    def str_from_file(self, fname):
        try:
            return open(fname).readline().strip()
        except:
            return "???"

    def __init__(self,title,parent):
        TouchDialog.__init__(self, title, parent)

        vbox_w = QWidget(self.centralWidget)

        # add various version info
        vbox = QVBoxLayout()
        
        # --------- kernel version -----------
        vbox.addWidget(VersionWidget("Linux", self.str_from_file("/proc/version").split()[2]))

        # --------- python version ----------
        py_ver_str = ""
        for i in range(len(sys.version_info)):
            py_ver_str += str(sys.version_info[i])
            if(i < 2): py_ver_str += "."
        vbox.addWidget(VersionWidget("Python", py_ver_str))

        # --------- qt -----------
        vbox.addWidget(VersionWidget("Qt", QT_VERSION_STR))

        vbox.addWidget(VersionWidget("PyQt", PYQT_VERSION_STR))

        vbox_w.setLayout(vbox)

        # put everything inside a scroll area
        scroll = QScrollArea(self.centralWidget)
        scroll.setWidget(vbox_w)

        self.setCentralWidget(scroll)
        
class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.w = TouchWindow("About")

        menu = self.w.addMenu()
        menu_ver = menu.addAction("Versions")
        menu_ver.triggered.connect(self.show_version)

        menu.addSeparator()
        
        menu_lic_gpl = menu.addAction("License")
        menu_lic_gpl.triggered.connect(self.show_license_gpl)

        self.vbox = QVBoxLayout()

        self.vbox.addStretch()
        
        # and add some text
        self.txt = QLabel("TouchUI\n\nA lightweight UI for small touchscreens")
        self.txt.setObjectName("smalllabel")
        self.txt.setWordWrap(True)
        self.txt.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.txt)

        self.vbox.addStretch()

        self.c = QLabel("(c) 2016 by Till Harbaum")
        self.c.setObjectName("tinylabel")
        self.c.setWordWrap(True)
        self.c.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.c)

        self.vbox.addStretch()
        self.w.centralWidget.setLayout(self.vbox)

        self.w.show()
        self.exec_()        
 
    def show_license_gpl(self):
        dialog = LicenseDialog("GPL", "gpl.txt", self.w)
        dialog.exec_()

    def show_version(self):
        dialog = VersionsDialog("Versions", self.w)
        dialog.exec_()
        
if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
