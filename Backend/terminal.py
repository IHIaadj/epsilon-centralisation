# Classe representant un terminal
import json
import socket


class Terminal:
    ALL_TERMINALS=[]
    FILE_NAME="terminaux.json"
    INITIALIZED=False
    def CreateTerminal(name,ipaddress,password):
        """
            returns:
                -3 : Ip address is invalid
                -2 : Ip address exists
                -1 : Name exists
                objet de type Terminal : Tout est valide
        """
        if(not Terminal.INITIALIZED):
            Terminal.load_all_terminals()
            Terminal.INITIALIZED=True

        # Input validation
        try:
            socket.inet_aton(ipaddress)
        except socket.error:
            return -3
        for i in range(len(Terminal.ALL_TERMINALS)):
            if Terminal.ALL_TERMINALS[i]["ip"].lower()==ipaddress.lower():
                return -2
            if Terminal.ALL_TERMINALS[i]["name"].lower()==name.lower():
                return -1

        return Terminal(name,ipaddress,password)

    def __init__(self,name,ipaddress,password):
        self.name=name
        self.ip=ipaddress
        self.pwd=password
        entry = {
                    "name":self.name,
                    "ip":self.ip,
                    "pwd":self.pwd
                }
        Terminal.ALL_TERMINALS.append(entry)
        Terminal.save_all_terminals()


    def load_all_terminals(): #json file .json input
        try:
            f=open(Terminal.FILE_NAME)
            Terminal.ALL_TERMINALS= json.loads(f.read())
        except FileNotFoundError:
            with open(Terminal.FILE_NAME,"w") as f:
                f.write(json.dumps(Terminal.ALL_TERMINALS))

        return Terminal.ALL_TERMINALS

    def save_all_terminals():
        with open(Terminal.FILE_NAME,"w") as f:
            f.write(json.dumps(Terminal.ALL_TERMINALS))

    def deleteTerminal(name):
        """
            returns
                -1 : terminal name inexistant
                0 : supprimé avec succès
        """
        for i in range(len(Terminal.ALL_TERMINALS)):
            if Terminal.ALL_TERMINALS[i]["name"].lower()==name.lower():
                del Terminal.ALL_TERMINALS[i]
                Terminal.save_all_terminals()
                return 0
        return -1
