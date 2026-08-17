import os
import resend
from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
 
# ── RESEND EMAIL CONFIG ───────────────────────────────
resend.api_key = os.environ.get('RESEND_API_KEY')
PHOTOGRAPHER_EMAIL = os.environ.get('PHOTOGRAPHER_EMAIL', 'thathvamasi.clicks@gmail.com')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'hello@thathvamasiclicks.com')

# ── DATABASE CONFIG ──────────────────────────────────
DB_CONFIG = {
    'host': os.environ.get('MYSQLHOST', 'localhost'),
    'port': int(os.environ.get('MYSQLPORT', '3306')),
    'user': os.environ.get('MYSQLUSER', 'root'),
    'password': os.environ.get('MYSQLPASSWORD', ''),  # Empty password
    'database': os.environ.get('MYSQLDATABASE', 'thathvamasi_db'),
    'connection_timeout': 30,
    'use_pure': True
}

def get_db_connection(database=None):
    """Get database connection, optionally with specific database"""
    try:
        conn_args = {
            'host': DB_CONFIG['host'],
            'port': DB_CONFIG['port'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password'],
            'connection_timeout': DB_CONFIG['connection_timeout'],
            'use_pure': DB_CONFIG['use_pure']
        }
        
        # Add database if specified
        if database:
            conn_args['database'] = database
        
        # Handle SSL for cloud hosts
        if 'aivencloud' in DB_CONFIG['host']:
            conn_args['ssl_disabled'] = False
            
        conn = mysql.connector.connect(**conn_args)
        return conn
    except Error as e:
        print(f"❌ DB Connection Error: {e}")
        return None

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        # Connect without specifying a database
        conn = get_db_connection()
        if not conn:
            print("❌ Cannot connect to MySQL server")
            return False
            
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{DB_CONFIG['database']}'")
        result = cursor.fetchone()
        
        if not result:
            print(f"📁 Database '{DB_CONFIG['database']}' not found. Creating...")
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"✅ Database '{DB_CONFIG['database']}' created successfully")
        else:
            print(f"✅ Database '{DB_CONFIG['database']}' already exists")
            
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def get_db():
    """Get database connection with database selected"""
    try:
        # First ensure database exists
        if not create_database_if_not_exists():
            return None
            
        # Now connect with database
        conn = get_db_connection(DB_CONFIG['database'])
        if conn:
            print(f"🔌 Connected to {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
            print("✅ DB Connected")
        return conn
    except Error as e:
        print(f"❌ DB Connection Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return None

def init_db():
    """Initialize database tables"""
    conn = get_db()
    if not conn:
        print("⚠️ No DB connection")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create bookings table
        cursor.execute("""CREATE TABLE IF NOT EXISTS bookings(
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
        print("✅ Bookings table ready")
        
        # Create contacts table
        cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            mobile VARCHAR(20),
            subject VARCHAR(200),
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        print("✅ Contacts table ready")
        
        # Create testimonials table
        cursor.execute("""CREATE TABLE IF NOT EXISTS testimonials(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            location VARCHAR(100),
            rating INT NOT NULL DEFAULT 5,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        print("✅ Testimonials table ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All tables ready")
        return True
        
    except Exception as e:
        print(f"❌ Table creation error: {e}")
        return False

# ── ROUTES ───────────────────────────────────────────
@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/ping')
def ping(): 
    return 'pong', 200

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/services')
def services(): 
    return render_template('services.html')

@app.route('/portfolio')
def portfolio(): 
    return render_template('portfolio.html')

@app.route('/pricing')
def pricing(): 
    return render_template('packages.html')

@app.route('/testimonials')
def testimonials(): 
    return render_template('testimonials.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        d = request.get_json()
        if not d:
            return jsonify({'success':False,'message':'No data'})

        # Save to DB
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO contacts(name,email,mobile,subject,message) VALUES(%s,%s,%s,%s,%s)",
                    (d.get('name',''), d.get('email',''), d.get('mobile',''),
                     d.get('subject',''), d.get('message',''))
                )
                conn.commit()
                cursor.close()
                conn.close()
                print("✅ Contact saved to database")
        except Exception as e:
            print(f"❌ Contact DB error: {e}")

        # Send email via Resend
        try:
            resend.Emails.send({
                "from": f"Thathvamasi Clicks <{FROM_EMAIL}>",
                "to": [PHOTOGRAPHER_EMAIL],
                "reply_to": d.get('email',''),
                "subject": f"New Contact: {d.get('subject','General Inquiry')}",
                "html": f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h2 style="color:#d4af37">Thathvamasi Clicks</h2>
                    <p style="color:#fff">New Contact Form Message</p>
                  </div>
                  <div style="padding:24px;background:#fff">
                    <p><b>Name:</b> {d.get('name','')}</p>
                    <p><b>Email:</b> {d.get('email','')}</p>
                    <p><b>Mobile:</b> {d.get('mobile','Not provided')}</p>
                    <p><b>Event Type:</b> {d.get('eventType','Not specified')}</p>
                    <p><b>Subject:</b> {d.get('subject','No subject')}</p>
                    <p><b>Message:</b><br>{d.get('message','')}</p>
                  </div>
                  <div style="background:#0d0d1a;padding:14px;text-align:center">
                    <p style="color:#d4af37;margin:0">Thathvamasi Clicks | Pallipalayam, Erode</p>
                  </div>
                </div>"""
            })
            print("✅ Contact email sent via Resend")
        except Exception as e:
            print(f"❌ Contact Resend error: {e}")

        return jsonify({'success':True,'message':'Message sent successfully!'})
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
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO bookings(
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
                bid = cursor.lastrowid
                cursor.close()
                conn.close()
                print(f"✅ Booking saved — ID #{bid}")
            else:
                bid = "N/A"
                print("⚠️ No DB — email only mode")
        except Exception as e:
            bid = "N/A"
            print(f"❌ DB error: {e}")

        # ── Email to Photographer via Resend ──
        try:
            print("📧 Sending photographer email via Resend...")
            resend.Emails.send({
                "from": f"Thathvamasi Clicks <{FROM_EMAIL}>",
                "to": [PHOTOGRAPHER_EMAIL],
                "reply_to": d.get('email',''),
                "subject": f"📸 New Booking #{bid} — {d.get('event_type','')}",
                "html": f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h2 style="color:#d4af37;margin:0">Thathvamasi Clicks</h2>
                    <p style="color:#fff;font-size:13px">🎉 New Booking Received!</p>
                  </div>
                  <div style="padding:28px;background:#fff">
                    <table style="width:100%;border-collapse:collapse;font-size:14px">
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888;width:140px"><b>Booking ID</b></td>
                        <td style="padding:10px;color:#d4af37;font-weight:bold">#{bid}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Client Name</b></td>
                        <td style="padding:10px">{d.get('full_name','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Mobile</b></td>
                        <td style="padding:10px">{d.get('mobile','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Email</b></td>
                        <td style="padding:10px">{d.get('email','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Event</b></td>
                        <td style="padding:10px">{d.get('event_type','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Date</b></td>
                        <td style="padding:10px">{d.get('event_date','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Time</b></td>
                        <td style="padding:10px">{d.get('start_time','')} – {d.get('end_time','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Venue</b></td>
                        <td style="padding:10px">{d.get('venue_name','')}, {d.get('city','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Address</b></td>
                        <td style="padding:10px">{d.get('full_address','')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Package</b></td>
                        <td style="padding:10px;color:#d4af37;font-weight:bold">{d.get('package','').title()}</td>
                      </tr>
                      <tr>
                        <td style="padding:10px;color:#888;vertical-align:top"><b>Notes</b></td>
                        <td style="padding:10px">{d.get('special_requests','None')}</td>
                      </tr>
                    </table>
                  </div>
                  <div style="background:#0d0d1a;padding:14px;text-align:center">
                    <p style="color:#d4af37;margin:0;font-size:12px">
                      Thathvamasi Clicks | +91 89391 16189 | Pallipalayam, Erode
                    </p>
                  </div>
                </div>"""
            })
            print("✅ Photographer email sent via Resend!")
        except Exception as e:
            print(f"❌ Photographer Resend error: {e}")

        # ── Confirmation Email to Client via Resend ──
        try:
            print("📧 Sending client confirmation via Resend...")
            resend.Emails.send({
                "from": f"Thathvamasi Clicks <{FROM_EMAIL}>",
                "to": [d.get('email','')],
                "subject": f"✅ Booking Confirmed #{bid} — Thathvamasi Clicks",
                "html": f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h1 style="color:#d4af37;margin:0">📸 Thathvamasi Clicks</h1>
                    <p style="color:#fff;margin:6px 0">Capturing Moments, Creating Memories</p>
                  </div>
                  <div style="padding:30px;background:#fff">
                    <h2 style="color:#0d0d1a">Hi {d.get('full_name','')}! 🎉</h2>
                    <p style="color:#555;line-height:1.7">
                      Thank you for booking with <b>Thathvamasi Clicks</b>!
                      Your booking has been received and our team will
                      contact you shortly to confirm the details.
                    </p>
                    <div style="background:#f9f9f9;border-left:4px solid #d4af37;
                                padding:16px;margin:20px 0;border-radius:4px">
                      <h3 style="color:#0d0d1a;margin-top:0">Booking Summary</h3>
                      <p style="margin:6px 0"><b>Booking ID:</b> #{bid}</p>
                      <p style="margin:6px 0"><b>Event:</b> {d.get('event_type','')}</p>
                      <p style="margin:6px 0"><b>Date:</b> {d.get('event_date','')}</p>
                      <p style="margin:6px 0"><b>Time:</b> {d.get('start_time','')} – {d.get('end_time','')}</p>
                      <p style="margin:6px 0"><b>Venue:</b> {d.get('venue_name','')}, {d.get('city','')}</p>
                      <p style="margin:6px 0"><b>Package:</b> {d.get('package','').title()}</p>
                    </div>
                    <p style="color:#555">
                      For queries: <b>+91 89391 16189</b><br>
                      Email: thathvamasi.clicks@gmail.com
                    </p>
                    <p style="color:#555">
                      With love,<br>
                      <b style="color:#0d0d1a">Team Thathvamasi Clicks</b>
                    </p>
                  </div>
                  <div style="background:#0d0d1a;padding:15px;text-align:center">
                    <p style="color:#d4af37;margin:0;font-size:12px">
                      © 2024 Thathvamasi Clicks | Pallipalayam, Erode, Tamil Nadu
                    </p>
                  </div>
                </div>"""
            })
            print("✅ Client confirmation email sent via Resend!")
        except Exception as e:
            print(f"❌ Client Resend error: {e}")

        return jsonify({
            'success': True,
            'message': f'Booking confirmed! ID #{bid}. Check your email.',
            'booking_id': bid
        })

    return render_template('booknow.html')

@app.route('/api/review', methods=['POST'])
def add_review():
    d = request.get_json()
    try:
        conn = get_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO testimonials(name,location,rating,message) VALUES(%s,%s,%s,%s)",
                (d.get('name',''), d.get('location',''),
                 d.get('rating',5), d.get('message',''))
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Review saved to database")
    except Exception as e:
        print(f"❌ Review error: {e}")
    return jsonify({'success':True})

# ── RUN ──────────────────────────────────────────────
if __name__ == '__main__':
    print("🚀 Starting Thathvamasi Clicks Application...")
    
    # Initialize database
    if init_db():
        print("✅ Database initialized successfully")
    else:
        print("⚠️ Database initialization failed - running in email-only mode")
    
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Server running on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
