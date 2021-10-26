from os import listdir
from os.path import isfile, join


def route(arg):

    # 

    def decorator(func):

        print("Inside the decorater" + arg)

        def wrapper():

            print("inside the wrapper" + arg)

            if (arg == "/"):
                pass
            else:
                func() # this should ultimately run after the decorator gets the proper file.


        return wrapper
    return decorator

@route("/")
def ordinaryFunc(*args):
    print( "Hello World")


ordinaryFunc()

