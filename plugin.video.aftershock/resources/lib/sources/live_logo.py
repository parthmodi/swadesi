# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import datetime, base64, os, json
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import logger
from resources.lib.libraries import cleantitle

class source:
    def __init__(self):
        self.live_link = base64.b64decode('aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vdmluZWVndS9hZnRlcnNob2NrLXJlcG8vbGl2ZS1sb2dvcy5qc29u')
        self.now = datetime.datetime.now()
        self.list = {}

    def getLivePosters(self):
        try :
            logger.debug('logos local : %s' % control.setting('livelocal'))

            if control.setting('livelocal') == 'true':
                dataPath = control.dataPath
                filename = os.path.join(dataPath, 'live-logos.json')
                filename = open(filename)
                result = filename.read()
                filename.close()
            else :
                result = client.request(self.live_link)

            channels = json.loads(result)

            channelNames = channels.keys()
            channelNames.sort()

            for channel in channelNames:
                channelObj = channels[channel]
                if not channelObj['enabled'] == 'false':
                    self.list[channel] = channelObj['iconimage']
            return self.list
        except:
            import traceback
            traceback.print_exc()
            pass