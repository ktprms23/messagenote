import socket               # Import socket module
import thread

class SocketConnectionModel():
    #def __init__(self):
        # none

    def initParameters(self, ip, port, roleType):
        self.ip = ip
        self.port = port
        self.roleType = roleType
        print "pass 0 roletype = " + str(self.roleType)
        self.connectionFlag = False

    # create connection as server(wait connection) or client(connect to server)
    # readCallBack for reading loop
    def createConnection(self, readCallBack):
        # connect
        # roleType 0 -> server, 1 -> client
        try:
            self.s = socket.socket()         # Create a socket object
           # print "pass 1 roletype = " + self.roleType
            if self.roleType == 0:
                print "before host name"
                host = socket.gethostname() # Get local machine name
                print "pass host name"
                #port = 12345                # Reserve a port for your service.
                self.s.bind((self.ip, self.port))        # Bind to the port
                print "pass bind"
                self.s.listen(5)                 # Now wait for client connection.
                print "pass listen"
                self.cilentSocket, self.clientAddr = self.s.accept()     # Establish connection with client.
                print "pass 3"
            else:
                #host = socket.gethostname() # Get local machine name
                #port = 12345                # Reserve a port for your service.
                self.s.connect((self.ip, self.port))
                print "pass connect"

            self.connectionFlag = True
            # start reading loop
            self.readingLoop(readCallBack)

            # when reading loop exit because connection flag is false,
            # start disconnect socket
            self.disconnectSocket()
        except:
            print sys.exc_info()
        #try:
        #    thread.start_new_thread( self.readingLoop, (readCallBack,) )
        #except:
        #    readCallBack( "Error: unable to start Reading Loop" )
        #    self.disconnectSocket()

    def readingLoop(self, readCallBack):
        while self.connectionFlag == True:
            if( self.roleType == 0 ):
                readCallBack( 1, self.cilentSocket.recv(1024))
            else:
                readCallBack( 1, self.s.recv(1024))
    def sendMessage(self, msg):
        if self.connectionFlag == True:
            if( self.roleType == 0 ):
                self.cilentSocket.send(msg)
            else:
                self.s.send(msg)

    # set the thread flag to false,
    # and the reading loop, send message function will stop, then disconnect.
    def stopConnection(self):
        self.connectionFlag = False

    def disconnectSocket(self):   
        # ensure the connect flag is false
        if self.connectionFlag == False:
            if self.roleType == 0:
                self.cilentSocket.close()
            self.s.close()
        
