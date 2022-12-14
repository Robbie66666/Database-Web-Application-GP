from flask import Flask, render_template,request,redirect, url_for
import requests#python
import json
import os 
import csv
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from datbase import OracleDB

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


def hello():
    return "hello world"


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/work")
def work():
    return render_template("work.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")



@app.route("/register",methods=["GET","POST"])#default is using get , you need to change to post
def register():
    print("in register:")
    user = None
    ##This will not work class = user() because it has three inputs ##
    #args gets data for URL 
    ##email= request.args.get("email")
    #email= request.form.get("email")
    print('request.method:',request.method)
    if requests.method == "POST":
        name=requests.form.get('name')
        email=requests.form.get('email')
        password=requests.form.get('password')

        print("email:",email)
        print('name:',name)
        print("password:",password)
        user= User(name,email,password)
        #email=request.form.get("email")
    return render_template("register.html",title="register",user=user)

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/todos")
def todo():
    url = 'https://jsonplaceholder.typicode.com/todos'
    with requests.get(url) as response:
        #print('response', response.content)
        data = json.loads(response.content)

    return render_template("todos.html", title="Todo",todos=data,user=User)



@app.errorhandler(404)
def page_not_found(e):##E is expception 
    return render_template ("404.html"),404

@app.route('/employee',methods=['GET','POST'])
def employee():
    print('in employees:', request.method)
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
                        insert_statement= '''
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
                                        '''
                        cursor=connection.cursor() 
                        cursor.executemany(insert_statement, data)
                        connection.commit()


                        ##refreshes employeepage 
                        return redirect( url_for('employee') )

                        
            

    elif request.method =="GET":
        with OracleDB().get_connection() as connection:
            query = '''
                    select * from HR_EMPLOYEE_STAGE 
                    '''
            cursor=connection.cursor()
            cursor.execute(query)
            data=cursor.fetchall() #gets all records

            print(len(data)) 
            
    
        return render_template("employee.html",title="Employees", data=data)

@app.route('/employee_edit/<id>',methods=['GET','POST'])
def employee_edit(id):
    print('in employee_edit:', request.method)
    print('employee id:',id)###th
    data = None
    if request.method == 'GET':
        with OracleDB().get_connection() as connection:
           query = '''
                    select * from HR_EMPLOYEE_STAGE where employee_id = :employee_id

                    '''
        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button


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

        cursor=connection.cursor()
        cursor.execute(query,employee_id=id,first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,
        hire_date=datetime_object,job_id=job_id,salary=salary,commission_pct=commission_pct,manager_id=manager_id,
        department_id=department_id,department_name=department_name
        )
        print(type(datetime_object))
        print(datetime_object)
        connection.commit()
        return redirect( url_for('employee') )


    return render_template("employee_edit.html",title=" edit Employees", data=data)





@app.route('/employee_delete/<id>',methods=['GET','POST'])
def employee_delete(id):
    print('in employee_delete:', request.method)

    print('employee id:',id)###only for deleting and editing a record due to the ID


    data = None
    if request.method == 'GET':
        with OracleDB().get_connection() as connection:
           query = '''
                    select * from HR_EMPLOYEE_STAGE where employee_id = :employee_id

                    '''
        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
        data=cursor.fetchone() #gets all records
    elif request.method == 'POST':##save button
        with OracleDB().get_connection() as connection:
            query='''

            delete from HR_EMPLOYEE_STAGE 
            where  employee_id = :employee_id
            
        '''

        cursor=connection.cursor()
        cursor.execute(query,employee_id=id)
      
        connection.commit()
        return redirect( url_for('employee') )


    return render_template("employee_delete.html",title=" delete Employees", data=data)



@app.route('/employee_add/',methods=['GET','POST'])
def employee_add():
    print('in employee_add:', request.method)
    data = None
    if request.method == 'GET':
        return render_template("employee_add.html",title=" Add Employees")
        
    elif request.method == 'POST':##save button
        with OracleDB().get_connection() as connection:

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




    


if __name__=="__main__":
    #print('do something')
    app.run(debug=True) #only if this work then this runs

    


