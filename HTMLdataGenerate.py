#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:23:54 2021

@author: teo
"""

import json
import wget #se non presente va installato 

from os.path import exists, os

topHTML = '''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>
<style>
#menuBar{
text-align: center;
color: black;
}
.menuLink{
color: black;}
.menuLink:hover{
color: grey;}
</style>
<body>
<div>
<p>'''

covidTitle= '<h2> Ospedale -> Statistiche Vaccinazioni Covid</h2>'
prenTitle= '<h2> Ospedale -> Prenota Prestazione</h2>'
adminTitle= '<h2> Ospedale -> Administration</h2>'

topHTML2='''<div id="menuBar"><a class="menuLink" href="index.html">Home</a>
            <a class="menuLink" href="info.html">Info</a></p></div>'''


bottomHTML= '''</div></body></html>'''

DATA_FILE= 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.json'
OUT_PATH_JSON = 'json' #relative path

def convertLabelCovid(nameField):
    #se nameField non corrispopnde a nessun caso viene restituito non modificato
    newLabel = nameField
    if nameField == "percentuale_somministrazione":
        newLabel = '%'
    if nameField == "dosi_somministrate":
        newLabel = "somministrate"
    if nameField == "dosi_consegnate":
        newLabel =  "consegnate"
    if nameField == "nome_area":
        newLabel = "regione"
    return newLabel

def refreshCovidData():
    name_file= wget.detect_filename(DATA_FILE)
    pathFile = OUT_PATH_JSON + '/' + name_file
    #se il file esiste lo cancello dalla directory
    if exists(pathFile):
        os.remove(pathFile)
        print("File vecchio rimosso\n")
        #scarico il file da github elo salvo nella dir. corrente
    wget.download(DATA_FILE,OUT_PATH_JSON)
    
    #apro il file e lo converto tramite modulo json in oggetto python (dictionary)
    with open(pathFile,"r") as data:
        lines = data.read()
        data=json.loads(lines)

    tableHeader= '<table id="covidTable"><tr>'
    rowClose= '</tr>'
    tableClose = '</table>'
    headerRow = ''
    #array di intestazioni della tabella
    headerList = []

    #creazione intestazione della table
    for field in data["schema"]["fields"]:
        nameField = field["name"]
        if nameField != "ultimo_aggiornamento":
            headerList.append(nameField)
        nameField = convertLabelCovid(nameField)
        if nameField != "ultimo_aggiornamento":
            headerRow += '<th>'+ nameField +'</th>'
        
    #composizione di header table dati
    tableHeader += headerRow + rowClose

    dataRow = ''
    #creazione righe tabella con valori presi dal file json
    for dataValue in data["data"]:
        dataRow += '<tr>'
        for dataName in headerList:
            #creazione delle colonne di una riga della tabella con i dati
            dataRow += '<td>'+ str(dataValue[dataName]) +'</td>'
            
        dataRow += '</tr>'
        
        dataTime=data["data"][0]["ultimo_aggiornamento"]
    lastUpdateInfo = '<p>Ultimo aggiornamento: </p>' + dataTime
    table = tableHeader + dataRow + tableClose
    return topHTML+covidTitle+topHTML2 + lastUpdateInfo + table + bottomHTML

topBodyPrenot= '''
<div>
		<form method="post" accept-charset=utf-8>
			<div>
				Selezionare Dottore:'''
				#qui va inserito il selettore con elenco aggiornato 
bottomBodyPrenot='''				
			</div>
			<div>
				<p> Selezionare prestazione: 
					<select name="prestazione" style="font-size: 12pt">
 					<option value="tampone">Tampone</option>
  					<option value="sangue">analisi sangue</option>
  					<option value="visita-specialistica">visita specialistica</option>
  					<option value="intervento">intervento</option>
					</select>
				</p>
			</div>
			<p>
				<label for="fname">Nome:</label>
  				<input type="text" id="fname" name="fname"><br>
			</p>
			<p>
				<label for="lname">Cognome:</label>
  				<input type="text" id="lname" name="lname"><br><br>
			</p>
			<input type="submit" value="Submit" style="">
		</form>
	</div>
'''

def genPrenotVisita():
    #con questo metodo si genera la pagina della prenotazione con la select list
    #aggiornata con i medici nuovi aggiunti
    bodyPage = topBodyPrenot + '<select name="doctor" style="font-size: 12pt">'
    with open("json/dottori.json", "r") as out:
        lines = out.read()
        dott=json.loads(lines)
    
    for dottCode in dott["code"]:
        idx_code = dott["code"].index(dottCode)
        code_name_dott = dott["name"][idx_code]+' '+dottCode
        print(code_name_dott + ' '+ dottCode)
        bodyPage += '<option value="'+ dott["code"][idx_code]+'">'+ code_name_dott+'</option>'
    bodyPage += '</select>'

    return topHTML + prenTitle + topHTML2 + bodyPage + bottomBodyPrenot + bottomHTML

formDott = '''
<div id="doctorManage">
	<h3>Gestione Dottori</h3>
	<p>Il dottore aggiunto sarà visibile nell'elenco dei dottori nella sezione "Prenota prestazione"</p>
	    <form method="get" accept-charset=utf-8>
		<p>
		<label for="dottName">Nome:</label>
  		<input type="text" id="dottName" name="dottName"><br>
		</p>
		<p>
		<label for="dottCode">Codice:</label>
  		<input type="text" id="dottCode" name="dottCode"><br><br>
		</p>
		<p>(Nella rimozione occorre solo il codice del dottore)</p>
		<p>
		<label for="mode">Aggiungi</label>
  		<input type="radio" id="modeAdd" name="mode" value="add" checked="checked">
  		<br>
  		<label for="mode">Rimuovi</label>
  		<input type="radio" id="modeRemove" name="mode" value="remove">
  		</p>
		<input type="submit" value="Applica" style="">
		<input type="reset">
	     </form>
 '''
formDottClose= '</table><div id="tableDott"></div></div>'
prenView='''<div id="prenotView"><h3>Elenco Prenotazioni</h3>'''

def genAdminHTMLPage():
    #metodo per la generazione della pagina di Amministrazione con tabelle
    #aggiornate di medici e visite
    dottTable = '<table><tr> <th>Nome</th><th>Cod.Dottore</th></tr>'
    
    pageHTML= topHTML + adminTitle +topHTML2+formDott
    with open("json/dottori.json", "r") as out:
        lines = out.read()
        dott=json.loads(lines)

    for dottCode in dott["code"]:
        idx_name = dott["code"].index(dottCode)
        dottTable +="<tr><td>"+dott["name"][idx_name]+"</td><td>"+ dottCode +"</td></tr>"
    
    dottTable += formDottClose
    pageHTML += dottTable + prenView
    
    #generazione tabella prenotazioni
    prenTable = '''<table><tr> <th>Nome</th><th>Cognome</th><th>Dottore</th>
                    <th>Cod.Dottore</th><th>Servizio</th></tr>'''
    
    with open("json/prenotazioni.json", "r") as out:
        lines = out.read()
        pren=json.loads(lines)
        
    #costruzione della tabella prenotazioni
    for pren in pren["prenotazioni"]:
        dottCode=pren["doctor"]
        
        if dottCode in dott["code"]:
            idx_name = dott["code"].index(dottCode)
            nameD=dott["name"][idx_name]
        else:
            nameD=" "
        prenTable += ('<tr><td>'+pren["name"]+'</td><td>'+pren["lastName"]+'</td><td>'+
                       nameD +'</td><td>'+pren["doctor"]+'</td><td>'+pren["service"]+'</td></tr>')
    prenTable +='</table></div>'
    
    pageHTML += prenTable+bottomHTML
    return pageHTML;
