from django.forms import forms
from django.forms import ModelForm
from .models import Venue, event

class venueForm(ModelForm):
    class Meta():
        model = Venue
        fields = ('name', 'adress' , 'email', 'web', 'zip_code', 'phone', 'image', )


class EventsForm(ModelForm):
    class Meta():
        model = event
        fields = ('name', 'date' , 'venue', 'description', 'attendees', )

class EventsFormAdmin(ModelForm):
    class Meta():
        model = event
        fields = ('name', 'date' , 'venue', 'manager', 'description', 'attendees', )