
import socket
from Server.ViewHelper import View
from ServerClass import HttpServer

server = HttpServer("127.0.0.1", 8000, False)


# return methods for showing different things!!

@server.route("/")
def Index():
    return View("Index")

@server.route("/home")
def Home():
    return View("Home")

@server.route("/new")
def Invalid():
    return View("DoesNotExist")






# sets up the server and regesters the return methods
server.setupServer()



if __name__ == "__main__":
    server.start()
