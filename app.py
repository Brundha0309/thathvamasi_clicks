import os
import resend
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── RESEND EMAIL CONFIG ───────────────────────────────
resend.api_key = os.environ.get('RESEND_API_KEY')
PHOTOGRAPHER_EMAIL = os.environ.get('PHOTOGRAPHER_EMAIL', 'thathvamasi.clicks@gmail.com')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'hello@thathvamasiclicks.com')

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
    # No database — page will show only static/hardcoded reviews from the template
    return render_template('testimonials.html', db_reviews=[])


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        d = request.get_json()
        if not d:
            return jsonify({'success': False, 'message': 'No data'})

        # Send email via Resend
        try:
            resend.Emails.send({
                "from": f"Thathvamasi Clicks <{FROM_EMAIL}>",
                "to": [PHOTOGRAPHER_EMAIL],
                "reply_to": d.get('email', ''),
                "subject": f"New Contact: {d.get('subject', 'General Inquiry')}",
                "html": f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h2 style="color:#d4af37">Thathvamasi Clicks</h2>
                    <p style="color:#fff">New Contact Form Message</p>
                  </div>
                  <div style="padding:24px;background:#fff">
                    <p><b>Name:</b> {d.get('name', '')}</p>
                    <p><b>Email:</b> {d.get('email', '')}</p>
                    <p><b>Mobile:</b> {d.get('mobile', 'Not provided')}</p>
                    <p><b>Event Type:</b> {d.get('eventType', 'Not specified')}</p>
                    <p><b>Subject:</b> {d.get('subject', 'No subject')}</p>
                    <p><b>Message:</b><br>{d.get('message', '')}</p>
                  </div>
                  <div style="background:#0d0d1a;padding:14px;text-align:center">
                    <p style="color:#d4af37;margin:0">Thathvamasi Clicks | Pallipalayam, Erode</p>
                  </div>
                </div>"""
            })
            print("✅ Contact email sent via Resend")
        except Exception as e:
            print(f"❌ Contact Resend error: {e}")

        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    return render_template('contact.html')

@app.route('/booknow', methods=['GET', 'POST'])
def booknow():
    if request.method == 'POST':
        d = request.get_json()
        print(f"📥 Booking received: {d}")
        if not d:
            return jsonify({'success': False, 'message': 'No data received'})

        # No database — generate a simple reference using timestamp instead of an auto-increment ID
        import time
        bid = int(time.time())

        # ── Email to Photographer via Resend ──
        try:
            print("📧 Sending photographer email via Resend...")
            resend.Emails.send({
                "from": f"Thathvamasi Clicks <{FROM_EMAIL}>",
                "to": [PHOTOGRAPHER_EMAIL],
                "reply_to": d.get('email', ''),
                "subject": f"📸 New Booking #{bid} — {d.get('event_type', '')}",
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
                        <td style="padding:10px">{d.get('full_name', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Mobile</b></td>
                        <td style="padding:10px">{d.get('mobile', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Email</b></td>
                        <td style="padding:10px">{d.get('email', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Event</b></td>
                        <td style="padding:10px">{d.get('event_type', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Date</b></td>
                        <td style="padding:10px">{d.get('event_date', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Time</b></td>
                        <td style="padding:10px">{d.get('start_time', '')} – {d.get('end_time', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Venue</b></td>
                        <td style="padding:10px">{d.get('venue_name', '')}, {d.get('city', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Address</b></td>
                        <td style="padding:10px">{d.get('full_address', '')}</td>
                      </tr>
                      <tr style="border-bottom:1px solid #eee">
                        <td style="padding:10px;color:#888"><b>Package</b></td>
                        <td style="padding:10px;color:#d4af37;font-weight:bold">{d.get('package', '').title()}</td>
                      </tr>
                      <tr>
                        <td style="padding:10px;color:#888;vertical-align:top"><b>Notes</b></td>
                        <td style="padding:10px">{d.get('special_requests', 'None')}</td>
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
                "to": [d.get('email', '')],
                "subject": f"✅ Booking Confirmed #{bid} — Thathvamasi Clicks",
                "html": f"""
                <div style="font-family:Arial;max-width:600px;margin:auto">
                  <div style="background:#0d0d1a;padding:20px;text-align:center">
                    <h1 style="color:#d4af37;margin:0">📸 Thathvamasi Clicks</h1>
                    <p style="color:#fff;margin:6px 0">Capturing Moments, Creating Memories</p>
                  </div>
                  <div style="padding:30px;background:#fff">
                    <h2 style="color:#0d0d1a">Hi {d.get('full_name', '')}! 🎉</h2>
                    <p style="color:#555;line-height:1.7">
                      Thank you for booking with <b>Thathvamasi Clicks</b>!
                      Your booking has been received and our team will
                      contact you shortly to confirm the details.
                    </p>
                    <div style="background:#f9f9f9;border-left:4px solid #d4af37;
                                padding:16px;margin:20px 0;border-radius:4px">
                      <h3 style="color:#0d0d1a;margin-top:0">Booking Summary</h3>
                      <p style="margin:6px 0"><b>Booking ID:</b> #{bid}</p>
                      <p style="margin:6px 0"><b>Event:</b> {d.get('event_type', '')}</p>
                      <p style="margin:6px 0"><b>Date:</b> {d.get('event_date', '')}</p>
                      <p style="margin:6px 0"><b>Time:</b> {d.get('start_time', '')} – {d.get('end_time', '')}</p>
                      <p style="margin:6px 0"><b>Venue:</b> {d.get('venue_name', '')}, {d.get('city', '')}</p>
                      <p style="margin:6px 0"><b>Package:</b> {d.get('package', '').title()}</p>
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
    # No database — reviews can't be stored/persisted anymore.
    # If you want new reviews to show up, add them manually into testimonials.html.
    return jsonify({'success': True, 'message': 'Thanks! (Note: reviews are not saved without a database)'})

# ── RUN ──────────────────────────────────────────────
if __name__ == '__main__':
    print("🚀 Starting Thathvamasi Clicks Application (email-only mode, no database)...")
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Server running on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)