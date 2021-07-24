#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIOLANI MATTEO 
MATRICOLA: 921109

PROGETTO DI PROGRAMMAZIONE RETI, TRACCIA 2 WEB-SERVER
@author: teo
"""
import sys, signal
import http.server
import socketserver
import cgi
import json
import HTMLdataGenerate as HTMLgen

#modulo per estrapolazione di parametri da richiesta tipo GET
#da installare pip install w3lib
from w3lib.url import url_query_parameter as url_param

ADMIN_PATH_PAGE = "html/admin.html"
INFO_PATH = 'html/info.html'

PRENOT_PAGE = '/prenVisita.html'
ADMIN_PAGE = '/admin.html'
COVID_PAGE = '/covid.html'
INFO_PAGE = '/info.html'
ADD_DOTT = 'add'
RMV_DOTT = 'remove'
PREN_PAGE = '/prenVisita.html'

#configurazione porta socket server, se non specificata il default è 8080
if sys.argv[1:] :
    port = int(sys.argv[1])
else:
    port = 8080

server_addr= ('',port)

#pagina di accesso alla schermata da amministratore
logInPage= '''<html><body>
                <form method="post" accept-charset=utf-8>
                <h2>Accesso Amministratore</h2>
                <p>
				<label for="user">User: </label>
  				<input type="text" id="user" name="user"><br>
			</p>
			<p>
				<label for="psw">Password: </label>
  				<input type="password" id="psw" name="psw"><br><br>
			</p>
			<input type="submit" value="login" style="">
                </form>
                </body></html>'''
                
#pagina di negato login causa password o user non corretti
loginErrorPage= '''<html>
<body><h2>User o Password Errate</h2>
<p>Clicca qui per riprovare--> <a href="admin.html">riprova<a></p>
</body></html>'''

addDoctorSuccessPage ='''<html>
<body><h2>Aggiunta/Rimozione dottore avvenuta con successo</h2>
<p>Clicca qui per tonrare indietro--> <a href="admin.html">Indietro<a></p>
</body></html>'''

editDoctorFailPage = '''<html>
<body><h2>Aggiunta/Rimozione dottore NON CONCLUSA</h2>
<p>Il nome inserito non corripsonde a nessun medico presente nel sistema</p>
<p>Clicca qui per tonrare indietro--> <a href="admin.html">Indietro<a></p>
</body></html>'''

#
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def logInPage(self):
        self.send_response(307) #codice stato http di temporaneo reindirizzamento
        self.end_headers()
        self.wfile.write(bytes(logInPage, 'utf-8'))
            
    def failDoctorPage(self):
        self.send_response(200)
        self.end_headers()
        #invio di pagina di errore rimozione dottore
        self.wfile.write(bytes(editDoctorFailPage, 'utf-8'))
        
    def editDoctorRequest(self):
        request = self.path
        # estrapolazione dati prenotazione ricevuti dal form
        nameDoctor= url_param( request,'dottName')
        codeDoctor= url_param( request,'dottSurn')
        editMode= url_param(request, 'mode')
#       print(nameDoctor)
#       print(codeDoctor)
#       print(editMode)
        #memorizzazione nuovo medico nel file json (databse ipotetico)
        with open("json/dottori.json", "r+") as out:
                #conversione dei file json in oggetto python--> vocabolario
                dott =json.loads(out.read())
                #aggiunta del dottore inserito nel file
                try:
                    if editMode == ADD_DOTT:
                        #se i campi sono vuoti non aggiungere medico vuoto
                        if (not nameDoctor) or (not codeDoctor):
                            #se uno dei due campi è vuoto si genera una eccezione
                            #che manda al client la pagina di fallimento aggiunta
                           raise TypeError
                        else:
                           dott["name"].append(nameDoctor)
                           dott["surn"].append(codeDoctor)
                    else:
                       #richiesta di cancellazione dottore, effetuata solo 
                       #se presente nel database
                       if nameDoctor in dott["name"] and editMode == RMV_DOTT:
                           #ricava l'indice in cui si trova il cod. del medico
                           idx_name = dott["name"].index(nameDoctor)
                           
                           #rimozione di nameDoctor e codeDoctor dal dizionario python
                           #che poi sara convertito in file json
                           dott["name"].pop(idx_name)
                           dott["surn"].pop(idx_name)
                       
                       else:
                          raise TypeError

                    print(dott)
                   
                    #cancellazione del file
                    out.seek(0)
                    out.truncate()
                    #scrittura dell'oggeto python in formato json
                    json.dump(dott,out)
                    #risposta di OK al client
                    self.send_response(200)
                    self.end_headers()
                    #invio di pagina di conferma aggiunta dottore
                    self.wfile.write(bytes(addDoctorSuccessPage, 'utf-8'))
                except:
                    self.failDoctorPage()

    def checkLogin(self):
        try:
            form = cgi.FieldStorage(    
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
            
            #estrapolo i campi immessi in delle variabili
            #(si trascura la sicurezza dei dati)
            user= form.getvalue('user')
            pssw= form.getvalue('psw')
            
            with open("json/login.json", "r") as inFile:
                #caricamento e conversione dati da formato json a 
                #dictionary di python
                users = json.loads(inFile.read())

                if (users[user] == pssw):
                    #se esiste l'username inserito si verifica che la password
                    #digitata corrisonda con quella salvata nel database (login.json)
                    self.send_response(200)
                    self.end_headers()
                    adminHTMLpage = HTMLgen.genAdminHTMLPage()
                    self.wfile.write(bytes(adminHTMLpage, 'utf-8'))

                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(bytes(loginErrorPage,'utf-8'))
                                    
        except :
            self.send_response(401)
            self.end_headers()
            self.wfile.write(bytes(loginErrorPage,'utf-8'))

    #in questo metodo si definisce come il server deve agirea richieste di tipo GET      
    def do_GET(self):
        request = self.path
        print('file REQUESTED: ' + request)
        #se si vuole accedere alla pagina da amministratore prima si viene reindirizzati
        #alla logInPage
        if request == ADMIN_PAGE:
            self.logInPage()
        else:
            #gestione della richiesta di aggiungere un nuovo medico;
            #verifico che la path ricevuta contenga i campi del form che rigurda
            #l'aggiunta del medico
            if (request.__contains__(ADMIN_PAGE) and 
                request.__contains__("dottName") and
                request.__contains__("dottSurn")):
                print("RICHIESTA AGGIUNTA DOTTORE")
                self.editDoctorRequest()
            else:
                if request == COVID_PAGE:
                    #il client ha rischiesto la pagina con i dati covid
                    self.send_response(200)
                    self.end_headers()
                    #scarico il file json con i dati delle vaccinazioni in locale
                    covidHTML = HTMLgen.refreshCovidData()
                    #restituisco la pagina con tab covid aggiornata
                    self.wfile.write(bytes(covidHTML, 'utf-8'))
                else:
                    if request == PREN_PAGE:
                        #il client ha richiesto la pagina delle prenotazioni
                        #genera la pagina delle prenotazioni a runtime
                        prenHTML = HTMLgen.genPrenotVisita()
                        self.send_response(200)
                        self.end_headers()
                        #invio la pagina della prenotazione al client in risposta
                        self.wfile.write(bytes(prenHTML, 'utf-8'))
                    else:
                        #se pagina info richiesta, reindirizzati alla corretta path
                        if request == INFO_PAGE:
                            self.path = INFO_PATH
                        #se non si tratta di nessun caso sopra chiamo il metodo del
                        #modulo per risolvere la richiesta e restituire il file
                        #, se presente nella path, corrispondente all 'url digitato
                        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def doPrenotazione(self):
        print('\nPrenotazione_POST')
        try:
            # estrapolazione dati prenotazione ricevuti dal form
            form = cgi.FieldStorage(    
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
        
        # Con getvalue prendo i dati inseriti dall'utente
            doctor = form.getvalue('doctor')
            healthService = form.getvalue('prestazione')
            name = form.getvalue('fname')
            lastName = form.getvalue('lname')

        # creo messaggio da restituire all'utente
            output="RICHIESTA ACCOLTA  NOME e COGNOME: " + name + " "+ lastName +" Prestazione: " + healthService + " Dottore: "+ doctor +"\n"
            succP1 = '''<html><body><h2>Aggiunta dottore avvenuta con successo</h2>''' +output
            succP2='''<br><p>Clicca qui per tonrare indietro--> <a href="/prenVisita.html">Indietro<a></p></body></html>'''
            #comunico al client che il mesasggio post è stato ricevuto correttamente
            self.send_response(200)
        except: 
            self.send_error(404, 'Campi non compilati presenti!')
            return;
        self.end_headers()
        #invio al client un messaggio di ricevuta consegna
        self.wfile.write(bytes(succP1+succP2, 'utf-8'))
        
        # Salvataggio prenotazione in formato json in un file (ipotetico database)
        with open("json/prenotazioni.json", "r+") as out:
            lines = out.readlines()
            #eliminazione ultime due righe di chiusura json
            out.seek(0)
            out.truncate()
            out.writelines(lines[:-2])
            #creazione stringa da aggiungere in fondo al file, per aggiungere
            #prenotazione nuova effettuata
            info = ',{"name": "' + name + '","lastName" :"' + lastName +'", "doctor" : "'+ doctor+ '","service" : "'+ healthService + '" } \n'
            info += '] \n }'
            #scrittura nuova prenotazione con chiusura oggetto json
            out.write(info)

    def do_POST(self):
        print("POST path: "+self.path)
        #con l'if vado a distiguere i casi dei due form, quello delle prenotazini
        #da quello utilizzato per il login dell'admin
        if (self.path == PRENOT_PAGE):
            self.doPrenotazione()
                
        else :
            #RICHIESTA (POST) LOGIN PAGINA ADMIN
            if (self.path == ADMIN_PAGE):
                print("\nlogin_POST")
                self.checkLogin()
                    
            else :
                self.send_error(404, 'Richiesta non gestita')

Handler = MyHttpRequestHandler
#configurazione di un server multi thread per consentire l'accesso multimo
server = socketserver.ThreadingTCPServer(server_addr,Handler)

server.daemon_threads = True 

#concede la riassegnazione del socket
server.allow_reuse_address = True


#funzione interupt per consentire l'arresto del server corretamente
def signal_handler(signal, frame):
    print("Ctrl+C premuto: interruzione http server...")
    try:
        if (server):
            server.server_close()
            print('server terminato correttamente')
    finally:
        sys.exit()
        
#l'interupt da tastiera (ctrl-c) avvia signal_handler
signal.signal(signal.SIGINT, signal_handler)
print("Server avviato correttamente\n")
print("...in attesa di richieste sulla porta: "+ str(port))
while True:
    server.serve_forever()

server.server_close()