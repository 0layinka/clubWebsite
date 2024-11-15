from django.urls import path
from . import views
urlpatterns = [
# base
    path('', views.home, name='home'),
    path('<int:year>/<str:month>', views.home, name='home'),
    path('generate_text/', views.generate_text_file, name='generate_text'),
    path('generate_csv/', views.generate_csv_file, name='generate_csv'),
    path('generate_pdf/', views.generate_pdf_file, name='generate_pdf'),
# venue
    path('venue/', views.list_venue, name='list-venue'),
    path('add-venue/', views.addVenue, name='add-venue'),
    path('show-venue/<venueId>', views.showVenue, name='show-venue'),
    path('search-venue', views.searchVenue, name='search-venue'),
    path('update-venue/<venueId>', views.updateVenue, name='update-venue'),
    path('delete-venue/<venueId>', views.deleteVenue, name='delete-venue'),
# events
    path('events', views.event_page, name='events-list'), 
    path('add-events/', views.addEvents, name='add-events'),
    path('update-events/<eventId>', views.updateEvents, name='update-events'),
    path('delete-events/<eventId>', views.deleteEvent, name='delete-event'),
    path('search-events/', views.searchEvents, name='search-events'),
    path('approve-events/', views.approveEvents, name='approve-events')
]
