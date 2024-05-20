from colorama import Cursor
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
        cursor.execute("INSERT INTO customers (customerid, customername, contactno, customeraddress) VALUES (:1, :2, :3, :4)",
                    (customer_id, customer_name, contact_no, customer_address))
        
        # Commit the transaction and close the database connection
        db.commit()
        cursor.close()
        return 'Customer added successfully!'

    # Return a success message to the client
    return render_template('add_customer.html')


@app.route('/get_customers')
def get_customers():
    # Connect to the Oracle database
    dsn=cx_Oracle.makedsn("localhost",1521,"orcl")
    db=cx_Oracle.connect("system","oracle",dsn)
    cursor = db.cursor()

    # Execute a SELECT query to retrieve customer information from the "customers" table
    cursor.execute("SELECT customerid, customername, contactno, customeraddress FROM customers")
    rows = cursor.fetchall()
    
    # Convert the rows to a list of dictionaries
    customers = []
    for row in rows:
        customer = {
            'customer_id': row[0],
            'customer_name': row[1],
            'contact_no': row[2],
            'customer_address': row[3]
        }
        customers.append(customer)
    
    # Close the database connection
    cursor.close()


    # Pass the customer information to the HTML template and render it
    return render_template('get_customers.html', customers=customers)

@app.route('/ADDvenue', methods=['GET', 'POST'])
def ADDvenue():
    # Get the customer information from the request data
    if request.method == 'POST':
        venueid = request.form['venueid']
        address = request.form['address']
        venuename = request.form['venuename']
        capacity = request.form['capacity']
        mcontactnumber = request.form['mcontactnumber']
        costpday = request.form['costpday']
        
        # Connect to the Oracle database
        cursor = db.cursor()

        # Insert the customer information into the "customers" table
        cursor.execute("INSERT INTO venue (venueid, address, venuename, capacity, mcontactnumber, costpday) VALUES (:1, :2, :3, :4, :5, :6)", (venueid, address, venuename, capacity, mcontactnumber, costpday))
        
        # Commit the transaction and close the database connection
        db.commit()
        cursor.close()
        return 'Venue added successfully!'

    # Return a success message to the client
    return render_template('ADDvenue.html')

@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'POST':
        # Get the customer ID from the form
        customer_id = request.form.get('customer_id')

        # Create a cursor object to execute SQL statements
        cursor = db.cursor()

        # Execute a delete statement to remove the customer with the specified ID
        cursor.execute("DELETE FROM customers WHERE customerid = :customer_id", {'customer_id': customer_id})

        # Commit the transaction to save the changes to the database
        db.commit()

        # Close the cursor and the database connection
        cursor.close()

        # Redirect to the home page after the deletion
        return 'Customer deleted successfully!'
    else:
        # Render the delete_customer.html
        return render_template('delete_customer.html')
    
   


@app.route("/updatecustomer")
def update_form():
    return render_template("update_customer.html")

    
    
@app.route("/update_customer", methods=["POST"])
def update_customer():
        if request.method == 'POST':
            customer_id = request.form.get("customer_id")
            customer_name = request.form.get("customer_name")
            customer_no = request.form.get("customer_no")
            customer_address = request.form.get("customer_address")

            # Execute the SQL statement to update the customer table
            cursor = db.cursor()
            sql = "UPDATE customers SET customername = :1, contactno = :2, customeraddress = :3 WHERE customerid = :4"
            cursor.execute(sql, (customer_name, customer_no, customer_address, customer_id))
            db.commit()
            cursor.close()

            return "Customer information updated successfully!"
        

@app.route("/get_venues")
def venues():
    # Execute the SQL statement to select data from the venue table
    cursor = db.cursor()
    sql = "SELECT venueid, address, venuename, capacity, mcontactnumber, costpday FROM venue"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    # Render the data in an HTML table using the venues.html template
    return render_template("GETvenue.html", data=data)



@app.route("/insert_events", methods=["GET", "POST"])
def event():
    if request.method == "POST":
        # Get the form data from the request
        eventid = request.form["eventid"]
        edate = request.form["edate"]
        customerid = request.form["customerid"]
        eventtype = request.form["eventtype"]
        venueid = request.form["venueid"]
        paymentid = request.form["paymentid"]
        vendorid = request.form["vendorid"]
        equipmentid = request.form["equipmentid"]

        # Execute the SQL statement to insert data into the event table
        cursor = db.cursor()
        sql = "INSERT INTO event (eventid, edate, customerid, eventtype, venueid, paymentid, vendorid, equipmentid) VALUES (:eventid, :edate, :customerid, :eventtype, :venueid, :paymentid, :vendorid, :equipmentid)"
        cursor.execute(sql, [eventid, edate, customerid, eventtype, venueid, paymentid, vendorid, equipmentid])
        db.commit()
        cursor.close()

        # Redirect to the event form to clear the inputs
        return 'Event added successfully!'
    else:
        # Render the event form using the event.html template
        return render_template("event.html")


@app.route('/event-data')
def event_data():
    # execute a SQL query to get the event data
    cursor = db.cursor()
    query = "SELECT eventid, edate, customerid, eventtype, venueid, paymentid, vendorid, equipmentid FROM event"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    
    # render the HTML template with the event data
    return render_template('event_show.html', data=data)

@app.route('/vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        vendor_name = request.form['vendor_name']
        contact_no = request.form['contact_no']
        address = request.form['address']
        # Insert the vendor data into the database
        cursor = db.cursor()
        cursor.execute("INSERT INTO vendors (vendorid, vendorname, contactno, address) VALUES (:1, :2, :3, :4)",
                       (vendor_id, vendor_name, contact_no, address))
        db.commit()
        cursor.close()
    return render_template('add_vendor.html')

@app.route('/vendors')
def vendors():
    cursor = db.cursor()
    cursor.execute("SELECT vendorid, vendorname, contactno, address FROM vendors")
    vendors = cursor.fetchall()
    cursor.close()
    return render_template('vendors.html', vendors=vendors)


@app.route("/submit", methods=["POST"])
def submit():
    paymentid = request.form["paymentid"]
    amount = request.form["amount"]
    pdate = request.form["pdate"]
    eventid = request.form["eventid"]

    cursor = db.cursor()
    sql = "INSERT INTO payments (paymentid, amount, paymentdate, eventid) VALUES (:1, :2, :3, :4)"
    cursor.execute(sql, (paymentid, amount, pdate, eventid))
    db.commit()
    cursor.close()

    return render_template("payment.html")


@app.route("/get_payments")
def index():
    return render_template("payment.html")

@app.route('/show_payments')
def payments():
    # Execute SQL query to retrieve payment information
    cursor = db.cursor()
    cursor.execute("SELECT paymentid, amount, paymentdate, eventid FROM payments")
    payments = cursor.fetchall()
    cursor.close()

    # Render HTML template with payment information
    return render_template('show_payments.html', payments=payments)

# Define route for the form submission
@app.route('/update_payment', methods=['POST'])
def update_payment():
    # Retrieve form data
    payment_id = request.form['payment_id']
    amount = request.form['amount']
    operation = request.form['operation']

    # Connect to the database

    # Execute the SQL query based on the operation specified
    if operation == 'increase':
        query = 'UPDATE payments SET amount = amount + :amount WHERE paymentid = :payment_id'
    elif operation == 'decrease':
        query = 'UPDATE payments SET amount = amount - :amount WHERE paymentid = :payment_id'
    cursor = db.cursor()
    cursor.execute(query, {'amount': amount, 'payment_id': payment_id})
    db.commit()

    # Close the database connection
    cursor.close()

    # Redirect to the home page
    return 'Amount updated successfully'

@app.route('/hemloo')
def home_boy():
    return render_template('update_payment.html')


if __name__ == '__main__':
    app.run(debug=True)