from os import PRIO_USER
import socket
from datetime import datetime
from Server.RouteParser import getRoute, favIcon
from Server.FileHandler import GEThandler
from termcolor import colored, cprint





class HttpServer:
    def __init__(self, ServerHost: str, ServerPort: int, verbose: bool):
        self._host = ServerHost
        self._port = ServerPort
        self._client_connection = ""
        self._client_address = ""
        self._request = ""
        self._response = ""
        self._logging = verbose
        self._registeredRoutes = {}
        self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # this decorator creates a list of all the registered function
    def route(self, *args):
            def register(func):
                self._registeredRoutes[args[0]] = func
                return func
            register.all = self._registeredRoutes
            return register

    # initializes the server, esentially taking in all the parameters and ensuring that the server is set up.
    # additionally the route function decorator is called with registers all the methods for routing.  need to add 
    # specific paths so that it can search different places for files.  

    def setupServer(self):
        self._serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._serverSocket.bind((self._host, self._port))
        self._serverSocket.listen(1)
        serverStr = colored('The server is listening on port: ', 'green')
        serverStr = serverStr + colored(f'{self._port}', 'red',)
        print(serverStr)
        regall = self.route()
        if self._logging == True:
            print("Get a list of all the routes available in the server")
            print(regall.all)
        return self._serverSocket

    
    # This defines the main control loop of the application.  

    def start(self):
        while True:
            curDate = f'{datetime.now()}'

            # wait for connections
            self._client_connection, self._client_address = self._serverSocket.accept()

            ######################################################################################
            # verbose logging
            if self._logging == True:
                print(f"{datetime.now()} :: A connection was recieved from {self._client_address}")
            ######################################################################################

            # catch the incomming client request.
            # Notes: using a local variable seems to increase reliabiltiy.
            thisRequest = self._client_connection.recv(1024).decode()
            self._request = thisRequest
            
            # getRoute parses the incoming request and returns a tuple that includes the request
            # type and the route ex: ('GET','/favicon.ico')
            request = getRoute(thisRequest)
                

            ######################################################################################
            # verbose logging
            if self._logging == True:
                print(f"{datetime.now()} : {self._request}")
            ######################################################################################

            else:

                # this check catched unregestered request such as favicon or css or files directly requested.
                # security needs to be implmented on this method so that only files in the static directory can 
                # accessed.
                if request != None and request[1] not in self._registeredRoutes:
                    finalRes = GEThandler(request)
                    self._client_connection.send(finalRes)    

                elif request != None and request[1] != '/favicon.ico':
                    if request[1] in self._registeredRoutes:
                        self._response =  self._registeredRoutes[request[1]]()
                        if self._response == 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found':
                            print( f"{colored(curDate, 'white', 'on_red')}, '{request[0]} {request[1]}' recieved from {self._client_address} No File exists."  )
                        else:
                            print(f"{colored(curDate, 'white', 'on_green')}: '{request[0]} {request[1]}' recieved from {self._client_address}")
                    else:
                        self._response = 'HTTP/1.0 404 NOT FOUND\n\nRoute Not Found'
                        print( f"{colored(curDate, 'white', 'on_red')}, '{request[0]} {request[1]}' recieved from {self._client_address} No Route exists."  )
                    
                    self._client_connection.sendall(self._response.encode())

                
                    
                

            # Send the response
            # self._client_connection.sendall(self._response.encode())
            self._client_connection.close()

    def close(self):
        self._serverSocket.close()


