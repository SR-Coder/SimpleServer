# so what is the purpose of a template engine?? what does it do?
# well it is essentially a compiler so what does a compiler do
# well for python it needs to return a function that creates a string of html
# it should accept variables such as context a dictionary of all the things we want to express
# this function needs to be returned as a string and then run in exec() and then returned 
# the server for final render.
import re
import os


class MethodBuilder:
    def __init__(self, indent=0):
        self.codeString = []
        self.allVars = set()
        self.loopVars = set()
        self.indentLevel = indent
    
        self._indentAmt = 4

    def addline(self, line):
        self.codeString.extend([" " * self.indentLevel, line, '\n'])

    def indent(self):
        self.indentLevel += self._indentAmt

    def dedent(self):
        self.indentLevel -= self._indentAmt

    def addSection(self):
        section = MethodBuilder(self.indentLevel)
        self.codeString.append(section)
        return section
    
    # ultimately runs the assembled string and returns the code result
    def get_globals(self):
        source = str(self)
        global_namespace = {}
        exec(source, global_namespace)
        return global_namespace

    # allows the methodbuilder object to be viewed as a string.
    def __str__(self) -> str:
        return "".join(str(c) for c in self.codeString)


class TemplateEngine:
    def __init__(self, html, *contexts):

        # dictionary for all variables passed into context from the user
        self.context = {}

        
        # unpacks the arguments into the context dictionary
        for context in contexts:
            self.context.update(context)

        # creates the code object that keeps track of all our lines
        ##### - code is object that organizes our code
        code = MethodBuilder()
        code.addline('def renderTemplate(context):')
        code.indent()
        varsBlock = code.addSection()
        code.addline("results = []")
        code.addline("\n")
        #####

        # add all the context variables to the varsBlock section
        for key,value in self.context.items():
            varsBlock.addline(f'{key} = context["{key}"]')

        # getting the variables
        buffered = []
        def flush_output():
            if len(buffered) == 1:
                code.addline(f'results.append({buffered[0]})')
            elif len(buffered) > 1:
                code.addline(f'results.extend([", ".join({buffered})])')
            del buffered[:]

        operatorStack = []

        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", html)


        # this logic determines what is actually in the inside the html file
        for token in tokens:
            
            #  comment handler
            if token.startswith('{#'):
                # print(f'Comment --> {repr(token)}')
                continue # ignores the comments

            # Constant handler
            elif token.startswith('{{'):
                varName = token[2:-2].strip() # removes the '{{}}' and all white space
                self._addVariable(varName, code.allVars)
                buffered.append("f'{%s}'" % varName)

            # expression handler
            elif token.startswith('{%'):
                # print(f'Function --> {repr(token)}')
                # need to decide how to finish this out.
                continue

            else:
                if token:
                    # print(f'Literal --> {repr(token)}')
                    buffered.append(repr(token))
            
            # addes the line of code 
            flush_output()
        # print(self.context)
        # print(code)


        code.addline('return results')

        self.finalCode = code.get_globals()['renderTemplate']
        # print(self.finalCode(context))


        

    def render(self):
        # takes the context dictionary passed in
        _output = self.finalCode(self.context)
        _htmlResult = "".join(_output)
        return _htmlResult

    # HELPER FUNCTIONS
    # ----------------------------------------------
    # handles the raising of errors can be use anywhere
    def _raiseError(self, errMsg, errorCause):
        raise TemplateSyntaxError(f'{errMsg}: {errorCause}')


    def _addVariable(self, varName, varSet):
        # need to make sure that it is a valid variable name else raise error
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", varName):
            self._raiseError('Invalid Var Name!', varName)
        varSet.add(varName)


        

    

context = {
    "FName": "Jane",
    "LName": "Pancakes",
    "allNames": ['john','jane', 'jim', 'jack']
}

dirname = os.path.dirname(__file__)

checkFile = os.path.join(dirname, f'../Views/PassDataTest.html')
fileIn = open(checkFile)
htmlDoc = fileIn.read()
fileIn.close()


myTemp = TemplateEngine(htmlDoc, context)
print(myTemp.render())



# lets look at the function we would want to create a simple web page

# def createHtmlString(context):
#     result = []
#     # location for local variables
#     FName = "Jane"
#     LName = "Pancakes"
#     result.append('<!DOCTYPE html> \n')
#     result.append('<html lang="en" \n')
#     result.append('<head> \n')
#     result.append('    <meta charset="UTF-8"> \n')
#     result.append('    <meta http-equiv="X-UA-Compatible" content="IE=edge"> \n')
#     result.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0"> \n')
#     result.append('    <title>Document</title> \n')
#     result.append('</head> \n')
#     result.append('<body> \n')
#     result.append(f'{FName} '  )
#     result.append(f' {LName}'  )



#     return ''.join(result)


# print(createHtmlString('hello'))



myHtml = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
{# this is a comment #}
    {{ FName }} , {{ LName }}
    <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Est illum ipsum eum! Saepe omnis porro laboriosam minima. Cum qui nostrum nisi accusantium ducimus sint libero beatae, eligendi dicta quis dolores?</p>
    <ul>
    {% for name in allNames %}
        <li>{{ name }}</li>
    {% endfor %}
    </ul>
</body>
</html>
'''



