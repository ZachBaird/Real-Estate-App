from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.mail import send_mail
from .models import Contact, Inquiry

from .send_docs import send_document_for_signing

import time
import imapclient
import pyzmail
import bs4


def contact(request):
    # Determine if the HTTP request was a POST
    if request.method == 'POST':
        # Pull submitted data
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already inquired after this listing.')
                return redirect('/listings/'+listing_id)

        # Create contact object
        contact = Contact(listing=listing, listing_id=listing_id, name=name,
                          email=email, phone=phone, message=message, user_id=user_id)

        # Save contact object to db
        contact.save()

        # Send email to realtor
        send_mail(
            'New Listing Inquiry',
            'New Inquiry for listing '+listing +
            '. Log in to the admin panel to review the contact info.',
            'zachbairddev@gmail.com',
            [realtor_email, 'johnreese690@gmail.com'],
            fail_silently=False
        )

        messages.success(
            request, 'Your request has been submitted and a realtor will get back to you soon.')

        return redirect('/listings/'+listing_id)


def getemails(request):
    # Check to make sure a super user is using this page
    if request.user.is_authenticated and request.user.email == 'zach@gmail.com':
        # We declare our imap object, 'conn', specifying our imap server and that we're using SSL encryption.
        # After that, we log in with my credentials and select the inbox folder. We set readonly so I don't delete stuff
        conn = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        conn.login({{username}} {{password}})
        conn.select_folder('INBOX', readonly=True)

        # We pull out email IDs that meet the criteria in my search and store them in a list
        email_ids = conn.search(['FROM', 'zdb1994@yahoo.com'])

        # Declare our empty lists for processing
        raw_messages = []
        pyz_messages = []
        message_strs = []
        inquiry_names = []
        inquiry_emails = []
        inquiry_phones = []
        inquiry_zipcodes = []
        inquiry_headlines = []
        inquiry_ref_ids = []
        inquiries = []

        # For each email ID, pull and store a raw message
        for Id in email_ids:
            # Here I am pulling out the raw text of my first ID I stored, searching for the BODY[] and FLAGS
            raw_messages.append(conn.fetch([Id], ['BODY[]', 'FLAGS']))

        # For each email Id, grab that Id's raw_message and abstract the data into pyz_messages
        index = 0
        while index < len(email_ids):
            pyz_messages.append(pyzmail.PyzMessage.factory(
                raw_messages[index][email_ids[index]][b'BODY[]']))

            index += 1

        # For each pyzmessage that we now have, grab the html payload
        for pyzmessage in pyz_messages:
            message_strs.append(
                pyzmessage.html_part.get_payload().decode('UTF-8'))

        # Close the imap connection
        conn.logout()

        # Time to start constructing our data to pass to the template
        # For each message...
        for html_message in message_strs:
            # Declare our beautiful soup object with the html parser.
            soup = bs4.BeautifulSoup(html_message, 'html.parser')

            inquiry_names.append(soup.select(
                'tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > span')[0].text)
            inquiry_emails.append(soup.select(
                'tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(3) > td:nth-child(3) > span > a')[0].text)
            inquiry_phones.append(soup.select(
                'tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(4) > td:nth-child(3) > span')[0].text)
            inquiry_zipcodes.append(soup.select(
                'tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(5) > td:nth-child(3) > span')[0].text)
            inquiry_headlines.append(soup.select(
                'tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(12) > td:nth-child(3) > span')[0].text)
            inquiry_ref_ids.append(soup.select(
                'tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(14) > td:nth-child(3) > span')[0].text)

        print(inquiry_emails)

        index = 0
        while index < len(inquiry_names):
            # Pull existing inquiries to check existing data.
            existing_inquiries = Inquiry.objects.all().filter(
                email=inquiry_emails[index])

            if not existing_inquiries:
                print(
                    f'Email {inquiry_emails[index]} does not exist in the db.')
                    
                new_dict = {
                    'inquiry_name': inquiry_names[index],
                    'inquiry_phone': inquiry_phones[index],
                    'inquiry_email': inquiry_emails[index],
                    'inquiry_zipcode': inquiry_zipcodes[index],
                    'inquiry_headline': inquiry_headlines[index],
                    'inquiry_ref_id': inquiry_ref_ids[index]
                }

                inquiries.append(new_dict)
            index += 1

        context = {
            'inquiries': inquiries
        }

        return render(request, 'pages/email_list.html', context)
    else:
        return redirect('index')


def sendnda(request):
    if request.method == 'POST':
        name = request.POST['inquiryName']
        email = request.POST['inquiryEmail']
        phone = request.POST['inquiryPhone']
        zipcode = request.POST['inquiryZipcode']
        ref_id = request.POST['inquiryRefId']
        headline = request.POST['inquiryHeadline']

        results = send_document_for_signing(name, email)

        inquiry = Inquiry(name=name, email=email, phone=phone,
                          zipcode=zipcode, ref_id=ref_id, headline=headline, nda_sent=True)

        inquiry.save()

        messages.success(request, 'An NDA has been sent to ' + name)
        return redirect('getemails')
