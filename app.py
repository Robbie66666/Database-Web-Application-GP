###insert after error handler 


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
                                 INSERT INTO HR_EMPLOYEE_STAGE
                                        (
                                        )
                                         VALUES(

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
                    select * from HR_EMPLOYEE_STAGE 
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
                    select * from HR_EMPLOYEE_STAGE where employee_id = :employee_id

                    '''
        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button
 ##insert  for football

        first_name= request.form.get('first_name')
        last_name= request.form.get('last_name')
        email= request.form.get('email')
        phone_number= request.form.get('phone_number')
        hire_date= request.form.get('hire_date')
        job_id= request.form.get('job_id')
        salary= request.form.get('salary')
        commission_pct= request.form.get('commission_pct')
        manager_id= request.form.get('manager_id')
        department_id= request.form.get('department_id')
        department_name= request.form.get('department_name')
        datetime_object=datetime.strptime(str(hire_date), '%Y-%m-%d %H:%M:%S')


        

        



        with OracleDB().get_connection() as connection:
             ##insert  for football
            query='''

            update HR_EMPLOYEE_STAGE 
            set
            first_name=:first_name,
            last_name=:last_name,
            email=:email,
            phone_number=:phone_number,
            hire_date=:hire_date,
            job_id=:job_id,
            salary=:salary,
            commission_pct=:commission_pct,
            manager_id=:manager_id,
            department_id=:department_id,
            department_name=:department_name
            where employee_id=:employee_id
        '''
 ##insert  for football
        cursor=connection.cursor()
        cursor.execute(query,employee_id=id,first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,
        hire_date=datetime_object,job_id=job_id,salary=salary,commission_pct=commission_pct,manager_id=manager_id,
        department_id=department_id,department_name=department_name
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
                    select * from HR_EMPLOYEE_STAGE where employee_id = :employee_id

                    '''
        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button

           ##insert  for football
        with OracleDB().get_connection() as connection:
            query='''

            delete from HR_EMPLOYEE_STAGE 
            where  employee_id = :employee_id
            
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
                                        EMPLOYEE_ID,
                                        FIRST_NAME,
                                        LAST_NAME,
                                        EMAIL,
                                        PHONE_NUMBER,
                                        HIRE_DATE,
                                        JOB_ID,
                                        SALARY,
                                        COMMISSION_PCT,
                                        MANAGER_ID,
                                        DEPARTMENT_ID,
                                        DEPARTMENT_NAME)
                                         VALUES(
                                        :EMPLOYEE_ID,
                                        :FIRST_NAME,
                                        :LAST_NAME,
                                        :EMAIL,
                                        :PHONE_NUMBER,
                                        :HIRE_DATE,
                                        :JOB_ID,
                                        :SALARY,
                                        :COMMISSION_PCT,
                                        :MANAGER_ID,
                                        :DEPARTMENT_ID,
                                        :DEPARTMENT_NAME
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

    
