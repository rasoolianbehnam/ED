import imapclient
import pyzmail
import getpass
from pprint import pprint
import datetime

password = getpass.getpass()
imapObj = imapclient.IMAPClient('outlook.office365.com', port=993, ssl=True)
imapObj.login('szh0102@tigermail.auburn.edu', password)
try:
    imapObj.select_folder('INBOX', readonly=True)
    #UIDs = imapObj.search(['SINCE 01-Jul-2018'])
    UIDs = imapObj.search(['SINCE', datetime.date(2018, 10, 21)])
    print(UIDs)
    rawMessages = imapObj.fetch(UIDs[-1], ['BODY[]'])
    message = pyzmail.PyzMessage.factory(rawMessages[UIDs[-1]]['BODY[]'])
    print(message.get_subject())
    #if message.text_part is not None:
    #    pprint(message.text_part.get_payload().decode(message.text_part.charset))
    #if message.html_part is not None:
    #    pprint(message.text_part.get_payload().decode(message.text_part.charset))
except Exception as e:
    pprint("Error Occured!")
    print(e)
finally:
    #imapObj.logout()
    #print('Connection closed safely!')
    pass
