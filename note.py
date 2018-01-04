import os

class note:

    pisah = "~"
    def __init__( self, user_id,folder):
      self.filetxt = user_id + ".txt"
      self.pathScript =os.path.dirname(os.path.realpath('__file__'))
      self.pathfile =os.path.join(self.pathScript,folder)
      self.pathtxt = os.path.join(self.pathfile,self.filetxt)
    
    def validFolderFile(self):
        if (not os.path.exists(self.pathfile)):
            os.makedirs(self.pathfile)
        if(not os.path.exists(self.pathtxt)):
            fo = open(self.pathtxt, "w")
            fo.close
    def inputData(self,stringMasukan):
        self.validFolderFile()
        fo = open(self.pathtxt, "a")
        fo.write(stringMasukan + "~\n")
        fo.close()
    def isDataExist(self):
        if os.path.isfile(self.pathtxt):
            return os.path.getsize(self.pathtxt)>0
        else:
            return os.path.isfile(self.pathtxt) 
    def readData(self):
        #I.S : file tidak boleh kosong
        #F.s : ngehasilin array dari hasilnya di split ~\n
        fo = open(self.pathtxt, "r")
        data = fo.read()
        fo.close()
        return data.split('~\n')
    def deleteAllData(self):
        fo = open(self.pathtxt,"w")
        fo.close()

    def deleteData(self,nomor):
        data = self.readData()
        del data[nomor-1]
        fo = open(self.pathtxt,"w")
        for dat in data:
            fo.write(dat+"~\n")
        fo.close()