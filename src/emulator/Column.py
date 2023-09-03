from Gate import Gate

class Column:
    def __init__(self, index, type, ctlr=[]):
        self.index = index
        self.gate = Gate(type, ctlr)
    
    def get_gate(self):
        return self.gate