from msilib.schema import Error
from typing import overload
from node import Node
from blockchain import Blockchain
from block import Block
from data_parser import DataParser
import time
import threading
import appendix
import os
import socket
import random
import inspect

import winsound

from numba import jit, cuda

'''
import os
CUDA_VISIBLE_DEVICES = 0
print("os.environ[\"CUDA_VISIBLE_DEVICES\"] = ",os.environ["CUDA_VISIBLE_DEVICES"])
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
'''

#global variable
STOP = False
PAUSE = False
node = Node()
blockchain = Blockchain()
data_parser = DataParser()
#golbal variable

def Beep():
    winsound.Beep(440,500)
    time.sleep(0.5)
    winsound.Beep(554,500)
    time.sleep(0.5)
    winsound.Beep(660,500)

class sudoku():
    def __init__(self,data = (0,0,0,0,0,0,0,0,0)):
        self.data = data
        #print("init data = ",self.data)
        arr = list()
        arr.append(self.data)

    def getobj(self):
        return self
    
    def to_string(self):
        return str(self.data)
    def to_obj(self,string):
        #print("para in:",string)

        return string
    
    def spec(self,string):
        #print("[sudoku.spec]======================")
        #print("[sudoku.spec]string:",string)
        if("sdk:" in string):
            #print("sdk: is in string")
            string = string.split("sdk:")
            #print(string)
            #print(string[1])    #[(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)]
            string = string[1].replace("[","").replace("]","")
            #print(string)   #(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)
            string = string.replace("(","")
            #print(string)
            string = string.split(")")
            string = string[0:-1]
            #print(string)   #['9, 8, 7, 6, 5, 4, 3, 2, 1', '1, 2, 3, 4, 5, 6, 7, 8, 1', '']
            data = list()
            for _ in string:
                temp = _.split(",")
                row = list()
                for x in temp:
                    row.append(int(x))
                #print(temp)
                data.append(row)
            #print("[spec]",data)
            return data
        else:
            pass
            #print("sdk: is not in string")
        #print("[sudoku.spec]======================")

def init():
    #init
    print("[main.init]__name__ = ",__name__)

    if node.server_port == 5000:
        port = 5001
        node.client_init(port)
        port = 5002
        node.client_init(port)
        port = 5003
        node.client_init(port)
    elif node.server_port == 5001:
        port = 5000
        node.client_init(port)
        port = 5002
        node.client_init(port)
        port = 5003
        node.client_init(port)
    elif node.server_port == 5002:
        port = 5000
        node.client_init(port)
        port = 5001
        node.client_init(port)
        port = 5003
        node.client_init(port)
    elif node.server_port == 5003:
        port = 5000
        node.client_init(port)
        port = 5001
        node.client_init(port)
        port = 5002
        node.client_init(port)
    else:
        print("[main.init]node.server_port is not in list!")

    time.sleep(5)
    '''debug

    '''
    blockchain.Set_malicious_score(node)

    t = threading.Thread(target = retriever,args = (node,))
    t.start()

    t = threading.Thread(target = miner,args = (blockchain,))
    #if node.server_port == 5000:t.start()
    t.start()
    print("\n======init done======\n")
    
def miner(blockchain):
    global STOP
    global PAUSE
    while STOP == False:
        while(len(blockchain.blockqueue) >= 1 and STOP == False):
            #print("(debug)[main.miner]while start")
            block = blockchain.mine()
            if block == False:  #代表有人先挖到 有更新
                break
            #block.print_block("[main.miner]I mined a block")
            #print("(debug)[main.miner]i mine a block len =",len(blockchain.chain))
            #node.broadcast("update//"+block.conv_block_to_str()+"//appendix//miner:node"+str(node.server_port)+"ip"+str(node.server_ip)+" ("+str(round(time.time(),2))+") "+"\\sdk:["+sudoku((9,8,7,6,5,4,3,2,1)).to_string()+sudoku((1,2,3,4,5,6,7,8,1)).to_string()+"]")
            time.sleep(1)
            #send ledge
            if (blockchain.chain[-1].id % 10 == 0):
                #print("(debug)[main.miner]enter 1st cond")
                Share_Ledge()
                threading.Thread(target=Beep).start()
                '''
                while(not(STOP)):
                    #print("(debug)[main.miner]enter loop blockchain.CONFLICT = ",blockchain.CONFLICT,"blockchain.LEDGE = ",blockchain.LEDGE,"STOP = ",STOP,"PAUSE = ",PAUSE)
                    if(blockchain.RECV_LEDGE == True or blockchain.CONFLICT == True): break
                    pause()
                    if(blockchain.send_ledge(node) == True):  
                        #print("(debug)[main.miner]enter cond1")
                        #resume()    #註解調因為送完之後等大家驗證，更新完
                        break
                    else:
                        print("[main.miner]blockchain.send_ledge(node) False")
                        pause()
                        blockchain.CONFLICT = False   #發生衝突 ex兩個節點都在傳帳本
                        blockchain.LEDGE = False #是否正在傳帳本
                        blockchain.RECV_LEDGE = False
                        time.sleep(random.randint(3,10))
                '''

        #print("[main.miner]the len of blockqueue less than 1")
        time.sleep(1)
    pass

def retriever(node):
    global STOP
    counter = 0
    anc_head = 0
    anc_tail = 0
    while STOP == False:
        data = node.server_retriever()  #if node stop, data == None
        # data = {{"msg":{"tag":tag,"content":content,"appendix":appendix}} ,"source":來源的socket物件}
        if(data == None): 
            # node stop
            break

        if(type(data) == dict):
            print("[retriever]",data)
            if data["msg"]["tag"] == "block":
                #print("[retriever]:data is block type")
                #data["msg"]["content"].print_block("call by block")
                blockchain.append_blockqueue(data["msg"]["content"])
            
            elif data["msg"]["tag"] == "cmd":
                if(data["msg"]["content"] == "new block"):
                    #new_block(True)
                    pass

                elif(data["msg"]["content"][0:10] == "send_ledge"):
                    try:
                        print("(debug)[main.retriever]contet == send_ledge")
                        blockchain.RECV_LEDGE = True
                    
                        string = data["msg"]["content"].split(' ')
                        #print("(debug)[main.retriever.elif(send_ledge)string before split]",data["msg"]["content"])
                        #print("(debug)[main.retriever.elif(send_ledge)]string:",string)
                        if(len(string) != 5): raise Exception

                        anc_head = string[2]
                        anc_tail = string[4]
                        counter = 0
                        print("(debug)[main.retriever]string = ",string,"head = ",anc_head,"tail = ",anc_tail)

                        print("(debug)[main.retriever]content == send_ledge string = ",string)
                        print("(debug)[main.retriever]anc_head =",anc_head,"anc_tail =",anc_tail)
                        print("(debug)[main.retriever]str(data[\"source\"].getpeername()) =",str(data["source"].getpeername()))
                        blockchain.others_ledge_set(str(data["source"].getpeername()))
                    except:
                        print("(error)[main.retriever]content = send_ledge cond unknown error!")

                elif(data["msg"]["content"] == "pause"):
                    blockchain.blockchain_pause("got cmd by"+str(data["source"].getpeername()))
                    print("[main.retriever]pause")
                    pause(0b000)

                elif(data["msg"]["content"] == "resume"):
                    resume(0b000)
                    print("[main.retriever]resume")

                else:   #這裡是以定義命列字串以外的 
                    blockchain.Inc_malicious_score(data["source"])

            elif data["msg"]["tag"] == "update":
                #print("[retriever]:data is for updating blockchain",blockchain)
                #data["msg"]["content"].print_block("call by update")
                blockchain.update_blockchain(data["msg"]["content"])

            elif data["msg"]["tag"] == "ledge":
                #print("(debug)[main.retriever.elif ledeg]data:",data)
                #print("[main.retriever]i recv ledge blockchain.LEDGE = ",blockchain.LEDGE)
                if(blockchain.LEDGE == True):
                    blockchain.IS_conflict()
                    print("[main.retriever]i recv ledge blockchain.CONFLICT = ",blockchain.CONFLICT)
                else:
                    #data["msg"]["content"].print_block(debug = "[main.retriever]datatag == ledge")
                    #print("(debug)[main.retriever]elif ledge::else data:",data,"data[\"msg\"][\"content\"]:",data["msg"]["content"])
                    blockchain.others_ledge_append(data["msg"]["content"])
                    counter += 1
                    #print("(debug)[main.retriever.data = ledge]counter:",counter,"int(anc_tail)-int(anc_head):",int(anc_tail)-int(anc_head))
                    if(counter > int(anc_tail)-int(anc_head)):  #1~10 10-1=9 counter > 9, counter = 10
                        blockchain.others_ledge_verify()

            elif data["msg"]["tag"] == "data":
                print("(debug)[main.retriever]data:",data["msg"]["content"])
            ##print("[main.retriever]appendix:",data["msg"]["appendix"])
            #print("[main.retriever]miner is ",appendix.miner(data["msg"]["appendix"]),",spec is:",sudoku().spec(data["msg"]["appendix"]))
            elif data["msg"]["tag"] == "groundstation":
                pass
        else:
            print("[retriever]:data is not type dict")

        blockchain.MinusAll_malicious_score(1)
        for x in blockchain.malicious_score:
            if(x["score"] > 100):
                node.server_del_client(x["client"])
                blockchain.Set_malicious_score()
        pass

def new_block(auto = False):
    if auto == False:
        info = input("new block:")
        block = Block(info,node.server_ip+":"+str(node.server_port))
        for i in range(2):
            node.broadcast("block//"+block.conv_block_to_str()+"//appendix//test")
            blockchain.append_blockqueue(block)
    else:
        print("[main.new_block]:auto new_block start")
        time.sleep(1)
        count = 0
        while True:
            info = "test {count} port {port}".format(count = count,port = node.server_port)
            #print("[main.new_block]info = ",info)
            block = Block(info,node.server_ip+":"+str(node.server_port))
            node.broadcast("block//"+block.conv_block_to_str()+"//appendix//test")
            blockchain.append_blockqueue(block)
            if count < 15: count += 1
            else: break
            time.sleep(0.3)

def send_data():
    ret = data_parser.Check()
    if(ret == False):
        print("(debug)[main.send_data]enter where i don't want")
        return False
    else:
        print("(deubg)[main.send_data]enter where i want")
        for line in ret:
            node.broadcast("data//"+line+"//appendix//test")
    return True

def pause(para = 0b001):    # (reserve) (reserve) (1 broadcast; 0 don't broadcast)
    global PAUSE
    PAUSE = True
    if(para & 0b001): node.broadcast("pause")
    blockchain.blockchain_pause()

def resume(para = 0b001):
    print("(debug)[main.resume]start")
    global PAUSE
    PAUSE = False
    if(para & 0b001): node.broadcast("resume")
    blockchain.blockchain_resume()

def Share_Ledge():
    print("(debug)[Share_Ledge]start")
    while(not(STOP)):
        #print("(debug)[main.miner]enter loop blockchain.CONFLICT = ",blockchain.CONFLICT,"blockchain.LEDGE = ",blockchain.LEDGE,"STOP = ",STOP,"PAUSE = ",PAUSE)
        if(blockchain.RECV_LEDGE == True or blockchain.CONFLICT == True): break
        pause()
        if(blockchain.send_ledge(node) == True):  
            #print("(debug)[main.miner]enter cond1")
            #resume()    #註解調因為送完之後等大家驗證，更新完
            break
        else:
            print("[main.miner]blockchain.send_ledge(node) False")
            pause()
            blockchain.CONFLICT = False   #發生衝突 ex兩個節點都在傳帳本
            blockchain.LEDGE = False #是否正在傳帳本
            blockchain.RECV_LEDGE = False
            time.sleep(random.randint(3,10))
    print("(debug)[Share_Ledge]done")

def ShowStatus():
    print("(debug)[main.ShowStatus]\n\tblockqueue.length:",len(blockchain.blockqueue),
        "\n\tSTOP:",STOP,
        "\n\tPAUSE:",PAUSE,
        sep="")
    blockchain.ShowStatus(1)


if __name__ == "__main__":
    init()
    
    #flag

    #run
    blockchain.run(node.server_port)

    while STOP == False:
        
        if(node.server_port != 5003 or True): msg = input()   #阻塞
        else:
            msg = "tesdfsefsasdf"
            time.sleep(0.5)

        if (msg == 'exit' or msg == "x"):
            break
        elif msg == "show blockchain":
            #blockchain.print_blockchain()
            blockchain.write_log(port = node.server_port)
        elif msg == "show blockqueue":
            print(blockchain.blockqueue)
        elif msg == "show block":
            if len(blockchain.blockqueue) >= 1:
                blockchain.blockqueue[int(input("input index:"))].print_block()
            else: print("[main]there is not anything in blockqueue!")
        elif (msg == "new block" or msg == "nb"):
            block = new_block(True)
        elif msg == "show serverlist":
            node.show_serverlist()
        elif msg == "show clientlist":
            node.show_clientlist()
        elif (msg == "show others ledge" or msg == "ol"):
            blockchain.others_ledge_show()       
        elif msg == "send":
            time.sleep(1)
            blockchain.send_ledge(node)
        elif msg == "pause":
            pause()
        elif (msg == "resume" or msg == "rs"):
            resume()
        elif (msg == "status" or msg == "st"):
            ShowStatus()
        elif(msg == "send data"):
            pass
            f = open("data.txt","r")
            buf = f.read()
            print("(debug)[main loop]buf:\n",buf)
            node.broadcast(buf)
        elif(msg == "data"):
            send_data()
        elif(msg == "test"):
            node.send_to_groundstation()
        else:
            pass

        node.broadcast(msg)

    blockchain.write_log(port = node.server_port,bDebug=False,show=False)   #auto show blockchain

    STOP = True
    blockchain.blockchain_stop()

    time.sleep(1)
    node.stop()

    print("===end===")
    print("[main.end]blockchain.blockqueue = ",blockchain.blockqueue)
    print("[main.end]len of blockchain.blockqueue = ",len(blockchain.blockqueue))
    print("===end===")
    
'''
sdk you by chen,pin-jui
'''
