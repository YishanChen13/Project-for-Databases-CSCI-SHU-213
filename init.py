from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='password',
                               database='project1')


#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/registerselect')
def registerselect():
	return render_template('register.html')

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

#Define a route to customer function
@app.route('/customer')
def customer():
	username = session['username']
	return render_template('customer.html', username=username)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	userType = request.form['userType']
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM {} WHERE username = {}'
	cursor.execute(query.format(userType, email))
	#stores the results in a variable
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES({}, {})'
		cursor.execute(ins.format(email, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Define a route to search_flight function
@app.route('/search_flight', methods=['GET', 'POST'])
def upcoming_flight():
	text = ""
	if request.method == 'POST':
		arrival_city  = request.form['arrival_city']
		departure_city = request.form['departure_city']
		departure_date = request.form['departure_date']
		query = "SELECT * FROM flight WHERE departure_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND arrival_airport = (SELECT airport_name FROM airport WHERE city = '{}') AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(arrival_city, departure_city, departure_date))
		text = cursor.fetchall()
		cursor.close()
	return render_template('upcoming_flight.html', text=text)



#Define a route to flight_status function
@app.route('/flight_status', methods=['GET', 'POST'])
def flight_status():
	text = ""
	if request.method == 'POST':
		flight_num  = request.form['flight_num']
		departure_date = request.form['departure_date']
		query = "SELECT status FROM flight WHERE flight_num = '{}' AND DATE(departure_time) = DATE('{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(flight_num, departure_date))
		text = cursor.fetchall()
		cursor.close()
	return render_template('flight_status.html', text=text)

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 9000, debug = True)
