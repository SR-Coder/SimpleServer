
import socket
from Server.ViewHelper import View
from ServerClass import HttpServer

server = HttpServer("127.0.0.1", 8000, False)


# return methods for showing different things!!

@server.route("/")
def sayHi():
    return View("Index")

@server.route("/home")
def sayHello():
    return View("Home")

@server.route("/new")
def newPage():
    return View("DoesNotExist")






# sets up the server and regesters the return methods
server.setupServer()



if __name__ == "__main__":
    server.start()
