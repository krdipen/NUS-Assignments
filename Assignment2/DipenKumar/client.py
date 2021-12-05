from socket import *
import sys

infile = open(sys.argv[1],"r")     # open the input file containing the list of the proxies and the server along with the file to download

# Read first two line
txt = infile.readline()
txt += infile.readline()

request = txt.split()              # request is the list of three strings <file name to download> <proxy1-ip-address/hostname> <port>
serverName = request[1]            # serverName = <proxy1-ip-address/hostname>
serverPort = int(request[2])       # serverPort = <port>
clientSocket = socket(AF_INET, SOCK_STREAM)        # create a tcp socket
clientSocket.connect((serverName,serverPort))      # connect the tcp socket to hostname at port specified

# the name of the downloaded file will be the name to the file to download appended with _downloaded with same extension
name = request[0].split(".",1)
try:
    outfile = open(name[0]+"_downloaded."+name[1],"wb")
except:
    outfile = open(name[0]+"_doenloaded","wb")

# Send the remaining input file to proxy or server as string/stream after encoding it in binary
data = request[0] + " "     # every entry in input file is separated by space
data = data.encode()        # encoded in binary
clientSocket.send(data)     # send the file in fraction to allow pipeling and increases efficiency

# continue sending the other fraction of the input file
for line in infile:
    request = line.split()
    data = request[0] + " " + request[1] + " "
    data = data.encode()
    clientSocket.send(data)
infile.close()              # close the input file once sent entirely
data = " "                  # double space in the stream helps the proxy or server identify the end of the stream
data = data.encode()
clientSocket.send(data)
bytes = 0                   # byte counter that are downloaded till time
while True:                 # keep receiving downloading the file
    data = clientSocket.recv(1024)        # receives 1024 bytes
    if not data:
        # break when no byte received that marks the end of the file since server/proxy has closed the tcp connection
        break
    sys.stdout.write("\rDownloaded: %d bytes " % (bytes))    # print the number of bytes downloaded till now on console
    bytes += len(data)          # increase the counter to bytes downloaded till now
    outfile.write(data)         # write the received file in some file to store it locally
sys.stdout.write("\rDownloaded: %d bytes\n" % (bytes))       # print the final size of the downloaded file on console
outfile.close()                 # close the file once written
clientSocket.close()            # close the tcp connection once downloaded
