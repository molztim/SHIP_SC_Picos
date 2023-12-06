from time import sleep
import _thread

class dummy():
    
    def __init__(self):
        self.data = 0
        self.op_flag = False
    
    def set_data(self,data):
        self.data = data
        return None
    
    def get_data(self):
        return self.data
    
    def set_flag(self,status):
        self.op_flag = status
        return None
    
    def get_flag(self):
        return self.op_flag
        
    def server(self):
        while True:
            while not self.op_flag:
                pass
            self.data = self.data * 2
            self.op_flag = False
            

global_exchange = ""
global_flag = 0
dummy_1 = dummy()
second_thread = _thread.start_new_thread(dummy_1.server, ())

while True:
    data = 0
    print("Start: ",data)
    for i in range(5):
        print(i)
        sleep(1)
    dummy_1.set_data(25)
    dummy_1.set_flag(True)
    while dummy_1.get_flag() == True:
        pass
    data = dummy_1.get_data()
    print("Ende: ", data)
    
    
        