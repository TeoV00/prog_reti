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
#se il file esiste lo cancello dalla directory
    if exists(name_file):
        os.remove(name_file)
        print("File vecchio rimosso\n")
        #scarico il file da github elo salvo nella dir. corrente
    wget.download(DATA_FILE,OUT_PATH_JSON)
    pathFile = OUT_PATH_JSON + '/' + name_file
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

def genPrenotVisita():
    bodyPage = ''
    return topHTML + prenTitle + topHTML2 + bodyPage + bottomHTML

    
    
    
    
    
    
    
    