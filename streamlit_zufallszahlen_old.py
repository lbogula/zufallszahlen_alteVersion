# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 21:47:14 2022

Gibt Zufallszahlen mit fester, einstellbarer Summe aus. 

@author: Laura
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


st.title("Zufallszahlengenerator")

#Number Input, Zahleneingabe:

my_expander_Zahlen = st.expander("Eingabe von Gesamtsumme, \
                                 Mittelwert und Varianz")
with my_expander_Zahlen:
    Summe = st.number_input("Gesamtsumme eingeben",100)
    
    col11, col12 = st.columns(2)
    Mittelwert = col11.slider("Mittelwert",5.,10.,7.)
    Varianz = col12.slider("Varianz",0.1,5.,1.)
    Anzahl = int(np.round(Summe/Mittelwert))
    st.write("daraus berechnete Anzahl an Verkäufen = " , Anzahl)
    st.write("Anzahl = Summe/Mittelwert" )
    



st.success("eingegebene Werte: \n \n Summe = %.1f €, Mittelwert = %.1f €, \
           Varianz = %.1f € \n \n daraus ergeben sich %s Verkäufe" \
           %(Summe, Mittelwert,Varianz, Anzahl))



my_expander_minmax = st.expander(label='Minimal- und Maximalwerte für \
                                 einzelne Verkäufe definieren:')
with my_expander_minmax:
    col1, col2 = st.columns(2)
    col1.text("Minimum")
    Wert_min = col1.number_input("Minimalwert eingeben, z.B. 2",2)
    col2.text("Maximum")
    Wert_max = col2.number_input("Maximalwert eingeben, z.B. 2",15)

st.warning("Der gewählte Preis liegt zwischen: min = %.1f € und max = %.1f €" %(Wert_min,Wert_max))



#########################################################################

#st.markdown(" ##### Visualisierung: So sieht die gewählte Verteilung bei großer Stichprobegröße aus")
#st.text(" Die grünen Linien geben die Grenzen an unterhalb, bzw. oberhalb derer  \n abgeschnitten wird. Diese können oben manuell gesetzt werden.")
#Erstellen der Zufallsdaten zum Testen der Verteilung
Stichprobengröße = 200000

data = np.random.normal(Mittelwert, Varianz, Stichprobengröße)

#hist_values = np.histogram(data)[0]
#st.bar_chart(hist_values)

fig, ax = plt.subplots(figsize=(8,5))
ax.hist(data,bins=120)
ax.plot([Mittelwert,Mittelwert], [0, 6500],c='k')
ax.plot([Wert_min,Wert_min], [0, 6500],c='r')
ax.plot([Wert_max,Wert_max], [0, 6500],c='r')
ax.annotate("Mittelwert", (Mittelwert-1.2,6600),c='k')
ax.annotate("min", (Wert_min-0.4,6600),c='r')
ax.annotate("max", (Wert_max-0.4,6600),c='r')
ax.set_ylim(0,7000)
ax.set_xlabel("Verkaufswert \n \n rote Linien: Grenzen für Zufallszahlen",fontsize=14)
ax.set_ylabel("Anzahl", fontsize = 14)
#st.pyplot(fig)




# Mit Schleife bis es aufgeht:
def gibZufallszahlen(Summe,Anzahl,Mittelwert,Varianz):
    Fertig = False
    Anzahl_Versuche = 0
    
    while Fertig == False:
        Anzahl_Versuche = Anzahl_Versuche + 1
        x_list = []
        X_sum = 0
        i=0
        while i < (Anzahl-1):
            x = np.round(np.random.normal(Mittelwert,Varianz,1),1)
            if x>Wert_min and x<Wert_max:
                X_sum = X_sum + x
                x_list.append(x)
                i = i+1
                
        last_x = np.round(Summe-X_sum,1)
        print("Summe bis hier = %s, letztes x = %s"%(X_sum,last_x))
        if last_x<Wert_min or last_x>Wert_max: 
            print('please repeat')
        else:
            x_list.append(last_x)
        
        if len(x_list)==Anzahl:
            x_list_new = [x_list[r][0] for r in range(len(x_list))]
            return x_list_new
            Fertig = True
        if Anzahl_Versuche > 300:
            #st.error("Fehler: die Parameter (Mittelwert, Varianz und Grenzen) sind schlecht gewählt (siehe Gaußkurve), bitte ändern")
            Fertig = True



x = gibZufallszahlen(Summe,Anzahl,Mittelwert,Varianz)

if x != None:
    fig2, ax2 = plt.subplots(figsize=(8,5))
    ax2.hist(x,bins=Anzahl)
    ax2.plot([Mittelwert,Mittelwert], [0, 8],c='k')
    ax2.annotate("Mittelwert", (Mittelwert+0.25,8),c='k')
    ax2.set_xlabel("Verkaufswert ",fontsize=14)
    ax2.set_ylabel("Anzahl", fontsize = 14)
    #st.pyplot(fig2)
    
    export = str(x[0])   
    for ii in range(len(x)-1):
        export = export + "\n" + str(x[ii+1])  

    #st.write("Zahlen:", export)
    #st.download_button(label = "Download der  als txt", data = export, file_name="Zufallszahlen.txt")

    #st.subheader("Zufallszahlen")
    col1_ausgabe, col2_ausgabe = st.columns(2)
    col1_ausgabe.markdown("#### Gewählte Verteilung ")
    col1_ausgabe.pyplot(fig)
    #col1_ausgabe.write("rot: Grenzen für Zufallszahlen")
    col2_ausgabe.markdown("#### Zufallszahlen ")
    col2_ausgabe.pyplot(fig2)
    col2_ausgabe.success("Zahlen: %s" %x)
    col2_ausgabe.download_button(label = "Download der Zufallszahlen als txt", data = export, file_name="Zufallszahlen.txt")

else:
    col1_ausgabe, col2_ausgabe = st.columns(2)
    col1_ausgabe.markdown("#### Gewählte Verteilung ")
    col1_ausgabe.pyplot(fig)
    col1_ausgabe.write("grün: Grenzen für Zufallszahlen")
    col2_ausgabe.markdown("#### Zufallszahlen ")
    col2_ausgabe.error("Berechnung nicht möglich, Bitte Parameter (Mittelwert, Varianz und Grenzen) anpassen - siehe Verteilung links")


