from Tkinter import *
from PIL import ImageTk, Image
import pygtk
pygtk.require('2.0')
import gtk
import socket               # Import socket module
import thread
# connection socket
from SocketConnectionModel import SocketConnectionModel

#import PIL.ImageTk
class MainViewWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

        # connection Status: 0 -> None, 1 -> Connection
        self.connectionStatus = 0

        # role type: 0 -> server, 1 -> client
        self.roleType = 0
        
    def createWidgets(self):

        self.var = IntVar()
        self.serverRadioButton = Radiobutton(self, text="Server",
                                        variable=self.var, value=0,
                                        command=self.changeServerClient)
        self.serverRadioButton.grid(row=0, column=0, sticky=W)

        self.clientRadioButton = Radiobutton(self, text="Client",
                                        variable=self.var, value=1,
                                        command=self.changeServerClient)
        self.clientRadioButton.grid(row=0, column=1, sticky=W)

        self.connectButton = Button(self)
        self.connectButton["text"] = "Connect"
        self.connectButton.grid(row=0, column=2)
        #self.connectButton.config(state='disabled')
        self.connectButton["command"] = self.startConnectOrDisconnect



        
        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=1, column=0, columnspan=5, sticky=W)

        self.sendButton = Button(self)
        self.sendButton["text"] = "Send"
        self.sendButton.grid(row=1, column=5)
        self.sendButton["command"] = self.addMessage
        
        self.messageField = Text(self)
        self.messageField["width"] = 60
        self.messageField["height"] = 10
        self.messageField["state"] = "disabled"
        self.messageField.grid(row=2, column=0, columnspan=6, sticky=W)

        self.imgPathLabel = Label(self)
        self.imgPathLabel["text"] = ""
        self.imgPathLabel.grid(row=3, column=0, columnspan=6, sticky=W)

        self.imgDisplayButton = Button(self)
        self.imgDisplayButton["text"] = "Display"
        self.imgDisplayButton.grid(row=3, column=5)
        self.imgDisplayButton.config(state='disabled')
        self.imgDisplayButton["command"] = self.displayImage

        self.imgPathBrowseButton = Button(self)
        self.imgPathBrowseButton["text"] = "Browse"
        self.imgPathBrowseButton.grid(row=3, column=7, sticky=W)
        self.imgPathBrowseButton["command"] = self.browseImageFile
    
        
      ##  path = "WiiU_screenshot_TV_014D2.jpeg"
       ## oriImg = Image.open(path)
      ##  imgWidth = 600
      ##  ratio = float(imgWidth)/oriImg.size[0]
     ##   imgHeight = int(oriImg.size[1]*ratio)
     ##   nim = oriImg.resize( (imgWidth, imgHeight), Image.BILINEAR )
     ##   img = ImageTk.PhotoImage(nim)
        
        self.imageLabel = Label(self, text="No Pic select")
       # self.imageLabel.image = img
        #self.imageLabel.pack()
        self.imageLabel.grid(row=4, column=0, sticky=W+E+N+S, columnspan=7)
        

    # add message to the message Text
    # msgType = 0 -> msg from entry, msgType = 1 => msg from parameter
    def addMessage(self, msgType = 0, msg = "Message"):
        self.messageField["state"] = "normal"
        if msgType == 0:
            self.messageField.insert(END, self.inputField.get())
            # send message to server/client
            #print "before send check" 
            if self.connectionStatus == 1:
                #print "enter send"
                self.connectionSocketManager.sendMessage(self.inputField.get())
                #print "pass send"
            self.inputField.delete( 0, len(self.inputField.get()))
        else:
            self.messageField.insert(END, msg)
        self.messageField.insert(END, "\r\n")
        self.messageField["state"] = "disabled"

        

    def browseImageFile(self):
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        try:
            filter = gtk.FileFilter()
            filter.set_name("Images")
            filter.add_mime_type("image/png")
            filter.add_mime_type("image/jpeg")
            filter.add_mime_type("image/gif")
            filter.add_pattern("*.png")
            filter.add_pattern("*.jpg")
            filter.add_pattern("*.gif")
            filter.add_pattern("*.tif")
            filter.add_pattern("*.xpm")
            dialog.add_filter(filter)

            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                self.imgDisplayButton.config(state='normal')
                self.imgPathLabel["text"] = dialog.get_filename()
            elif response == gtk.RESPONSE_CANCEL:
                self.imgDisplayButton.config(state='disabled')
                self.imgPathLabel["text"] = "No File Select"
        
        finally:
            dialog.destroy()
    
        
    def displayImage(self):
        oldPath = self.imgPathLabel.cget("text")
        path = oldPath.replace('\\', '/')
        print path
        #path = "WiiU_screenshot_TV_014D2.jpeg"
        oriImg = Image.open(path)
        if( oriImg.size[0] > 480 ):
            imgWidth = 480
            ratio = float(imgWidth)/oriImg.size[0]
            imgHeight = int(oriImg.size[1]*ratio)
            nim = oriImg.resize( (imgWidth, imgHeight), Image.BILINEAR )
            img = ImageTk.PhotoImage(nim)
        else:
            img = ImageTk.PhotoImage(oriImg)

        #self.imageLabel = Label(self, image=img)
        self.imageLabel.configure(image = img)
        self.imageLabel.image = img
        #self.pack()
        #self.imageLabel.grid(row=3, column=0)

    def saveMessage(self):
        f = open("messages.txt", "ab")
        f.write( self.messageField().get(0) )
        f.close()


# ==== Socket ====
    def openSocketServerSide(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        s.bind((host, port))        # Bind to the port

        s.listen(5)                 # Now wait for client connection.
        while True:
           c, addr = s.accept()     # Establish connection with client.
           print 'Got connection from', addr
           c.send('Thank you for connecting')
           c.close()                # Close the connection
           
    def openSocketClientSide(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.

        s.connect((host, port))
        print s.recv(1024)
        s.close                     # Close the socket when done

    def changeServerClient(self):
        self.addMessage(1, "Radio " + str(self.var.get()))
        #self.messageField["state"] = "normal"
        #self.messageField.insert(END, "Radio " + str(self.var.get()))
        #self.messageField.insert(END, "\r\n")
        #self.messageField["state"] = "disabled"
        #self.inputField.delete( 0, len(self.inputField.get()))
    def startConnectOrDisconnect(self):
        if self.connectionStatus == 0:
            # connect
            self.connectionSocketManager = SocketConnectionModel()
            self.connectionSocketManager.initParameters("127.0.0.1", 5566, self.var.get())
            # create a thread to handle connection process.
            try:
                thread.start_new_thread( self.connectionSocketManager.createConnection,
                                         (self.addMessage,) )
                self.connectionStatus = 1
            except:
                print "Error: unable to start Reading Loop\r\n"
                print sys.exc_info()
                self.connectionStatus = 0
        else:
            self.connectionSocketManager.stopConnection()
            # wait 1s?
            self.connectionSocketManager.disconnectSocket()
            self.connectionStatus = 0
            self.addMessage(1, "Disconnection")
       # if(self.var == 0):
       #     self.roleType = 0
            #self.connectionSocketManager = SocketConnectionModel()
       # else:
        #    self.roleType = 1

        
        
        # create a thread to handle connection process.
        #try:
            #thread.start_new_thread( self.readingLoop, (readCallBack,) )
        #except:
            #print "Error: unable to start Reading Loop\r\n"
            
        
    
# ==== End Socket ====

if __name__ == '__main__':
    root = Tk()
    app = MainViewWindow(master=root)
    app.mainloop()
