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
app.config['MAIL_USERNAME']       = 'thathvamasi.clicks@gmail.com'
app.config['MAIL_PASSWORD']       = 'nzwhkcqghfzsdnbq'
app.config['MAIL_DEFAULT_SENDER'] = 'thathvamasi.clicks@gmail.com'
app.config['MAIL_DEBUG']          = True
app.config['MAIL_SUPPRESS_SEND']  = False

PHOTOGRAPHER_EMAIL = 'thathvamasi.clicks@gmail.com'

mail = Mail(app)

# ── DATABASE ─────────────────────────────────────────
DB_CONFIG = {
    'host':         os.environ.get('MYSQLHOST',     'localhost'),
    'port':         int(os.environ.get('MYSQLPORT', 3306)),
    'database':     os.environ.get('MYSQLDATABASE', 'thathvamasi_db'),
    'user':         os.environ.get('MYSQLUSER',     'root'),
    'password':     os.environ.get('MYSQLPASSWORD', 'Brundha@0309'),
    'ssl_disabled': False,
    'connection_timeout': 30,
}

def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Database Connected")
        return conn
    except Error as e:
        print(f"❌ Database Error: {e}")
        return None

def init_db():
    conn = get_db()
    if not conn:
        return
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
    print("✅ All Tables Ready")

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        d = request.get_json()
        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO contacts(name,email,mobile,subject,message) VALUES(%s,%s,%s,%s,%s)",
                (d['name'], d['email'], d.get('mobile', ''), d.get('subject', ''), d['message'])
            )
            conn.commit()
            cur.close()
            conn.close()
        try:
            mail.send(Message(
                subject=f"New Contact: {d.get('subject','General Inquiry')}",
                recipients=[PHOTOGRAPHER_EMAIL],
                html=f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h2 style="color:#d4af37">Thathvamasi Clicks</h2>
                    <p style="color:#fff;font-size:13px">New Contact Form Submission</p>
                  </div>
                  <div style="padding:28px;background:#fff">
                    <p><b>Name:</b> {d['name']}</p>
                    <p><b>Email:</b> {d['email']}</p>
                    <p><b>Mobile:</b> {d.get('mobile','Not provided')}</p>
                    <p><b>Event:</b> {d.get('eventType','Not specified')}</p>
                    <p><b>Subject:</b> {d.get('subject','No subject')}</p>
                    <p><b>Message:</b><br>{d['message']}</p>
                  </div>
                  <div style="background:#0d0d1a;padding:14px;text-align:center">
                    <p style="color:#d4af37;margin:0;font-size:12px">Thathvamasi Clicks | Pallipalayam, Erode</p>
                  </div>
                </div>"""
            ))
            print("✅ Contact email sent")
        except Exception as e:
            print(f"❌ Contact mail error: {e}")
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    return render_template('contact.html')


@app.route('/booknow', methods=['GET', 'POST'])
def booknow():
    if request.method == 'POST':
        d = request.get_json()
        print("📥 Booking received:", d)

        conn = get_db()
        bid = None

        try:
            if conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO bookings(
                        full_name,mobile,email,event_type,event_date,
                        start_time,end_time,venue_name,city,
                        full_address,package,special_requests
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    d['full_name'], d['mobile'], d['email'],
                    d['event_type'], d['event_date'],
                    d['start_time'], d['end_time'],
                    d['venue_name'], d['city'],
                    d['full_address'], d['package'],
                    d.get('special_requests', '')
                ))
                conn.commit()
                bid = cur.lastrowid
                cur.close()
                conn.close()
                print(f"✅ Booking saved — ID #{bid}")
            else:
                bid = "N/A"
                print("❌ DB not connected — email only mode")
        except Exception as db_err:
            bid = "N/A"
            print(f"❌ DB Exception: {db_err}")

        # ── Email to Photographer ──
        try:
            mail.send(Message(
                subject=f"New Booking #{bid} — {d['event_type']}",
                recipients=[PHOTOGRAPHER_EMAIL],
                html=f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h2 style="color:#d4af37;margin:0">Thathvamasi Clicks</h2>
                    <p style="color:#fff;font-size:13px">New Booking Received!</p>
                  </div>
                  <div style="padding:28px;background:#fff">
                    <table style="width:100%;border-collapse:collapse;font-size:14px">
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888;width:140px"><b>Booking ID</b></td><td style="padding:10px;color:#d4af37;font-weight:bold">#{bid}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Client Name</b></td><td style="padding:10px">{d['full_name']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Mobile</b></td><td style="padding:10px">{d['mobile']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Email</b></td><td style="padding:10px">{d['email']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Event</b></td><td style="padding:10px">{d['event_type']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Date</b></td><td style="padding:10px">{d['event_date']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Time</b></td><td style="padding:10px">{d['start_time']} – {d['end_time']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Venue</b></td><td style="padding:10px">{d['venue_name']}, {d['city']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Address</b></td><td style="padding:10px">{d['full_address']}</td></tr>
                      <tr style="border-bottom:1px solid #eee"><td style="padding:10px;color:#888"><b>Package</b></td><td style="padding:10px;color:#d4af37;font-weight:bold">{d['package'].title()}</td></tr>
                      <tr><td style="padding:10px;color:#888;vertical-align:top"><b>Notes</b></td><td style="padding:10px">{d.get('special_requests','None')}</td></tr>
                    </table>
                  </div>
                  <div style="background:#0d0d1a;padding:14px;text-align:center">
                    <p style="color:#d4af37;margin:0;font-size:12px">Thathvamasi Clicks | +91 89391 16189 | Pallipalayam, Erode</p>
                  </div>
                </div>"""
            ))
            print("✅ Email sent to photographer")
        except Exception as e:
            print(f"❌ Photographer mail error: {e}")

        # ── Confirmation Email to Client ──
        try:
            mail.send(Message(
                subject=f"Booking Confirmed #{bid} — Thathvamasi Clicks",
                recipients=[d['email']],
                html=f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h1 style="color:#d4af37;margin:0">Thathvamasi Clicks</h1>
                    <p style="color:#fff;margin:6px 0">Capturing Moments, Creating Memories</p>
                  </div>
                  <div style="padding:30px;background:#fff">
                    <h2 style="color:#0d0d1a">Hi {d['full_name']}! Your booking is confirmed</h2>
                    <p style="color:#555;line-height:1.7">
                      Thank you for booking with <b>Thathvamasi Clicks</b>!
                      Our team will contact you shortly to confirm the details.
                    </p>
                    <div style="background:#f9f9f9;border-left:4px solid #d4af37;padding:16px;margin:20px 0;border-radius:4px">
                      <p style="margin:6px 0"><b>Booking ID:</b> #{bid}</p>
                      <p style="margin:6px 0"><b>Event:</b> {d['event_type']}</p>
                      <p style="margin:6px 0"><b>Date:</b> {d['event_date']}</p>
                      <p style="margin:6px 0"><b>Time:</b> {d['start_time']} – {d['end_time']}</p>
                      <p style="margin:6px 0"><b>Venue:</b> {d['venue_name']}, {d['city']}</p>
                      <p style="margin:6px 0"><b>Package:</b> {d['package'].title()}</p>
                    </div>
                    <p style="color:#555">For queries: <b>+91 89391 16189</b></p>
                    <p style="color:#555">With love,<br><b>Team Thathvamasi Clicks</b></p>
                  </div>
                  <div style="background:#0d0d1a;padding:15px;text-align:center">
                    <p style="color:#d4af37;margin:0;font-size:12px">Thathvamasi Clicks | Pallipalayam, Erode, Tamil Nadu</p>
                  </div>
                </div>"""
            ))
            print("✅ Confirmation email sent to client")
        except Exception as e:
            print(f"❌ Client mail error: {e}")

        return jsonify({
            'success': True,
            'message': f'Booking confirmed! ID #{bid}. Check your email.',
            'booking_id': bid
        })

    return render_template('booknow.html')


@app.route('/api/review', methods=['POST'])
def add_review():
    d = request.get_json()
    conn = get_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO testimonials(name,location,rating,message) VALUES(%s,%s,%s,%s)",
                (d['name'], d.get('location', ''), d.get('rating', 5), d['message'])
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)
    return jsonify({'success': True})


# ── RUN ──────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)