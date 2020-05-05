#
#
#


from inc_noesis import *
import os


def registerNoesisTypes():
    handle = noesis.register("The Kreed (2004)", ".pak")
    noesis.setHandlerExtractArc(handle, pakExtractResources)
    
    return 1
 
 
class FileEntry:
    def __init__(self):
        self.name = ""
        self.size = 0 
        self.offset = 0
        
    def read(self, reader):
        length = reader.readUInt()
        self.name = reader.readBytes(length).decode("ascii").rstrip("\0")
        self.size = reader.readUInt()
        self.offset = reader.readUInt()
        
        
class PAKFile:
    def __init__(self, reader):
        self.files = []
        self.reader = reader

    def readHeader(self, reader):
        if not reader.readUInt() == 541802832: # PAK
            return 1
        reader.seek(4, NOESEEK_REL) 
        
    def readTable(self, reader):
        count = reader.readUInt()
        for i in range(count):        
            entry = FileEntry()
            entry.read(reader)
            
            self.files.append(entry)

    def read(self):
        if self.readHeader(self.reader) == 1:
            return 0
            
        self.readTable(self.reader)

        return 1        
        
        
def pakExtractResources(fileName, fileLen, justChecking):    
    with open(fileName, "rb") as f:
        if justChecking: #it's valid
            return 1   
        
        filereader = NoeBitStream(f.read())    
    
        pak = PAKFile(filereader)
        if pak.read() == 0:
            return 0
          
        for file in pak.files:                        
            filereader.seek(file.offset + 4, NOESEEK_ABS) 
            fileData = filereader.readBytes(file.size) 
            
            rapi.exportArchiveFile(file.name, fileData)
       
    return 1