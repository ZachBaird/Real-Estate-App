from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

import time


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
