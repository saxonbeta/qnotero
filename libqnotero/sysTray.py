#  This file is part of Qnotero.
#
#      Qnotero is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Qnotero is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Qnotero.  If not, see <https://www.gnu.org/licenses/>.
#      Copyright (c) 2019 E. Albiter

#

from libqnotero.qt.QtGui import QSystemTrayIcon, QMenu
from libqnotero.qt.QtCore import pyqtSignal
import platform


class SysTray(QSystemTrayIcon):

    """The Qnotero system tray icon"""

    listenerActivated = pyqtSignal()

    def __init__(self, qnotero):

        """
        Constructor

        Arguments:
        qnotero -- a Qnotero instance
        """

        QSystemTrayIcon.__init__(self, qnotero)
        self.qnotero = qnotero
        self.menu = QMenu()
        self.re_init()
        self.activated.connect(self.activate)
        self.listenerActivated.connect(self.activate)

    def activate(self, reason=None):

        """
        Handle clicks on the systray icon

        Keyword arguments:
        reason -- the reason for activation (default=None)
        """
        print("sysTray.activate(): Activating qnotero reason: %s" % reason)
        if reason == QSystemTrayIcon.Context or (platform.system() == 'Darwin' and reason is not None):
            print("sysTray.activate(): Exiting wthout activate Qnotero")
            return
        if self.qnotero.isVisible():
            self.qnotero.popDown()
        else:
            self.qnotero.popUp()

    def re_init(self):
        self.setIcon(self.qnotero.theme.icon("qnotero", ".png"))
        self.menu.clear()
        self.menu.addAction(self.qnotero.theme.icon("show"), "Show",	self.qnotero.popUp)
        self.menu.addAction(self.qnotero.theme.icon("preferences"),	"Preferences", self.qnotero.preferences)
        self.menu.addAction(self.qnotero.theme.icon("close"), "Close", self.qnotero.close)
        self.setContextMenu(self.menu)
