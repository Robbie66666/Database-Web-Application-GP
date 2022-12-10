from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import os 
import csv
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from dbConnection import OracleDB

print ("__name__:",__name__)
app= Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'
#models ###models almost represent a table in the DB 
class User():
    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=password

#####################

@app.route('/', methods=['GET','POST'])
@app.route('/football',methods=['GET','POST']) ##insert for football
def football():##insert for football
    print('in football:', request.method)
    if request.method == "POST":
        file =request.files ['dataFile']
        print('in football:', "POST IF STATEMENT")
        if file: ##this mean
            filename=secure_filename(file.filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            #print("file_path:",file_path)
            file.save(file_path)



            data=[]
            with open(file_path) as file_object:
                reader_obj=csv.reader(file_object)

                next(reader_obj)##SKIPS A ROW 
                
            
                for row in reader_obj:
                    #print(row)
                    data.append(row)
                
                if data:
                    with OracleDB().get_connection() as connection:
                        #print(data)

                        ##insert for football
                        insert_statement= '''
                                 INSERT INTO FOOTBALL_MATCHES
                                        (
                                        
                                        FB_DATE,
                                        FB_HOME_TEAM,
                                        FB_AWAY_TEAM,
                                        FB_H_CONTINENT,
                                        FB_A_CONTINENT,
                                        FB_HT_SCORE,
                                        FB_AT_SCORE,
                                        FB_TOURNAMENT,
                                        FB_CITY,
                                        FB_COUNTRY,
                                        FB_N_LOCATION,
                                        FB_SHOOT_OUT,
                                        FB_HT_RESULT)

                                        VALUES(
                                        
                                        :FB_DATE,
                                        :FB_HOME_TEAM,
                                        :FB_AWAY_TEAM,
                                        :FB_H_CONTINENT,
                                        :FB_A_CONTINENT,
                                        :FB_HT_SCORE,
                                        :FB_AT_SCORE,
                                        :FB_TOURNAMENT,
                                        :FB_CITY,
                                        :FB_COUNTRY,
                                        :FB_N_LOCATION,
                                        :FB_SHOOT_OUT,
                                        :FB_HT_RESULT)
                                        '''

                        print('Insert Statement:', insert_statement)
                        cursor=connection.cursor() 
                        cursor.executemany(insert_statement, data)
                        connection.commit()


                        ##refreshes employeepage 
                        return redirect( url_for('football') )

                        
            

    elif request.method =="GET":
        with OracleDB().get_connection() as connection:
            ##insert  for football
            query = '''
                    select * from FOOTBALL_MATCHES 
                    '''
            cursor=connection.cursor()
            cursor.execute(query)
            data=cursor.fetchall() #gets all records

            print(len(data)) 
            
    
        return render_template("football.html",title="football", data=data)

@app.route('/football_edit/<id>',methods=['GET','POST'])
def football_edit(id):
    print('in football_edit:', request.method)
    print('football id:',id)###th
    data = None
    if request.method == 'GET':
         ##insert  for football
        with OracleDB().get_connection() as connection:
           query = '''
                    select * from FOOTBALL_MATCHES where FB_ID = :FB_ID
                    '''
        cursor=connection.cursor()
        cursor.execute(query,FB_ID=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button
 ##insert  for football

        FB_DATE= request.form.get('FB_DATE')
        FB_HOME_TEAM= request.form.get('FB_HOME_TEAM')
        FB_AWAY_TEAM= request.form.get('FB_AWAY_TEAM')
        FB_H_CONTINENT= request.form.get('FB_H_CONTINENT')
        FB_A_CONTINENT= request.form.get('FB_A_CONTINENT')
        FB_HT_SCORE= request.form.get('FB_HT_SCORE')
        FB_AT_SCORE= request.form.get('FB_AT_SCORE')
        FB_TOURNAMENT= request.form.get('FB_TOURNAMENT')
        FB_CITY= request.form.get('FB_CITY')
        FB_COUNTRY= request.form.get('FB_COUNTRY')
        FB_N_LOCATION= request.form.get('FB_N_LOCATION')
        FB_SHOOT_OUT= request.form.get('FB_SHOOT_OUT')
        FB_HT_RESULT= request.form.get('FB_HT_RESULT')
        
        
        datetime_object=datetime.strptime(str(FB_DATE), '%Y-%m-%d %H:%M:%S')


        

        



        with OracleDB().get_connection() as connection:
             ##insert  for football
            query='''
            update FOOTBALL_MATCHES 
            set
            FB_DATE=:FB_DATE,
            FB_HOME_TEAM=:FB_HOME_TEAM,
            FB_AWAY_TEAM=:FB_AWAY_TEAM,
            FB_H_CONTINENT=:FB_H_CONTINENT,
            FB_A_CONTINENT=:FB_A_CONTINENT,
            FB_HT_SCORE=:FB_HT_SCORE,
            FB_AT_SCORE=:FB_AT_SCORE,
            FB_TOURNAMENT=:FB_TOURNAMENT,
            FB_CITY=:FB_CITY,
            FB_COUNTRY=:department_id,
            FB_N_LOCATION=:FB_N_LOCATION,
            FB_SHOOT_OUT=:FB_SHOOT_OUT,
            FB_HT_RESULT=:FB_HT_RESULT
            where FB_ID=:FB_ID
        '''
 ##insert  for football
        cursor=connection.cursor()
        cursor.execute(query,FB_ID=id,FB_DATE=FB_DATE,FB_HOME_TEAM=FB_HOME_TEAM,FB_AWAY_TEAM=FB_AWAY_TEAM,FB_H_CONTINENT=FB_H_CONTINENT,
        FB_A_CONTINENT=FB_A_CONTINENT,FB_HT_SCORE=FB_HT_SCORE,FB_AT_SCORE=FB_AT_SCORE,FB_TOURNAMENT=FB_TOURNAMENT,FB_CITY=FB_CITY,
        FB_COUNTRY=FB_COUNTRY,FB_N_LOCATION=FB_N_LOCATION,FB_SHOOT_OUT=FB_SHOOT_OUT,FB_HT_RESULT=FB_HT_RESULT
        )
        print(type(datetime_object))
        print(datetime_object)
        connection.commit()
        return redirect( url_for('football') )


    return render_template("football_edit.html",title=" edit football", data=data)





@app.route('/football_delete/<id>',methods=['GET','POST'])
def football_delete(id):
    print('in football_delete:', request.method)

    print('football id:',id)###only for deleting and editing a record due to the ID


    data = None
    if request.method == 'GET':
        with OracleDB().get_connection() as connection:
           ##insert  for football
           query = '''
                    select * from FOOTBALL_MATCHES where FB_ID = :FB_ID
                    '''
        cursor=connection.cursor()
        cursor.execute(query,FB_ID=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button

           ##insert  for football
        with OracleDB().get_connection() as connection:
            query='''
            delete from FOOTBALL_MATCHES 
            where  FB_ID = :FB_ID
            
        '''

        cursor=connection.cursor()
        cursor.execute(query,FB_ID=id)
      
        connection.commit()
        return redirect( url_for('football') )


    return render_template("football_delete.html",title=" delete football", data=data)



@app.route('/football_add/',methods=['GET','POST'])
def football_add():
    print('in employee_add:', request.method)
    data = None
    if request.method == 'GET':
        return render_template("football_add.html",title=" Add Employees")
        
    elif request.method == 'POST':##save button
        with OracleDB().get_connection() as connection:
##insert  for footbal
            cursor=connection.cursor()##open database with cursor
            insert_statement="""
                                 INSERT INTO FOOTBALL_MATCHES
                                        (
                                        FB_ID,
                                        FB_DATE,
                                        FB_HOME_TEAM,
                                        FB_AWAY_TEAM,           
                                        FB_H_CONTINENT,
                                        FB_A_CONTINENT,
                                        FB_HT_SCORE,
                                        FB_AT_SCORE,
                                        FB_TOURNAMENT,
                                        FB_CITY,
                                        FB_COUNTRY,
                                        FB_N_LOCATION,
                                        FB_SHOOT_OUT,
                                        FB_HT_RESULT)
                                    
                                         VALUES(
                                        :FB_ID,
                                        :FB_DATE,
                                        :FB_HOME_TEAM,
                                        :FB_AWAY_TEAM,                                      
                                        :FB_H_CONTINENT,
                                        :FB_A_CONTINENT,
                                        :FB_HT_SCORE,
                                        :FB_AT_SCORE,
                                        :FB_TOURNAMENT,
                                        :FB_CITY,
                                        :FB_COUNTRY,
                                        :FB_N_LOCATION,
                                        :FB_SHOOT_OUT,
                                        :FB_HT_RESULT)
                                        )
                                        """
##insert  for footbal
            seq_statement = """
                select FOOTBALL_MATCHES_seq.nextval from dual
                """
            cursor.execute(seq_statement)
            FB_ID = cursor.fetchone()[0]
            FB_DATE = request.form.get("FB_DATE")
            FB_HOME_TEAM = request.form.get("FB_HOME_TEAM")
            FB_AWAY_TEAM = request.form.get("FB_AWAY_TEAM")
            FB_H_CONTINENT = request.form.get("FB_H_CONTINENT")
            FB_A_CONTINENT = request.form.get("FB_A_CONTINENT")
            FB_HT_SCORE = request.form.get("FB_HT_SCORE")
            FB_AT_SCORE = request.form.get("FB_AT_SCORE")
            FB_TOURNAMENT = request.form.get("FB_TOURNAMENT")
            FB_CITY = request.form.get("FB_CITY")
            FB_COUNTRY = request.form.get("FB_COUNTRY")
            FB_N_LOCATION = request.form.get("FB_N_LOCATION")
            FB_SHOOT_OUT = request.form.get("FB_SHOOT_OUT")
            FB_HT_RESULT = request.form.get("FB_HT_RESULT")
            #change datatype for hire_date(str) to datetime when saving it back to database
            datetime_object = datetime.strptime(FB_DATE, '%Y-%m-%d %H:%M:%S')

            
 
            cursor.execute(insert_statement,FB_ID=FB_ID,FB_DATE=FB_DATE,FB_HOME_TEAM=FB_HOME_TEAM,FB_AWAY_TEAM=FB_AWAY_TEAM,FB_H_CONTINENT=FB_H_CONTINENT,
            FB_A_CONTINENT=FB_A_CONTINENT,FB_HT_SCORE=FB_HT_SCORE,FB_AT_SCORE=FB_AT_SCORE,FB_TOURNAMENT=FB_TOURNAMENT,FB_CITY=FB_CITY,
            FB_COUNTRY=FB_COUNTRY,FB_N_LOCATION=FB_N_LOCATION,FB_SHOOT_OUT=FB_SHOOT_OUT,FB_HT_RESULT=FB_HT_RESULT) 
            connection.commit()
            return redirect(url_for('football'))


    return render_template("football_add.html",title=" delete football", data=data)




@app.route("/football_graph")
def football_graph():
    return football_graph("football_graph.html")
  


if __name__=="__main__":
    #print('do something')
    app.run(debug=True) #only if this work then this runs
