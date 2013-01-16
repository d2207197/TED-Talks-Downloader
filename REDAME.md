TED Talks webpage parser, video and subtitle downloader
=============

Create TedTalk object
--------

    >>> import tedtalk

    >>> tt = tedtalk.TedTalk(url = 'http://www.ted.com/talks/simon_lewis_don_t_take_consciousness_for_granted.html')
    >>> tt = tedtalk.TedTalk(searchPattern = "Don't take consciousness for granted")  # search google

Usage ob TedTalk object
--------

### Basic parse result ###

    >>> tt.topic
    u"Don't take consciousness for granted"

    >>> tt.speaker
    u'Simon Lewis'

    >>> tt.url
    'http://www.ted.com/talks/simon_lewis_don_t_take_consciousness_for_granted.html'

    >>> tt.mp4url
    'http://download.ted.com/talks/SimonLewis_2010P.mp4?apikey=TEDDOWNLOAD'

    >>> tt.webpage
    u'<!doctype html>\r\n<html lang="en">\r\n<head>\r\n<meta charset="utf-8">\r\n\r\n\r\n<link rel="shortcut icon" href="http://assets.tedcdn.com/favicon.ico">\r\n\r\n<meta name="title" content="Simon Lewis: Don&#039;t take consciousness for granted | Video on TED.com" />\n<meta name="description" content="TED Talks After a catastrophic ca...

### Get video ###

    >>> tt.get_mp4_filename()
    u'SimonLewis_2010P.mp4'

    >>> with open(tt.get_mp4_filename(), 'wb') as mp4:
    >>>    tt.download_mp4(mp4)
    SimonLewis_2010P.mp4    100%   67MB  33.5MB/s   00:02

### Get subtitle ###

    >>> tt.obtain_subtitle(lang = 'english')
    Downloading subtitles from ted id: 1186, language: english

    >>> tt.subtitle
    [{'content': 'There was a time in my life',
      'duration': 3000,
      'startOfParagraph': False,
      'startTime': 0},
     {'content': 'when everything seemed perfect.',
      'duration': 3000,
      'startOfParagraph': False,
      'startTime': 3000},
     {'content': 'Everywhere I went, I felt at home.',
      'duration': 2000,
      'startOfParagraph': False,
      'startTime': 6000},
     {'content': 'Everyone I met,',
      'duration': 2000,
      'startOfParagraph': False,
      'startTime': 8000},
      ...


    >>> tt.get_subtitle_paragraph()   # list of subtitle splited according to paragraph
    ["There was a time in my life when everything seemed perfect. Everywhere I went, I felt at home. Everyone I met, I felt I knew them for as long as I could remember. And I want to share with you how I came to that place and what I've learned since I left it.",...
