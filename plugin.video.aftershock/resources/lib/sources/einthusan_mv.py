# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://www.einthusan.com'
        self.search_link = '/search/?search_query=%s&lang=%s'
        self.cdn_link = 'http://cdn.einthusan.com/geturl/'
        self.cdn_extn = '/hd/'


    def get_movie(self, imdb, title, year):
        try:
            search = 'http://www.omdbapi.com/?i=%s' % imdb
            search = client.source(search)
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            languages = ['hindi', 'tamil', 'telugu', 'malayalam']
            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in languages)][0]

            query = self.search_link % (urllib.quote_plus(title), language)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'div', attrs = {'class': 'search-category'})
            result = [i for i in result if 'Movies' in client.parseDOM(i, 'p')[0]][0]
            result = client.parseDOM(result, 'li')

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'a')[0]) for i in result]
            r = [i for i in result if any(x in i[1] for x in years)]
            if not len(r) == 0: result = r
            result = [i[0] for i in result if title == cleantitle.movie(i[1])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = url.replace('../', '/')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            #http://cdn.einthusan.com/movies_hindi/movie_high/2766.mp4?st=LIoADUvnHgCdQowNQ9F1Pw&e=1448814347
            #http://169.45.89.74/einthusancom/hot/D2766.mp4?st=2XKN2EAyZBtfGRw_wIrOJw&e=1448796478
            movieId = re.compile('(id|url|v|si|sim|data-config)=(.+?)/').findall(url+'/')[0][1]
            try :
                cdn_url = self.cdn_link + movieId + self.cdn_extn
                result = client.source(cdn_url)
            except:
                pass
            #result = None
            if (not (result is None)) and len(result) > 1 :
                url = result
                return url
            else :
                try:
                    result = client.source(url)
                    result = re.compile("setupJwplayer\(\'(.+?)\'\)").findall(result)[0]
                    url = 'http://p.jwpcdn.com/6/12/jwplayer.flash.swf' + result
                except:
                    pass
            return url
        except:
            return