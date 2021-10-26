import os


# This file will handle everything to do with getting files and parsing them so that they can be returned to the client
# eventually this will be the home of the direct parsing so that we can include python code directly in the html pages.


def View(ViewName: str):

    # we need to read in the file onto a variable and return that so that 
    # it can be sent as the response.
    errorMsg = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
    fileName = ViewName + ".html"

    dirname = os.path.dirname(__file__)

    checkFile = os.path.join(dirname, f'../Views/{fileName}')

    if os.path.exists(checkFile):
        fileIn = open(checkFile)
        htmlDoc = 'HTTP/1.0 200 OK\n\n'
        htmlDoc = htmlDoc + fileIn.read()
        fileIn.close()
        return htmlDoc

    return errorMsg

View("hi")

