#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:09:50 2019

@author: florian
"""

"""TODO:
    Filepath für Windows anpassen (OS erkennen?)
    User für Raspi einrichten und im code anpassen
    


"""


import paramiko
import pysftp
import tkinter as tk
from tkinter import messagebox
import time
import re


#%% Funktionen

def verbinden():
    verbindenKnopf.configure(state = tk.DISABLED)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    try:
        ssh.connect("raspberrypi.local", 22, "pi", "raspberry")
    except:
        verbindenInfo.configure(text = "Verbindungsfehler")
        verbindenKnopf.configure(state = tk.NORMAL)
    
    global channel
    channel = ssh.invoke_shell()
    time.sleep(1)
    verbindenInfo.configure(text = "Verbindung Aufgebaut")
    if channel.closed == True:
        verbindenInfo.configure(text = "Verbindungsfehler")
        verbindenKnopf.configure(state = tk.NORMAL)
    window.update_idletasks()

def spektrumAufnehmen(belichtung, bild):
    global befehl
    global bildZahl
    schleifenEnde = str("work")
    aufnahmeStatus = str()
    schleifenFehler = 0
    
    befehl = "python3 spectrometer.py Spektrum" + str(bild) + " " + str(belichtung) + "\n"
    channel.send(befehl)
    
    spektrumAufnehmenKnopf.configure(state = tk.DISABLED)
    
    while bool(re.search("work", schleifenEnde)) == True or schleifenFehler < 5 or bool(re.search("Done", schleifenEnde)) == False :
        if channel.recv_ready():
            aufnahmeStatus = channel.recv(9999)
            aufnahmeStatus = str(aufnahmeStatus)
            
            if bool(re.search("exposure", aufnahmeStatus)) == True:
                exposure = re.findall(r"[-+]?\d*\.\d+|\d+", aufnahmeStatus)
                belichtungStatus.configure(text = "Belichtung: " + str(exposure))
        if bool(re.search("pi@raspberrypi", aufnahmeStatus)) == True:
            schleifenFehler += 1
            
        if schleifenFehler >= 10:
            spektrumAufnehmenStatus.configure(text = "Fehler: Bitte Spektrum erneut aufnehmen")
            window.update_idletasks()
            time.sleep(10)
            break
    
        spektrumAufnehmenStatus.configure(text = "Status: " + aufnahmeStatus )
        schleifenEnde = aufnahmeStatus
        window.update_idletasks()
        time.sleep(0.5)
     
    graphAbholen()               
    spektrumAufnehmenStatus.configure(text = "Status: ")
    spektrumAufnehmenKnopf.configure(state = tk.NORMAL)
    bildZahl += 1
    
    window.update_idletasks()
        
    
    
   
    

def setBelichtungszeit():
    global belichtungszeit
    belichtungszeit =  zeit.get()
    try:
        belichtungszeit = int(belichtungszeit)
        status.configure(text = "Belichtungszeit: " + str(belichtungszeit)) 
    except:
        belichtungszeit = 1000
        status.configure(text = valueError)
    
    
    

def graphAbholen():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  
    spektrumAufnehmenStatus.configure(text = "Status: Transfer Data")
    window.update_idletasks()
    with pysftp.Connection(host = "raspberrypi.local" , username = "pi", password = "raspberry", cnopts=cnopts) as sftp:
        time.sleep(.5)
   
        ##Graph abholen
        remotefilepath = "/home/pi/Spektrum" + str(bildZahl) + "_chart.png"
        localfilepath = "/home/florian/Pictures/RaspiPics/Spektrum" + str(bildZahl) + "_chart.png"
        sftp.get(remotefilepath, localfilepath)
        ##RAW abholen
        remotefilepath = "/home/pi/Spektrum" + str(bildZahl) + "_raw.jpg"
        localfilepath = "/home/florian/Pictures/RaspiPics/Spektrum" + str(bildZahl) + "_raw.jpg"
        sftp.get(remotefilepath, localfilepath)
        ##Auswertung abholen
        remotefilepath = "/home/pi/Spektrum" + str(bildZahl) + "_out.jpg"
        localfilepath = "/home/florian/Pictures/RaspiPics/Spektrum" + str(bildZahl) + "_out.jpg"
        sftp.get(remotefilepath, localfilepath)
        ##CSV Abholen
        remotefilepath = "/home/pi/Spektrum" + str(bildZahl) + ".csv"
        localfilepath = "/home/florian/Pictures/RaspiPics/Spektrum" + str(bildZahl) + ".csv"
        sftp.get(remotefilepath, localfilepath)
        

def hilfeBox():
    hilfetext = """Hinweise zum Bedienen des Programs \n
    Stellen sie zunächst die Verbindung zum Spektrometer über die Schaltfläche "Verbindung herstellen" her \n
    Als nächstes geben sie eine Belichtungszeit an, die Belichtungszeit wird in Millisekunden angegeben \n
    Über den Knopf "Spektrum Aufnehmen" nehmen sie Ihr Spektrum auf, es kann je nach Belichtungszeit bis zu mehrere Minuten dauern bis das Spektrum aufgenommen wurde \n 
    Der Wert für die Belichtung sollte stehts zwischen 0.15 und 0.3 liegen, passen sie evtl. die Belichtungszeit entsprechend an \n
    Die Daten aus dem Spektrometer sollten nach erfolgreicher Aufnahme in der Bildergalerie zu finden sein."""
    tk.messagebox.showinfo(title = "Hilfe", message = hilfetext)
            



#%% Fenster

global exposure
global aufnahmeStatus
exposure = 0.
aufnahmeStatus = ""

global valueError
valueError = "Status: FEHLER! Bitte nur ganze Zahlen eingeben"

global defaultStatus
defaultStatus = "Status: "

global belichtungszeit
belichtungszeit = 1000

global verbindenText
verbindenText = "Mit Spektrometer verbinden"

global bildZahl
bildZahl = 0

window = tk.Tk()
window.title("Spektrometer")
window.geometry('450x150')


verbindenInfo = tk.Label(window, text = verbindenText )
verbindenInfo.grid(column = 0, row = 0)

verbindenKnopf = tk.Button(window, text = "Ok", command = verbinden)
verbindenKnopf.grid(column = 1, row = 0)


lbl = tk.Label(window, text="Belichtungszeit in ms")
lbl.grid(column=0, row=1)

zeit = tk.Entry(window,width=10)
zeit.grid(column=1, row=1)

belichtungKnopf = tk.Button(window, text="Ok", command=setBelichtungszeit)
belichtungKnopf.grid(column=2, row=1)

status = tk.Label(window, text = " ")
status.grid(column = 0, row = 2)


spektrumAufnehmenInfo = tk.Label(window, text = "Spektrum aufnehmen")
spektrumAufnehmenInfo.grid(column = 0, row = 3)

spektrumAufnehmenKnopf = tk.Button(window, text = "Ok", command = lambda: spektrumAufnehmen(belichtungszeit, bildZahl))
spektrumAufnehmenKnopf.grid(column = 1, row = 3)

spektrumAufnehmenStatus = tk.Label(window, text = "Status: ")
spektrumAufnehmenStatus.grid(column = 0, row = 4)

belichtungStatus = tk.Label(window, text = "Belichtung: " + str(exposure))
belichtungStatus.grid(column = 0, row = 5)

hilfeknopf = tk.Button(window, text = "Hilfe", command = hilfeBox)
hilfeknopf.grid(column = 0, row = 6)


window.mainloop()



