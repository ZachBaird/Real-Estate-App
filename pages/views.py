from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import price_choices, bedroom_choices, state_choices
import imaplib
import email
import imapclient
import pyzmail
import bs4


def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def index(request):
    listings = Listing.objects.order_by(
        '-list_date').filter(is_published=True)[:3]

    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.all()
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)


def getemails(request):
    imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imapObj.login('zachbairddev@gmail.com', '[password]')
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
