from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices


def index(reqeest):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 1)
    page = reqeest.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(reqeest, 'listings/listings.html', context)

def listing(reqeest, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }

    return render(reqeest, 'listings/listing.html', context)

def search(reqeest):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in reqeest.GET:
        keywords = reqeest.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in reqeest.GET:
        city = reqeest.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in reqeest.GET:
        state = reqeest.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in reqeest.GET:
        bedrooms = reqeest.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # price
    if 'price' in reqeest.GET:
        price = reqeest.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': reqeest.GET
    }
    return render(reqeest, 'listings/search.html', context)