class JParser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.ptr = 0
    
    def is_empty(self):
        return self.ptr >= len(self.tokens)
    
    def is_not_empty(self):
        return not self.is_empty()
    
    def peek(self,offset=0):
        if self.ptr+offset >= len(self.tokens):
            return None
        return self.tokens[self.ptr+offset]

    def chop(self):
        r = self.peek()
        if r is not None:
            self.ptr += 1
            if r == "\n":
                self.line += 1
        return r
