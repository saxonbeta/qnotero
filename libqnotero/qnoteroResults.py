"""
This file is part of qnotero.

qnotero is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

qnotero is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with qnotero.  If not, see <http://www.gnu.org/licenses/>.
"""

from libqnotero.qt.QtGui import QListWidget
from libqnotero.qt.QtCore import Qt
import subprocess
import os
import platform


class QnoteroResults(QListWidget):
    """The Qnotero result list"""

    def __init__(self, qnotero):

        """
		Constructor

		Arguments:
		qnotero -- a Qnotero instance
		"""

        QListWidget.__init__(self, qnotero)
        self.setMouseTracking(True)

    def mousePressEvent(self, e):

        """
		Start a drag operation

		Arguments:
		e -- a QMouseEvent
		"""

        if e.button() == Qt.RightButton:
            item = self.itemAt(e.pos())
            if item is None:
                return
            note = item.zoteroItem.get_note()
            if note is not None:
                self.qnotero.previewNote(note)
            return

        QListWidget.mousePressEvent(self, e)
        qnoteroItem = self.currentItem()
        if qnoteroItem is None:
            return
        if not hasattr(qnoteroItem, "zoteroItem"):
            return
        zoteroItem = qnoteroItem.zoteroItem
        if zoteroItem.fulltext is None and zoteroItem.url is None:
            print('qnoteroResults.mousePressEvent(): no file attachment nor url')
            return
        if zoteroItem.fulltext is None:
            path = zoteroItem.url
        else:
            path = zoteroItem.fulltext

        print("qnoteroResults.mousePressEvent(): prepare to open %s"
              % path)
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', path))
            elif platform.system() == 'Windows':  # Windows
                path = os.path.normpath(path)
                os.startfile(path)
            else:  # linux variants
                subprocess.call(('xdg-open', path))
            print("qnoteroResults.mousePressEvent(): file opened")
        except Exception as exc:
            print("qnoteroResults.mousePressEvent(): failed to open file, sorry... %s" % exc)

    def keyPressEvent(self, e):

        """
		Handle key presses

		Arguments:
		e -- a QKeyEvent
		"""

        if (e.key() == Qt.Key_Up and self.currentRow() == 0) \
                or (e.key() == Qt.Key_F and Qt.ControlModifier & e.modifiers()):
            self.qnotero.ui.lineEditQuery.selectAll()
            self.qnotero.ui.lineEditQuery.setFocus()
            return
        QListWidget.keyPressEvent(self, e)
