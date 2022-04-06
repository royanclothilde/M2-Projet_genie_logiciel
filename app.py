# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 19:35:20 2020

@author: jerom
"""

#se mettre dans le cmd
#set FLASK_APP=app.py
#set FLASK_ENV=development
#=> flask run
# taper dans le navigateur : http://127.0.0.1:5000/
# bien ouvrir le prompt dans le dossier du code 

from flask import Flask, render_template, request
import psycopg2
import json
import random
import os.path 
import io
import random
from flask import Response
from matplotlib.figure import Figure
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from matplotlib import pyplot as plt
import base64
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
#        ,data=[{'name':'Auvergne Rhone Alpes'}, {'name':'Bourgogne Franche Comte'}, {'name':'Bretagne'}, {'name':'Centre Val de Loire'}, {'name':'Corse'}, {'name':' Grand est'},{'name':'Hauts-de-France'},{'name':'Ile-de-France'},{'name':' Nouvelle Aquitaine'},{'name':'Normandie'},{'name':'Occitanie'},{'name':'Pays de la Loire'}, {'name':'Provence Alpes Cote d Azur'}])

# Importation des accès à POSTGRE
with open("Configuration/postgre.json") as file:
    postgre = json.load(file)


connection = psycopg2.connect(
    host=postgre["host"],
    database=postgre["database"],
    user=postgre["user"],
    password=postgre["password"])


cursor = connection.cursor()
 # Print PostgreSQL Connection properties
print ( connection.get_dsn_parameters(),"\n")

#  # Print PostgreSQL version
# cursor.execute("SELECT version();")
# record = cursor.fetchone()
# print("You are connected to - ", record,"\n")
# postgres_insert_query = """ insert into consommation (idconsommation, consommationgaz, consommationelec) VALUES(DEFAULT, '3000', '4');  """

# cursor.execute(postgres_insert_query)

# connection.commit()
# count = cursor.rowcount
# print (count, "Record inserted successfully into consommation table")
# PEOPLE_FOLDER = os.path.join('static', 'people_photo')

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/function_sreen', methods=["GET","POST"])
def function_sreen():    

    

       global value
       if request.method == 'POST':
           post_idtemp = request.form.get('temperature_button')
           post_idconso_elec = request.form.get('conso_electrique_button')
           post_idconso_gaz = request.form.get('conso_gaz_button')
           
           regions= request.form.get('regions')
           
           post_date_start1 = request.form.get('start')
           post_date_start2 = request.form.get('start2')
           
          # sélection de la conso ele  et gaz selon la date et la région et la temp associée
           if (post_idconso_gaz is not None and post_idtemp is not None and post_idconso_elec is not None) and post_date_start1 != post_date_start2 :
               
                   cursor.execute("select date, nom_region, consommation_electricite, consommation_gaz, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date between %s and %s and nom_region = %s order by date", [post_date_start1,post_date_start2,regions])
                   data = cursor.fetchall() 
                   df = pd.DataFrame(list(data),columns=["date","region","gaz","elec", "temperature"])
                   x = df.date
                   y = df.temperature
                   V = df.region

                   graphe_alt = df.plot(x='date',y='temperature', title='Température journalière en '+ str (V[0]), grid='true', fontsize=6).get_figure()
                   buf = io.BytesIO()
                   graphe_alt.savefig(buf, format='png')
                   buf.seek(0)
                   buffer = b''.join(buf)
                   b2 = base64.b64encode(buffer)
                   graphe_alt2=b2.decode('utf-8')
                   
                   #tracage courbe conso elec
                   df1 = pd.DataFrame(list(data),columns=["date","region","gaz","elec", "temperature"])
                   x1 = df1.date
                   y1 = df1.elec

                   graphe_alt3 = df.plot(x='date',y='elec', title='Consommation journalière d electricite en MW en '+ str (V[0]), grid='true', fontsize=6).get_figure()
                   buf1 = io.BytesIO()
                   graphe_alt3.savefig(buf1, format='png')
                   buf1.seek(0)
                   buffer1 = b''.join(buf1)
                   b3 = base64.b64encode(buffer1)
                   graphe_alt4=b3.decode('utf-8')
                   
                   #tracage courbe conso gaz
                   df2 = pd.DataFrame(list(data),columns=["date","region","gaz","elec", "temperature"])
                   x2 = df2.date
                   y2 = df2.gaz
                   graphe_alt5 = df.plot(x='date',y='gaz', title='Consommation journalière de gaz en MW en '+ str (V[0]), grid='true', fontsize=6).get_figure()
                   buf2 = io.BytesIO()
                   graphe_alt5.savefig(buf2, format='png')
                   buf2.seek(0)
                   buffer2 = b''.join(buf2)
                   b4 = base64.b64encode(buffer2)
                   graphe_alt6=b4.decode('utf-8')
                   
                   
                   
                   
                   return render_template("index.html", value=data,graphe_alt=graphe_alt2, graphe_alt3=graphe_alt4, graphe_alt5=graphe_alt6 )
               
                
          

           elif (post_idconso_gaz is not None and post_idtemp is not None and post_idconso_elec is not None) and post_date_start1 == post_date_start2 : 
                   cursor.execute("select date, nom_region, consommation_electricite, consommation_gaz, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date = %s and nom_region = %s order by date", [post_date_start1, regions])
                   data = cursor.fetchall() 
                   return render_template("index.html", value=data)



           elif (post_idconso_elec is not None and post_idtemp is not None) and post_date_start1 == post_date_start2 :
                   cursor.execute("select date, nom_region, consommation_electricite, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date = %s and nom_region = %s", [post_date_start1,regions])
                   data = cursor.fetchall() 
                   return render_template("index.html", value=data)
               
                # consommation elec, intervalle ok
                
                
                
           elif (post_idconso_elec is not None and post_idtemp is not None) and post_date_start1 != post_date_start2 :
                   #consommation de gaz sur un intervalle de date
                   cursor.execute("select date, nom_region, consommation_electricite, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date between %s and %s and nom_region = %s order by date", [post_date_start1,post_date_start2,regions])    
                   data = cursor.fetchall() 
                   df = pd.DataFrame(list(data),columns=["date","region", "elec", "temperature"])
                   x = df.date
                   y = df.temperature
                   V = df.region
                   graphe_alt = df.plot(x='date',y='temperature', title='Température journalière en MW en '+ str (V[0]), grid='true', fontsize=6).get_figure()
                   buf = io.BytesIO()
                   graphe_alt.savefig(buf, format='png')
                   buf.seek(0)
                   buffer = b''.join(buf)
                   b2 = base64.b64encode(buffer)
                   graphe_alt2=b2.decode('utf-8')
                   
                   #tracage courbe conso elec
                   df1 = pd.DataFrame(list(data),columns=["date","region","elec", "temperature"])
                   x1 = df1.date
                   y1 = df1.elec
            
                   graphe_alt3 = df.plot(x='date',y='elec', title='Consommation journalière d electricite en MW en '+ str (V[0]), grid='true', fontsize=6).get_figure()
                   buf1 = io.BytesIO()
                   graphe_alt3.savefig(buf1, format='png')
                   buf1.seek(0)
                   buffer1 = b''.join(buf1)
                   b3 = base64.b64encode(buffer1)
                   graphe_alt4=b3.decode('utf-8')
                   return render_template("index.html", value=data,graphe_alt=graphe_alt2, graphe_alt3=graphe_alt4)     
               
            

            
           # Consommation gaz
           elif (post_idconso_gaz is not None and post_idtemp is not None) and post_date_start1 != post_date_start2 :
               #consommation de gaz sur un intervalle de date
               cursor.execute("select date, nom_region, consommation_gaz, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date between %s and %s and nom_region = %s order by date", [post_date_start1,post_date_start2,regions])    
               data = cursor.fetchall() 
               df = pd.DataFrame(list(data),columns=["date","region","gaz", "temperature"])
               x = df.date
               y = df.temperature
               V = df.region
               graphe_alt = df.plot(x='date',y='temperature', title='Température journalière en '+ str (V[0]), grid='true', fontsize=6).get_figure()
               buf = io.BytesIO()
               graphe_alt.savefig(buf, format='png')
               buf.seek(0)
               buffer = b''.join(buf)
               b2 = base64.b64encode(buffer)
               graphe_alt2=b2.decode('utf-8')
            #tracage courbe conso gaz
               df2 = pd.DataFrame(list(data),columns=["date","region","gaz", "temperature"])
               x2 = df2.date
               y2 = df2.gaz
               graphe_alt5 = df.plot(x='date',y='gaz', title='Consommation journalière de gaz en MW en '+ str (V[0]), grid='true', fontsize=6).get_figure()
               buf2 = io.BytesIO()
               graphe_alt5.savefig(buf2, format='png')
               buf2.seek(0)
               buffer2 = b''.join(buf2)
               b4 = base64.b64encode(buffer2)
               graphe_alt6=b4.decode('utf-8')
                               
               
               
               
               return render_template("index.html", value=data,graphe_alt=graphe_alt2, graphe_alt5=graphe_alt6 )         
           elif (post_idconso_gaz is not None and post_idtemp is not None) and post_date_start1 == post_date_start2 :
               #consommation de gaz sur une seule date
               cursor.execute("select date, nom_region, consommation_gaz, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date = %s and nom_region = %s", [post_date_start1,regions])
               data = cursor.fetchall() 
               return render_template("index.html", value=data)
           
           # if post_idconso_gaz is not None and post_idtemp is not None and post_idconso_elec is not None :    
           #     cursor.execute("select date, nom_region, consommation_gaz, consommation_electricite, t_moyenne from relation join region on (relation.code_insee=region.code_insee) join consommation on (consommation.id_conso=relation.id_conso) join temperature on (relation.id_temperature=temperature.id_temperature) where date = %s and nom_region = %s", [post_date_start1,regions])
           #     data = cursor.fetchall() 
           #     return render_template("index.html", value=data)



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

images_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = images_folder

@app.route('/France.png')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'France.png')
    return render_template("index.html", user_image = full_filename)


def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == '      ': #faire quelque chose
            pass # do something
        elif request.form['submit_button'] == '      ': # faire quelque chose d'autre
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

    
