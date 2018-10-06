import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(subject, body):
    # me == my email address
    # you == recipient's email address
    me = "stockalerts33@gmail.com"
    you = "stockalerts33@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head>
      <style>
        table {{
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }}
        
        #stocks td, #stocks th {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        
        #stocks tr:nth-child(even){{background-color: #f2f2f2;}}
        
        #stocks tr:hover {{background-color: #ddd;}}
        
        #stocks th {{
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #4CAF50;
            color: white;
        }}
      </style>
      </head>
      <body>
        {body}
      </body>
    </html>
    """.format(body=body)

    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login("stockalerts33@gmail.com","K1shore123@")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
