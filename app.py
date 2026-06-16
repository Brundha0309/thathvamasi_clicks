import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# ── CONFIG ──────────────────────────────────────────
app.config['SECRET_KEY']          = os.environ.get('SECRET_KEY', 'thathvamasi_secret_2024')
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USERNAME']       = os.environ.get('MAIL_USERNAME', 'your_email@gmail.com')
app.config['MAIL_PASSWORD']       = os.environ.get('MAIL_PASSWORD', 'your_app_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'your_email@gmail.com')

PHOTOGRAPHER_EMAIL = os.environ.get('PHOTOGRAPHER_EMAIL', 'your_email@gmail.com')

mail = Mail(app)

# ── DATABASE ─────────────────────────────────────────
DB_CONFIG = {
    'host':     os.environ.get('MYSQLHOST', 'localhost'),
    'port':     int(os.environ.get('MYSQLPORT', 3306)),
    'database': os.environ.get('MYSQLDATABASE', 'thathvamasi_db'),
    'user':     os.environ.get('MYSQLUSER', 'root'),
    'password': os.environ.get('MYSQLPASSWORD', 'Brundha@0309')
}

def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"DB Error: {e}")
        return None

def init_db():
    conn = get_db()
    if not conn: return
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS bookings(
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        mobile VARCHAR(20) NOT NULL,
        email VARCHAR(100) NOT NULL,
        event_type VARCHAR(50) NOT NULL,
        event_date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        venue_name VARCHAR(150) NOT NULL,
        city VARCHAR(100) NOT NULL,
        full_address TEXT NOT NULL,
        package VARCHAR(50) NOT NULL,
        special_requests TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS contacts(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        mobile VARCHAR(20),
        subject VARCHAR(200),
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS testimonials(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        location VARCHAR(100),
        rating INT NOT NULL DEFAULT 5,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit(); cur.close(); conn.close()

# ── ROUTES ───────────────────────────────────────────
@app.route('/')
def home(): return render_template('index.html')

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/services')
def services(): return render_template('services.html')

@app.route('/portfolio')
def portfolio(): return render_template('portfolio.html')

@app.route('/pricing')
def pricing(): return render_template('pricing.html')

@app.route('/testimonials')
def testimonials(): return render_template('testimonials.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        d = request.get_json()
        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO contacts(name,email,mobile,subject,message) VALUES(%s,%s,%s,%s,%s)",
                (d['name'],d['email'],d.get('mobile',''),d.get('subject',''),d['message']))
            conn.commit(); cur.close(); conn.close()
        try:
            mail.send(Message(
                subject=f"Contact: {d.get('subject','')}",
                recipients=[PHOTOGRAPHER_EMAIL],
                body=f"From: {d['name']} <{d['email']}>\nMobile: {d.get('mobile','')}\n\n{d['message']}"
            ))
        except Exception as e: print(e)
        return jsonify({'success':True,'message':'Message sent successfully!'})
    return render_template('contact.html')

@app.route('/booknow', methods=['GET','POST'])
def booknow():
    if request.method == 'POST':
        d = request.get_json()
        conn = get_db(); bid = None
        if conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO bookings(full_name,mobile,email,event_type,event_date,
                start_time,end_time,venue_name,city,full_address,package,special_requests)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (d['full_name'],d['mobile'],d['email'],d['event_type'],d['event_date'],
                 d['start_time'],d['end_time'],d['venue_name'],d['city'],
                 d['full_address'],d['package'],d.get('special_requests','')))
            conn.commit(); bid = cur.lastrowid; cur.close(); conn.close()

        try:
            mail.send(Message(
                subject=f"New Booking #{bid} – {d['event_type']}",
                recipients=[PHOTOGRAPHER_EMAIL],
                html=f"<h2>Booking #{bid}</h2><p><b>Name:</b> {d['full_name']}<br><b>Mobile:</b> {d['mobile']}<br><b>Email:</b> {d['email']}<br><b>Event:</b> {d['event_type']}<br><b>Date:</b> {d['event_date']}<br><b>Time:</b> {d['start_time']} – {d['end_time']}<br><b>Venue:</b> {d['venue_name']}, {d['city']}<br><b>Address:</b> {d['full_address']}<br><b>Package:</b> {d['package']}</p>"
            ))
        except Exception as e: print(e)

        try:
            mail.send(Message(
                subject=f"Booking Confirmed #{bid} – Thathvamasi Clicks",
                recipients=[d['email']],
                html=f"""<div style="font-family:Arial;max-width:600px;margin:auto">
                <div style="background:#0d0d1a;padding:20px;text-align:center">
                  <h1 style="color:#d4af37">📸 Thathvamasi Clicks</h1>
                  <p style="color:#fff">Capturing Moments, Creating Memories</p>
                </div>
                <div style="padding:30px">
                  <h2>Hi {d['full_name']}! Your booking is confirmed 🎉</h2>
                  <p><b>Booking ID:</b> #{bid}<br>
                  <b>Event:</b> {d['event_type']}<br>
                  <b>Date:</b> {d['event_date']}<br>
                  <b>Time:</b> {d['start_time']} – {d['end_time']}<br>
                  <b>Venue:</b> {d['venue_name']}, {d['city']}<br>
                  <b>Package:</b> {d['package'].title()}</p>
                  <p>We'll contact you soon. Thank you!</p>
                </div>
                <div style="background:#0d0d1a;padding:15px;text-align:center">
                  <p style="color:#d4af37">© 2024 Thathvamasi Clicks</p>
                </div></div>"""
            ))
        except Exception as e: print(e)

        return jsonify({'success':True,'message':f'Booking confirmed! ID #{bid}. Check your email.','booking_id':bid})
    return render_template('booknow.html')

@app.route('/api/review', methods=['POST'])
def add_review():
    d = request.get_json()
    conn = get_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO testimonials(name,location,rating,message) VALUES(%s,%s,%s,%s)",
                (d['name'],d.get('location',''),d.get('rating',5),d['message']))
            conn.commit(); cur.close(); conn.close()
        except Exception as e:
            print(e)
    return jsonify({'success':True})

# ── RUN ──────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)