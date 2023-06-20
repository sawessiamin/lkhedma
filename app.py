import psycopg2
from flask import Flask , render_template, request, url_for, flash, redirect
from flask import jsonify 
from flask_cors import CORS, cross_origin
import hashlib
import time
import json
import datetime
import winwifi
from wireless import Wireless
import os 


from werkzeug.exceptions import abort


conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="admin",
                        port="5432")

cursor = conn.cursor()

def convert_string (string) :
    return "'"+str(string) +"'"

def select_function (table_name , column_name , cond) :
    command = "select "+ column_name +" from "+table_name + " WHERE " + cond +" ;"
    cursor.execute(command) 
    conn.commit()
    data = cursor.fetchall()
    conn.close
    return data 

def insert_function (table_name , values) :
    the_values= ""
    for elem in values :
        the_values += convert_string(elem) + ", "  
    the_values = the_values[0:len(the_values)-2]

    command = "insert into "+ table_name +" values "+"("+the_values+")" +" ;"
    data = cursor.execute(command) 
    conn.commit()
    conn.close

    print(data , command)

    return data 

def update_function(table_name , toModify , values , cond) :
    the_values= ""
    for i in range(0,len(values)) :
        elem = values[i]
        elem2 = toModify[i]
        the_values += str(elem2)+" = " + convert_string(elem) +" , "
       
    the_values = the_values[0:len(the_values)-2]

    command = "Update "+ table_name +" set  "+the_values+ " WHERE " + cond +" ;"
    print(command)
    data = cursor.execute(command) 
    conn.commit()
    conn.close

    print(data , command)

    return 0 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/insert_signup', methods=['POST'])
@cross_origin()
def insert_signup():
    request_data = json.loads(request.data)
    
    email = str( request_data["email"] )
    phone = str(request_data["phone"] )
    nom = str(request_data["nom"] )
    prenom = str(request_data["prenom"] )
    region = str(request_data["region"])
    password = str(request_data["password"])
    hashed_pass = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    thetime = datetime.datetime.now()

    insert_function ("sj_client" , [nom , prenom ,email,phone,hashed_pass,region,thetime, thetime])
    return jsonify({"status": True })

@app.route('/database_password', methods=['POST'])
@cross_origin()
def database_password():
    request_data = json.loads(request.data)
    email = str(request_data["email"])
    password = str(request_data["password"])
    database_password = select_function ("sj_client" , "passsword" , "email ="+convert_string(email))
    print(database_password ,"database_password")
    if (len(database_password) == 0) :
        database_password = False
    else :
        database_password_comp = database_password[0][0]
        hashed_password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        print(hashed_password ,database_password_comp , len(password))
        print(hashed_password ,database_password_comp , "password")
        if (hashed_password == database_password_comp) :
            database_password = True
        else :
            database_password = False
    return jsonify({"database_password": database_password})


@app.route('/get_email_phone_bool', methods=['POST'])
@cross_origin()
def get_email_phone_bool():
    request_data = json.loads(request.data)
    email = str(request_data["email"]) 
    phone = str(request_data["phone"])

    email_db = select_function ("sj_client" , "email" , " email = "+convert_string(email))
    phone_db = select_function ("sj_client" , "mobile" , " mobile = "+convert_string(email))
    
    email_bool = True
    phone_bool = True

    if (len(email_db) != 0) :
        email_bool = False
    if (len(phone_db) != 0) :
        phone_bool = False
        
    print(email_bool)
    print(phone_bool)
    return jsonify({"email": email_bool, "phone": phone_bool})




@app.route('/fb_user', methods=['POST'])
@cross_origin()
def fb_user():
    request_data = json.loads(request.data)
    email = str(request_data["email"]) 
    uid = str(request_data["uid"]) 

    Orgfirst_tab_data = select_function("sj_client" ,"email,firstname ,lastname ,mobile " ,"email = "+convert_string(email))
    if (len(Orgfirst_tab_data) != 0) :
        first_tab_data = Orgfirst_tab_data
        print(first_tab_data , "first_tab_data")
        the_email = first_tab_data[0][0]
        the_firstname = first_tab_data[0][1]
        the_lastname = first_tab_data[0][2]
        the_mobile = first_tab_data[0][3]
        thetime = datetime.datetime.now()

        second_tab_data = select_function("sj_client_auth" ,"email,firstname ,lastname ,mobile " ,"email = "+convert_string(email))
        print(second_tab_data , "second_tab_data")
        new = False
        if len(second_tab_data) == 0 :
            new = True
        if (new) :
            insert_function("sj_client_auth" , [uid,the_firstname,the_lastname,the_email,the_mobile,thetime,
            thetime,thetime,1,1,uid])
        else :
            nbr_react = select_function("sj_client_auth" ,"nbr_react" ,"email ="+convert_string(the_email))[0][0]
            update_function("sj_client_auth" ,["last_date" ,"nbr_react"] ,[thetime,nbr_react+1] , "email ="+convert_string(the_email))
        return jsonify({"status": True})
    else :
        return jsonify({"status": False})



@app.route('/save_file', methods=['POST'])
@cross_origin()
def save_file():
   
    file = request.files['file']
    if (file.filename != '') :
        full_path = os.path.join("./uploads", file.filename)
        file.save(full_path)

 
  
    #file.save("./"+str(file_name))
    return jsonify({"status": False})

#insert_function("test2" , [12,"you"])
#data = select_function("test2" ,"*" ,"TRUE")
#update_function("test2" ,["num" ,"nom"] ,[5,"rr4444r"] , "TRUE")