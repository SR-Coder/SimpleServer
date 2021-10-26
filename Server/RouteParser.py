import os


def getRoute(request):
    head = request.split('\n')
    requestType = head[0].split()[0]
    requestRoute = head[0].split()[1]
    if requestRoute == "/favicon.ico":
        return ('GET', '/favicon.ico')
    else:
        return (requestType,requestRoute)


def favIcon():
    dirname = os.path.dirname(__file__)
    reldir = os.path.join(dirname, '../Static/favicon.ico')
    header = 'HTTP/1.1 200 OK\n'
    mimetype = 'image/x-icon'

    header += 'Content-Type: '+str(mimetype)+'<strong>\n\n</strong>'

    header.encode("utf-8")
    fileIco = open(reldir, 'rb') # reads the file as binary
    iconStream = fileIco.read()
    fileIco.close()

    finalRes = header.encode("utf-8")
    finalRes += iconStream


    return finalRes