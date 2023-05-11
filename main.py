from flask import Flask, render_template, request
import cx_Oracle

app = Flask(__name__)
dsn=cx_Oracle.makedsn("localhost",1521,"orcl")
db=cx_Oracle.connect("system","oracle",dsn)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employees WHERE ename=:username AND epassword=:password",
                       {'username': username, 'password': password})
        user = cursor.fetchone()
        cursor.close()
        if user:
            return render_template('dashboard.html')
        else:
            return "Invalid username or password."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        epid = request.form['epid']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM EMPLOYEES WHERE employeeid=:epid", {'epid': epid})
        user = cursor.fetchone()
        if user:
            return "User already exists!"
        else:
            cursor.execute("INSERT INTO EMPLOYEES VALUES (:epid,:address,:username, :password)", {'epid':epid,'address':address,'username': username, 'password': password})
            db.commit()
            return "Registration successful!"
    return render_template('register.html')


@app.route('/insert_event')
def to_event():
    if request.method == 'POST':
        # Get the data from the request
        event_id = request.form['event_id']
        event_type = request.form['event_type']
        customer_id = request.form['customer_id']
        venue_id = request.form['venue_id']
        budget = request.form['budget']
        equipment = request.form['equipment']
        payments = request.form['payments']
        attendees = request.form['attendees']

        # Insert the data into the database
        db=cx_Oracle.connect("system","oracle",dsn)
        cursor = db.cursor()
        cursor.execute('INSERT INTO events (event_id, event_type, customer_id, venue_id, budget, equipment, payments, attendees) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)', (event_id, event_type, customer_id, venue_id, budget, equipment, payments, attendees))
        db.commit()
        cursor.close()
        db.close()

        return 'Event inserted successfully!'
    return render_template('insert_event.html')
    

@app.route('/events')
def get_events():
    # Connect to the database
    conn = cx_Oracle.connect("system","oracle",dsn)
    cursor = conn.cursor()

    # Query the database for events
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the events template with the event data
    return render_template('events.html', events=events)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    # Get the customer information from the request data
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        contact_no = request.form['contact_no']
        customer_address = request.form['customer_address']

        # Connect to the Oracle database
        cursor = db.cursor()

        # Insert the customer information into the "customers" table
        cursor.execute("INSERT INTO customers (customer_id, customer_name, contact_no, customer_address) VALUES (:1, :2, :3, :4)",
                    (customer_id, customer_name, contact_no, customer_address))
        
        # Commit the transaction and close the database connection
        db.commit()
        cursor.close()
        db.close()
        return render_template('add_customer.html')

    # Return a success message to the client
    return render_template('add_customer.html')
    


if __name__ == '__main__':
    app.run(debug=True)