# -*- coding:utf-8 -*-

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

import platform

config = {
    u"autoFire": 500,
    u"autoUpdateCheck": False,
    u"cfgVer": 0,
    u"firstRun": True,
    u"listenerPort": 43250,
    u"minQueryLength": 3,
    u"noteProvider": u"gnote",
    u"theme": u"Light",
    u'appStyle': u'Fusion',
    u"updateUrl": u"",
    u"pos": u"Top right",
    u"zoteroPath": u"",
    u"mdNoteproviderPath": u"",
    u'showAbstract': False,
    }


def getConfig(setting):

    """
    Retrieve a setting

    Returns:
    A setting or False if the setting does not exist
    """

    return config[setting]


def setConfig(setting, value):

    """
    Set a setting

    Arguments:
    setting -- the setting name
    value -- the setting value
    """

    config[setting] = value
    config[u"cfgVer"] += 1


def restoreConfig(settings):

    """
    Restore settings from a QSetting

    Arguments:
    settings -- a QSetting
    """

    for setting, default in config.items():
        if isinstance(default, bool):
            if platform.system() == u'Darwin':
                value = bool(settings.value(setting, default))
            else:
                value = settings.value(setting, default) == 'true'
        elif isinstance(default, str):
            value = str(settings.value(setting, default))
        elif isinstance(default, int):
            value = int(settings.value(setting, default))
        elif isinstance(default, float):
            value = float(settings.value(setting, default))
        else:
            raise Exception(u'Unknown default type')
        setConfig(setting, value)


def saveConfig(settings):

    """
    Save settings to a QSetting

    Arguments:
    setting -- a QSetting
    """

    for setting, value in config.items():
        settings.setValue(setting, value)
