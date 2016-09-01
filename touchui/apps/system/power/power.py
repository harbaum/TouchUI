#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, os, socket
from subprocess import call
from TouchStyle import *

class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.w = TouchWindow("Power")

        self.vbox = QVBoxLayout()

        self.vbox.addStretch()

        self.poweroff = QToolButton()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(QPointF(3,3))
        self.poweroff.setGraphicsEffect(shadow)
        self.poweroff.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.poweroff.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pix = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "powerdown"))
        icon = QIcon(pix)
        self.poweroff.setIcon(icon)
        self.poweroff.setIconSize(pix.size())
        self.poweroff.setText("Power off")
        self.poweroff.clicked.connect(self.on_poweroff)
        self.vbox.addWidget(self.poweroff)

        self.vbox.addStretch()

        self.reboot = QToolButton()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(QPointF(3,3))
        self.reboot.setGraphicsEffect(shadow)
        self.reboot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reboot.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pix = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "reboot"))
        icon = QIcon(pix)
        self.reboot.setIcon(icon)
        self.reboot.setIconSize(pix.size())
        self.reboot.setText("Reboot")
        self.reboot.clicked.connect(self.on_reboot)
        self.vbox.addWidget(self.reboot)

        self.vbox.addStretch()

        self.w.centralWidget.setLayout(self.vbox)

        self.w.show()
        self.exec_()        
 
    def on_poweroff(self):
        print("poweroff")
        self.notify_launcher("Shutting down ...")
        call(["sudo", "poweroff"])

    def on_reboot(self):
        print("reboot")
        self.notify_launcher("Rebooting ...")
        call(["sudo", "reboot"])

    def notify_launcher(self, msg):
        # send a signal so launcher knows that the app
        # is up and can stop the busy animation
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect(("localhost", 9000))
            sock.sendall(bytes("msg {}\n".format(msg), "UTF-8"))
        except socket.error as msg:
            print(("Unable to connect to launcher:", msg))
        finally:
            sock.close()

if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
