#!/usr/bin/env python3

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


# Use cx_Freeze to make the windows installer
from cx_Freeze import setup, Executable
from libqnotero.qnotero import Qnotero
import sys

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable(
        'qnotero',
        base=base,
        icon='data\qnotero.ico',
    )
]

# Setup options
options = {
    'build_exe': {
        'optimize': '2',
        'silent': '0',
        'includes': [
            'sip'
        ],
        'packages': [
				"libqnotero",
				"libzotero",
				"libqnotero._themes",
				"libzotero._noteProvider",
		],
        'include_files': [
            'resources',
            'data\qnotero.ico',
        ],
    },
}


setup(name="qnotero",
      version=Qnotero.version,
      description="Standalone sidekick to the Zotero reference manager",
      author="E. Albiter",
      author_email="ealbitere@ipn.mx",
      url="",
      options=options,
      executables=executables
      )
