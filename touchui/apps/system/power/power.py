#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, os, socket
from subprocess import call
from TouchStyle import *

# a toolbutton with drop shadow
class ShadowButton(QToolButton):
    def __init__(self, iconname):
        QToolButton.__init__(self)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(QPointF(3,3))
        self.setGraphicsEffect(shadow)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pix = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), iconname))
        icon = QIcon(pix)
        self.setIcon(icon)
        self.setIconSize(pix.size())

        # hide shadow while icon is pressed
    def mousePressEvent(self, event):
        self.graphicsEffect().setEnabled(False)
        QToolButton.mousePressEvent(self,event)

    def mouseReleaseEvent(self, event):
        self.graphicsEffect().setEnabled(True)
        QToolButton.mouseReleaseEvent(self,event)

class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.w = TouchWindow("Power")

        self.vbox = QVBoxLayout()

        self.vbox.addStretch()

        self.poweroff = ShadowButton("powerdown")
        self.poweroff.setText("Power off")
        self.poweroff.clicked.connect(self.on_poweroff)
        self.vbox.addWidget(self.poweroff)

        self.vbox.addStretch()

        self.reboot = ShadowButton("reboot")
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
