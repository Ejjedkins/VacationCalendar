import mysql.connector
from mysql.connector import Error
import hashlib
import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
import datetime
import time
from datetime import datetime


#creating connection to mysql database
conn = create_connection('cis3368-22.cpjnynkz2kye.us-east-2.rds.amazonaws.com', 'Ejjedkin', '08ej03!3368', 'CIS3368db')
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser
cursor = conn.cursor(dictionary = True)

trip_table = """
    CREATE TABLE IF NOT EXISTS trip(
    id INT AUTO_INCREMENT NOT NULL,
    destinationid INT UNSIGNED NOT NULL,
    transportation varchar(50) NOT NULL,
    startdate date NOT NULL,
    enddate date NOT NULL,
    tripname varchar(100),
    FOREIGN KEY fk_destinationid(destinationid) REFERENCES destination(id),
    PRIMARY KEY (id)


)"""
#execute_query(conn, trip_table )

destination_table = """
    CREATE TABLE IF NOT EXISTS destination(
    id INT UNSIGNED AUTO_INCREMENT NOT NULL,
    country varchar(80),
    city varchar(80),
    sightseeing varchar(200),
    Primary Key (id)
    
)"""
#execute_query(conn, description_table )

#Dispays the destinations
@app.route('/api/destination', methods =['GET'])
def api_destination_list():
    sql = "SELECT * FROM destination"
    trip = execute_read_query(conn, sql)
    return jsonify(trip)

#Adds a destination to the db table
@app.route('/api/destination', methods =['POST'])
def api_add_desti():
    request_data = request.get_json()   
    if 'DELETE' in request_data:
            sql = "DELETE FROM destination where id = %s"
            vals = (request_data['destdi'])
            cursor.execute(sql, vals)
            return "delete request successful"
    else:
            newcountry= request_data['country']
            newcity= request_data['city']
            newsight = request_data['sightseeing']
            sql = "INSERT INTO destination (country, city, sightseeing) VALUES (%s, %s, %s)"
            vals = (newcountry, newcity, newsight)
            cursor.execute(sql, vals)
            return 'Add request successful'

#Updates the destination table
@app.route('/api/destination', methods =['PUT'])
def api_upd():
    request_data = request.get_json()
    sightUpd= request_data['sightseeing']
    newcountry= request_data['country']
    newcity= request_data['city']
    idToGet = request_data['destid']
    sql_upd = "UPDATE destination SET city = %s, country = %s, sightseeing = %s where id = %s "
    vals = (newcity, newcountry, sightUpd, idToGet)
    cursor.execute(sql_upd, vals)
    return 'Sight successfully updated'

#Deletes a destination from the destination table
@app.route('/api/destination/<int:destid>', methods =['DELETE'])
def api_del_dest(destid):
    request_Data = request.get_json()

    sql = "DELETE FROM destination where id = %s"
    vals = (destid,)
    cursor.execute(sql, vals)
    return "delete request successful"


#API function that will display the trip table
@app.route('/api/trip', methods =['GET'])
def api_trip_list():
    sql = "SELECT * FROM trip"
    trip = execute_read_query(conn, sql)
    return jsonify(trip)


#API function that will display the trip table
@app.route('/api/trip/<int:tripid>', methods =['GET'])
def api_trip_get(tripid):
   
    sql = "SELECT * FROM trip where id = %s"
    cursor.execute(sql, [tripid])

    return jsonify(cursor.fetchone())

#Added an api function that wil
# l add a trip to the table
@app.route('/api/trip', methods =['POST'])
def api_add_trip():
    request_data = request.get_json()
    
    if 'DELETE' in request_data:
        sql = "DELETE FROM trip where id = %s"
        vals = (request_data['tripdi'])
        cursor.execute(sql, vals)
        return "delete request successful"

    else:
        newdestination = int(request_data['destinationid'])
        newtransport = request_data['transportation']
        newstart = request_data['startdate'] #.split('/')
        newend = request_data['enddate']#.split('/')
        #Code to adjust the format of the inserted dates. In Json the date must be inserted in MM/DD/YY format
        #newstart = "20{0}-{1}-{2}".format(22, 10,1)
        #newend = "20{0}-{1}-{2}".format(22, 10,2)
        print(newstart, newend)
        newtripname = request_data['tripname']
        sql = "INSERT INTO trip (destinationid, transportation, startdate, enddate, tripname)  VALUES (%s,%s,%s,%s,%s)"
        vals = (newdestination, newtransport, newstart, newend, newtripname)
        cursor.execute(sql, vals)
        return 'Add request successful'

@app.route('/api/destination/<int:destid>', methods =['GET'])
def api_dest_get(destid):
   
    sql = "SELECT * FROM destination where id = %s"
    cursor.execute(sql, [destid])

    return jsonify(cursor.fetchone())

#Updates the mode of transportaion depending on the id
@app.route('/api/trip', methods =['PUT'])
def api_upd_trip():
    request_data = request.get_json()
    transportUpd= request_data['transportation']
    idToGet = int(request_data['tripid'])
    newstart = request_data['startdate'] #.split('/')
    newend = request_data['enddate']#.split('/')
    name = request_data['tripname']
    sql_upd = "UPDATE trip SET transportation = %s, startdate = %s, enddate = %s, tripname = %s where id = %s "
    vals = (transportUpd, newstart, newend, name, idToGet)
    cursor.execute(sql_upd, vals)
    return 'Transport successfully updated'

#API that deletes a row in the trip table depending on the id 
@app.route('/api/trip/<int:tripid>', methods =['DELETE'])
def api_del_trip(tripid):
    request_Data = request.get_json()

    sql = "DELETE FROM trip where id = %s"
    vals = (tripid,)
    cursor.execute(sql, vals)
    return "delete request successful"

#Creating an User to log in
#The password to log in is Houston
username =  'Eli123'
password = '00cc7d9b5e8b01238856bf7f9d2c5bb12313bbe47f9f612374db95f0f30519ac'

@app.route('/api/login', methods=['GET'])
def auth_login():
    if request.authorization:
        encoded=request.authorization.password.encode()
        hashedResult = hashlib.sha256(encoded)
        if request.authorization.username == username and hashedResult.hexdigest() == password:
            return '<h1> You successully logged in </h1>'
    return make_response('Log in was unsucessful :(', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})



app.run()
