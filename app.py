@app.route('/football',methods=['GET','POST']) ##insert for football
def football():##insert for football
    print('in football:', request.method)
    if request.method == "POST":
        file =request.files ['dataFile']
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
                                 INSERT INTO football_matches
                                        (
                                        fb_id,
                                        fb_date,
                                        fb_home_team,
                                        fb_away_team,
                                        PHONE_NUMBER,
                                        fb_h_continent,
                                        fb_a_continent,
                                        fb_ht_score,
                                        fb_at_score,
                                        fb_tournament,
                                        fb_country,
                                        fb_n_location,
                                        fb_shoot_out,
                                        fb_ht_result)
                                    
                                         VALUES(
                                        :fb_id,
                                        :fb_date,
                                        :fb_home_team,
                                        :fb_away_team,
                                        :PHONE_NUMBER,
                                        :fb_h_continent,
                                        :fb_a_continent,
                                        :fb_ht_score,
                                        :fb_at_score,
                                        :fb_tournament,
                                        :fb_country,
                                        :fb_n_location,
                                        :fb_shoot_out,
                                        :fb_ht_result)
                                        )
                                        '''
                        cursor=connection.cursor() 
                        cursor.executemany(insert_statement, data)
                        connection.commit()


                        ##refreshes employeepage 
                        return redirect( url_for('football') )

                        
            

    elif request.method =="GET":
        with OracleDB().get_connection() as connection:
            ##insert  for football
            query = '''
                    select * from football_matches 
                    '''
            cursor=connection.cursor()
            cursor.execute(query)
            data=cursor.fetchall() #gets all records

            print(len(data)) 
            
    
        return render_template("football.html",title="football", data=data)

@app.route('/football_edit/<id>',methods=['GET','POST'])
def football_edit(id):
    print('in football_edit:', request.method)
    print('employee id:',id)###th
    data = None
    if request.method == 'GET':
         ##insert  for football
        with OracleDB().get_connection() as connection:
           query = '''
                    select * from football_matches where fb_id = :fb_id

                    '''
        cursor=connection.cursor()
        cursor.execute(query,fb_id=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button
 ##insert  for football

        fb_date= request.form.get('fb_date')
        fb_home_team= request.form.get('fb_home_team')
        fb_away_team= request.form.get('fb_away_team')
        fb_h_continent= request.form.get('fb_h_continent')
        fb_a_continent= request.form.get('fb_a_continent')
        fb_ht_score= request.form.get('fb_ht_score')
        fb_at_score= request.form.get('fb_at_score')
        fb_tournament= request.form.get('fb_tournament')
        fb_city= request.form.get('fb_city')
        fb_country= request.form.get('fb_country')
        fb_n_location= request.form.get('fb_n_location')
        fb_shoot_out= request.form.get('fb_shoot_out')
        fb_ht_result= request.form.get('fb_ht_result')
        
        
        datetime_object=datetime.strptime(str(hire_date), '%Y-%m-%d %H:%M:%S')


        

        



        with OracleDB().get_connection() as connection:
             ##insert  for football
            query='''

            update football_matches 
            set
            fb_date=:fb_date,
            fb_home_team=:fb_home_team,
            fb_away_team=:fb_away_team,
            fb_h_continent=:fb_h_continent,
            fb_a_continent=:fb_a_continent,
            fb_ht_score=:fb_ht_score,
            fb_at_score=:fb_at_score,
            fb_tournament=:fb_tournament,
            fb_city=:fb_city,
            fb_country=:department_id,
            fb_n_location=:fb_n_location,
            fb_shoot_out=:fb_shoot_out,
            fb_ht_result=:fb_ht_result
            where fb_id=:fb_id
        '''
 ##insert  for football
        cursor=connection.cursor()
        cursor.execute(query,fb_id=id,fb_date=fb_date,fb_home_team=fb_home_team,fb_away_team=fb_away_team,fb_h_continent=fb_h_continent,
        fb_a_continent=fb_a_continent,fb_ht_score=fb_ht_score,fb_at_score=fb_at_score,fb_tournament=fb_tournament,fb_city=fb_city,
        fb_country=fb_country,fb_n_location=fb_n_location,fb_shoot_out=fb_shoot_out,fb_ht_result=fb_ht_result
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
                    select * from football_matches where fb_id = :fb_id

                    '''
        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button

           ##insert  for football
        with OracleDB().get_connection() as connection:
            query='''

            delete from football_matches 
            where  fb_id = :fb_id
            
        '''

        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
      
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

                                 INSERT INTO HR_EMPLOYEE_STAGE
                                         (
                                        fb_id,
                                        fb_date,
                                        fb_home_team,
                                        fb_away_team,
                                        PHONE_NUMBER,
                                        fb_h_continent,
                                        fb_a_continent,
                                        fb_ht_score,
                                        fb_at_score,
                                        fb_tournament,
                                        fb_country,
                                        fb_n_location,
                                        fb_shoot_out,
                                        fb_ht_result)
                                    
                                         VALUES(
                                        :fb_id,
                                        :fb_date,
                                        :fb_home_team,
                                        :fb_away_team,
                                        :PHONE_NUMBER,
                                        :fb_h_continent,
                                        :fb_a_continent,
                                        :fb_ht_score,
                                        :fb_at_score,
                                        :fb_tournament,
                                        :fb_country,
                                        :fb_n_location,
                                        :fb_shoot_out,
                                        :fb_ht_result)
                                        )
                                        """
##insert  for footbal
            seq_statement = """
                select seq_emp.nextval from dual

                """
            cursor.execute(seq_statement)
            employee_id = cursor.fetchone()[0]
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            hire_date = request.form.get("hire_date")
            job_id = request.form.get("job_id")
            salary = request.form.get("salary")
            commission_pct = request.form.get("commission_pct")
            manager_id = request.form.get("manager_id")
            department_id = request.form.get("department_id")
            department_name = request.form.get("department_name")
            #change datatype for hire_date(str) to datetime when saving it back to database
            datetime_object = datetime.strptime(hire_date, '%Y-%m-%d %H:%M:%S')

            cursor.execute(insert_statement, employee_id=employee_id, first_name=first_name,last_name=last_name,email = email,phone_number = phone_number,hire_date=datetime_object,job_id = job_id,salary = salary,commission_pct = commission_pct,manager_id = manager_id,department_id = department_id,department_name = department_name) 
            connection.commit()
            return redirect(url_for('employee'))


    return render_template("employee_add.html",title=" delete Employees", data=data)




@app.route("/football_graph")
def football_graph():
    return football_graph("football_graph.html")
  


if __name__=="__main__":
    #print('do something')
    app.run(debug=True) #only if this work then this runs

    


