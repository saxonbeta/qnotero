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

import sys
import os
import os.path
import platform
from libqnotero.qnoteroException import QnoteroException
from libqnotero.qt.QtGui import QIcon, QPixmap
from libqnotero.qt.QtGui import QLabel
from libqnotero.qt.QtCore import Qt


class Light:
    """The default Qnotero theme"""

    def __init__(self, qnotero):

        """
		Constructor
		
		qnotero -- a Qnotero instance
		"""

        self.qnotero = qnotero
        self.setThemeFolder()
        self.setWindowProperties()
        self.setScrollBars()

    def icon(self, iconName, overrideIconExt=None):

        """
		Retrieves an icon from the theme
		
		Arguments:
		iconName -- the name of the icon
		
		Returns:
		A QIcon		
		"""
        if overrideIconExt is None:
            return QIcon(os.path.join(self._themeFolder, iconName) +
                         self._iconExt)
        else:
            return QIcon(os.path.join(self._themeFolder, iconName) +
                         overrideIconExt)

    @staticmethod
    def iconExt():

        """
		Determines the file format of the icons
		
		Returns:
		An extension (.png, .svg, etc.)
		"""

        return ".png"

    def iconWidget(self, iconName):

        """
		Return a QLabel with an icon
		
		Arguments:
		iconName -- the name of the icon
		
		Returns:
		A QLabel
		"""

        l = QLabel()
        l.setPixmap(self.pixmap(iconName))
        return l

    def lineHeight(self):

        """
		Determines the line height of the results
		
		Returns:
		A float (e.g., 1.1) for the line height
		"""

        return 1.1

    def pixmap(self, pixmapName):

        """
		Retrieves an icon (as QPixmap) from the theme
		
		Arguments:
		pixmapName -- the name of the icon
		
		Returns:
		A QPixmap
		"""

        return QPixmap(os.path.join(self._themeFolder, pixmapName) \
                       + self._iconExt)

    @staticmethod
    def roundness():

        """
		Determines the roundness of various widgets
		
		Returns:
		A roundness as a radius in pixels
		"""

        return 0

    def setScrollBars(self):

        """Set the scrollbar properties"""

        self.qnotero.ui.listWidgetResults.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.qnotero.ui.listWidgetResults.setVerticalScrollBarPolicy(
             Qt.ScrollBarAlwaysOff)

    def setThemeFolder(self):

        """Initialize the theme folder"""

        import sys
        self._themeFolder = os.path.join(os.path.dirname(sys.argv[0]),
                                         "resources", self.themeFolder())
        self._iconExt = self.iconExt()
        if not os.path.exists(self._themeFolder):
            if (platform.system() == 'Darwin' or platform.system() == 'Windows')\
                    and hasattr(sys, 'frozen'):
                self._themeFolder = os.path.join(os.path.dirname(sys.executable),
                                                 self.themeFolder())
            else:
                self._themeFolder = os.path.join("/usr/share/qnotero/resources/",
                                                 self.themeFolder())
            if not os.path.exists(self._themeFolder):
                raise QnoteroException("Failed to find resource folder! %s" % self._themeFolder)
        print("libqnotero._themes.light.__init__(): using '%s'" \
              % self._themeFolder)

    def setWindowProperties(self):

        """Set the window properties (frameless, etc.)"""
        self.qnotero.setWindowFlags(Qt.FramelessWindowHint)

    def themeFolder(self):

        """
		Determines the name of the folder containing the theme resources
		
		Returns:
		The name of the theme folder
		"""
        if platform.system() == 'Darwin' and hasattr(sys, 'frozen'):
            return 'themes/light'
        else:
            return 'light'
