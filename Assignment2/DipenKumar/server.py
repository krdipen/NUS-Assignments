from socket import *
import threading
import sys

def upload (connectionSocket,addr):
    txt = ""
    prev = ""
    count = 0
    while True:
        data = connectionSocket.recv(1)     # receive the input request from client byte by byte
        # this means we now have 3 entries/strings/words that are <file name to download> <proxy1-ip-address/hostname> <port>
        # now we can forward rest input and act as a proxy
        if count > 2:
            clientSocket.send(data)    # forwarding the input to next proxy/server
        data = data.decode()
        if data == " ":                # check if the byte is space the this means the end of entry/string/word
            count += 1                 # increase the counter of entry/string/word
            if prev == " ":
                # break when two consecutive byte is space that is end of input stream
                break
        txt += data           # keep storing bytes in a single string variable to split latter with space
        prev = data           # update the previous byte with current byte
        if count == 3:        # we now have 3 entries/strings/words that are <file name to download> <proxy1-ip-address/hostname> <port>
            request = txt.split(" ")                            # split the single string to get all three entries/strings/words in list
            ServerName = request[1]                             # ip-address/hostname of next proxy/server
            serverPort = int(request[2])                        # port number to connect to next proxy/server
            clientSocket = socket(AF_INET, SOCK_STREAM)         # create a tcp clientSocket
            clientSocket.connect((ServerName,serverPort))       # connect the tcp socket to hostname at port specified
            # send the file name to download to next proxy/server with space to separate entries/strings/words after encoding in binary
            data = request[0] + " "
            data = data.encode()
            clientSocket.send(data)
    if count == 2:      # this means the input stream had single entry/string/word ended with two spaces
        # this is server
        request = txt.split(" ")       # removes the extra space in filename
        file = open(request[0],"rb")   # open the file to download in binary
        while True:                    # keep reading the file
            data = file.read(1024)     # read 1024 bytes in chunk
            if not data:
                # break when nothing to read and send
                break
            connectionSocket.send(data)    # send the file to client via proxies
        file.close()                       # close the file once read completely and sent
        connectionSocket.close()           # close the connectionSocket
    else:               # else it is a proxy
        while True:     # keep receiving the data from forward-proxy/server and keep sending it to previous proxy/client
            data = clientSocket.recv(1024)    # blocks received are forwarded instead waiting for entire file
            if not data:
                # break when transfered completely and have nothing to send
                break
            connectionSocket.send(data)       # blocks received are forwarded instead waiting for entire file
        clientSocket.close()                  # close the clientSocket created by proxy to connected to another proxy/server
        connectionSocket.close()              # close the connectionSocket
    sys.exit()                                # terminate the thread once downloading is done

serverPort = int(sys.argv[1])                 # assigned the serverPort with the command line input received
serverSocket = socket(AF_INET,SOCK_STREAM)    # created a serverSocket
serverSocket.bind(('',serverPort))            # this will be the welcoming socket
serverSocket.listen(5)                        # listen for some client. parameter specifies the maximum number of queued connections
while 1:
    connectionSocket, addr = serverSocket.accept()     # wait for client to accept the tcp connection
    # create and start a new thread for that tcp connection with the client and allow other clients to connect
    # server must support concurrent connections
    thread = threading.Thread(target=upload,args=(connectionSocket,addr))
    thread.start()
