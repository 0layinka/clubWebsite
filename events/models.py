from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=200)
    adress = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Phone Number', max_length=25, blank=True)
    web = models.URLField('Website Adress', max_length=200, blank=True)
    email = models.CharField('Email Adress', max_length=200, blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, null=False, default= 1)
    image = models.ImageField(null=True, blank=True, upload_to='media/images/')
    
    def __str__(self):
        return f"{self.name} Venue"




# class clubUser(models.Model):
#     First_name = models.CharField('First Name', max_length=200)
#     Last_name = models.CharField('Last Name', max_length=200)
#     email = models.EmailField(max_length=200)

#     def __str__(self):
#         return f"{self.Last_name} {self.First_name}"

class event(models.Model):
    name = models.CharField('Event Name', max_length=200)
    date = models.DateTimeField('Event date', max_length=200)
    venue = models.ForeignKey(Venue, null=True, blank=True , on_delete=models.CASCADE,)
    manager = models.ForeignKey(User, max_length=150, null=True, blank=True, on_delete=models.SET_NULL, related_name='manager')
    description = models.TextField(blank=True, null=True)
    attendees = models.ManyToManyField(User, blank=True, related_name="attenddees")
    approved = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name}'s Event"
        
    @property
    def till_date(self):
        today = date.today()
        days_till = self.date.date() - today
        return f"{days_till.days} days to go" if days_till.days >= 0 else "Date has passed"