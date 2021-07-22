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

topHTML2='''<div id="menuBar"><a class="menuLink" href="index.html">Home</a>
            <a class="menuLink" href="info.html">Info</a></p></div>'''
covidTitle= '<h2> Ospedale -> Statistiche Covid</h2>'
prenTitle= '<h2> Ospedale -> Prenota Prestazione</h2>'

bottomHTML= '''</div></body></html>'''

DATA_FILE= 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.json'
OUT_PATH_JSON = 'json' #relative path

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

    tableHeader= '<table><tr>'
    rowClose= '</tr>'
    tableClose = '</table>'
    headerRow = ''
    headerList = []

    #creazione intestazione della table
    for field in data["schema"]["fields"]:
        nameField = field["name"]
        headerList.append(nameField)
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

    table = tableHeader + dataRow + tableClose
    return topHTML+covidTitle+topHTML2 +table + bottomHTML

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
  					<option value="sangue">ananlisi sangue</option>
  					<option value="visita-specilistica">visita specilistica</option>
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
    
    for dottName in dott["name"]:
        idx_name = dott["name"].index(dottName)
        bodyPage += '<option value="'+ dott["code"][idx_name] +'">'+ dottName+'</option>'
    bodyPage += '</select>'

    return topHTML + prenTitle + topHTML2 + bodyPage + bottomBodyPrenot + bottomHTML

    
    
    
    
    
    
    
    