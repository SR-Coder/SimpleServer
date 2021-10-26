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


    # print (os.path.exists(checkFile))
    # print(checkFile)

    try:
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
        print( f"     {colored(curDate, 'white', 'on_red')}, '{request[0]} {request[1]}' No File exists.")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response ='<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body>z</html>'.encode('utf-8')
        final_response = header.encode()
        final_response += response
        return final_response
                
