from inc_noesis import *
import os.path
import os


def registerNoesisTypes():
    handle = noesis.register( "The Kreed (2004) 3D model", ".skn")

    noesis.setHandlerTypeCheck(handle, kreedModelCheckType)
    noesis.setHandlerLoadModel(handle, kreedModelLoadModel)
        
    return 1 
    
    
class Vector3F:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        
    def read(self, reader):
        self.x, self.y, self.z = noeUnpack('3f', reader.readBytes(12)) 
        
    def getStorage(self):
        return (self.x, self.y, self.z)     


class Vector4F:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0  
        
    def read(self, reader):
        self.x, self.y, self.z, self.w = noeUnpack('4f', reader.readBytes(16))
        
    def getStorage(self):
        return (self.x, self.y, self.z, self.w)      
    

class Vector2F:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def read(self, reader):
        self.x, self.y = noeUnpack('2f', reader.readBytes(8))
 
    def getStorage(self):
        return (self.x, self.y) 
  

class Vector3UI16:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        
    def read(self, reader):
        self.x, self.y, self.z = noeUnpack('3H', reader.readBytes(6))
        
    def getStorage(self):
        return (self.x, self.y, self.z)         
 

class KreedMeshVertex:
    def __init__(self):
        self.coordinates = []
        self.uv = Vector2F()
        self.normal = Vector3F()
        
    def read(self, reader):
        self.normal.read(reader)   
        self.uv.read(reader) 
        
        reader.seek(36, NOESEEK_REL) 
        count = reader.readUShort()         
        reader.seek(2, NOESEEK_REL) 
        for i in range(count):
            reader.seek(8, NOESEEK_REL)        
            coordinates = Vector3F()
            coordinates.read(reader)
            self.coordinates.append(coordinates) 


class KreedMeshWeghtedVertex:
    def __init__(self):
        self.coordinates = []
        self.weights = None
        self.boneIndexes = None
        
    def read(self, reader):
        self.boneIndexes = noeUnpack('6H', reader.readBytes(12))           
        self.weights = noeUnpack('6f', reader.readBytes(24))
        for i in range(6):             
            coordinates = Vector3F()
            coordinates.read(reader)
            self.coordinates.append(coordinates)           
  
  
class KreedObjectMesh:
    def __init__(self):
        self.name = ''
        self.vertexCount = 0
        self.faceCount = 0
        self.vertexes = []
        self.vertexes2 = []
        self.faceIndexes = []
        self.faceIndexes2 = []
        self.unkCount1 = 0   
        self.unkCount2 = 0
        
    def readHeader(self, reader):
        self.name = reader.readBytes(68).decode('ascii').rstrip('\0')
        self.vertexCount = reader.readUShort()         
        self.faceCount = reader.readUShort() 
        reader.seek(2, NOESEEK_REL)         
        self.vertexCount2 = reader.readUShort()         
        self.faceCount2 = reader.readUInt()         
        reader.seek(24, NOESEEK_REL) 

    def readData(self, reader):
        for i in range(self.faceCount):
            indexes = Vector3UI16()
            indexes.read(reader)

            self.faceIndexes.append(indexes)
           
        for i in range(self.vertexCount):
            vert = KreedMeshVertex()
            vert.read(reader)

            self.vertexes.append(vert)

        reader.seek(2 * self.vertexCount, NOESEEK_REL) #

        for i in range(self.faceCount2):
            indexes = Vector3UI16()
            indexes.read(reader)

            self.faceIndexes2.append(indexes)
           
        for i in range(self.vertexCount2):
            vert = KreedMeshWeghtedVertex()
            vert.read(reader)

            self.vertexes2.append(vert)                        

    def read(self, reader):
        self.readHeader(reader)
        self.readData(reader)
 

class KreedModelBone:
    def __init__(self):    
        self.index = 0
        self.name = ""
        
    def read(self, reader): 
        self.index = reader.readShort()      
        reader.seek(2, NOESEEK_REL)
        try:         
            self.name = reader.readBytes(64).decode('ascii').rstrip('\0')
        except:
            pass      
  
  
class KreedModel:
    def __init__(self, reader):
        self.reader = reader
        self.version = 0
        self.boneCount = 0
        self.meshCount = 0
        self.boneList = []
        self.meshes = []
           
    def readHeader(self, reader):
        magic = reader.readUInt()   
        self.version = reader.readUShort()             
        reader.seek(64, NOESEEK_REL) # name
        self.meshCount = reader.readUShort()   
        self.boneCount = reader.readUShort()   
        reader.seek(14, NOESEEK_REL) 
        
    def readMeshes(self, reader):
        for i in range(self.meshCount):
            mesh = KreedObjectMesh()
            mesh.read(reader)

            self.meshes.append(mesh)

    def readBoneNames(self, reader):
        for i in range(self.boneCount):
            bone = KreedModelBone()
            bone.read(reader)
            self.boneList.append(bone)
                        
    def read(self):
        self.readHeader(self.reader)
        self.readBoneNames(self.reader)       
        self.readMeshes(self.reader) 

    
def kreedModelCheckType(data):     
    
    return 1     
    

def kreedModelLoadModel(data, mdlList):
    #noesis.logPopup()

    model = KreedModel(NoeBitStream(data))
    model.read()
   
    ctx = rapi.rpgCreateContext()
    
    materials = []
    textures = []    
    
    textureName = noesis.getSelectedDirectory() + "/tex/crbb1.dds" 
    normalTextureName = noesis.getSelectedDirectory() + "/tex/crbnm.dds"
    
    texList = [textureName, normalTextureName]
    for texName in texList:
        texture = rapi.loadExternalTex(texName)
        textures.append(texture)           
        
    material = NoeMaterial("mat", textureName)
    material.setNormalTexture(normalTextureName)
    material.setFlags(noesis.NMATFLAG_TWOSIDED, 1)
    materials.append(material)   
    
    for mesh in model.meshes:
        rapi.rpgSetName(mesh.name)
        rapi.rpgSetMaterial("mat")
        
        for face in mesh.faceIndexes:
            rapi.immBegin(noesis.RPGEO_TRIANGLE)
            
            for index in face.getStorage():
                rapi.immNormal3(mesh.vertexes[index].normal.getStorage()) 
                rapi.immUV2(mesh.vertexes[index].uv.getStorage())            
                rapi.immVertex3(mesh.vertexes[index].coordinates[0].getStorage()) 
       
            rapi.immEnd()  
            
        # for face in mesh.faceIndexes2:   
            # rapi.immBegin(noesis.RPGEO_TRIANGLE)
            
            # for index in face.getStorage():
                # for i in range(6):                    
                    # rapi.immVertex3(mesh.vertexes2[index].coordinates[i].getStorage()) 
                    
            # rapi.immEnd() 
                
    mdl = rapi.rpgConstructModelSlim()
    #mdl.setModelMaterials(NoeModelMaterials(textures, materials))     
    mdlList.append(mdl)        
            
    return 1
 