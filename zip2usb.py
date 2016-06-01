import pdb
import pprint
import os,sys
import os.path
from os.path import expanduser
import shutil
from time import gmtime, localtime, strftime
import subprocess
import wmi

path2Backup=backupFolder=   [r"C:\Users\Moshe\Google Drive"]
backupDrive=                         "E:"
backupPath=                          os.path.join(backupDrive,"backups")
zipProg=                                r"C:\Program Files\7-Zip\7z"
backupFileName=                   "backup"


def getFreeSpace(backupDrive):
    c = wmi.WMI ()
    for d in c.Win32_LogicalDisk():
        if d.Caption == backupDrive:
            print "Drive {0} free space={1}".format( d.Caption, d.FreeSpace)
            return int(d.FreeSpace)

def getCurrentDate():
    return strftime("%Y%m%d_%H_%M_%S", localtime()) 
    
class backupInfo:
    def __init__(self,bInstance=None):
        if bInstance==None:
            self.setDefault()
        else:    
            self.bInfo=bInstance
            
    def setDefault(self):       
        self.bInfo={}    
        self.bInfo["name"]       = "tbd" 
        self.bInfo["date"]       = getCurrentDate()         
        self.bInfo["zipFileName"]   = ''    
        self.bInfo["fileCnt"]    = 0
        self.bInfo["unzippedfileCnt"]   = 0
        self.bInfo["source"]     = ""
        self.bInfo["backupHome"]  =""
        
    def getInfo(self):
        return self.bInfo
        
    def getFileToBackup(self):
        return self.getCryptFileName()
        
    def setBackupHome(self,home):
        self.bInfo["backupHome"]=home
        
    def getName(self):
        return self.bInfo["name"]
        
    def setName(self,name):
        self.bInfo["name"]=name
        
    def printMe(self):
        print json.dumps(self.bInfo, sort_keys=True, indent=4)
     
    def getBackFileName(self):
        return self.bInfo["zipFileName"]
 
    def setFileNames(self,zipFileName):
        zf=zipFileName+"_{0}.7z".format(self.bInfo["date"])
        self.bInfo["zipFileName"]   = os.path.join(self.bInfo["backupHome"],zf)
 
    def setBackSource(self,source):
        self.bInfo["source"] = source

    def getBackSource(self):
        return self.bInfo["source"]

    def getDate(self):
        return self.bInfo["date"]   

    def setZipStartDate(self):
        self.bInfo["zipStartDate"]=getCurrentDate()
        
    def setZipEndDate(self):
        self.bInfo["zipEndDate"]=getCurrentDate()    
        
  
class zipIt_7z:
    def __init__(self,bInfo):
        self.bInfo=bInfo
        bInfo.setZipStartDate()
        print("Begin at "+ bInfo.getDate())    
        print "Start Zipping google drive"
        zFile=bInfo.getBackFileName()
        for elem  in path2Backup:
            try:    
                rc = subprocess.call([zipProg, 'a', '-mhe=on', '-pSecret', zFile,elem])
                print "Moving Zipped file to USB drive"
            except Exception as e:
                print e
                bInfo.incUnzippedfileCnt()
                print "********* failed to zip {0}".format(name)
                sys.exit(1)
                
        shutil.move(zFile, backupPath)           
        bInfo.setZipEndDate()                        
        print("Finished at "+strftime(getCurrentDate())) # Time in Greenwich time.
  
      
def setBackupHome(backupHome,bd=backupDrive):
    if not os.path.isdir(backupHome):
        try:
            os.makedirs(backupHome)
        except:
            print("Failed to create backup home dir {0}".format(backupHome))
            sys.exit(1)
  
    if not os.path.isdir(bd):
        try:
            os.makedirs(bd)
        except:
            print("Failed to create backup home dir {0}".format(bd))
            sys.exit(1)  
 
 
def setBackupEnv(backupFolder):
    bInfo=backupInfo()
    home = expanduser("~")  #Setup backup path home
    backupDir="backupWorkingFolder"
    backupHome=os.path.join(home,backupDir)  
    setBackupHome(backupHome)
    bInfo.setBackupHome(backupHome)
    bInfo.setBackSource(backupFolder)        #setup backup source path
    zf=backupFileName                          #Setup zip file name based on the backup source
    bInfo.setName(zf)
    bInfo.setFileNames(zf)
    return bInfo
    
    
if __name__ == "__main__":
    pdb.set_trace()
    freeSpace=getFreeSpace(backupDrive)
    bInfo=setBackupEnv(backupFolder)
    zipIt_7z(bInfo)
    sys.exit(0)
    

    
 
 
 

