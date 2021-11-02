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

# View("hi")

# view test for taking a html file that has python in it and running the python
# and returning only an html file.
def ViewP(ViewName: str, *context: dict):

    # we need to read in the file onto a variable and return that so that 
    # it can be sent as the response.
    errorMsg = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
    fileName = ViewName + ".html"

    context = context[0]

    dirname = os.path.dirname(__file__)

    checkFile = os.path.join(dirname, f'../Views/{fileName}')

    if os.path.exists(checkFile):
        fileIn = open(checkFile)
        htdoc = fileIn.read()
        
        print(_parseFile(htdoc, context))


        # this code returns the parsed file with the correct header
        header = 'HTTP/1.0 200 OK\n\n'
        htmlDoc = header + htdoc
        fileIn.close()
        return htmlDoc

    return errorMsg

def _parseFile(file, context):
    i = 1
    doc = file
    for line in doc.split('\n'):
        line = line.strip()
        if line.startswith("@"):

            retCode = _executor(line, context)

            print(retCode)

            newLine = line.replace(line, "hello")

            print(f'{i}: {newLine}')
            
        else:
            print(f'{i}: {line}')
        i+=1
    return doc



def _executor(code: str, context):
    try:
        pass
    except Exception as e:
        return e.args





ctx = {'foo':'bar'}


ViewP("PassDataTest",ctx)



