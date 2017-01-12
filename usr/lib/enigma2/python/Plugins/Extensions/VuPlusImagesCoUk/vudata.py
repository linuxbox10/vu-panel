# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/vudata.py
import urllib2
import HTMLParser
import cStringIO
import datetime
import operator 

class HTML2Text(HTMLParser.HTMLParser):
    """
    extract text from HTML code
    """

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.output = cStringIO.StringIO()

    def get_text(self):
        """get the text output"""
        return self.output.getvalue()

    def handle_starttag(self, tag, attrs):
        """handle  tags"""
        if tag == 'br':
            self.output.write('\n')

    def handle_data(self, data):
        """normal text"""
        self.output.write(data)

    def handle_endtag(self, tag):
        if tag == 'p':
            self.output.write('\n')


def getnew(idate = None):
    try:
        now = datetime.datetime.now()
        cdate = now.strftime('%Y-%b-%d')
        d1 = datetime.datetime.strptime(idate, '%Y-%b-%d')
        d2 = datetime.datetime.strptime(str(cdate), '%Y-%b-%d')
        delta = d2 - d1
        if delta.days < 32:
            return True
        return False
    except:
        return False


def getdata(urlStr, searchstr = None):
    data = []
    try:
        fileHandle = urllib2.urlopen(urlStr)
        html = fileHandle.read()
        fileHandle.close()
    except IOError:
        print 'Cannot open URL %s for reading' % urlStr
        return (False, data)

    try:
        p = HTML2Text()
        p.feed(html)
        text = p.get_text()
        raw_list = text.splitlines()
    except:
        return (False, data)

    textlist = []
    for line in raw_list:
        line = line.strip()
        print line
        if searchstr:
            if searchstr == ' ':
                if line != ' ' and '.zip' in line:
                    nfiparts = []
                    nfiparts = line.split('.zip')
                    url = nfiparts[0] + '.zip'
                    spart = nfiparts[1].strip()
                    sizdateparts = spart.split(' ')
                    idate = sizdateparts[0]
                    try:
                        itime = sizdateparts[1]
                    except:
                        print line
                        itime = ''

                    isize = sizdateparts[len(sizdateparts) - 1]
                    line = line + '\n'
                    idate = idate.strip()
                    print 'idate', idate
                    if getnew(idate):
                        try:
                            imdate = datetime.datetime.strptime(idate, '%d-%b-%Y')
                        except:
                            imdate = None

                        data.append([url,
                         imdate,
                         itime,
                         isize])
            elif line != ' ' and '.zip' in line and searchstr.lower() in line.lower():
                nfiparts = []
                nfiparts = line.split('.zip')
                url = nfiparts[0] + '.zip'
                spart = nfiparts[1].strip()
                sizdateparts = spart.split(' ')
                idate = sizdateparts[0]
                try:
                    itime = sizdateparts[1]
                except:
                    print line
                    itime = ''

                isize = sizdateparts[len(sizdateparts) - 1]
                line = line + '\n'
                try:
                    imdate = datetime.datetime.strptime(idate, '%d-%b-%Y')
                except:
                    imdate = None

                data.append([url,
                 imdate,
                 itime,
                 isize])
        elif line != ' ' and '.zip' in line:
            nfiparts = []
            nfiparts = line.split('.zip')
            url = nfiparts[0] + '.zip'
            spart = nfiparts[1].strip()
            sizdateparts = spart.split(' ')
            idate = sizdateparts[0]
            try:
                itime = sizdateparts[1]
            except:
                print line
                itime = ''

            isize = sizdateparts[len(sizdateparts) - 1]
            line = line + '\n'
            try:
                imdate = datetime.datetime.strptime(idate, '%d-%b-%Y')
            except:
                imdate = ''

            data.append([url,
             imdate,
             itime,
             isize])

    try:
        data.sort(key=operator.itemgetter(1))
    except:
        pass

    data.reverse()
    return (True, data)


def getplidata(urlStr, searchstr = None):
    data = []
    print ' ', urlStr
    try:
        fileHandle = urllib2.urlopen(urlStr)
        html = fileHandle.read()
        fileHandle.close()
    except IOError:
        print 'Cannot open URL %s for reading' % urlStr
        return (False, data)

    try:
        p = HTML2Text()
        p.feed(html)
        text = p.get_text()
        raw_list = text.splitlines()
    except:
        return (False, data)

    data = []
    textlist = []
    for line in raw_list:
        line = line.strip()
        if searchstr:
            if line != ' ' and '.zip' in line and searchstr.lower() in line.lower():
                nfiparts = []
                nfiparts = line.split('\n')
                x = len(nfiparts)
                if x == 1:
                    url = nfiparts[0]
                    idate = ''
                    itime = ''
                    isize = ''
                    data.append([url,
                     idate,
                     itime,
                     isize])
                    continue
                try:
                    url = nfiparts[1]
                except:
                    url = ''

                infoparts = nfiparts[0].split(' ')
                y = len(infoparts)
                try:
                    idate = infoparts[0]
                except:
                    idate = ''

                try:
                    isize = infoparts[y - 1]
                except:
                    isize = ''

                itime = ''
                data.append([url,
                 idate,
                 itime,
                 isize])
        elif line != ' ' and '.zip' in line:
            nfiparts = []
            nfiparts = line.split('\t')
            x = len(nfiparts)
            if x == 1:
                url = nfiparts[0]
                idate = ''
                itime = ''
                isize = ''
                data.append([url,
                 idate,
                 itime,
                 isize])
                continue
            try:
                url = nfiparts[1]
            except:
                url = ''

            infoparts = nfiparts[0].split(' ')
            y = len(infoparts)
            try:
                idate = infoparts[0]
            except:
                idate = ''

            try:
                isize = infoparts[y - 1]
            except:
                isize = ''

            itime = ''
            data.append([url,
             idate,
             itime,
             isize])

    print data
    return (True, data)