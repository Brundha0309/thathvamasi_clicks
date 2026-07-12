import smtplib

email = "thathvamasi.clicks@gmail.com"
app_password = "ipva sfog qcad rcfn"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, app_password)
    print("Login Successful!")
    server.quit()
except Exception as e:
    print(e)