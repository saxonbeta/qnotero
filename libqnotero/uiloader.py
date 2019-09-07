#-*- coding:utf-8 -*-

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

import os
import platform
from libqnotero.qt import QtCore, uic


class UiLoader(QtCore.QObject):
    
    """
    desc:
        A base object from classes that dynamically load a UI file.
    """
    
    def loadUi(self, ui):
        
        """
        desc:
            Dynamically loads a UI file.
            
        arguments:
            ui:
                desc:   The name of a UI file, which should match.
                        libqnotero/ui/[name].ui
                type:   str
        """

        path = os.path.dirname(__file__)
        # If we are running from a frozen state, we
        # need to find the UI files relative to the executable directory,
        # because the modules are packaged into library.zip.
        if platform.system() == 'Windows':
            import sys
            if hasattr(sys, 'frozen') or hasattr(sys, 'importers'):
                path = os.path.join(os.path.dirname(sys.executable),
                                    'lib\libqnotero')
        uiPath = os.path.join(path, 'ui', '%s.ui' % ui)
        self.ui = uic.loadUi(uiPath, self)
