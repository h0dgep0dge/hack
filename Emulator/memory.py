class Memory:
    def __init__(self,buffer=[]):
        self.buffer = {}
        for i in range(0,len(buffer)):
            self.buffer[i] = buffer[i]
    
    def read(self,index):
        if index in self.buffer:
            return self.buffer[index]
        return 0
    
    def write(self,index,value):
        if index == 30001:
            print(value)
        self.buffer[index] = value
    
    def __len__(self):
        return 32768
    
    def __getitem__(self,index):
        return self.read(index)
    
    def __setitem__(self,index,value):
        self.write(index,value)

    
class CodeMemory(Memory):
    def __init__(self,code):
        buffer = []
        for inst in code:
            buffer.append(int(inst,2))
        super().__init__(buffer)
    
    def read(self,index):
        return "{:016b}".format(super().read(index))
    
    def write(self,index,value):
        raise Exception("CodeMemory is read only")