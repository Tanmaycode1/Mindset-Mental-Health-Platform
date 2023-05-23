import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mail(email):
   sender_email = "examplemsit@gmail.com"
   receiver_email = email
   password = "smwtujbcmobbmbda"

   message = MIMEMultipart("alternative")
   message["Subject"] = "Confirmation regarding online psychiatrist appointment"
   message["From"] = sender_email
   message["To"] = receiver_email


   text = """

Dear Patient,

I hope this email finds you well. As we previously discussed, your appointment with our psychiatrist is successfully scheduled.
To join the video call, please click on the Zoom link provided below:
[Insert Zoom Link Here]
Please make sure to join the call a few minutes before your scheduled appointment time to ensure that you have a stable internet connection and that your video and audio are working properly.
If you have any questions or concerns, please do not hesitate to contact me. We look forward to speaking with you soon.

Best regards,
MindSet
"""


   part1 = MIMEText(text, "plain")

   message.attach(part1)

   context = ssl.create_default_context()
   with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
       server.login(sender_email, password)
       server.sendmail(
           sender_email, receiver_email, message.as_string()
       )
