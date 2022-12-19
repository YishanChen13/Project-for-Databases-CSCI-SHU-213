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
	if userType == "agent":
		customer_email = request.form['customer']

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
		if userType == "customer":
			query5 = "INSERT INTO purchases VALUES({}, '{}', null, CURDATE())"
			cursor.execute(query5.format(max[0] + 1, username))
			conn.commit()
			cursor.close()
			return render_template("flight_info_purchase.html", message = message)
		else:
			query6 = "INSERT INTO purchases VALUES({}, '{}', (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}'), CURDATE())"
			cursor.execute(query6.format(max[0] + 1, customer_email, username))
			conn.commit()
			cursor.close()
			return render_template("flight_info_purchase_b.html", message = message)

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
	cursor = conn.cursor()
	query = "SELECT flight_num, airline_name, departure_airport, arrival_airport, departure_time, arrival_time, status, ticket_id, customer_email \
			FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN booking_agent \
			WHERE booking_agent_email = '{}' AND DATE(departure_time) > CURDATE()"
	cursor.execute(query.format(username))
	data = cursor.fetchall()
	cursor.close()
	return render_template('agent.html', username=username, data=data)

#Define a route to flight_info_purchase_b function
@app.route('/flight_info_purchase_b', methods=['GET', 'POST'])
def flight_info_purchase_b():
	username = session['username']
	userType = session['userType']
	data = []
	type = ""
	cursor = conn.cursor()
	if request.method == 'POST':
		#grabs information from the forms
		type = request.form['type']
		arrival = request.form['arrival']
		departure = request.form['departure']
		departure_date = request.form['departure_date']
	if(type == "city"):
		query = "SELECT * FROM flight WHERE airline_name IN (SELECT airline_name FROM works_with where booking_agent_email = '{}') AND departure_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND arrival_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND DATE(departure_time) = DATE('{}')"
		cursor.execute(query.format(username, arrival, departure, departure_date))
		data = cursor.fetchall()
		cursor.close()
	if(type == "airport"):
		query = "SELECT * FROM flight WHERE airline_name IN (SELECT airline_name FROM works_with where booking_agent_email = '{}') AND WHERE departure_airport = '{}' AND arrival_airport = '{}' AND DATE(departure_time) = DATE('{}')"
		cursor.execute(query.format(username, arrival, departure, departure_date))
		data = cursor.fetchall()
		cursor.close()
	return render_template('flight_info_purchase_b.html', data=data, userType=userType)

#Define commission function
@app.route('/commission', methods=['GET', 'POST'])
def commission():
	username = session['username']
	userType = session['userType']
	d = [30]
	cursor = conn.cursor() 
	query1 = "SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') and DATEDIFF(CURDATE(), purchase_date) <= 30"
	cursor.execute(query1.format(username))
	total = cursor.fetchone()
	query2 = "SELECT AVG(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') and DateDiff(CURDATE(), purchase_date) <= 30"
	cursor.execute(query2.format(username))
	average = cursor.fetchone()
	query3 = "SELECT COUNT(*) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') and DateDiff(CURDATE(), purchase_date) <= 30"
	cursor.execute(query3.format(username))
	count = cursor.fetchone()

	if request.method == 'POST':
		start = request.form["start_date"]
		end = request.form['end_date']
		query4 = "SELECT sum(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') and purchase_date between '{}' and '{}'"
		cursor.execute(query4.format(username, start, end))
		total = cursor.fetchone()
		query5 = "SELECT AVG(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') and purchase_date between '{}' and '{}'"
		cursor.execute(query5.format(username, start, end))
		average = cursor.fetchone()
		query6 = "SELECT COUNT(*) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') and purchase_date between '{}' and '{}'"
		cursor.execute(query6.format(username, start, end))
		count = cursor.fetchone()
		query7 = "SELECT TIMESTAMPDIFF(DAY, '{}', '{}')"
		cursor.execute(query7.format(start, end))
		d = cursor.fetchone()
	cursor.close()
	return render_template("commission.html", total=total[0], average=average[0], count=count[0], d=d[0], userType=userType)

#Define top_customers function
@app.route('/top_customers', methods=['GET', 'POST'])
def top_customers():
	username = session['username']
	cursor = conn.cursor() 
	query1 = "SELECT customer_email, name, COUNT(*) FROM purchases NATURAL JOIN customer WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') AND DateDiff(CURDATE(), purchase_date) <= 365/2  GROUP BY customer_email ORDER BY count(*) DESC limit 5"
	cursor.execute(query1.format(username))
	top_count = cursor.fetchall()
	query2 = "SELECT customer_email, name, SUM(price) FROM purchases NATURAL JOIN customer NATURAL JOIN flight NATURAL JOIN ticket WHERE booking_agent_ID = (SELECT booking_agent_ID FROM booking_agent WHERE booking_agent_email = '{}') AND DateDiff(CURDATE(), purchase_date) <= 365  GROUP BY customer_email ORDER BY sum(*) DESC limit 5"
	cursor.execute(query2.format(username))
	top_commission = cursor.fetchall()
	cursor.close()
	return render_template("top_customers.html", top_count=top_count, top_commission=top_commission)

#Airline staff use cases
#--------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/staff', methods=['GET', 'POST'])
def staff():
	username = session['username']
	admin = ""
	operator = ""
	cursor = conn.cursor()
	query = "SELECT flight_num, airline_name, departure_airport, arrival_airport, departure_time, arrival_time, status FROM airline_staff NATURAL JOIN flight where username = '{}' AND DATE(departure_time) between CURDATE() AND CURDATE()+30"
	cursor.execute(query.format(username))
	data = cursor.fetchall()
	query = "SELECT admin from airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	a = cursor.fetchone()
	if a[0] == 1:
		admin = "Admin"
		session['admin'] = "admin"
	query2 = "SELECT operator from airline_staff WHERE username = '{}'"
	cursor.execute(query2.format(username))
	o = cursor.fetchone()
	if o[0] == 1:
		operator = "Operator"
		session['operator'] = "operator"
	d=[30]
	if request.method == 'POST':
		start = request.form["start_date"]
		end = request.form['end_date']
		arrival = request.form['arrival']
		departure = request.form['departure']
		type = request.form['type']
		if type == "city":
			query2 = "SELECT flight_num, airline_name, departure_airport, arrival_airport, departure_time, arrival_time, status FROM airline_staff NATURAL JOIN flight WHERE username = '{}' AND departure_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND arrival_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND DATE(departure_time) BETWEEN '{}' AND '{}'"
			cursor.execute(query2.format(username, arrival, departure, start, end))
			data = cursor.fetchall()
		if type == "airport":
			query2 = "SELECT flight_num, airline_name, departure_airport, arrival_airport, departure_time, arrival_time, status FROM airline_staff NATURAL JOIN flight WHERE username = '{}' AND departure_airport = '{}' AND arrival_airport = '{}' AND DATE(departure_time) BETWEEN '{}' AND '{}'"
			cursor.execute(query2.format(username, arrival, departure, start, end))
			data = cursor.fetchall()
		query3 = "SELECT TIMESTAMPDIFF(DAY, '{}', '{}')"
		cursor.execute(query3.format(start, end))
		d = cursor.fetchone()
	cursor.close()
	return render_template('staff.html', username=username, data=data, d=d[0], admin=admin, operator=operator)

@app.route('/customer_list', methods=['GET', 'POST'])
def customer_list():
	flight_num = request.form['flight_num']
	airline_name = request.form['airline_name']
	cursor = conn.cursor()
	query = "SELECT customer_email, name FROM customer NATURAL JOIN purchases NATURAL JOIN ticket WHERE flight_num = {} AND airline_name = '{}'"
	cursor.execute(query.format(flight_num, airline_name))
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer_list.html', flight_num=flight_num, data=data)

@app.route('/create_flights', methods=['GET', 'POST'])
def create_flights():
	if session["admin"] == "admin":
		if request.method == 'POST':
			flight_num = request.form["flight_num"]
			departure_airport = request.form["departure_airport"]
			departure_time = request.form["departure_time"]
			arrival_airport = request.form["arrival_airport"]
			arrival_time = request.form["arrival_time"]
			price = request.form["price"]
			status = request.form["status"]
			airplane_ID = request.form["airplane_ID"]
			cursor = conn.cursor()	
			username = session["username"]
			query = "select airline_name from airline_staff where username = '{}'"
			cursor.execute(query.format(username))
			airline_name = cursor.fetchone() [0]
			query2 = "SELECT * FROM flight WHERE airline_name = '{}' and flight_num = {}"
			cursor.execute(query2.format(airline_name, flight_num))
			data = cursor.fetchall()
			if data:
				message = "This Flight Already Exists"
				return render_template('create_flight.html', message = message)
			ins = "INSERT INTO flight VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
			cursor.execute(ins.format(flight_num, airline_name, airplane_ID, departure_airport, arrival_airport, departure_time, arrival_time, price, status))
			conn.commit()
			cursor.close()
			message = "Successfully Created A Flight!"
			return render_template('create_flights.html', message = message)
		else:
			return render_template('create_flights.html', message = "Create A Flight")
	else:
		return render_template('staff.html', message = "You do not have permission!")

@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
	if session["operator"] == "operator":
		status = request.form['status']
		flight_num = request.form['flight_num']
		airline_name = request.form['airline_name']
		cursor = conn.cursor()
		query = "UPDATE flight SET status = '{}' WHERE flight_num = {} AND airline_name = '{}'"
		cursor.execute(query.format(status, flight_num, airline_name))
		conn.commit()
		cursor.close()
		return render_template('staff.html', message = "Status Updated")
	else:
		return render_template('staff.html', message = "You do not have permission!")

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	if session["admin"] == "admin":
		if request.method == 'POST':
			airplane_ID = request.form["airplane_ID"]
			num_of_seats = request.form['num_of_seats']
			cursor = conn.cursor()	
			username = session["username"]
			query = "select airline_name from airline_staff where username = '{}'"
			cursor.execute(query.format(username))
			airline_name = cursor.fetchone() [0]
			query2 = "SELECT * FROM airplane WHERE airplane_ID = {} and airline_name = '{}'"
			cursor.execute(query2.format(airplane_ID, airline_name))
			data = cursor.fetchall()
			if data:
				message = "This Airplane Already Exists"
				return render_template('add_airplane.html', message = message)
			ins = "INSERT INTO airplane VALUES({}, '{}', {})"
			cursor.execute(ins.format(airplane_ID, airline_name, num_of_seats))
			conn.commit()
			cursor.close()
			message = "Successfully Added A Airplane!"
			return render_template('add_airplane.html', message = message)
		else:
			return render_template('add_airplane.html', message = "Add A Airplane")
	else:
		return render_template('staff.html', message = "You do not have permission!")

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	if session["admin"] == "admin":
		if request.method == 'POST':
			airport_name = request.form["airport_name"]
			city = request.form['city']
			cursor = conn.cursor()	
			query = "SELECT * FROM airport WHERE airport_name = '{}'"
			cursor.execute(query.format(airport_name))
			data = cursor.fetchall()
			if data:
				message = "This Airport Already Exists"
				return render_template('add_airport.html', message = message)
			ins = "INSERT INTO airport VALUES('{}', '{}')"
			cursor.execute(ins.format(airport_name, city))
			conn.commit()
			cursor.close()
			message = "Successfully Added A Airport!"
			return render_template('add_airport.html', message = message)
		else:
			return render_template('add_airport.html', message = "Add A Airport")
	else:
		return render_template('staff.html', message = "You do not have permission!")

@app.route('/top_agents', methods=['GET', 'POST'])
def top_agents():
	username = session["username"]
	cursor = conn.cursor() 
	query = "select airline_name from airline_staff where username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone() [0]
	query2 = "SELECT booking_agent_email, booking_agent_ID, COUNT(*) FROM purchases NATURAL JOIN booking_agent NATURAL JOIN works_with WHERE airline_name = '{}' AND DateDiff(CURDATE(), purchase_date) <= 365  GROUP BY booking_agent_ID, booking_agent_email ORDER BY count(*) DESC limit 5"
	cursor.execute(query2.format(airline_name))
	top_count = cursor.fetchall()
	query3 = "SELECT booking_agent_email, booking_agent_ID, SUM(price) FROM (SELECT booking_agent_email, booking_agent_ID, ticket_id, purchase_date FROM purchases NATURAL JOIN booking_agent NATURAL JOIN works_with WHERE airline_name = '{}') AS temp NATURAL JOIN ticket NATURAL JOIN flight WHERE DateDiff(CURDATE(), purchase_date) <= 365  GROUP BY booking_agent_ID, booking_agent_email ORDER BY SUM(price) DESC limit 5"
	cursor.execute(query3.format(airline_name))
	top_commission = cursor.fetchall()
	cursor.close()
	return render_template("top_agents.html", top_count=top_count, top_commission=top_commission)

@app.route('/view_customers', methods=['GET', 'POST'])
def view_customers():
	username = session["username"]
	flights = []
	cursor = conn.cursor() 
	query = "select airline_name from airline_staff where username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone() [0]
	query2 = "SELECT customer_email, name, COUNT(DISTINCT(ticket_id)) FROM (SELECT DISTINCT(ticket_id), name, customer_email, departure_time FROM purchases NATURAL JOIN customer NATURAL JOIN flight WHERE airline_name = '{}') AS temp WHERE DateDiff(DATE(departure_time), CURDATE()) <= 365 GROUP BY customer_email, name ORDER BY COUNT(ticket_id) DESC limit 1"
	cursor.execute(query2.format(airline_name))
	top = cursor.fetchall()
	if request.method == 'POST':
		username = request.form["username"]
		query3 = "SELECT flight_num, DATE(departure_time) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = '{}' AND airline_name = '{}' AND DateDiff(DATE(departure_time), CURDATE()) <= 365"
		cursor.execute(query3.format(username, airline_name))
		flights = cursor.fetchall()
	cursor.close()
	return render_template("view_customers.html", top=top, flights=flights)

@app.route('/refresh')
def refresh():
	return staff()

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 9000, debug = True)
