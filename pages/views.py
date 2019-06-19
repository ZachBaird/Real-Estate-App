from django.shortcuts import render
import imaplib
import email
import imapclient
import pyzmail
from django.http import HttpResponse
import bs4


def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def getemails(request):
    '''
      user = 'zachbairddev@gmail.com'
      password = 'Cryolenix1'
      imap_url = 'imap.gmail.com'

      conn = imaplib.IMAP4_SSL(imap_url)

      conn.login(user, password)
      conn.select('INBOX')
      result, data = conn.fetch(b'0', '(RFC822)')
      raw = email.message_from_bytes(data[0][1])
      # print(get_body(raw))
      msgs = pull_emails(search('FROM', 'mail-noreply@google.com', conn))
      for msg in msgs:
          print(get_body(email.message_from_bytes(msg[0][1])))
    '''

    imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imapObj.login('zachbairddev@gmail.com', 'Cryolenix1')
    imapObj.select_folder('INBOX', readonly=True)
    UIDS = imapObj.search(['SINCE', '15-JUN-2019'])
    print(UIDS)

    rawMessages = imapObj.fetch([82], ['BODY[]', 'FLAGS'])

    message = pyzmail.PyzMessage.factory(rawMessages[82][b'BODY[]'])

    subject = message.get_subject(),
    sender = message.get_addresses('from')
    message_body_html = message.html_part.get_payload().decode(message.html_part.charset)

    htmlParse = bs4.BeautifulSoup(message_body_html)

    story = htmlParse.select('td .email-fontSize18')

    return HttpResponse(f'<p>Subject is {subject}</p><br><p>Sender is {sender[0]}</p><br><p>Body Copy is {story[0]}</p>')
