from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from .choices import price_choices, state_choices, bedroom_choices

# For paging, see Django documentation


def index(request):
    # Get listings from db
    # listings = Listing.objects.all()
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Instantiating the pagination with our data and # of entities per page
    paginator = Paginator(listings, 6)

    # Configuring the request URL to include a page query
    page = request.GET.get('page')

    # Our paged listings that we want to pass into context
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    # listing = Listing.objects.get(id=listing_id) this does work

    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    # We pull all objects from the database
    queryset_list = Listing.objects.order_by('-list_date')

    # Check the query strings and pull the values for filtering
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        # Check it's not an empty string
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET['city']
        # Check it's not an empty string
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    if 'state' in request.GET:
        state = request.GET['state']
        # Check it's not an empty string
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        # Check it's not an empty string
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    if 'price' in request.GET:
        price = request.GET['price']
        # Check it's not an empty string
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'price_choices': price_choices,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
