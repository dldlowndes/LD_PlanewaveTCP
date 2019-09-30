import select
import socket
import time

import PlanewaveTCP

my_PW = PlanewaveTCP.PlanewaveTCP("127.0.0.1", 8877)

print(my_PW.GetStatus())

#def SendMsg(socket_Obj, message):
#    message+="\n"
#    print("COMMAND:", message.encode("ascii"))
#    my_Socket.sendall(message.encode("ascii"))
#    reply = GetResponse(my_Socket)
#    print("REPLY:", reply)
#    return reply
#
#def GetResponse(socket_Obj):
#    buffer_Size = 1
#    response = ""
#    while(IsReadable(socket_Obj)):
#        data = socket_Obj.recv(buffer_Size)
#        if not data: 
#            break
#        else:
#            response += data.decode("UTF-8")
#    return response
#
#def GetResponse2(socket_Obj):
#    response = ""
#    while not IsReadable(socket_Obj):
#        pass
#    while not response.endswith("\n"):
#        response += socket_Obj.recv(1).decode("UTF-8")
#    return response
#
#def IsReadable(socket_Obj):
#    return len(select.select([socket_Obj], [], [socket_Obj], 2)[0]) > 0
#
#ip_Addr = "127.0.0.1"
##ip_Addr = "0.0.0.0"
#tcp_Port = 8877
#
#my_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#my_Socket.connect((ip_Addr, tcp_Port))
#my_Socket.setblocking(False)
#
#SendMsg(my_Socket, "status")
#time.sleep(2)
#
#
###################################################
#
##SendMsg(my_Socket, "gotoradecapp\n0\n0")
##time.sleep(5)
#
###################################################
#
#cmds = [
#        ["gotoradecapp", "0", "0"],
#        ["gotoradecapp", "3", "22.5"],
#        ["gotoradecapp", "6", "45"],
#        ["gotoradecapp", "9", "22.5"],
#        ["gotoradecapp", "12", "0"]
#        ]
#
#for cmd in cmds:
#    SendMsg(my_Socket, "\n".join(cmd))
##    time.sleep(5)
#
###################################################
#    
