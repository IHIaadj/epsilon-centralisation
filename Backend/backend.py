# Regrouper toutes les fonctions
import sys
import os
import subprocess
import re
import platform
import shutil
import json
import socket
from terminal import Terminal
from terminal import TerminalManager

''' Just for the tests had les variables globales sinon machi plassethoum :p '''

terminalManager =TerminalManager()

IP_TERMINALS = ["127.0.0.1"]
USERNAME='root'
ROOT_PASSWORD='0000'
SSH_PORT='3122'
PATH_TO_SCRIPTS="/home/masci/Desktop/Scripts/"
PATH_TO_LOCAL_REPO_FOLDER="/home/masci/Desktop/LocalRepo"
PATH_TO_REMOTE_REPO_FOLDER="/root/Desktop/LocalRepo"
BACKUPS_FOLDER="/home/masci/Desktop/bacdeb"
LOCAL_PACKAGES_LIST=['vlc','openJDK','ila akhirihi']
CONF_FILE='/home/masci/Desktop/conf.json'

def getSshSyntax(ip,scriptFileName):
    OS_Type = getOsType()
    with open(PATH_TO_SCRIPTS+scriptFileName, 'r') as scriptFile:
        commands=scriptFile.read().replace('\n', ' ')
    if (OS_Type == "Linux"):
        #SSH_Syntax = ['sshpass', '-p', ROOT_PASSWORD, 'ssh', '-p', SSH_PORT, USERNAME+'@'+ip, "'bash -s'" ,'<']
        SSH_Syntax = ['sshpass', '-p', ROOT_PASSWORD, 'ssh', '-p', SSH_PORT, USERNAME+'@'+ip,commands]
    else:
        SSH_Syntax = ['c:\\Windows\\System32\\cmd.exe','/c ', 'plink', '-P' ,SSH_PORT,  USERNAME+'@'+ip, '-pw', ROOT_PASSWORD,commands ]
    return SSH_Syntax

def getOsType():
    return platform.system()


def checkConnexion(ip):
    out = subprocess.check_output(getSshSyntax(ip,'checkconnexion.sh'))
    if "Online" in str(out) :
        return True
    return False

def getDiskUsage(ip):

    out = subprocess.check_output(getSshSyntax(ip,'diskusage.sh'))
    out = str(out)
    out = re.findall(r'([0-9]*\.[0-9]+|[0-9]+)', out)
    print("Taille : " , out[1])
    print("Used : ", out[2])
    print( out[4], "%")
    print(getSshSyntax(ip,'diskusage.sh'))


def getRamUsage(ip):
   # script= subprocess.check_output(['cat',PATH_TO_SCRIPTS+
    out = subprocess.check_output(getSshSyntax(ip,'ramusage.sh'))
    out = str(out)
    out = re.findall(r'([0-9]*\.[0-9]+|[0-9]+)', out)
    print("Dispo : " , out[2])


def getCpuUsage(ip):
   # script= subprocess.check_output(['cat',PATH_TO_SCRIPTS+
    out = subprocess.check_output(getSshSyntax(ip,'cpuusage.sh'))
    out = str(out)
    out = re.findall(r'([0-9]*\.[0-9]+|[0-9]+)', out)
    print(out[0] , "%")

def linkState(ip):
    out = subprocess.check_output(getSshSyntax(ip,'check.sh' ))
    out = str(out)
    if "ERROR" in out:
        return False
    return True

def installPackageFromInternet(ip,packageName):
    out = subprocess.check_output(getSshSyntax(ip,'installFromInternet.sh' )+[packageName])
    out = str(out)
    if "ERROR" in out:
        print(out)
        return False
    return True

def removePackage(ip,packageName):
    out = subprocess.check_output(getSshSyntax(ip,'removePackage.sh' )+[packageName])
    out = str(out)
    if "ERROR" in out:
        print(out)
        return False
    return True

def installPackageFromLocal(ip,packageName): #todo adapt it to windows
    #les packages local doivent etre dans des dossiers, tel que chaque dossier porte le nom du package est contient le package et toute ses dependendances
    out = subprocess.check_output(['scp','-r',USERNAME+'@'+ip+':',PATH_TO_LOCAL_REPO_FOLDER+'/'+packageName,PATH_TO_REMOTE_REPO_FOLDER+'/'+packageName+'/']) #transfer the packages
    out2 = subprocess.check_output(['sshpass', '-p', ROOT_PASSWORD, 'ssh', '-p', SSH_PORT, USERNAME+'@'+ip,'dpkq', '-i', PATH_TO_REMOTE_REPO_FOLDER+'/*.deb'])
    #todo check out2 for errors

def addPackageToLocalRepo(packageName): #works only on a debian host with the same cpu architecture as the terminal
    # create a directory with the name 'packageName'
    # if already exist just clean it (pour le mettre a jour)
    # 'cd' 7ta ltem and use this command to download package and it dependencies 'apt-get download $(apt-rdepends < package >| grep -v "^ ")'
    # add the package to LOCAL_PACKAGES_LIST

    path=PATH_TO_LOCAL_REPO_FOLDER+'/'+packageName
    packageAlreadyExists=os.path.exists(path)
    if packageAlreadyExists:
        shutil.rmtree(path)
    try:
        if not os.path.exists(PATH_TO_LOCAL_REPO_FOLDER) :
            os.mkdir(PATH_TO_LOCAL_REPO_FOLDER)

        os.mkdir(path)
    except OSError:
        #print("Creation of the directory %s failed" % path)
        pass
    else:
        pass
        #print("Successfully created the directory %s " % path)

    #print (path)
    os.system(' cd'+path)
   # out = subprocess.check_output(['ls',''])
    out2 = subprocess.check_output(['apt-get download $(apt-rdepends '+packageName+' | grep -v "^ ")'])
    if not packageAlreadyExists:
        LOCAL_PACKAGES_LIST.append(packageName)


def newBackup(ip,backupName):#works only on linux , rsync must be installed on both server and terminal
    path = BACKUPS_FOLDER + '/' + backupName
    packageAlreadyExists = os.path.exists(path)
    if packageAlreadyExists:
        shutil.rmtree(path)
    try:
        if not os.path.exists(BACKUPS_FOLDER):
            os.mkdir(BACKUPS_FOLDER)

        os.mkdir(path)
    except OSError:
        # print("Creation of the directory %s failed" % path)
        pass
    else:
        pass

    print('rsync', '-azAXv', '--delete','--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"}' , '--rsh='+'"sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'"',ip+':/',path)

    #out = subprocess.check_output(['rsync', '-azAXvh', '--delete' ,'--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"}' ,  '--rsh='+'"sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+ip+':/',path])
    out = subprocess.check_output('rsync '+ '-azAXv '+ '--delete '+'--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} ' + '--rsh='+'"sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+ip+':/ '+path,shell=True)
    print(out)
    #os.system('rsync '+ '-azAXv '+ '--delete '+'--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} ' + '--rsh='+'"sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+ip+':/ '+path)

def restoreFromBackup(ip,backupName):
    path = BACKUPS_FOLDER + '/' + backupName

    print('rsync '+ '-azAXv '+ '--delete '+ '--rsh="sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+path+' '+ip+':/')
    #out = subprocess.check_output(['rsync', '-azAXv '+ '--delete ' +'--progress ' + '--rsh="sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+backupFolderAndPath+' '+ip+':/'])
    #out = subprocess.check_output(['rsync', '-azAXvh', '--delete' ,'--progress','--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"}',path ,  '--rsh='+'"sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+ip+':/'])
    out = subprocess.check_output('rsync '+ '-azAXvh '+ '--delete ' +'--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} '+path +' --rsh='+'"sshpass -p '+ROOT_PASSWORD+' ssh -p '+SSH_PORT+' -o StrictHostKeyChecking=no -l '+ USERNAME+'" '+ip+':/',shell=True)
    print(out)


def start(): #charge la list des terminaux et les configuration de l'app
    global USERNAME
    global ROOT_PASSWORD
    global SSH_PORT
    terminalManager.load_all_terminals()
    with open(CONF_FILE, "r") as read_file:
        confDict=json.load(read_file)
    USERNAME = confDict['USERNAME']
    ROOT_PASSWORD = confDict['ROOT_PASSWORD']
    SSH_PORT = confDict['SSH_PORT']

def changeConf(rootUsername,rootPass,sshPort): #change les configuration de l'app
    global USERNAME
    global ROOT_PASSWORD
    global SSH_PORT
    USERNAME=rootUsername
    ROOT_PASSWORD = rootPass
    SSH_PORT = sshPort
    confDict = {"ROOT_PASSWORD":ROOT_PASSWORD,"USERNAME":USERNAME,"SSH_PORT":SSH_PORT}
    with open(CONF_FILE, "w") as write_file:
        json.dump(confDict, write_file)





#removePackage("127.0.0.1","ssh")

#getCpuUsage("127.0.0.1")
#getDiskUsage("127.0.0.1")
#addPackageToLocalRepo("nautilus")
#installPackageFromInternet("127.0.0.1","ssh")
#INTERNET_STATUS = checkConnexion("127.0.0.1")
#newBackup('127.0.0.1','bactroi')
#restoreFromBackup('127.0.0.1','bacun')
changeConf(USERNAME,ROOT_PASSWORD,SSH_PORT)
start()

#print(INTERNET_STATUS)
getDiskUsage("127.0.0.1")
#getRamUsage()
#getCpuUsage()

#linkState("127.0.0.1")
#linkState("127.0.0.3")