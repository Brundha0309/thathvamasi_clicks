import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# ── MAIL — hardcoded for reliability ─────────────────
app.config['SECRET_KEY']          = 'thathvamasi_secret_2024'
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USE_SSL']        = False
app.config['MAIL_USERNAME']       = 'thathvamasi.clicks@gmail.com'
app.config['MAIL_PASSWORD']       = 'nzwhkcqghfzsdnbq'
app.config['MAIL_DEFAULT_SENDER'] = 'thathvamasi.clicks@gmail.com'
app.config['MAIL_DEBUG']          = False
app.config['MAIL_SUPPRESS_SEND']  = False

PHOTOGRAPHER_EMAIL = 'thathvamasi.clicks@gmail.com'

mail = Mail(app)

# ── DATABASE ─────────────────────────────────────────
def get_db():
    try:
        host = os.environ.get('MYSQLHOST', 'localhost')
        conn_args = {
            'host':               host,
            'port':               int(os.environ.get('MYSQLPORT', 3306)),
            'database':           os.environ.get('MYSQLDATABASE', 'thathvamasi_db'),
            'user':               os.environ.get('MYSQLUSER', 'root'),
            'password':           os.environ.get('MYSQLPASSWORD', 'Brundha@0309'),
            'connection_timeout': 30,
        }
        if 'aivencloud' in host:
            conn_args['ssl_disabled'] = False
        conn = mysql.connector.connect(**conn_args)
        print("✅ DB Connected")
        return conn
    except Error as e:
        print(f"❌ DB Error: {e}")
        return None

def init_db():
    conn = get_db()
    if not conn:
        print("⚠️ No DB connection")
        return
    try:
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
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Tables Ready")
    except Exception as e:
        print(f"❌ Table error: {e}")

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
def pricing(): return render_template('packages.html')

@app.route('/testimonials')
def testimonials(): return render_template('testimonials.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        d = request.get_json()
        if not d:
            return jsonify({'success':False,'message':'No data'})
        try:
            conn = get_db()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO contacts(name,email,mobile,subject,message) VALUES(%s,%s,%s,%s,%s)",
                    (d.get('name',''),d.get('email',''),d.get('mobile',''),
                     d.get('subject',''),d.get('message',''))
                )
                conn.commit(); cur.close(); conn.close()
        except Exception as e:
            print(f"❌ Contact DB: {e}")
        try:
            mail.send(Message(
                subject=f"New Contact: {d.get('subject','Inquiry')}",
                recipients=[PHOTOGRAPHER_EMAIL],
                html=f"""<div style="font-family:Arial;max-width:600px;margin:auto">
                <div style="background:#0d0d1a;padding:20px;text-align:center">
                  <h2 style="color:#d4af37">Thathvamasi Clicks</h2>
                </div>
                <div style="padding:24px;background:#fff">
                  <p><b>Name:</b> {d.get('name','')}</p>
                  <p><b>Email:</b> {d.get('email','')}</p>
                  <p><b>Mobile:</b> {d.get('mobile','')}</p>
                  <p><b>Event:</b> {d.get('eventType','')}</p>
                  <p><b>Message:</b><br>{d.get('message','')}</p>
                </div></div>"""
            ))
            print("✅ Contact email sent")
        except Exception as e:
            print(f"❌ Contact email error: {e}")
        return jsonify({'success':True,'message':'Message sent!'})
    return render_template('contact.html')


@app.route('/booknow', methods=['GET','POST'])
def booknow():
    if request.method == 'POST':
        d = request.get_json()
        print(f"📥 Booking received: {d}")
        if not d:
            return jsonify({'success':False,'message':'No data received'})

        bid = None

        # Save to DB
        try:
            conn = get_db()
            if conn:
                cur = conn.cursor()
                cur.execute("""INSERT INTO bookings(
                    full_name,mobile,email,event_type,event_date,
                    start_time,end_time,venue_name,city,
                    full_address,package,special_requests
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    d.get('full_name',''), d.get('mobile',''), d.get('email',''),
                    d.get('event_type',''), d.get('event_date',''),
                    d.get('start_time',''), d.get('end_time',''),
                    d.get('venue_name',''), d.get('city',''),
                    d.get('full_address',''), d.get('package',''),
                    d.get('special_requests','')
                ))
                conn.commit()
                bid = cur.lastrowid
                cur.close(); conn.close()
                print(f"✅ Booking saved ID #{bid}")
            else:
                bid = "N/A"
        except Exception as e:
            bid = "N/A"
            print(f"❌ DB error: {e}")

        # Email to Photographer
        try:
            print("📧 Sending photographer email...")
            msg = Message(
                subject=f"New Booking #{bid} — {d.get('event_type','')}",
                recipients=[PHOTOGRAPHER_EMAIL]
            )
            msg.html = f"""<div style="font-family:Arial;max-width:600px;margin:auto">
            <div style="background:#0d0d1a;padding:20px;text-align:center">
              <h2 style="color:#d4af37">Thathvamasi Clicks — New Booking!</h2>
            </div>
            <div style="padding:24px;background:#fff">
              <p><b>Booking ID:</b> #{bid}</p>
              <p><b>Name:</b> {d.get('full_name','')}</p>
              <p><b>Mobile:</b> {d.get('mobile','')}</p>
              <p><b>Email:</b> {d.get('email','')}</p>
              <p><b>Event:</b> {d.get('event_type','')}</p>
              <p><b>Date:</b> {d.get('event_date','')}</p>
              <p><b>Time:</b> {d.get('start_time','')} – {d.get('end_time','')}</p>
              <p><b>Venue:</b> {d.get('venue_name','')}, {d.get('city','')}</p>
              <p><b>Address:</b> {d.get('full_address','')}</p>
              <p><b>Package:</b> {d.get('package','').title()}</p>
              <p><b>Notes:</b> {d.get('special_requests','None')}</p>
            </div>
            <div style="background:#0d0d1a;padding:14px;text-align:center">
              <p style="color:#d4af37;margin:0">Thathvamasi Clicks | +91 89391 16189</p>
            </div></div>"""
            mail.send(msg)
            print("✅ Photographer email sent!")
        except Exception as e:
            print(f"❌ Photographer email FAILED: {e}")

        # Confirmation to Client
        try:
            print("📧 Sending client email...")
            msg2 = Message(
                subject=f"Booking Confirmed #{bid} — Thathvamasi Clicks",
                recipients=[d.get('email','')]
            )
            msg2.html = f"""<div style="font-family:Arial;max-width:600px;margin:auto">
            <div style="background:#0d0d1a;padding:20px;text-align:center">
              <h1 style="color:#d4af37">Thathvamasi Clicks</h1>
              <p style="color:#fff">Capturing Moments, Creating Memories</p>
            </div>
            <div style="padding:30px;background:#fff">
              <h2>Hi {d.get('full_name','')}! Booking Confirmed 🎉</h2>
              <div style="background:#f9f9f9;border-left:4px solid #d4af37;padding:16px;margin:20px 0">
                <p><b>Booking ID:</b> #{bid}</p>
                <p><b>Event:</b> {d.get('event_type','')}</p>
                <p><b>Date:</b> {d.get('event_date','')}</p>
                <p><b>Time:</b> {d.get('start_time','')} – {d.get('end_time','')}</p>
                <p><b>Venue:</b> {d.get('venue_name','')}, {d.get('city','')}</p>
                <p><b>Package:</b> {d.get('package','').title()}</p>
              </div>
              <p>For queries: <b>+91 89391 16189</b></p>
              <p>With love,<br><b>Team Thathvamasi Clicks</b></p>
            </div>
            <div style="background:#0d0d1a;padding:15px;text-align:center">
              <p style="color:#d4af37;margin:0">Thathvamasi Clicks | Pallipalayam, Erode</p>
            </div></div>"""
            mail.send(msg2)
            print("✅ Client email sent!")
        except Exception as e:
            print(f"❌ Client email FAILED: {e}")

        return jsonify({
            'success':    True,
            'message':    f'Booking confirmed! ID #{bid}. Check your email.',
            'booking_id': bid
        })

    return render_template('booknow.html')


@app.route('/api/review', methods=['POST'])
def add_review():
    d = request.get_json()
    try:
        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO testimonials(name,location,rating,message) VALUES(%s,%s,%s,%s)",
                (d.get('name',''),d.get('location',''),d.get('rating',5),d.get('message',''))
            )
            conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print(f"❌ Review error: {e}")
    return jsonify({'success':True})


# ── RUN ──────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)