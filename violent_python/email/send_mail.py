import smtplib
from email.mime.text import MIMEText
import getpass
from process_attachment import *

def sendGmail(user, pwd="", to="", subject="", text=""):
    msg = MIMEText(text)
    msg['From'] = user
    msg['T'] = to
    msg['Subject'] = subject
    try:
        smtpServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print "[+] Connecting To Mail Server."
        smtpServer.ehlo()
        #print "[+] Staring Encrypted Session."
        #smtpServer.starttls()
        #smtpServer.ehlo()
        print "[+] Logging Into Mail Server."
        smtpServer.login(user, pwd)
        print "[+]Sending Mail."
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print "[+] Mail Sent Successfully."
    except Exception, e:
        print "[-] Sending Failed.",
        print e
    
def sendAumail(user, pwd, to, subject="", text="", attachment=None, From=None):
    if attachment:
        msg = MIMEMultipart()
        msg.attach(attachment)
    else:
        msg = MIMEText(text)
    msg['From'] = user
    if From:
        msg['From'] = From
    msg['T'] = to
    msg['Subject'] = subject
    try:
        smtpServer = smtplib.SMTP('outlook.office365.com', 25)
        print "[+] Connecting To Mail Server."
        smtpServer.ehlo()
        print "[+] Staring Encrypted Session."
        smtpServer.starttls()
        smtpServer.ehlo()
        print "[+] Logging Into Mail Server."
        smtpServer.login(user, pwd)
        print "[+]Sending Mail."
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print "[+] Mail Sent Successfully."
    except Exception, e:
        print "[-] Sending Failed.",
        print e
 
attachment = create_attachment('run.sh')
gmail_user = 'behnam.rasoulian@gmail.com'
auburn_user = 'bzr0014@tigermail.auburn.edu'
password = getpass.getpass("Please enter password: ")
to = 'bzr0014@auburn.edu'
subject = "test"
text = "text"
sendAumail(auburn_user, password, to, subject=subject,\
        text=text, attachment=attachment)