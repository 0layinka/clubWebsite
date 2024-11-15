from django.shortcuts import render, redirect, get_object_or_404
import calendar 
from django.contrib import messages
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.models import User
from .models import event, Venue
from .forms import venueForm, EventsForm,  EventsFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
import io
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
# Create your views here.


# home
def home(request, year=2024, month=datetime.now().strftime('%B')):
    # conversion
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    cal = HTMLCalendar().formatmonth(year,
                                     month_number)
    now = datetime.now()
    current_year = now.year
    time = now.strftime('%H:%M %p')

    events = event.objects.filter(
        date__year=year,
        date__month=month_number
    )




    name = request.user
    data = {
        'name': name,
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'current_year': current_year,
        'time': time,
        'events': events
    }
    return render(request, 'events/home.html', data)


# EVENTS

# events page
def event_page(request):
    events = event.objects.all().order_by('-id')

    data = {
        'Event': events
    }
    return render(request, 'events/event.html', data)
# add events
def addEvents(request):
    submited = False
    if request.method == 'POST':
        
        if request.user.is_superuser:
            form = EventsFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add-events?submited=True')

        else:
            form = EventsForm(request.POST)
            if form.is_valid():
                events = form.save(commit=False)
                events.manager = request.user
                events.save()
                return HttpResponseRedirect('/add-events?submited=True')
    else:
        if request.user.is_superuser:
            form = EventsFormAdmin()
        else:
           form = EventsForm() 

        if 'submited' in request.GET:
            submited = True

    return render(request, 'events/add_events.html', {'form': form, 'submited': submited})
# approve events (admin)
def approveEvents(request):
    user_counts = User.objects.all().count()
    venue_counts = Venue.objects.all().count()
    event_counts = event.objects.all().count()
    if request.method == 'POST':
        checked = request.POST.getlist('checked')
        event.objects.all().update(approved = False)
        for box in  checked:
            event.objects.all().filter(pk = int(box)).update(approved = True)

        return redirect(event_page)
    else:
        events = event.objects.all().order_by('-date')
        data = {
            'events': events,
            'user_counts': user_counts,
            'event_counts': event_counts,
            'venue_counts': venue_counts,
        }
        return render(request, 'events/approve_event.html', data)
    
# delete events
def deleteEvent(request, eventId):
    events = get_object_or_404(event, pk=eventId)
    if request.user == events.manager:
        messages.success(request, 'Deleted Successfully')
        events.delete()
        return redirect('events-list')
    else:
        messages.success(request, 'You Cant Delete This......')
        return redirect('events-list')
# search events
def searchEvents(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        events = event.objects.filter(name__contains=searched)

        data = {
            'searched': searched,
            'events': events
        }
        return render(request, 'events/search_events.html', data)
    else:
        return redirect('home')
   

# VENUE
# add venue
def addVenue(request):
    submited = False
    if request.method == 'POST':
        form = venueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/add-venue?submited=True')
    else:
        form = venueForm()

    if 'submited' in request.GET:
        submited = True

    return render(request, 'venue/add-venue.html', {'form': form, 'submited': submited})
# venue paginator 
def list_venue(request):
    venues = Venue.objects.all()

    p = Paginator(venues, 2)
    page = request.GET.get('page')
    p_venue = p.get_page(page)

    data = {
        'venue': venues,
        'paginations': p_venue
    }

    return render(request, 'venue/venue.html', data)
# show venue
def showVenue(request, venueId):
    venues = Venue.objects.get(pk = venueId)
    venue_owner = User.objects.get(pk=venues.owner)
    
    data = {
        'venue': venues,
        'owner': venue_owner
    }
    return render(request, 'venue/show-venue.html', data)
# update venue
def updateVenue(request, venueId):
    venue = get_object_or_404(Venue, pk=venueId)

    if request.method == 'POST':
        form = venueForm(request.POST, request.FILES,  instance=venue)
        if form.is_valid():
            form.save()
            return redirect('list-venue')
    else:
        form = venueForm(instance=venue)

    return render(request, 'venue/update-venue.html', {'form': form})
# search venue
def searchVenue(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        venue = Venue.objects.filter(name__contains=searched)

        data = {
            'searched': searched,
            'venue': venue
        }
        return render(request, 'venue/search-venue.html', data)
    else:
        return redirect('home')
# update venue
def updateEvents(request, eventId):
    events = get_object_or_404(event, pk=eventId)
    eventManager = event.objects.get(pk=eventId).manager

    if request.method == 'POST':
        if not request.user.is_superuser:
            form = EventsForm(request.POST, instance=events)
            if form.is_valid():
                form.save()
                return redirect('events-list')
        else:
            form = EventsFormAdmin(request.POST, instance=events)
            if form.is_valid():
                form.save()
                return redirect('events-list')
    else:
        if request.user.is_superuser:
            form = EventsFormAdmin(instance=events)
        else:
           form = EventsForm(instance=events) 


    return render(request, 'events/update_events.html', {'form': form, 
                                                         'manager': eventManager})
# delete venue
def deleteVenue(request, venueId):
    venue = get_object_or_404(Venue, pk=venueId)
    venue.delete()
    return redirect('list-venue')


# file generator
def generate_text_file(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="text.txt"'
    lines = []
    venues = Venue.objects.all()
    for venue in venues:
        lines.append(f'{venue.name}\n')  
    response.writelines(lines)
    return response
def generate_csv_file(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'

    writer = csv.writer(response)

    writer.writerow(['name', 'adress', 'email', 'web', 'zip_code', 'phone'])
    venues = Venue.objects.all()
    for venue in venues:
        writer.writerow([venue.name, venue.adress, venue.phone, venue.email, venue.web, venue.zip_code, ])

    return response
def generate_pdf_file(request):
    # Create a byte stream buffer
    buffer = io.BytesIO()

    # Create a canvas using the buffer as its "file"
    pdf = canvas.Canvas(buffer)

    # Set the title of the document
    pdf.setTitle("Venue List")

    # Starting position of text in the PDF
    x = 100
    y = 750

    # Write a title to the PDF
    pdf.drawString(x, y, "List of Venues")
    y -= 30  # Move the y position for the next line

    # Get all venues (or any dynamic data you're working with)
    venues = Venue.objects.all()

    # Loop through venues and write their details in the PDF
    for venue in venues:
        pdf.drawString(x, y, f"Name: {venue.name}")
        y -= 20
        pdf.drawString(x, y, f"Address: {venue.adress}")
        y -= 20
        pdf.drawString(x, y, f"Web: {venue.web}")
        y -= 20
        pdf.drawString(x, y, f"Zip Code: {venue.zip_code}")
        y -= 20
        pdf.drawString(x, y, f"Phone: {venue.phone}")
        y -= 40 

        # If we reach the bottom of the page, start a new page
        if y < 100:
            pdf.showPage()
            y = 750  # Reset y position for new page

    # Save the PDF to the buffer
    pdf.save()

    # Move the buffer's position to the beginning
    buffer.seek(0)

    # Create an HTTP response with the correct PDF content type
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venues.pdf"'

    return response






