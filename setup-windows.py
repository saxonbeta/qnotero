#!/usr/bin/env python3

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

---
desc:
	Windows packaging procedure:
	
	1. Build Qnotero into `dist` with `setup-win.py py2exe`		
	2. Create `.exe` installer with `.nsi` script
	3. Rename `.exe` installer
	4. Rename `dist` and pack it into `.zip` for portable distribution
---
"""
# Use cx_Freeze to make the windows installer
from cx_Freeze import setup, Executable
from libqnotero.qnotero import Qnotero
import sys

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

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
    'bdist_msi_options': {
        'upgrade_code': '{69620F3A-DC3A-11E2-B341-002210FE9B01E}',
        'install_icon': './data/qnotero.ico'
    }
}

executables = [
    Executable(
        'qnotero',
        base=base,
        shortcutName='Qnotero',
        shortcutDir='DesktopFolder',
    )
]

setup(name="qnotero",
      version=Qnotero.version,
      description="Standalone sidekick to the Zotero reference manager",
      author="E. Albiter",
      author_email="ealbiter@gmail.com",
      url="",
      options=options,
      executables=executables
      )
