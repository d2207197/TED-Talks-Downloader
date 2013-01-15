
class UrlError(Exception):
    pass
class ParseError(Exception):
    pass
class SearchError(Exception):
    pass

class TedTalk():
    def __init__(self, url = None, searchPattern = None):
        if searchPattern and url:
            raise UrlError("can't set both searchPattern and url")
        elif url:
            self.url = url
        elif searchPattern:
            self._set_url_by_search(searchPattern)

        self._set_webpage_by_url()
        self._parse_webpage()
        # self._set_mp4url_by_webpage()
        # self._set_tedid_by_webpage()
        # self._set_topic_speaker_by_webpage()


    def _set_url_by_search(self, searchfor):
        import json
        import urllib
        query = urllib.urlencode({'q': searchfor, 'as_sitesearch': 'ted.com'})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&{}'.format( query )
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        try:
            data = results['responseData']
        except:
            raise SearchError
        # print 'Total results: %s' % data['cursor']['estimatedResultCount']
        # hits = data['results']
        # print 'Top %d hits:' % len(hits)
        # for h in hits: print ' ', h['url']
        # print 'For more results, see %s' % data['cursor']['moreResultsUrl']
        self.url = data['results'][0]['url']

    def _set_webpage_by_url(self):
        import urllib
        try:

            connection = urllib.urlopen(self.url)
            encoding = connection.headers.getparam('charset')
            self.webpage = connection.read().decode(encoding)
        except:
            raise UrlError

    def _parse_webpage(self):
        from HTMLParser import HTMLParser
        from collections import defaultdict

        class _TEDPageParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.intitle = True
                self.mp4url = self.title = self.tedid = None

            # def close(self):
                # HTMLParser.close(self)
                # if not self.mp4url or not self.title or not self.tedid:
                    # raise ParseError



            def handle_starttag(self, tag, attrs):
                attrs = defaultdict(str, attrs)

                if self.mp4url and self.title and self.tedid:
                    # self.close()
                    return

                if tag == 'title':
                    self.intitle = True
                elif tag == 'a' and attrs['id'] == 'no-flash-video-download':
                    if  attrs.has_key('href') :
                        self.mp4url = attrs['href'] + '?apikey=TEDDOWNLOAD'
                    else:
                        raise ParseError
                elif tag == 'input' and attrs['id'] == "wordpresscom":
                    import re
                    tedid = re.search('\[ted id=(\d+)\]', attrs['value'])
                    if tedid:
                        self.tedid = int(tedid.group(1))
                    else:
                        raise ParseError


            def handle_data(self, data):
                if self.intitle:
                    self.title = data
                    self.intitle = False

        parser = _TEDPageParser()
        parser.feed(self.webpage)
        self.mp4url = parser.mp4url
        self.title = parser.title
        self.tedid = parser.tedid





    # def _set_mp4url_by_webpage(self):

    #     from HTMLParser import HTMLParser
    #     from collections import defaultdict
    #     class _TEDPageParser(HTMLParser):

    #     parser = _TEDPageParser()
    #     parser.feed(self.webpage)
    #     self.mp4url = parser.mp4url



    # def _set_tedid_by_webpage(self):
    #     import re

    #     tedid = re.search('\[ted id=(\d+)\]', self.webpage)
    #     if tedid:
    #         self.tedid = int(tedid.group(1))
    #     else:
    #         raise ParseError


    def download_mp4(self, f):
        import urllib2

        u = urllib2.urlopen(self.mp4url)
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (f.name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = "{0:10d}  [{1:3.2f}%]".format(file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,



    def obtain_subtitle(self, lang = 'english'):
        import simplejson
        import urllib

        print 'Downloading subtitles from ted id: {}, language: {}'.format(self.tedid, lang)
        c = simplejson.load(urllib.urlopen('http://www.ted.com/talks/subtitles/id/{}/lang/{}'.format(self.tedid, lang)))
        self.subtitle =   c['captions']

    def get_subtitle_html(self):
        import StringIO
        subhtml = StringIO.StringIO()
        firstsent = True
        for sentraw in self.subtitle:
            if firstsent == True:
                subhtml.write(' <p> {}'.format(sentraw['content']))
                firstsent = False
            elif sentraw['startOfParagraph'] == True:
                subhtml.write(' </p> \n <p> {}'.format(sentraw['content']))
            else:
                subhtml.write(' ' + sentraw['content'])
        return subhtml.getvalue()


    def get_subtitle_paragraph(self):
        import StringIO
        subparagraph = StringIO.StringIO()
        sublist = []
        firstsent = True
        for sentraw in self.subtitle:
            if firstsent == True:
                subparagraph.write(sentraw['content'])
                firstsent = False
            elif sentraw['startOfParagraph'] == True:
                sublist.append(subparagraph.getvalue())
                subparagraph.seek(0)
                subparagraph.truncate()                  # clear subparagraph
                subparagraph.write(sentraw['content'])
            else:
                subparagraph.write(' ' + sentraw['content'])
        sublist.append(subparagraph.getvalue())
        subparagraph.close()
        return sublist

    def get_mp4_filename(self):
        from os.path import basename
        import urlparse

        return basename(urlparse.urlsplit(self.mp4url).path)



    # from web


    # def getVideoParameters(urldirection):
    #     ht = urllib.urlopen(urldirection).read()
    #     var = re.search('flashVars = {\n([^}]+)}', ht)
    #     if var:
    #         var = var.group(1)
    #     else:
    #         return None
    #     var = [a.replace('\t', '') for a in var.split('\n')]
    #     for a in range(len(var)):
    #         if var[a]:
    #             var[a] = var[a][:var[a].rfind(',')]
    #     resultado = []
    #     for a in var:
    #         l = a.find(':')
    #         if l != -1:
    #             resultado.append((a[:l], a[l+1:]))
    #     return dict(resultado)





    # def downloadSub(idtalk, lang, timeIntro):
    #     print("Downloading subtitles for language %s"%lang)
    #     c = simplejson.load(urllib.urlopen('http://www.ted.com/talks/subtitles/id/%s/lang/%s'%(idtalk, lang)))
    #     salida = file('subs_%s_%s.srt'%(idtalk,lang), 'w')
    #     conta = 1
    #     c = c['captions']
    #     for linea in c:
    #         salida.write("%d\n"%conta)
    #         conta += 1
    #         salida.write("%s --> %s\n"%(getFormatedTime(timeIntro+linea['startTime']), getFormatedTime(timeIntro+linea['startTime']+linea['duration'])))
    #         salida.write("%s\n\n"%(linea['content'].encode('utf-8')))
    #     salida.close()

    # def availableSubs(subs):
    #     a = subs.find("LanguageCode")
    #     if a == -1:
    #         return []
    #     subs = subs[a+len("LanguageCode"):]
    #     return [re.search("%22([^A-Z]+)%22", subs).group(1)] + availableSubs(subs)

    # def getFormatedTime(intvalue):
    #     mils = intvalue%1000
    #     segs = (intvalue/1000)%60
    #     mins = (intvalue/60000)%60
    #     hors = (intvalue/3600000)
    #     return "%02d:%02d:%02d,%03d"%(hors,mins,segs,mils)
