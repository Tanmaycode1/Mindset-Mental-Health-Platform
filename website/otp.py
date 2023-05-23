import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp(rr,email):
   sender_email = "examplemsit@gmail.com"
   receiver_email = email
   password = "smwtujbcmobbmbda"

   message = MIMEMultipart("alternative")
   message["Subject"] = "Otp for MindSet Signup"
   message["From"] = sender_email
   message["To"] = receiver_email


   text = """
   Hi welcome to Mind-Set
   Your otp for login is {}
   Never share this with Anyone We never ask for OTP""".format(rr)


   part1 = MIMEText(text, "plain")

   message.attach(part1)

   context = ssl.create_default_context()
   with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
       server.login(sender_email, password)
       server.sendmail(
           sender_email, receiver_email, message.as_string()
       )
