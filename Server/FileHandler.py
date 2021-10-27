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
                
