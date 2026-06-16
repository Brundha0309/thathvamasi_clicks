# 📷 Thathvamasi Clicks — Full-Stack Photography Website

## Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask
- **Database**: MySQL
- **Email**: Flask-Mail (Gmail SMTP)

---

## 📁 Project Structure
```
thathvamasi/
├── app.py                  ← Flask backend (all routes + email + DB)
├── requirements.txt        ← Python dependencies
├── setup.sql               ← MySQL database schema
├── README.md               ← This file
├── templates/
│   ├── base.html           ← Shared navbar + footer + lightbox
│   ├── index.html          ← Homepage
│   ├── about.html          ← About page
│   ├── services.html       ← All 15 services
│   ├── portfolio.html      ← 140+ portfolio images with filter
│   ├── pricing.html        ← 3 packages + comparison table
│   ├── testimonials.html   ← Reviews + submit form
│   ├── contact.html        ← Contact form + FAQ
│   └── booknow.html        ← 5-step booking wizard
└── static/
    ├── css/
    │   └── style.css       ← Complete styles (dark navy + gold theme)
    └── js/
        └── main.js         ← Navbar, particles, lightbox, reveals
```

---

## ⚙️ Setup Instructions

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database
```bash
mysql -u root -p < setup.sql
```

### 3. Configure app.py
Open `app.py` and update these values:

```python
# Gmail SMTP (use App Password — NOT your Gmail password)
app.config['MAIL_USERNAME']  = 'your_gmail@gmail.com'
app.config['MAIL_PASSWORD']  = 'your_16char_app_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_gmail@gmail.com'

PHOTOGRAPHER_EMAIL = 'photographer@yourdomain.com'

# MySQL credentials
DB_CONFIG = {
    'host':     'localhost',
    'database': 'thathvamasi_db',
    'user':     'root',
    'password': 'your_mysql_password'
}
```

### 4. Enable Gmail App Password
1. Go to myaccount.google.com → Security
2. Enable 2-Step Verification
3. Go to App Passwords → Generate password for "Mail"
4. Use that 16-character password in MAIL_PASSWORD

### 5. Run the application
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 📄 Pages
| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero, services preview, portfolio teaser, testimonials, CTA |
| About | `/about` | Story, team, timeline |
| Services | `/services` | All 15 services with images |
| Portfolio | `/portfolio` | 140+ images with category filter + lightbox |
| Pricing | `/pricing` | 3 packages + comparison table + add-ons |
| Testimonials | `/testimonials` | 12 reviews + submit form |
| Contact | `/contact` | Contact form + FAQ |
| Book Now | `/booknow` | 5-step booking wizard |

---

## 📦 Packages Offered
| Package | Price | Highlights |
|---------|-------|------------|
| Standard | ₹40,000 | 1 Traditional Photographer + Videographer, 220 images album |
| Classic | ₹55,000 | + Candid Photographer, 250 images album |
| Elite | ₹75,000 | Full team, 2 albums, Cinematic video |

---

## ✉️ Email Flow
- **On Booking Submit**: 
  - Photographer receives full booking details (HTML email)
  - Customer receives confirmation with booking ID
- **On Contact Submit**:
  - Photographer receives the message

---

## 🎨 Customization Tips
- **Logo/Brand**: Update `brand-text` in `base.html` and brand colors in `:root` in `style.css`
- **Phone/Email**: Search `+91 XXXXX XXXXX` and `hello@thathvamasi.com` in all templates
- **Portfolio Images**: Replace Unsplash URLs in `portfolio.html` with your actual photos
- **Services Images**: Replace Unsplash URLs in `services.html` with your actual service photos
- **Package Prices**: Edit in `pricing.html` and `booknow.html`
- **Social Links**: Update `href="#"` links in `base.html` footer

