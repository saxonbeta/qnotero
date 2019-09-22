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

from libqnotero._themes.light import Light
import platform
import sys


class Dark(Light):

	"""The Default theme with a window frame"""
	
	def __init__(self, qnotero):
	
		Light.__init__(self, qnotero)

	def themeFolder(self):
		if platform.system() == 'Darwin' and hasattr(sys, 'frozen'):
			return 'themes/dark'
		else:
			return 'dark'
