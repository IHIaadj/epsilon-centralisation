# Classe representant un terminal
import json
import socket


"""

    CreateGroup(group): Créer un groupe de terminaux
            =====> Retourne
                ERREUR_GROUPE_EXISTANT : group exists
                SUCCESS  : group added


    CreateTerminal(name,ipaddress,password,groupe) : Crée un terminal dans le groupe donné
            =====> Retourne
                    ERREUR_GROUPE_INEXISTANT : groupe inexistant
                    ERREUR_IP_INVALIDE : Ip address is invalid
                    ERREUR_IP_EXISTANTE : Ip address exists
                    ERREUR_NOM_EXISTANT : Name exists
                    objet de type Terminal : Tout est valide

    DeleteTerminal(name,groupe) : Supprime un terminal dans un groupe
            =====> Retourne
                    ERREUR_GROUPE_INEXISTANT : groupe inexistant
                    ERREUR_NOM_INEXISTANT : terminal name inexistant
                    SUCCESS : supprimé avec succès

    def EditTerminal(name,groupe,newName,newIp,newPwd,newGroupe) : modifier un terminal défini par (name,groupe)
            =====> Retourne
                ERREUR_NOM_EXISTANT : le nom newName est existant
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_IP_INVALIDE : Ip invalide
                ERREUR_IP_EXISTANTE : Ip existante
                ERREUR_NOM_INEXISTANT : terminal name inexistant
                SUCCESS : modifié avec succès


    getTerminalByName(name,groupe) : Retourne un objet de type terminal sous la forme:
                terminal.getName()
                terminal.getIp()
                terminal.getGroupe()
                terminal.getPwd()

            =====> Retourne
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_NOM_INEXISTANT : terminal name inexistant
                objet termianl : le terminal existe

    getTerminalByIp(ipaddress,groupe)
            =====> Retourne
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_IP_INVALIDE : ip invalide
                ERREUR_IP_INEXISTANTE : ip inexistante
                objet terminal : s'il est trouvé.. Objet de type Terminal

    getIpsList():
            =====> Retourne
                ERREUR_GROUPE_INEXISTANT : le groupe n'existe pas
                la liste des adresses Ip : si pas de pb

    getAllIps(): Retourne la liste des @Ip de tous les groupes

    getGroupesList(): Retourne la liste des groupes de terminaux
"""
class Terminal:
    def __init__(self,name,ipaddress,password,groupe):
        self.name=name
        self.ip=ipaddress
        self.pwd=password
        self.groupe=groupe

    def getGroupe(self):
        return sefl.groupe
    def getName(self):
        return self.name
    def getIp(self):
        return self.ip
    def getPwd(self):
        return self.pwd
    def modify(self,newName,newIp,newPwd,newGroupe):
        self.pwd=newPwd
        self.name=newName
        self.groupe=newGroupe
        self.ip=newIp

class TerminalManager:
    ALL_TERMINALS={}
    FILE_NAME="terminaux.json"
    INITIALIZED=False

    ERREUR_IP_INEXISTANTE = -7
    ERREUR_NOM_INEXISTANT = -6
    ERREUR_GROUPE_EXISTANT = -5
    ERREUR_GROUPE_INEXISTANT=-4
    ERREUR_IP_INVALIDE=-3
    ERREUR_IP_EXISTANTE=-2
    ERREUR_NOM_EXISTANT=-1
    SUCCESS=0

    def CreateGroup(group):
        """
            returns:
                ERREUR_GROUPE_EXISTANT : group exists
                SUCCESS  : group added
        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        if group not in TerminalManager.ALL_TERMINALS:
            TerminalManager.ALL_TERMINALS[group]=[]
            TerminalManager.save_all_terminals()
            return TerminalManager.SUCCESS
        else :
            return TerminalManager.ERREUR_GROUPE_EXISTANT
    def CreateTerminal(name,ipaddress,password,groupe):
        """
            returns:
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_IP_INVALIDE : Ip address is invalid
                ERREUR_IP_EXISTANTE : Ip address exists
                ERREUR_NOM_EXISTANT : Name exists
                objet de type Terminal : Tout est valide
        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        # Input validation
        try:
            socket.inet_aton(ipaddress)
        except socket.error:
            return TerminalManager.ERREUR_IP_INVALIDE
        #Si le groupe existe, on fait une recherche pour voir si l'association nom/@IP existe.
        if groupe in TerminalManager.ALL_TERMINALS:
            for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
                if TerminalManager.ALL_TERMINALS[groupe][i].getIp()==ipaddress:
                    return TerminalManager.ERREUR_IP_EXISTANTE
                if TerminalManager.ALL_TERMINALS[groupe][i].getName().lower()==name.lower():
                    return TerminalManager.ERREUR_NOM_EXISTANT
        else:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT

        terminal=Terminal(name,ipaddress,password,groupe)

        TerminalManager.ALL_TERMINALS[groupe].append(terminal)
        TerminalManager.save_all_terminals()


        return terminal


    def load_all_terminals(): #json file .json input
        try:
            f=open(TerminalManager.FILE_NAME)
            toTransform=json.loads(f.read())
            for groupe in toTransform:
                TerminalManager.ALL_TERMINALS[groupe]=[]
                for term in toTransform[groupe]:
                    TerminalManager.ALL_TERMINALS[groupe].append(Terminal(term["name"],term["ip"],term['pwd'],groupe))
        except FileNotFoundError:
            with open(TerminalManager.FILE_NAME,"w") as f:
                f.write(json.dumps(TerminalManager.ALL_TERMINALS))
        TerminalManager.INITIALIZED=True

        return TerminalManager.ALL_TERMINALS

    def save_all_terminals():
        toSave={}
        for groupe in TerminalManager.ALL_TERMINALS:
            toSave[groupe]=[]
            for term in TerminalManager.ALL_TERMINALS[groupe]:
                toSave[groupe].append({
                            "name":term.getName(),
                            "ip":term.getIp(),
                            "pwd":term.getPwd()
                         })
        with open(TerminalManager.FILE_NAME,"w") as f:
            f.write(json.dumps(toSave))

    def DeleteTerminal(name,groupe):
        """
            returns
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_NOM_INEXISTANT : terminal name inexistant
                SUCCESS : supprimé avec succès
        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        if groupe not in TerminalManager.ALL_TERMINALS:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT

        for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
            if TerminalManager.ALL_TERMINALS[groupe][i].getName().lower()==name.lower():
                del TerminalManager.ALL_TERMINALS[groupe][i]
                TerminalManager.save_all_terminals()
                return TerminalManager.SUCCESS
        return TerminalManager.ERREUR_NOM_INEXISTANT

    def EditTerminal(name,groupe,newName,newIp,newPwd,newGroupe):
        """
            returns
                ERREUR_NOM_EXISTANT : le nom newName est existant
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_IP_INVALIDE : Ip invalide
                ERREUR_IP_EXISTANTE : Ip existante
                ERREUR_NOM_INEXISTANT : terminal name inexistant
                SUCCESS : modifié avec succès
        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        try:
            socket.inet_aton(newIp)
        except socket.error:
            return TerminalManager.ERREUR_IP_INVALIDE

        if newGroupe not in TerminalManager.ALL_TERMINALS:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT

        for i in range(len(TerminalManager.ALL_TERMINALS[newGroupe])):
            if TerminalManager.ALL_TERMINALS[newGroupe][i].getName().lower()==newName.lower():
                return TerminalManager.ERREUR_NOM_EXISTANT
            if TerminalManager.ALL_TERMINALS[newGroupe][i].getIp()==newIp:
                return TerminalManager.ERREUR_IP_EXISTANTE

        for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
            if TerminalManager.ALL_TERMINALS[groupe][i].getName().lower()==name.lower():
                TerminalManager.ALL_TERMINALS[groupe][i].modify(newName,newIp,newPwd,newGroupe)
                TerminalManager.ALL_TERMINALS[newGroupe].append(TerminalManager.ALL_TERMINALS[groupe][i])
                del TerminalManager.ALL_TERMINALS[groupe][i]
                TerminalManager.save_all_terminals()
                return TerminalManager.SUCCESS
        return TerminalManager.ERREUR_NOM_INEXISTANT

    def getTerminalByName(name,groupe):
        """
            returns
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_NOM_INEXISTANT : terminal name inexistant
                objet termianl : le terminal existe

        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        if groupe not in TerminalManager.ALL_TERMINALS:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT
        for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
            if TerminalManager.ALL_TERMINALS[groupe][i].getName().lower()==name.lower():
                return TerminalManager.ALL_TERMINALS[groupe][i]
        return TerminalManager.ERREUR_NOM_INEXISTANT

    def getTerminalByIp(ip,groupe):
        """
            returns
                ERREUR_GROUPE_INEXISTANT : groupe inexistant
                ERREUR_IP_INVALIDE : ip invalide
                ERREUR_IP_INEXISTANTE : ip inexistante
                objet terminal : le terminal existe

        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        if groupe not in TerminalManager.ALL_TERMINALS:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT

        try:
            socket.inet_aton(ip)
        except socket.error:
            return TerminalManager.ERREUR_IP_INVALIDE

        if groupe not in TerminalManager.ALL_TERMINALS:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT

        for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
            if TerminalManager.ALL_TERMINALS[groupe][i].getIp()==ip:
                return TerminalManager.ALL_TERMINALS[groupe][i]
        return TerminalManager.ERREUR_IP_INEXISTANTE

    def getIpsList(groupe):
        """
            returns
                ERREUR_GROUPE_INEXISTANT : le groupe n'existe pas
        """
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        if groupe not in TerminalManager.ALL_TERMINALS:
            return TerminalManager.ERREUR_GROUPE_INEXISTANT

        liste_ips=[]
        for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
            liste_ips.append(TerminalManager.ALL_TERMINALS[groupe][i].getIp())
        return liste_ips

    def getGroupesList():
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        return list(TerminalManager.ALL_TERMINALS.keys())

    def getAllIps():
        if(not TerminalManager.INITIALIZED):
            TerminalManager.load_all_terminals()

        liste_ips=[]
        for groupe in TerminalManager.ALL_TERMINALS:
            for i in range(len(TerminalManager.ALL_TERMINALS[groupe])):
                liste_ips.append(TerminalManager.ALL_TERMINALS[groupe][i].getIp())
        return liste_ips
