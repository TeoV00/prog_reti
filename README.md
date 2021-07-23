# WebServer Reti
Webserver di una ipotetica azienda ospedaliera
la home page presenta diversi link che portano a pagine indipendenti che
mostrano infomrazioni o possono fornire servizi per i pazienti.

Nella pagina di prenotazione è quindi possbile effettuare una prenotazione
per un prestazione sanitaria, lasciando la possbilità di scegliere il medico
e la tipologia di servizio. E' obbligatoria la compilazione dei campi Nome e 
Cognome.
una volta effettuata la prenotazione si viene reindirizzati ad una pagina di
avvenuta registrazione della prenotazione.

Cliccando sul link "Statistiche Covid" viene aperta una pagina in cui è presente
la tabella aggiornata dei dati sulle vaccinazioni Covid-19.
I dati vengono prelevati ad ogni caricamento della pagina, direttamente dal repository
github della Presidenza del Consiglio dei Ministri, che giornalmente viene aggiornato.

Il link "Regolamento (PDF)" permette lo scaricamento di un file PDF.

Per finire il sito web oltre a fornire Info come orario e numeri di telefono utili nella 
apposita pagina cliccando il link "Info", permette l'accesso come amministratore.
In questa paginaè possibile aggiungere e togliere medici, indicando nome e codice medico 
(attualmente per la cancellazione occorre solo il nome).
Conclusa la modifica si viene reindirizzati ad una pagina di conferma, in caso contrario
si visualizzerà una pagina di errore con un link per ritornare indietro.
Dopo ogni modifica occorre, per sicurezza, rieffettuare il login.
Ovviamente è presente un pulsante per visulaizzare l'elenco dei medici attualmente presenti
del database (file json).
In questa pagina sono mostrate anche tutte le prenotazioni effettuate dai pazienti in una 
tabella. Sono indicati nome, congome, codDottore e servizio richiesto.

Da notare che le modifiche effettuate sui medici (aggiunta/rimozione) si ripercuote sull'elenco
dei medici selezionabile all'atto di prneotazione di una prestazione nella pagina "Prenota Prestazione".

## Moduli python utilizzati:
	
	socketserver
	http.server
	sys
	signal
	
	cgi
	json
	w3lib.url
Per installare le librerie mancanti utilizzare il package manager pip tramite terminale
	pip install [nome pacchetto]

## Utilizzo
Da terminale avviare il webServer con il comando:

	python3 server.py [port]

il campo port se non specificato è 8080
Per accedere al sito web collegarsi a localhost:[port] oppure all'ip della macchina su cui 
è in esecuzione il server.

## Credenziali accesso pagina Amministratore
Se si volgiono aggiungere credenziali/utenti admin, occorre modificare il file login.json

User: admin
Password: password

oppure

User: reti
Password: esame
