import socket
import threading
import sys
import time
from blockchain import Blockchain
from block import Block
import specification

#server 接收 只會有一個執行緒
#client 傳送 會有好幾個 connected的client(socket物件) 被self.client_list紀錄
#socket.timeout https://vimsky.com/zh-tw/examples/detail/python-method-socket.timeout.html

class timeout(): ...


class Node():
    def __init__(self):
        #flag
        self.STOP = False   # 0 run,1 stop

        #attribute
            #server
        self.server = socket.socket()
        self.server_ip = str()
        self.server_port = int()
        self.server_list_client = []    #接上我server的client
        self.server_data = []   #接收到所有資料都放入此佇列
            #client
        self.client_list_server = []   #client(連接別人) 列表

        #init
        self.server_init()
        time.sleep(3)

#init
#==============================================
#server

    def server_init(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.server_port = 5000
        while True:
            try:
                self.server.bind((self.server_ip,self.server_port))
                break
            except:
                self.server_port += 1
                continue
        print('ip and port:',self.server_ip,self.server_port)
        self.server.listen(5)
        t = threading.Thread(target = self.server_listen)
        t.start()

    def server_listen(self):
        while True:
            try:
                self.server.settimeout(5)   #時間到引發例外跳到except
                client,addr = self.server.accept()
                print("[server_listen]accept ",addr)
                client.send(("welcome! I'm "+str(self.server_ip)+" "+str(self.server_port)).encode("utf-8"))

                t = threading.Thread(target = self.server_recv_runner,args = (client,))
                t.start()
                self.server_list_client.append(client)

            except socket.timeout:
                if self.STOP == True:
                    print("[server_listen]stop")
                    self.server_data_recv_flag = "end"
                    break

            except:
                print("[server_listen]unknown error")

    def server_recv_runner(self,client):
        while self.STOP == False:
            msg = self.server_recv(client)
            if(msg == ConnectionResetError):
                time.sleep(5)
                self.server_del_client(client)
                break
            if(msg == timeout):
                continue
            if msg == "":
                try:
                    self.server_del_client(client)  #這裡用try因為預計在blockchain接收到exit就會移除
                except:
                    pass
                finally:
                    break
            
            spec = specification.specification(msg)
            if spec != False:
                
                self.server_data.append({"msg":spec,"source":client})
                
            #server_data = {{"msg":{"tag":tag,"content":content,"appendix":appendix}} ,"source":來源的socket物件}

            try:
                index = self.server_list_client.index(client)
            except:
                break

    def server_recv(self,client):
        try:
            client.settimeout(5)
            msg = client.recv(4096).decode("utf-8")
            #print("[server_recv]",msg,type(msg))
            if msg == "":
                #print("[server_recv] msg == \"\"")
                time.sleep(5)
            return msg
        except ConnectionResetError:
            print("[server_recv]ConnectionResetError")
            return ConnectionResetError
        except socket.timeout:
            return timeout
        except Exception as e:
            print("[node.server_recv]error:",e)
            return False

    def server_del_client(self,client):
        try:
            self.server_list_client.remove(client)
        except:
            print("[server_del_client]error")

    def server_retriever(self): #回傳前會阻塞
        while self.STOP == False:
            if len(self.server_data) > 0:
                try:
                    data = self.server_data.pop(0)
                    return data
                except:
                    print("[server_retriever]error")
        return None

    def server_send(self,msg = "",client = ""):
        print("(debug)[node.server_send]start")
        print("(debug)[node.server_send]server_list_client[0]",self.server_list_client[0])
        self.server_list_client[0].send("(debug)[node.server_send]start".encode("utf-8"))
        pass
#server
#==============================================
#client
    def client_init(self,port = None):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while 1:
            try:
                # original
                # ipt = input('plz input ip and port:').split()
                # ip = ipt[0]
                # port = int(ipt[1])
                # original

                # debug mode
                if port == None:
                    if self.server_port == 5000:
                        port = 5001
                        ip = self.server_ip
                    elif self.server_port == 5001:
                        port = 5000
                        ip = self.server_ip
                    else:
                        ipt = input('plz input ip and port:').split()
                        ip = ipt[0]
                        port = int(ipt[1])
                elif type(port) != int:
                    print("[client_init]type(port) != int")
                    raise TypeError
                else:
                    ip = self.server_ip
                # debug mode

                client.connect((ip,port))
                #print("[node.client_init]client.connect(",ip,",",port,")")
                break
            except Exception as e:
                print("[node.client_init]e:",e)
                #print("[client_init]error:plz input angin!")
                pass
        self.client_list_server.append(client)
        print("[node.client_init]connect done!")

    def client_send(self,msg = "",client = ""):
        if client == "":    #沒有輸入client
            #client = self.client_list_server[0]
            print("[node.client_send]no pass client!")
        msg = str(msg)
        try:
            client.send((msg).encode("utf-8"))
        except:
            print("[client_send]error")
    
    def client_del(self,client = ""):
        if(client == ""):
            print("(error)[client_del]didn't recv client parameter")
            return False
        try:
            self.client_list_server.remove(client)
            return True
        except:
            print("[client_del]error")
            return False        

    def broadcast(self,msg = ""):
        for _ in self.client_list_server:
            self.client_send(msg,_)
#client
#==============================================
#others
    def send_to_groundstation(self,msg = "",client = ""):
        pass
        self.server_send()
        #if(client == ""):
            #print("[node.send_to_groundstation]no pass client!")
        #else:
            #self.server_send()

    def stop(self):
        self.server_list_client = []
        self.client_list_server = []
        self.STOP = True

    def show_serverlist(self):
        print("[show_serverlist]len of serverlist:",len(self.server_list_client))
        for _ in self.server_list_client: print("\t",_,sep="")
    def show_clientlist(self):
        print("[show_clientlist]len of clientlist:",len(self.client_list_server))
        for _ in self.client_list_server: print("\t",_,sep="")


if __name__ == "__main__":
    try:
        node = Node()
        print("(debug)[main]node.server_ip:",node.server_ip)
        if node.server_port == 5000:
            node.client_init(5001)
        elif node.server_port == 5001:
            node.client_init(5000)
        STOP = False
        while(not(STOP)):
            msg = input()
            if msg == "exit": STOP = True
    finally:
        node.stop()

