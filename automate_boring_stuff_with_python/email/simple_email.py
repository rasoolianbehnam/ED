from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import os

#msg = MIMEText("Here is the body of my message")
#msg["From"] = "me@example.com"
#msg["To"] = "bzr0014@auburn.edu"
#msg["Subject"] = "This is the subject."
#p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
#p.communicate(msg.as_string())

def sendMail():
    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % "from@somewhere.com")
    p.write("To: %s\n" % "bzr0014@auburn.edu")
    p.write("Subject: thesubject\n")
    p.write("\n") # blank line separating headers from body
    p.write("body of the mail")
    status = p.close()
    if status != 0:
           print("Sendmail exit status", status)
sendMail()
