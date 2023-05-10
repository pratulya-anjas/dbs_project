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
        cursor.execute("SELECT * FROM logininfo WHERE username=:username AND password=:password",
                       {'username': username, 'password': password})
        user = cursor.fetchone()
        cursor.close()
        if user:
            return render_template('insert_event.html')
        else:
            return "Invalid username or password."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logininfo WHERE username=:username", {'username': username})
        user = cursor.fetchone()
        if user:
            return "User already exists!"
        else:
            cursor.execute("INSERT INTO logininfo VALUES (:username, :password)", {'username': username, 'password': password})
            db.commit()
            return "Registration successful!"
    return render_template('register.html')

@app.route('/insert_event', methods=['POST'])
def insert_event():
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


if __name__ == '__main__':
    app.run(debug=True)