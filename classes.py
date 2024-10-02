class Folder():
    def __init__(self,name):
        self.name = name     
        self.children = []
        self.parent = None
        self.address=None

class File():
    def __init__(self,name):
        self.name = name
        self.children=None
        self.parent = None
        self.address=None
        
