# Regrouper toutes les fonctions 
import sys 
import subprocess
import re 

''' Just for the tests had les variables globales sinon machi plassethoum :p '''
INTERNET_STATUS = checkConnexion() 
IP_TERMINALS = ["127.0.0.1"]

def checkConnexion(): 
    out = subprocess.check_output(['c:\\Windows\\System32\\cmd.exe','/c ', 'plink',  'user@127.0.0.1', '-pw', 'password', '-P' ,'2222',  '-m' ,'checkconnexion.sh'])
    if "Online" in str(out) : 
        return True 
    return False 

def getDiskUsage(ip):
    out = subprocess.check_output(['c:\\Windows\\System32\\cmd.exe','/c ', 'plink',  'user@',ip, '-pw', 'password', '-P' ,'2222',  '-m' ,'diskusage.sh'])
    out = str(out)
    out = re.findall(r'([0-9]*\.[0-9]+|[0-9]+)', out)
    print("Taille : " , out[1])
    print("Used : ", out[2])
    print( out[4], "%")


def getRamUsage(ip): 
    out = subprocess.check_output(['c:\\Windows\\System32\\cmd.exe','/c ', 'plink',  'user@',ip,  '-pw', 'password', '-P' ,'2222',  '-m' ,'ramusage.sh'])
    out = str(out)
    out = re.findall(r'([0-9]*\.[0-9]+|[0-9]+)', out)
    print("Dispo : " , out[2])


def getCpuUsage(ip): 
    out = subprocess.check_output(['c:\\Windows\\System32\\cmd.exe','/c ', 'plink',  'user@',ip,  '-pw', 'password', '-P' ,'2222',  '-m' ,'cpuusage.sh'])
    out = str(out)
    out = re.findall(r'([0-9]*\.[0-9]+|[0-9]+)', out)
    print(out[0] , "%")

def linkState(ip): 
    out = subprocess.check_output(['c:\\Windows\\System32\\cmd.exe','/c ', 'plink',  'user@',ip, '-pw', 'password', '-P' ,'2222', '-m', 'check.sh' ])
    out = str(out)
    if "ERROR" in out: 
        return False 
    return True 


print(INTERNET_STATUS)
getDiskUsage("127.0.0.1")
#getRamUsage()
#getCpuUsage()

linkState("127.0.0.1")
linkState("127.0.0.3")