from django.contrib import admin
from .models import event
from .models import Venue
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(event)
admin.site.unregister(Group)

@admin.register(Venue)
class venueAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('name', 'phone', 'zip_code')
    search_fields = ('name', 'zip_code')


admin.site.site_header = 'CLUB'
admin.site.index_title = "club's admin page"