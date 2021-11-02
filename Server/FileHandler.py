import os
from datetime import datetime
from termcolor import colored


def GEThandler(request):

    # standard r/programmerhumor comment: this gets the current date and time
    curDate = datetime.now()


    # checks to make sure that the request is of type 'GET' and returns an error
    # 
    if request[0] != "GET":
        return 'HTTP/1.1 400 Bad Request\n\n'

    
    thisRequest = request[1]
    getFile = thisRequest.lstrip('/')
    dirname = os.path.dirname(__file__)
    checkFile = os.path.join(dirname, f'../{getFile}')


    # Make sure that you put folder names in here that you want to be accessable
    # the outside world.
    ApprovedDir = ['Static']

    # this gets the requested directory so that it can be checked if it is allowed
    # or not.
    reqDir = getFile.split('/')

    # for debugging purposes:
    # print(reqDir)
    # print (os.path.exists(checkFile))
    # print(checkFile)

    try:
        if(reqDir[0] not in ApprovedDir):
            raise Exception("Error: Access denied")

        file = open(checkFile, 'rb')
        # print(os.path.exists(checkFile))
        resoponse = file.read()
        file.close()
        if(getFile.endswith(".css")):
            mimetype = 'text/css'
        elif (getFile.endswith('.ico')):
            mimetype = 'image/x-icon'
        else:
            mimetype = 'text/html'
        
        header ='HTTP/1.1 200 OK\n'

        # '<strong>\n\n</strong>'
        header +='Content-Type: '+str(mimetype)+'\n\n'
        final_response = header.encode('utf-8')
        final_response += resoponse
        print(f"     {colored(curDate, 'white', 'on_green')}: '{request[0]} {request[1]}'")
        return final_response

    except Exception as e:
        print( f"     {colored(curDate, 'white', 'on_red')}, '{request[0]} {request[1]}' {e.args}.")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response ='<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body>z</html>'.encode('utf-8')
        final_response = header.encode()
        final_response += response
        return final_response
                


# here is a list of mime types
allMimeTypes = {
    "aac": "audio/aac",
    "abw": "application/x-abiword",
    "ai": "application/postscript",
    "arc": "application/octet-stream",
    "avi": "video/x-msvideo",
    "azw": "application/vnd.amazon.ebook",
    "bin": "application/octet-stream",
    "bz": "application/x-bzip",
    "bz2": "application/x-bzip2",
    "csh": "application/x-csh",
    "css": "text/css",
    "csv": "text/csv",
    "doc": "application/msword",
    "dll": "application/octet-stream",
    "eot": "application/vnd.ms-fontobject",
    "epub": "application/epub+zip",
    "gif": "image/gif",
    "htm": "text/html",
    "html": "text/html",
    "ico": "image/x-icon",
    "ics": "text/calendar",
    "jar": "application/java-archive",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "js": "application/javascript",
    "json": "application/json",
    "mid": "audio/midi",
    "midi": "audio/midi",
    "mp2": "audio/mpeg",
    "mp3": "audio/mpeg",
    "mp4": "video/mp4",
    "mpa": "video/mpeg",
    "mpe": "video/mpeg",
    "mpeg": "video/mpeg",
    "mpkg": "application/vnd.apple.installer+xml",
    "odp": "application/vnd.oasis.opendocument.presentation",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "odt": "application/vnd.oasis.opendocument.text",
    "oga": "audio/ogg",
    "ogv": "video/ogg",
    "ogx": "application/ogg",
    "otf": "font/otf",
    "png": "image/png",
    "pdf": "application/pdf",
    "ppt": "application/vnd.ms-powerpoint",
    "rar": "application/x-rar-compressed",
    "rtf": "application/rtf",
    "sh": "application/x-sh",
    "svg": "image/svg+xml",
    "swf": "application/x-shockwave-flash",
    "tar": "application/x-tar",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "ts": "application/typescript",
    "ttf": "font/ttf",
    "txt": "text/plain",
    "vsd": "application/vnd.visio",
    "wav": "audio/x-wav",
    "weba": "audio/webm",
    "webm": "video/webm",
    "webp": "image/webp",
    "woff": "font/woff",
    "woff2": "font/woff2",
    "xhtml": "application/xhtml+xml",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.ms-excel",
    "xlsx_OLD": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xml": "application/xml",
    "xul": "application/vnd.mozilla.xul+xml",
    "zip": "application/zip",
    "3gp": "video/3gpp",
    "3gp_DOES_NOT_CONTAIN_VIDEO": "audio/3gpp",
    "3gp2": "video/3gpp2",
    "3gp2_DOES_NOT_CONTAIN_VIDEO": "audio/3gpp2",
    "7z": "application/x-7z-compressed"
}