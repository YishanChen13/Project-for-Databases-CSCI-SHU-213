from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='password',
                               database='project1')

#REQUIRED Application Use Cases
#--------------------------------------------------------------------------------------------------------------------------------------------

# Define a route to hello function
@app.route('/')
def hello():
    session["userType"] = "public"
    return render_template('index.html', message="Welcome to the Air Ticket Reservation System!")

#Define a route to flight_info function
@app.route('/flight_info', methods=['GET', 'POST'])
def flight_info():
	data = []
	type = ""
	if request.method == 'POST':
		#grabs information from the forms
		type = request.form['type']
		arrival = request.form['arrival']
		departure = request.form['departure']
		departure_date = request.form['departure_date']
	if(type == "city"):
		query = "SELECT * FROM flight WHERE departure_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND arrival_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(arrival, departure, departure_date))
		data = cursor.fetchall()
		cursor.close()
	if(type == "airport"):
		query = "SELECT * FROM flight WHERE departure_airport = '{}' AND arrival_airport = '{}' AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(arrival, departure, departure_date))
		data = cursor.fetchall()
		cursor.close()
	return render_template('flight_info.html', data=data)

#Define a route to flight_status function
@app.route('/flight_status', methods=['GET', 'POST'])
def flight_status():
	data = ""
	if request.method == 'POST':
		flight_num  = request.form['flight_num']
		departure_date = request.form['departure_date']
		query = "SELECT status FROM flight WHERE flight_num = '{}' AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(flight_num, departure_date))
		data = cursor.fetchone()
		cursor.close()
	return render_template('flight_status.html', data=data)

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	userType = request.form['userType']
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()

	if(userType == "customer"):
		query = 'SELECT * FROM customer WHERE customer_email = "{}" and password = md5("{}")'
	elif(userType == "agent"):
		query = 'SELECT * FROM booking_agent WHERE booking_agent_email = "{}" and password = md5("{}")'
	elif(userType == "staff"):
		query = 'SELECT * FROM airline_staff WHERE username = "{}" and password = md5("{}")'

	#executes query
	cursor.execute(query.format(username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['userType'] = userType
		return redirect(url_for(userType))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Define route for register
@app.route('/register')
def registerselect():
	return render_template('register.html')

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	userType = request.form['userType']

	if(userType == "customer"):
		customer_email = request.form['username']
		name = request.form['name']
		password = request.form['password']
		building_number = request.form['building_number']
		street = request.form['street']
		city = request.form['city']
		state = request.form['state']
		phone_number = request.form['phone_number']
		passport_number = request.form['passport_number']
		passport_expiration = request.form['passport_expiration']
		passport_country = request.form['passport_country']
		date_of_birth = request.form['date_of_birth']
	
		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = "SELECT * FROM customer WHERE customer_email = '{}'"
		cursor.execute(query.format(customer_email))
		# stores the results in a variable
		data = cursor.fetchone()
		# use fetchall() if you are expecting more than 1 data row
		error = None
		if data:
			error = "This customer already exists"
			return render_template('register.html', error=error)

		ins1 = "INSERT INTO customer VALUES({}, {}, md5('{}'), {}, {}, {}, {}, {}, {}, DATE('{}'), {}, DATE('{}'))"
		cursor.execute(ins1.format(customer_email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		message = "Successfully Registered!"
		return render_template('index.html', message=message)
	
	if(userType == "agent"):
		booking_agent_email = request.form['username2']
		booking_agent_ID = request.form['ID'] 
		password = request.form['password2']
	
		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = "SELECT * FROM booking_agent WHERE booking_agent_email = '{}'"
		cursor.execute(query.format(booking_agent_email))
		# stores the results in a variable
		data = cursor.fetchone()
		# use fetchall() if you are expecting more than 1 data row
		error = None
		if data:
			error = "This booking agent already exists"
			return render_template('register.html', error=error)

		ins2 = "INSERT INTO booking_agent VALUES('{}', {}, md5('{}'))"
		cursor.execute(ins2.format(booking_agent_email, booking_agent_ID, password))
		conn.commit()
		cursor.close()
		message = "Successfully Registered!"
		return render_template('index.html', message=message)
	
	if(userType == "staff"):
		username = request.form['username3']
		airline_name = request.form['airline_name'] 
		password = request.form['password3']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		date_of_birth = request.form['date_of_birth3']
	
		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query1 = "SELECT * FROM airline_staff WHERE username = '{}'"
		cursor.execute(query1.format(username))
		# stores the results in a variable
		data = cursor.fetchone()
		# use fetchall() if you are expecting more than 1 data row
		query2 = "SELECT * FROM airline WHERE airline_name = '{}'"
		cursor.execute(query2.format(airline_name))
		data2 = cursor.fetchone()

		error = None
		if data:
			error = "This airline staff already exists"
			return render_template('register.html', error=error)

		if not data2:
			error = "This airline does not exist"
			return render_template('register.html', error=error)

		ins3 = "INSERT INTO airline_staff VALUES('{}', '{}', md5('{}'), '{}', '{}', DATE('{}'))"
		cursor.execute(ins3.format(username, airline_name, password, first_name, last_name, date_of_birth))
		conn.commit()
		cursor.close()
		message = "Successfully Registered!"
		return render_template('index.html', message=message)

#Customer use cases
#--------------------------------------------------------------------------------------------------------------------------------------------

#Define a route to customer function
@app.route('/customer')
def customer():
	username = session['username']
	userType = session['userType']
	cursor = conn.cursor()
	query = "SELECT flight_num, airline_name, departure_airport, arrival_airport, departure_time, arrival_time, status, ticket_id \
			FROM purchases NATURAL JOIN ticket NATURAL JOIN flight \
			WHERE customer_email = '{}' AND DATE(departure_time) > CURDATE()"
	cursor.execute(query.format(username))
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer.html', username=username, data=data)

#Define a route to flight_info_purchase function
@app.route('/flight_info_purchase', methods=['GET', 'POST'])
def flight_info_purchase():
	username = session['username']
	userType = session['userType']
	data = []
	type = ""
	if request.method == 'POST':
		#grabs information from the forms
		type = request.form['type']
		arrival = request.form['arrival']
		departure = request.form['departure']
		departure_date = request.form['departure_date']
	if(type == "city"):
		query = "SELECT * FROM flight WHERE departure_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND arrival_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(arrival, departure, departure_date))
		data = cursor.fetchall()
		cursor.close()
	if(type == "airport"):
		query = "SELECT * FROM flight WHERE departure_airport = '{}' AND arrival_airport = '{}' AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(arrival, departure, departure_date))
		data = cursor.fetchall()
		cursor.close()
	return render_template('flight_info_purchase.html', data=data, userType=userType)

#Define purchase function
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
	username = session['username']
	userType = session['userType']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']

	cursor = conn.cursor() 
	#check airplane seats
	query = "SELECT num_of_seats FROM airplane NATURAL JOIN flight WHERE flight.airline_name = '{}' and flight.flight_num = {}"
	cursor.execute(query.format(airline_name, flight_num))
	seats = cursor.fetchone()
	
	query2 = "SELECT COUNT(*) FROM ticket WHERE airline_name = '{}' and flight_num = '{}'"
	cursor.execute(query2.format(airline_name, flight_num))
	count = cursor.fetchone()
	if count[0] >= seats[0]:
		cursor.close()
		message = "The ticket of this flight is sold out. Please choose other flights."
		return render_template("flight_info_purchase.html", message = message, userType=userType)
	else:
		message = "Purchase Complete!"
		query3 = "SELECT MAX(ticket_id) FROM ticket NATURAL JOIN flight WHERE flight.airline_name = '{}' and flight.flight_num = {}"
		cursor.execute(query3.format(airline_name, flight_num))
		max = cursor.fetchone()
		query4 = "INSERT INTO ticket VALUES({}, '{}', {})"
		cursor.execute(query4.format(max[0] + 1, airline_name, flight_num))
		conn.commit()
		query5 = "INSERT INTO purchases VALUES({}, '{}', null, CURDATE())"
		cursor.execute(query5.format(max[0] + 1, username))
		conn.commit()
		cursor.close()
		return render_template("flight_info_purchase.html", message = message, userType=userType)

#Define spending function
@app.route('/spending', methods=['GET', 'POST'])
def spending():
	username = session['username']
	userType = session['userType']
	m = [6]
	cursor = conn.cursor() 
	query1 = "SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{}' and DATEDIFF(CURDATE(), purchase_date) <= 365/2"
	cursor.execute(query1.format(username))
	total = cursor.fetchone()
	query2 = "SELECT sum(price), month(purchase_date) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE purchases.customer_email = '{}' and DateDiff(CURDATE(), purchase_date) <= 365/2 group by MONTH(purchase_date)"
	cursor.execute(query2.format(username))
	monthly = cursor.fetchall()
	if request.method == 'POST':
		start = request.form["start_date"]
		end = request.form['end_date']
		query3 = "SELECT sum(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{}' and purchase_date between '{}' and '{}'"
		cursor.execute(query3.format(username, start, end))
		total = cursor.fetchone()
		query4 = "SELECT sum(price), month(purchase_date) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{}' and purchase_date between '{}' and '{}' group by MONTH(purchase_date)"
		cursor.execute(query4.format(username, start, end))
		monthly = cursor.fetchall()
		query5 = "SELECT TIMESTAMPDIFF(MONTH, '{}', '{}')"
		cursor.execute(query5.format(start, end))
		m = cursor.fetchone()
	cursor.close()
	return render_template("spending.html", total=total[0], monthly=monthly, m=m[0], userType=userType)

#Define logout function
@app.route('/logout')
def logout():
	session.pop('username')
	session.pop('userType')
	return redirect('/')

#Booking agent use cases
#--------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/agent')
def agent():
	username = session['username']
	userType = session['userType']
	cursor = conn.cursor()
	query = "SELECT flight_num, airline_name, departure_airport, arrival_airport, departure_time, arrival_time, status, ticket_id, customer_email \
			FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN booking_agent \
			WHERE booking_agent_email = '{}' AND DATE(departure_time) > CURDATE()"
	cursor.execute(query.format(username))
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer.html', username=username, data=data)
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 9000, debug = True)
