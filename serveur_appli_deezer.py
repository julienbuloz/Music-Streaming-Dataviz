#!/usr/bin/env python3
#-*-encoding: UTF-8-*-
# Python 3 server exampl
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import http.client
import json

Application_ID = "517382"
Application_Name = "projet_data_visualisation"
clef_secrete = "14abf7bc38c97bad63fda5a4b0cf028c"
code = None
access_token = "frFVqwbNUG5MCm03Ubgn96OE13yJiQUYjpicfkAehH4XospqMb3"


hostName = "localhost"
serverPort = 8080


def envoi(adresse, **argus):
    if "/" in adresse:
        adresse, chemin = adresse.split("/", 1)
        chemin = "/" + chemin
    else:
        chemin = "/"
    print("URL contactée: %s"%(adresse+chemin))
    print("arguments passés : %s"%str(argus))
    if len(argus) > 0:
        chemin += "?" + "&".join([x + "=" + argus[x] for x in argus])
    conn = http.client.HTTPSConnection(adresse)
    conn.request("GET", chemin)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read()
    if type(data1) is bytes:
        data1 = data1.decode("utf-8")
    try:
        data2 = json.loads(data1)
        data1 = data2
    except json.JSONDecodeError:
        print("Erreur au décodage du JSON !")
        print(data1)
    return data1

def recup_historique(acces):
    with open("écoutes.json", "r", encoding="utf-8") as F:
        ecoutes = json.load(F)
    print("Il y a %d écoutes dans le fichier"%len(ecoutes))
    ecoutes = {x["timestamp"]:x for x in ecoutes}
    nouveaux = envoi("api.deezer.com/user/me/history", access_token = acces, output = "json", version="js-v1.0.0")
    data = nouveaux["data"]
    if "next" in nouveaux:
        suite = nouveaux["next"]
        argus = suite.split("?",1)[1].split("&")
        argus = {y[0]:y[1] for x in argus if (y:=x.split("=")) }
        argus["output"] = "json"
        data2 = envoi("api.deezer.com/user/me/history", **argus)["data"]
        data.extend(data2)
    data = {x["timestamp"]:x for x in data}
    n = 0
    for ts in data:
        if not ts in ecoutes:
            ecoutes[ts] = data[ts]
            n += 1
    print("Il y a %d nouvelles écoutes depuis la dernière fois."%n)
    ecoutes = [ecoutes[x] for x in ecoutes]
    ecoutes.sort(key = lambda x: x["timestamp"])
    with open("écoutes.json", "w", encoding="utf-8") as F:
        F.write(json.dumps(ecoutes))
    print("Il y a désormais %d écoutes dans le fichier"%len(ecoutes))
    



contenu_rep = os.listdir("fichiers_pour_serveur_python")

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
      try:
        chaine = self.path
        if "?" in chaine:
            chemin, requete = chaine.split("?", 1)
        else:
            chemin = chaine
            requete = ""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print("chemin : %s"%chemin)
        print("requête : %s"%requete)
        dico={}
        dicx = requete.split("&")
        dicx = [x for x in dicx if "=" in x]
        for x in dicx:
            y = x.split("=", 1)
            dico[y[0]] = y[1]
        print("dico des paramètres : %s"%repr(dico))
        while chemin.startswith("/"):
           chemin = chemin[1:]
        if chemin == "":
           with open("fichiers_pour_serveur_python/accueil.html", "r") as F:
              self.wfile.write(bytes(F.read(), "utf-8"))
        elif chemin == "redirection.php":
            self.wfile.write(bytes("<html><head><title>titre</title><meta charset='UTF-8'/></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))           
            self.wfile.write(bytes("<h1>Redirigé</h1>", "utf-8"))
            self.wfile.write(bytes("<p><b>reçu</b> %s</p>"%repr(dico), "utf-8"))            
            code = dico["code"]            
            retour = envoi("connect.deezer.com/oauth/access_token.php", app_id = Application_ID, secret = clef_secrete, code = code, output = "json")
            self.wfile.write(bytes("<p><b>retour</b> %s</p>"%str(retour), "utf-8")) 
            self.wfile.write(bytes("</body></html>", "utf-8"))
            recup_historique(retour["access_token"])
            
            
        elif chemin in contenu_rep:
           with open("fichiers_pour_serveur_python/" + chemin, "r") as F:
              self.wfile.write(bytes(F.read(), "utf-8"))
        else:
            self.wfile.write(bytes("<html><head><title>titre</title><meta charset='UTF-8'/></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))           
            self.wfile.write(bytes("<p>Requête: %s</p>" % chaine, "utf-8"))
            self.wfile.write(bytes("<p>Ceci est un exemple de serveur web.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
      except ConnectionResetError:
        print("Connexion stoppée")


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Serveur démarré http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Serveur arrêté.")
