import hashlib    
import time
import math

class Information():
    def __init__(self,data = 'Hello'):
        self.data = data
        #print("(debug)[block.Information.__init__ ")
    
    def get(self):
        return self.data

    def duplication(self):
        information = Information()
        information.data = self.data
        return information
        
class Block():
    def __init__(self,information = "",server_ip_port = "0.0.0.0:0",id = 0):
        #print("(debug)[block.Block.__init__ ")
        self.id = int(0)
        self.timestamp = round(time.time(),2)    #float
        self.nonce = int(0)
        self.prev_hash = '0'
        self.information = Information(information)
        self.source = str(server_ip_port)
        # id\timestamp\nonce\prev_hash\information\source
        self.attritube = ["id","timestamp","nonce","prev_hash","information.data","source"]

    def conv_block_to_str(self):
        str_block = str()
        str_block += str(self.id) \
            + "\\" + str(self.timestamp) \
            + "\\" + str(self.nonce) \
            + "\\" + str(self.prev_hash) \
            + "\\" + str(self.information.data) \
            + "\\" + str(self.source) \
            #+ '\n'
        return str_block

    def conv_str_to_block(self,sData):  #return 
        # 56\Mon Feb 21 14:29:13 2022\177\00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf\Hello\0.0.0.0
        try:
            pass
            list_block = sData.split('\n')  #['Tue Dec 14 00:21:29 2021\\hello\\0\\0\\172.30.5.59:5000', '']
            #print("[conv_str_to_block]\nsData\n",sData,"\nlist_block\n",list_block)
            list_block = list_block[0]          #  id    timestamp                   nonce  prev_hash                                                           information source
            list_block = list_block.split('\\') #['56', 'Mon Feb 21 14:42:57 2022', '178', '00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf', 'Hello', '0.0.0.0']

            self.id = int(list_block[0])
            self.timestamp = float(list_block[1])
            self.nonce = int(list_block[2])
            self.prev_hash = str(list_block[3])
            self.information = Information(list_block[4])
            self.source = str(list_block[5])
            return self
        except:
            pass
            #print("[conv_str_to_block]unknown error!")
            return False

    def get_blockhash(self,CallBy=""):
        #print("(debug)[block.get_blockhash]CallBy:",CallBy)
        new_block = self.duplication(CallBy="block.get_blockhash")
        new_block.id = 0
        return hashlib.sha256(new_block.conv_block_to_str().encode()).hexdigest()

    def is_same_as__(self,block):
        pass
        if self.id == block.id and self.timestamp == block.timestamp and self.source == block.source:
            #print("[block.is_same_as]True")
            return True
        else:
            #print("[block.is_same_as]False")
            return False

    def is_same_as(self,block):
        result = self.cmp(block)
        print("(debug)[block.is_same_as]")
        self.print_block(debug="self")
        block.print_block(debug="block")
        print("(debug)[block.is_same_as]")
        print("(debug)[block.is_same_as]result:",result)
        if "timestamp" in result and "information.data" and "source" in result:
            #print("[block.is_same_as]True")
            return True
        else:
            #print("[block.is_same_as]False")
            return False
    
    def cmp(self,block):    #return list ex. ["id","timestamp"] same item
        pass
        result = []
        if self.id == block.id:
            result.append("id")
        #print("[block.cmp]two timestamp = ",self.timestamp,block.timestamp)
        if float(self.timestamp) == float(block.timestamp):
            result.append("timestamp")
        if self.nonce == block.nonce:
            result.append("nonce")
        if self.prev_hash == block.prev_hash:
            result.append("prev_hash")
        if self.information.data == block.information.data:
            result.append("information.data")
        if self.source == block.source:
            result.append("source")
        #print("[cmp]result = ",result)
        return result

    def duplication(self,CallBy = ""):
        #print("(debug)[block.duplication]called by:",CallBy)
        block = Block()
        #print("(debug)[block.duplication]addr of block = ",hex(id(block)))
        block.id = self.id
        block.timestamp = self.timestamp
        block.nonce = self.nonce
        block.information = self.information.duplication()
        block.source = self.source
        return block

    def print_block(self,debug = "",show = True):
    
        # id\timestamp\nonce\prev_hash\information\source
        msg = str()
        msg += "====block===="+str("debug:" * (not(len(debug) == 0)))+str(debug)+   \
            "\nid:"+str(self.id)+   \
            "\ntimestamp:"+str(self.timestamp)+ \
            "\nnonce:"+str(self.nonce)+ \
            "\nprev_hash:"+str(self.prev_hash)+ \
            "\ninformation.data:"+str(self.information.data)+   \
            "\nsource:"+str(self.source)+   \
            "\n============="+  \
            "\nhash:"+str(self.get_blockhash(CallBy="block.print_block"))+    \
            "\n=============\n"
        if(show):print(msg,sep = "",end = "")
        
        return msg



if __name__ == "__main__":
    block = Block("test")
    block.timestamp = "123"
    new_block = block.duplication(CallBy="block.main")
    new_block._block()
    
